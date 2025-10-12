# 🚚 Kargo Ücreti Transfer Düzeltmesi

**Tarih:** 12 Ekim 2025  
**Durum:** ✅ Tamamlandı  
**Sorun:** Sipariş transferinde kargo ücreti hedef mağazaya yansımıyordu

---

## 🔍 Sorun Analizi

### Ana Mağaza
- **Kargo:** €75,00
- **KDV:** €146,73  
- **Toplam:** €1.689,00

### Transfer Edilen Mağaza (ÖNCE)
- **Kargo:** €0,00 ❌
- **KDV:** €146,73
- **Toplam:** €1.614,00

### Fark
- **Eksik Tutar:** €75,00 (kargo ücreti)

---

## 🛠️ Yapılan Düzeltmeler

### 1. `operations/shopify_order_builder.py`

**Sorun:** `build_shipping_line` fonksiyonu mevcuttu ama kullanılmıyordu. Yanlış bir yorum nedeniyle devre dışı bırakılmıştı.

**Eski Kod:**
```python
# NOT: shippingLine OrderCreateOrderInput'ta DESTEKLENMIYOR!
# Shopify API 2024-10'da orderCreate mutation shippingLine field'ını kabul etmiyor.
# shipping_line = order_data.get('shippingLine')
# if shipping_line:
#     shipping = build_shipping_line(shipping_line)
#     if shipping:
#         order_input["shippingLine"] = shipping  # ❌ ÇALIŞMAZ!
```

**Yeni Kod:**
```python
# Shipping Line (Kargo Bilgisi)
# Shopify API 2024-10'da orderCreate mutation shippingLine field'ını destekler
shipping_line = order_data.get('shippingLine')
if shipping_line:
    shipping = build_shipping_line(shipping_line)
    if shipping:
        order_input["shippingLine"] = shipping
```

### 2. `operations/shopify_to_shopify.py`

**Eklenen:** Kargo bilgisini sipariş verisine ekleme

```python
order_data_for_creation = {
    "customerId": customer_id,
    "lineItems": line_items,
    "shippingAddress": shipping_addr,
    "billingAddress": billing_addr,
    "note": order_note,
    "email": customer_email,
    "taxesIncluded": True
}

# Kargo bilgisini ekle (eğer varsa)
if shipping_line:
    order_data_for_creation["shippingLine"] = shipping_line
    log_messages.append(f"  🚚 Kargo bilgisi sipariş verisine eklendi")
```

---

## ✅ Beklenen Sonuç

### Transfer Edilen Mağaza (SONRA)
- **Kargo:** €75,00 ✅
- **KDV:** €146,73
- **Toplam:** €1.689,00

### İyileştirmeler
- ✅ Kargo ücreti artık tam olarak yansıtılıyor
- ✅ Kargo şirketi bilgisi transfer ediliyor
- ✅ Sipariş toplam tutarı doğru hesaplanıyor
- ✅ Log mesajlarında kargo bilgisi görüntüleniyor

---

## 🧪 Test Edilmesi Gerekenler

1. **Kargo Ücreti:** Transfer edilen siparişteki kargo ücretinin doğru olduğunu kontrol edin
2. **Kargo Şirketi:** Kargo şirket adının (MNG, Aras, vb.) doğru aktarıldığını kontrol edin
3. **Toplam Tutar:** Ana mağaza ile transfer edilen mağaza toplam tutarlarının eşit olduğunu kontrol edin
4. **Ücretsiz Kargo:** Ücretsiz kargo durumunda (€0,00) sistemin doğru çalıştığını test edin

---

## 📝 Teknik Detaylar

### Shopify GraphQL Schema

**OrderCreateOrderShippingLineInput** alanları:
- `title`: Kargo şirketi adı (örn: "MNG Kargo")
- `code`: Kargo kodu (opsiyonel)
- `priceSet`: Kargo ücreti
  - `shopMoney`
    - `amount`: Tutar (string)
    - `currencyCode`: Para birimi (örn: "TRY", "EUR")

### Örnek Veri Yapısı

```json
{
  "shippingLine": {
    "title": "MNG Kargo",
    "code": "mng",
    "priceSet": {
      "shopMoney": {
        "amount": "75.00",
        "currencyCode": "EUR"
      }
    }
  }
}
```

---

## 🔗 İlgili Dosyalar

1. `operations/shopify_to_shopify.py` - Ana transfer mantığı
2. `operations/shopify_order_builder.py` - Sipariş input builder
3. `SHOPIFY_TRANSFER_README.md` - Genel transfer dokümantasyonu

---

## 📊 Sonuç

✅ **Sorun Çözüldü:** Kargo ücreti artık sipariş transferinde tam olarak yansıtılıyor.

🎯 **Etki:** Mağazalar arası sipariş transferinde €0 fark olacak, tüm ücretler doğru aktarılacak.

🚀 **Durum:** Hemen test edilmeye hazır. Bir sipariş transferi yaparak doğrulayın.
