# operations/shopify_to_shopify.py

import logging
from .shopify_order_builder import create_order_input_builder

def find_or_create_customer(destination_api, source_customer):
    """Hedef mağazada müşteriyi e-postaya göre arar, bulamazsa yenisini oluşturur."""
    if not source_customer:
        raise Exception("Kaynak siparişte müşteri bilgisi bulunamadı.")
    
    email = source_customer.get('email')
    if not email:
        raise Exception("Kaynak siparişte müşteri e-postası bulunamadı.")
    
    customer_id = destination_api.find_customer_by_email(email)
    
    if customer_id:
        logging.info(f"Mevcut müşteri bulundu: {email}")
        return customer_id
    else:
        new_customer_id = destination_api.create_customer(source_customer)
        logging.info(f"Yeni müşteri oluşturuldu: {email}")
        return new_customer_id

def map_line_items(destination_api, source_line_items):
    """Kaynak mağazadaki ürünleri SKU'larına göre hedef mağazadaki varyant ID'leri ile eşleştirir."""
    line_items_for_creation = []
    logs = []
    
    for item in source_line_items:
        sku = (item.get('variant') or {}).get('sku')
        if not sku:
            logs.append(f"UYARI: '{item.get('title')}' ürününde SKU bulunamadı, siparişe eklenemiyor.")
            continue
        
        variant_id = destination_api.find_variant_id_by_sku(sku)
        if variant_id:
            # İndirimli fiyatı hesapla
            # discountedTotal = originalUnitPrice - discountAllocations
            original_price = float(item.get('originalUnitPriceSet', {}).get('shopMoney', {}).get('amount', '0'))
            discounted_price = float(item.get('discountedUnitPriceSet', {}).get('shopMoney', {}).get('amount', '0'))
            
            # Eğer indirimli fiyat yoksa, orijinal fiyatı kullan
            final_price = discounted_price if discounted_price > 0 else original_price
            
            line_item = {
                "variantId": variant_id,
                "quantity": item.get('quantity')
            }
            
            # Eğer indirimli fiyat varsa, onu da ekle (para birimi ile birlikte)
            if final_price > 0:
                line_item["price"] = str(final_price)
                # Para birimi bilgisini de ekle (priceSet için gerekli)
                currency = item.get('originalUnitPriceSet', {}).get('shopMoney', {}).get('currencyCode', 'TRY')
                line_item["currency"] = currency
            
            # Line item özel alanları (custom attributes)
            custom_attrs = item.get('customAttributes', [])
            if custom_attrs:
                line_item["customAttributes"] = custom_attrs
                logs.append(f"  📋 Ürün '{item.get('title')}' için {len(custom_attrs)} özel alan eklendi")
            
            line_items_for_creation.append(line_item)
            logs.append(f"Ürün eşleştirildi: SKU {sku}, Miktar: {item.get('quantity')}, Fiyat: ₺{final_price:.2f}")
        else:
            logs.append(f"HATA: SKU '{sku}' hedef mağazada bulunamadı.")
            
    return line_items_for_creation, logs

def transfer_order(source_api, destination_api, order_data):
    """
    Bir siparişi kaynak mağazadan alır ve hedef mağazada oluşturur.
    """
    log_messages = []
    
    try:
        # 1. Müşteriyi Hedef Mağazada Bul veya Oluştur
        customer_id = find_or_create_customer(destination_api, order_data.get('customer'))
        log_messages.append(f"Müşteri ID'si '{customer_id}' olarak belirlendi.")
        
        # 2. Ürün Satırlarını Eşleştir
        line_items, mapping_logs = map_line_items(destination_api, order_data.get('lineItems', {}).get('nodes', []))
        log_messages.extend(mapping_logs)

        if not line_items:
            raise Exception("Siparişteki hiçbir ürün hedef mağazada eşleştirilemedi.")

        # 3. Sipariş Verisini Hazırla ve Oluştur
        # Safe order input builder kullan
        builder = create_order_input_builder()
        
        # DÜZELTME: Doğru toplam tutarı hesapla (indirimli)
        # Shopify'da farklı toplam türleri:
        # - totalPriceSet: Orijinal toplam (indirimsiz)
        # - currentTotalPriceSet: Güncel toplam (indirimli)
        # - Manuel hesaplama: currentSubtotalPriceSet - totalDiscountsSet + shipping + tax
        
        # 1. Shopify'ın güncel toplamı (currentTotalPriceSet)
        current_total = float(order_data.get('currentTotalPriceSet', {}).get('shopMoney', {}).get('amount', '0'))
        
        # 2. Shopify'ın orijinal toplamı (totalPriceSet)
        original_total = float(order_data.get('totalPriceSet', {}).get('shopMoney', {}).get('amount', '0'))
        
        # 3. Manuel hesaplama
        subtotal = float(order_data.get('currentSubtotalPriceSet', {}).get('shopMoney', {}).get('amount', '0'))
        discounts = float(order_data.get('totalDiscountsSet', {}).get('shopMoney', {}).get('amount', '0'))
        shipping = float(order_data.get('totalShippingPriceSet', {}).get('shopMoney', {}).get('amount', '0'))
        tax = float(order_data.get('totalTaxSet', {}).get('shopMoney', {}).get('amount', '0'))
        calculated_total = subtotal - discounts + shipping + tax
        
        # 4. Hangi tutarı kullanacağımıza karar ver
        # Eğer currentTotalPriceSet varsa onu kullan (en güvenilir)
        if current_total > 0:
            total_amount = str(current_total)
            source = "currentTotalPriceSet"
        elif calculated_total > 0:
            total_amount = str(calculated_total)
            source = "manuel hesaplama"
        else:
            total_amount = str(original_total)
            source = "totalPriceSet (fallback)"
        
        # Debug bilgileri
        log_messages.append(f"💰 Tutar Analizi:")
        log_messages.append(f"  📊 Orijinal (totalPriceSet): ₺{original_total:.2f}")
        log_messages.append(f"  ✅ Güncel (currentTotalPriceSet): ₺{current_total:.2f}")
        log_messages.append(f"  📊 Manuel (subtotal-indirim+kargo+vergi): ₺{calculated_total:.2f}")
        log_messages.append(f"  📊 Detay: Subtotal ₺{subtotal:.2f} - İndirim ₺{discounts:.2f} + Kargo ₺{shipping:.2f} + Vergi ₺{tax:.2f}")
        log_messages.append(f"  🎯 Seçilen Toplam: ₺{total_amount} ({source})")
        log_messages.append(f"  🏷️ Vergi Dahil Fiyat: EVET (taxesIncluded=true)")

        # Ödeme yöntemi bilgisi
        payment_gateways = order_data.get('paymentGatewayNames', [])
        payment_method = "Bilinmiyor"
        if payment_gateways and len(payment_gateways) > 0:
            payment_method = payment_gateways[0]  # İlk ödeme yöntemi
            log_messages.append(f"  💳 Ödeme Yöntemi: {payment_method}")
        
        # Ödeme durumu (displayFinancialStatus kullan)
        financial_status = order_data.get('displayFinancialStatus', 'PENDING')
        if financial_status:
            status_display = {
                'Paid': '✅ Ödendi',
                'Pending': '⏳ Bekliyor',
                'Refunded': '💸 İade',
                'Partially refunded': '💸 Kısmi İade',
                'Voided': '❌ İptal',
                'Authorized': '🔐 Onaylandı',
                'Partially paid': '💰 Kısmi Ödeme'
            }.get(financial_status, financial_status)
            log_messages.append(f"  💰 Ödeme Durumu: {status_display}")
        
        # Kargo bilgileri
        shipping_line = order_data.get('shippingLine')
        shipping_title = "Bilinmiyor"
        shipping_price = 0
        if shipping_line:
            shipping_title = shipping_line.get('title') or 'Bilinmiyor'
            # originalPriceSet kullan (priceSet değil)
            price_set = shipping_line.get('originalPriceSet') or {}
            shop_money = price_set.get('shopMoney') or {}
            amount = shop_money.get('amount', '0')
            try:
                shipping_price = float(amount) if amount else 0
            except (ValueError, TypeError):
                shipping_price = 0
            log_messages.append(f"  📦 Kargo: {shipping_title} - ₺{shipping_price:.2f}")
        
        # İndirim kodları
        discount_codes = []
        discount_apps = order_data.get('discountApplications', {}).get('edges', [])
        if discount_apps:
            for edge in discount_apps:
                node = edge.get('node', {})
                # DiscountCodeApplication kontrolü
                if 'code' in node:
                    code = node.get('code')
                    discount_codes.append(code)
                    log_messages.append(f"  🎫 İndirim Kodu: {code}")
                # ManualDiscountApplication kontrolü
                elif 'title' in node:
                    title = node.get('title')
                    log_messages.append(f"  🎫 Manuel İndirim: {title}")
        
        # Teslimat durumu (displayFulfillmentStatus kullan)
        fulfillment_status = order_data.get('displayFulfillmentStatus')
        if fulfillment_status:
            status_display = {
                'Fulfilled': '✅ Teslim Edildi',
                'Unfulfilled': '📦 Hazırlanıyor',
                'Partially fulfilled': '📦 Kısmi Teslim',
                'Scheduled': '📅 Planlandı',
                'On hold': '⏸️ Beklemede',
                'In progress': '🔄 İşlemde'
            }.get(fulfillment_status, fulfillment_status)
            log_messages.append(f"  📦 Teslimat Durumu: {status_display}")

        
        # Kaynak veriyi düzenle
        # NOT: Transaction kaldırıldı - Shopify line item'lardan otomatik hesaplasın
        
        # Sipariş notunu hazırla (tüm önemli bilgileri içerecek)
        order_name = order_data.get('name') or 'Bilinmeyen'
        note_parts = [
            f"Kaynak Mağazadan Aktarılan Sipariş.",
            f"Orijinal Sipariş No: {order_name}",
            f"Net Tutar: ₺{total_amount}"
        ]
        
        # Ödeme yöntemi ekle
        if payment_method != "Bilinmiyor":
            note_parts.append(f"Ödeme: {payment_method}")
        
        # Ödeme durumu ekle
        if financial_status:
            note_parts.append(f"Ödeme Durumu: {financial_status}")
        
        # Kargo şirketi ekle
        if shipping_title != "Bilinmiyor":
            note_parts.append(f"Kargo: {shipping_title}")
        
        # İndirim kodları ekle
        if discount_codes:
            note_parts.append(f"Kupon: {', '.join(discount_codes)}")
        
        # Orijinal notu da ekle (varsa)
        original_note = order_data.get('note') or ''
        original_note = original_note.strip() if original_note else ''
        if original_note:
            note_parts.append(f"Not: {original_note}")
        
        order_note = " | ".join(note_parts)
        
        # Email güvenli şekilde al
        customer = order_data.get('customer') or {}
        customer_email = customer.get('email') or None
        
        order_data_for_creation = {
            "customerId": customer_id,
            "lineItems": line_items,
            "shippingAddress": order_data.get('shippingAddress') or {},
            "note": order_note,
            "email": customer_email,
            "taxesIncluded": True  # ÖNEMLİ: Fiyatlar vergi dahil
        }
        
        # Vergi bilgilerini ekle (eğer varsa)
        if tax > 0:
            tax_lines = []
            
            # Kaynak siparişten vergi bilgilerini al
            source_tax_lines = order_data.get('taxLines', [])
            
            if source_tax_lines:
                # Kaynak siparişteki vergi satırlarını kullan
                for tax_line in source_tax_lines:
                    # GraphQL'den gelen ratePercentage %10 olarak gelir, bunu 0.1'e çevirmemiz gerekiyor
                    rate_percentage = tax_line.get('ratePercentage', 10)  # Varsayılan %10
                    rate = float(rate_percentage) / 100  # %10 -> 0.1
                    
                    tax_amount = tax_line.get('priceSet', {}).get('shopMoney', {}).get('amount', '0')
                    
                    tax_lines.append({
                        "title": tax_line.get('title', 'KDV % 10 (Dahil)'),
                        "rate": rate,
                        "price": str(tax_amount)
                    })
                    log_messages.append(f"  📋 Vergi (Dahil): {tax_line.get('title')} - Oran: %{rate_percentage} - Tutar: ₺{tax_amount}")
            else:
                # Eğer kaynak siparişteki vergi satırları yoksa, manuel oluştur
                # Türkiye için varsayılan KDV %10 (dahil)
                tax_lines.append({
                    "title": "KDV % 10 (Dahil)",
                    "rate": 0.1,  # %10
                    "price": str(tax)
                })
                log_messages.append(f"  📋 Vergi (Dahil - manuel): KDV % 10 - Tutar: ₺{tax:.2f}")
            
            order_data_for_creation["taxLines"] = tax_lines
        
        # NOT: shippingLine field'ı OrderCreateOrderInput'ta YOK!
        # Shopify 2024-10'da sipariş oluştururken kargo bilgisi otomatik hesaplanır
        # veya sipariş oluşturulduktan SONRA fulfillment ile eklenir.
        # Kargo ücreti zaten totalShippingPriceSet'te dahil, bu yeterli.
        
        # Tags (Etiketler) - kaynak siparişten al
        tags = order_data.get('tags') or []
        if tags and isinstance(tags, (list, str)):
            order_data_for_creation["tags"] = tags
            tags_display = ', '.join(tags) if isinstance(tags, list) else tags
            log_messages.append(f"  🏷️ Etiketler: {tags_display}")
        
        # Özel alanlar (Custom Attributes)
        custom_attrs = order_data.get('customAttributes') or []
        if custom_attrs and isinstance(custom_attrs, list):
            order_data_for_creation["customAttributes"] = custom_attrs
            log_messages.append(f"  📋 Özel Alanlar: {len(custom_attrs)} adet ekstra bilgi")
        
        # Safe builder ile OrderCreateOrderInput oluştur
        order_input = builder['build_order_input'](order_data_for_creation)
        
        new_order = destination_api.create_order(order_input)
        log_messages.append(f"✅ BAŞARILI: Sipariş, hedef mağazada '{new_order.get('name')}' numarasıyla oluşturuldu.")
        
        return {"success": True, "logs": log_messages, "new_order_name": new_order.get('name')}

    except Exception as e:
        logging.error(f"Sipariş aktarımında kritik hata: {e}", exc_info=True)
        log_messages.append(f"❌ KRİTİK HATA: {str(e)}")
        return {"success": False, "logs": log_messages}