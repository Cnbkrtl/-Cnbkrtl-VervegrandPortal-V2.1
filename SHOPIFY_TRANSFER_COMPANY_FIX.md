# 🏢 Shopify Transfer - Şirket ve Fatura Bilgisi Düzeltmesi

## 📋 Yapılan İyileştirmeler

### ✅ 1. Sipariş Sorgusuna Yeni Alanlar Eklendi

**Dosya:** `connectors/shopify_api.py` - `get_orders_by_date_range()`

#### Müşteri Bilgilerine Eklenenler:
- ✅ `customer.defaultAddress` - Müşterinin varsayılan adresi
- ✅ `customer.defaultAddress.company` - Şirket bilgisi
- ✅ Tam adres detayları (address1, address2, city, province, zip, country, phone)

#### Sipariş Bilgilerine Eklenenler:
- ✅ `billingAddress` - Fatura adresi (tam detaylı)
- ✅ `billingAddress.company` - Fatura adresindeki şirket bilgisi
- ✅ `shippingAddress.company` - Kargo adresindeki şirket bilgisi

---

### ✅ 2. Müşteri Oluşturma Fonksiyonu Güncellendi

**Dosya:** `connectors/shopify_api.py` - `create_customer()`

#### Yeni Özellikler:
- ✅ Şirket bilgisi (`company`) artık müşteri kaydına ekleniyor
- ✅ Tam adres bilgileri (`addresses` array) ile müşteri oluşturuluyor
- ✅ `defaultAddress` verisinden şirket ve adres bilgileri otomatik çekiliyor
- ✅ Boş değerler temizleniyor (null hatalarını önler)

#### Eklenen Adres Alanları:
```python
{
  "address1": "...",
  "address2": "...",
  "city": "...",
  "company": "ŞİRKET ADI",  # ⭐ YENİ
  "firstName": "...",
  "lastName": "...",
  "phone": "...",
  "province": "...",
  "country": "...",
  "zip": "..."
}
```

---

### ✅ 3. Sipariş Transferinde Fatura Adresi Eklendi

**Dosya:** `operations/shopify_to_shopify.py` - `transfer_order()`

#### Yeni Özellikler:
- ✅ `billingAddress` artık sipariş oluşturulurken gönderiliyor
- ✅ Fatura adresi yoksa, kargo adresi fatura adresi olarak kullanılıyor
- ✅ Şirket bilgileri log mesajlarında gösteriliyor

#### Log İyileştirmeleri:
```
👤 Müşteri: Ahmet Yılmaz (ahmet@example.com)
🏢 Şirket: ÖRNEK TİCARET LTD. ŞTİ.
🆔 Müşteri ID'si: gid://shopify/Customer/123456
📦 Kargo Adresi - Şirket: ÖRNEK TİCARET LTD. ŞTİ.
🧾 Fatura Adresi - Şirket: FATURA ŞİRKETİ A.Ş.
```

---

### ✅ 4. Sipariş Builder'a Company Desteği Eklendi

**Dosya:** `operations/shopify_order_builder.py` - `build_mailing_address()`

#### Güncelleme:
- ✅ `MailingAddressInput` formatına `company` field'ı eklendi
- ✅ Hem shippingAddress hem de billingAddress için çalışıyor

---

## 🎯 Sonuç

Artık Shopify mağaza transfer modülü şu bilgileri tam olarak aktarıyor:

### Müşteri Bilgileri:
- ✅ Ad, Soyad, E-posta, Telefon
- ✅ **Şirket adı** (customer.defaultAddress.company)
- ✅ Tam adres bilgileri

### Sipariş Bilgileri:
- ✅ Kargo adresi (company dahil)
- ✅ **Fatura adresi** (company dahil)
- ✅ Ürünler, fiyatlar, vergiler
- ✅ İndirimler, notlar, özel alanlar

---

## 📊 Test Senaryoları

### Test 1: Şirketli Müşteri Transferi
1. Kaynak mağazada şirket bilgisi olan bir sipariş seçin
2. Transfer işlemini başlatın
3. Hedef mağazada müşteriyi kontrol edin
4. ✅ Şirket bilgisinin kaydedildiğini doğrulayın

### Test 2: Farklı Fatura Adresi
1. Kargo ve fatura adresinin farklı olduğu bir sipariş seçin
2. Transfer işlemini başlatın
3. Hedef mağazada siparişi kontrol edin
4. ✅ Her iki adresin de doğru kaydedildiğini doğrulayın

### Test 3: Fatura Adresinde Şirket
1. Sadece fatura adresinde şirket bilgisi olan bir sipariş seçin
2. Transfer işlemini başlatın
3. Log mesajlarını kontrol edin
4. ✅ "🧾 Fatura Adresi - Şirket: ..." mesajını görmelisiniz

---

## 🔧 Değiştirilen Dosyalar

1. ✅ `connectors/shopify_api.py`
   - `get_orders_by_date_range()` - Sorguya billingAddress ve customer.defaultAddress eklendi
   - `create_customer()` - Şirket ve adres desteği eklendi

2. ✅ `operations/shopify_to_shopify.py`
   - `transfer_order()` - billingAddress transferi eklendi
   - Log mesajları iyileştirildi

3. ✅ `operations/shopify_order_builder.py`
   - `build_mailing_address()` - company field'ı eklendi

---

## 🚀 Kullanım

Transfer modülünü şimdi kullandığınızda:

1. **Müşteri bilgileri** - Şirket adı dahil olmak üzere tam olarak aktarılır
2. **Fatura adresi** - Kargo adresinden farklıysa, ayrıca kaydedilir
3. **Şirket bilgileri** - Hem müşteri kaydında hem de sipariş adreslerinde saklanır
4. **Detaylı loglar** - Hangi bilgilerin aktarıldığını görebilirsiniz

---

## 📝 Notlar

- Eğer fatura adresi yoksa, kargo adresi otomatik olarak fatura adresi olarak kullanılır
- Şirket bilgisi boş olsa bile hata vermez, sadece atlanır
- Tüm değişiklikler Shopify'ın 2024-10 API versiyonuna uyumludur

**Tarih:** 6 Ekim 2025
**Durum:** ✅ Tamamlandı
