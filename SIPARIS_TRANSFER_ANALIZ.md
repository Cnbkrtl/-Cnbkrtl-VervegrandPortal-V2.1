# 🔍 SİPARİŞ TRANSFER MODÜLÜ ANALİZ RAPORU
**Tarih:** 4 Ekim 2025, 03:45  
**Modül:** Shopify Mağazalar Arası Sipariş Transferi  
**Durum:** ⚠️ EKSİKLER TESPİT EDİLDİ

---

## ✅ ÇALIŞAN ÖZELLİKLER

### 1. Müşteri Bilgileri
- ✅ E-posta
- ✅ Ad-Soyad (firstName/lastName)
- ✅ Telefon
- ✅ Müşteri ID eşleştirme (e-posta ile)
- ✅ Yeni müşteri oluşturma (yoksa)

### 2. Adres Bilgileri
- ✅ Teslimat Adresi (shippingAddress)
  - firstName/lastName
  - address1, address2
  - city, province, zip
  - country, phone
- ✅ Fatura Adresi (billingAddress) - opsiyonel

### 3. Ürün Bilgileri (Line Items)
- ✅ SKU bazlı ürün eşleştirme
- ✅ Varyant ID bulma
- ✅ Miktar (quantity)
- ✅ Orijinal fiyat (originalUnitPriceSet)
- ✅ İndirimli fiyat (discountedUnitPriceSet)
- ✅ **İndirim otomatik hesaplama** (discountedPrice kullanılıyor)
- ✅ Para birimi (currencyCode)

### 4. Tutar Hesaplamaları
- ✅ Alt toplam (currentSubtotalPriceSet)
- ✅ Toplam indirim (totalDiscountsSet)
- ✅ Kargo ücreti (totalShippingPriceSet)
- ✅ Vergi toplamı (totalTaxSet)
- ✅ Genel toplam (currentTotalPriceSet)
- ✅ **Akıllı tutar seçimi:**
  1. Önce currentTotalPriceSet (en güvenilir)
  2. Manuel hesaplama (subtotal - indirim + kargo + vergi)
  3. Fallback: totalPriceSet

### 5. Vergi Bilgileri
- ✅ Vergi dahil fiyat kontrolü (taxesIncluded: true)
- ✅ Vergi satırları (taxLines)
- ✅ Vergi oranı (ratePercentage → rate dönüşümü)
- ✅ Vergi tutarı (priceSet)
- ✅ Vergi başlığı (örn: "KDV % 10 (Dahil)")
- ✅ Line item bazında vergi bilgileri

### 6. Sipariş Meta Bilgileri
- ✅ Sipariş notu (note) - kaynak sipariş no ekleniyor
- ✅ E-posta
- ✅ Oluşturma tarihi

---

## ❌ EKSİK ÖZELLİKLER

### 1. Ödeme Yöntemi Bilgisi 🔴 KRİTİK
**Sorun:**
- GraphQL sorgusunda `paymentGatewayNames` veya `transactions` çekilmiyor
- Hedef mağazaya hangi ödeme yöntemi kullanıldığı aktarılmıyor

**Eksik Veri:**
```graphql
# ❌ ŞUAN YOK
paymentGatewayNames  # ["manual", "shopify_payments", "iyzico", vb.]
transactions {
  gateway
  kind
  status
  amountSet { shopMoney { amount currencyCode } }
}
```

**Etki:**
- Hedef mağazada "manuel" ödeme olarak kaydediliyor
- Gerçek ödeme yöntemi bilinmiyor
- Muhasebe/raporlama sorunları

---

### 2. Kargo Yöntemi Bilgisi 🔴 KRİTİK
**Sorun:**
- GraphQL sorgusunda `shippingLine` çekilmiyor
- Kargo şirketi ve kargo ücreti detayları eksik

**Eksik Veri:**
```graphql
# ❌ ŞUAN YOK
shippingLine {
  title  # Kargo şirketi adı (örn: "MNG Kargo")
  code   # Kargo kodu
  source # Kaynak
  priceSet { shopMoney { amount currencyCode } }
}
```

**Etki:**
- Kargo yöntemi bilgisi kaybolur
- Sadece tutar aktarılıyor, kargo şirketi bilgisi yok
- Lojistik takibi zorlaşır

---

### 3. Sipariş Durumu ve Tags
**Sorun:**
- `financialStatus` (ödeme durumu) aktarılmıyor
- `fulfillmentStatus` (teslimat durumu) aktarılmıyor
- `tags` (etiketler) çekiliyor ama hedef siparişe eklenmiyor

**Eksik Veri:**
```graphql
# ✅ ÇEKİLİYOR ama KULLANILMIYOR
tags
# ❌ HİÇ ÇEKİLMİYOR
financialStatus  # "PAID", "PENDING", "REFUNDED", vb.
fulfillmentStatus  # "FULFILLED", "UNFULFILLED", vb.
```

**Etki:**
- Sipariş durumu bilgisi kaybolur
- Etiketler hedef mağazaya taşınmıyor

---

### 4. Özel Alanlar (Custom Attributes)
**Sorun:**
- Line item'larda `customAttributes` çekilmiyor
- Sipariş düzeyinde `customAttributes` yok

**Eksik Veri:**
```graphql
# ❌ ŞUAN YOK
customAttributes {
  key
  value
}
```

**Etki:**
- Özel not/bilgiler kaybolur
- Entegrasyon uygulamalarının eklediği veriler taşınmaz

---

### 5. İndirim Kodları
**Sorun:**
- `discountApplications` çekilmiyor
- Hangi kupon/indirim kodunun kullanıldığı bilinmiyor

**Eksik Veri:**
```graphql
# ❌ ŞUAN YOK
discountApplications(first: 10) {
  edges {
    node {
      ... on DiscountCodeApplication {
        code
        value { ... }
      }
      ... on ManualDiscountApplication {
        title
        value { ... }
      }
    }
  }
}
```

**Etki:**
- İndirim tutarı aktarılıyor ama kaynak bilgisi yok
- "YILBASI20" gibi kupon kodları kaybolur

---

## 📊 MEVCUT VERİ AKIŞI

### Kaynak Sipariş → Hedef Sipariş Mapping

| Kaynak Alan | Hedef Alan | Durum | Not |
|-------------|------------|-------|-----|
| **Müşteri** |
| customer.email | email | ✅ | E-posta ile müşteri bulunur/oluşturulur |
| customer.id | customerId | ✅ | Hedef mağazadaki ID kullanılır |
| **Adres** |
| shippingAddress | shippingAddress | ✅ | Tam olarak aktarılıyor |
| billingAddress | billingAddress | ✅ | Opsiyonel |
| **Ürünler** |
| lineItems[].variant.sku | lineItems[].variantId | ✅ | SKU ile eşleştirme |
| lineItems[].quantity | lineItems[].quantity | ✅ | Doğrudan |
| lineItems[].discountedUnitPriceSet | lineItems[].priceSet | ✅ | İndirimli fiyat kullanılıyor |
| **Tutarlar** |
| currentTotalPriceSet | - | ✅ | Transaction'da kullanılıyor |
| totalDiscountsSet | - | ✅ | Log'da gösteriliyor |
| totalShippingPriceSet | - | ✅ | Transaction'a dahil |
| totalTaxSet | taxLines[].priceSet | ✅ | Vergi satırlarında |
| **Vergi** |
| taxesIncluded | taxesIncluded | ✅ | true olarak set ediliyor |
| taxLines | taxLines | ✅ | Detaylı aktarım |
| **Eksik** |
| paymentGatewayNames | ❌ | ❌ | Aktarılmıyor |
| shippingLine | ❌ | ❌ | Aktarılmıyor |
| financialStatus | ❌ | ❌ | Aktarılmıyor |
| tags | ❌ | ⚠️ | Çekiliyor ama kullanılmıyor |
| discountApplications | ❌ | ❌ | Hiç çekilmiyor |

---

## 🔧 ÖNERİLEN DÜZELTMELER

### 1. GraphQL Sorgusunu Genişlet (shopify_api.py)

**Eklenecek alanlar:**
```graphql
# get_orders_by_date_range() içinde
paymentGatewayNames  # Ödeme yöntemi
financialStatus      # Ödeme durumu
fulfillmentStatus    # Teslimat durumu

shippingLine {       # Kargo bilgileri
  title
  code
  source
  priceSet { shopMoney { amount currencyCode } }
}

discountApplications(first: 10) {  # İndirim kodları
  edges {
    node {
      ... on DiscountCodeApplication {
        code
        value {
          ... on MoneyV2 { amount currencyCode }
          ... on PricingPercentageValue { percentage }
        }
      }
      ... on ManualDiscountApplication {
        title
        description
        value {
          ... on MoneyV2 { amount currencyCode }
          ... on PricingPercentageValue { percentage }
        }
      }
    }
  }
}

customAttributes {   # Özel alanlar
  key
  value
}

lineItems(first: 50) {
  nodes {
    # ... mevcut alanlar ...
    customAttributes {
      key
      value
    }
  }
}
```

---

### 2. Order Builder'ı Genişlet (shopify_order_builder.py)

**Yeni builder fonksiyonları:**
```python
def build_shipping_line(shipping_data):
    """OrderCreateOrderShippingLineInput formatında kargo bilgisi"""
    if not shipping_data:
        return None
    
    shipping = {}
    if shipping_data.get('title'):
        shipping["title"] = shipping_data.get('title')
    if shipping_data.get('code'):
        shipping["code"] = shipping_data.get('code')
    
    # Kargo ücreti
    price = shipping_data.get('priceSet', {}).get('shopMoney', {}).get('amount')
    if price:
        shipping["priceSet"] = {
            "shopMoney": {
                "amount": str(price),
                "currencyCode": shipping_data.get('priceSet', {}).get('shopMoney', {}).get('currencyCode', 'TRY')
            }
        }
    
    return shipping if shipping else None

def build_custom_attributes(attributes_data):
    """Özel alanları formatla"""
    if not attributes_data:
        return None
    
    custom_attrs = []
    for attr in attributes_data:
        if attr.get('key') and attr.get('value'):
            custom_attrs.append({
                "key": attr['key'],
                "value": attr['value']
            })
    
    return custom_attrs if custom_attrs else None
```

---

### 3. Transfer Logic'i Güncelle (shopify_to_shopify.py)

**Eklenecek kodlar:**
```python
# Ödeme yöntemi bilgisi
payment_gateway = order_data.get('paymentGatewayNames', [])
if payment_gateway:
    payment_method = payment_gateway[0]  # İlk ödeme yöntemi
    log_messages.append(f"💳 Ödeme Yöntemi: {payment_method}")
    # Note'a ekle
    order_data_for_creation["note"] += f" | Ödeme: {payment_method}"

# Kargo bilgisi
shipping_line = order_data.get('shippingLine')
if shipping_line:
    shipping_title = shipping_line.get('title', 'Bilinmiyor')
    shipping_price = shipping_line.get('priceSet', {}).get('shopMoney', {}).get('amount', '0')
    log_messages.append(f"📦 Kargo: {shipping_title} - ₺{shipping_price}")
    
    # Hedef siparişe kargo bilgisi ekle
    order_data_for_creation["shippingLine"] = builder['build_shipping_line'](shipping_line)

# Tags (etiketler)
tags = order_data.get('tags', [])
if tags:
    # Virgülle ayrılmış string olarak ekle
    order_data_for_creation["tags"] = ", ".join(tags)
    log_messages.append(f"🏷️ Etiketler: {', '.join(tags)}")

# İndirim kodları
discount_apps = order_data.get('discountApplications', {}).get('edges', [])
if discount_apps:
    for edge in discount_apps:
        node = edge.get('node', {})
        if node.get('__typename') == 'DiscountCodeApplication':
            code = node.get('code')
            log_messages.append(f"🎫 İndirim Kodu: {code}")
            order_data_for_creation["note"] += f" | Kupon: {code}"

# Özel alanlar
custom_attrs = order_data.get('customAttributes', [])
if custom_attrs:
    order_data_for_creation["customAttributes"] = builder['build_custom_attributes'](custom_attrs)
```

---

## 🎯 ÖNCELİK SIRALAMASI

### 🔴 YÜKSEK ÖNCELİK (Hemen Yapılmalı)
1. **Ödeme Yöntemi** - Muhasebe için kritik
2. **Kargo Bilgisi** - Lojistik takibi için gerekli

### 🟡 ORTA ÖNCELİK (Yakın zamanda)
3. **Tags (Etiketler)** - Sipariş organizasyonu
4. **İndirim Kodları** - Pazarlama analizleri

### 🟢 DÜŞÜK ÖNCELİK (İsteğe bağlı)
5. **Custom Attributes** - Özel entegrasyonlar için
6. **Financial/Fulfillment Status** - Durum takibi

---

## 📝 TEST SENARYOLARI

### Senaryo 1: Normal Sipariş
- ✅ Müşteri bilgileri
- ✅ Adres
- ✅ 2 ürün (farklı fiyatlar)
- ✅ KDV dahil toplam
- ⚠️ Ödeme yöntemi (eksik)
- ⚠️ Kargo şirketi (eksik)

### Senaryo 2: İndirimli Sipariş
- ✅ Kupon kodu kullanılmış
- ✅ İndirim tutarı doğru hesaplanıyor
- ❌ Kupon kodu bilgisi kayboluyor

### Senaryo 3: Kargo Ücretli Sipariş
- ✅ Kargo ücreti toplama ekleniyor
- ❌ Kargo şirketi bilgisi yok
- ❌ Kargo kodu yok

### Senaryo 4: Özel Notlu Sipariş
- ⚠️ Line item custom attributes (test edilmedi)
- ⚠️ Sipariş düzeyinde custom attributes (test edilmedi)

---

## 💡 SONUÇ VE ÖNERİLER

### Özet
Sipariş transfer modülü **temel işlevlerde çalışıyor** ancak **ödeme ve kargo bilgileri eksik**. 

### Mevcut Kalite: 65/100
- ✅ Müşteri/Adres: 100%
- ✅ Ürün/Fiyat: 95%
- ✅ Vergi/Tutar: 90%
- ❌ Ödeme: 0%
- ❌ Kargo: 20% (sadece tutar)
- ⚠️ Meta Bilgiler: 40%

### Hedef Kalite: 95/100
Yukarıdaki düzeltmeler yapıldığında:
- ✅ Tüm kritik bilgiler aktarılacak
- ✅ Muhasebe tutarlılığı sağlanacak
- ✅ Lojistik takibi mümkün olacak
- ✅ Sipariş geçmişi korunacak

---

**Sonraki Adım:** Yüksek öncelikli düzeltmeleri uygulamak için onay bekliyorum.
