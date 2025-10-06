# 🎨 SEO Alt Metinli Resimler Modülü

## 📋 Genel Bakış

Bu modül, Shopify mağazanızdaki ürün resimlerinin **SEO optimizasyonunu** sağlar. Modül **SADECE** aşağıdaki işlemleri yapar:

1. ✅ Ürün resimlerinin **ALT TEXT**'ini ürün ismi ile günceller
2. ✅ SEO dostu **filename** oluşturur (Türkçe karakterler temizlenir)
3. ❌ **HİÇBİR** resim ekleme/silme/yeniden sıralama YAPMAZ

---

## 🎯 Ne Yapar?

### Örnek İşlem:

**Ürün:** "Büyük Beden Kısa Kollu Bisiklet Yaka Baskılı T-shirt 303734"

**Önce:**
```html
<img src="https://cdn.shopify.com/s/files/1/abc123.jpg" 
     alt="https://www.vervegrand.com/cdn/shop/files/o_d06afc59-b4b8-40-303734-a.jpg">
```

**Sonra:**
```html
<img src="https://cdn.shopify.com/s/files/1/abc123.jpg" 
     alt="Büyük Beden Kısa Kollu Bisiklet Yaka Baskılı T-shirt 303734">
```

**SEO Filename:** `buyuk-beden-kisa-kollu-bisiklet-yaka-baskili-t-shirt-303734`

---

## 🔧 Kullanım

### 1. Streamlit Arayüzünden:

1. **Sync** sayfasına gidin
2. Senkronizasyon tipini seçin: **"SEO Alt Metinli Resimler"**
3. Test modunu açın (ilk 20 ürün) veya kapatın (tüm ürünler)
4. **"🚀 Genel Senkronizasyonu Başlat"** butonuna tıklayın

### 2. Nasıl Çalışır:

```python
# Her ürün için:
1. Ürün ismi alınır: "Büyük Beden T-shirt 303734"
2. Tüm mevcut resimler sorgulanır
3. Her resmin ALT text'i ürün ismi ile güncellenir
4. Hiçbir resim eklenmez, silinmez veya yeniden sıralanmaz
```

---

## 📊 Teknik Detaylar

### Değiştirilen Dosyalar:

#### 1. `connectors/shopify_api.py`

**Yeni Fonksiyon:** `update_product_media_seo(product_gid, product_title)`

```python
def update_product_media_seo(self, product_gid, product_title):
    """
    🎯 SADECE SEO için ürün resimlerinin ALT text'ini günceller.
    HİÇBİR RESİM EKLEME/SİLME/YENİDEN SIRALAMA YAPMAZ.
    """
    # 1. Mevcut medyaları al
    # 2. Her resim için ALT text'i ürün ismi yap
    # 3. productUpdateMedia mutation ile güncelle
    # 4. Sonuç döndür
```

**Özellikler:**
- ✅ Sadece IMAGE tipindeki medyaları işler
- ✅ ALT text zaten ürün ismiyse atlar (gereksiz API çağrısı önlenir)
- ✅ Rate limit koruması (her resim arası 0.3 saniye bekler)
- ✅ Hata durumunda detaylı log mesajları

**Yardımcı Fonksiyon:** `_create_seo_filename(title)`

Türkçe karakterleri temizler ve SEO dostu filename oluşturur:

```python
"Büyük Beden T-shirt 303734" 
→ "buyuk-beden-t-shirt-303734"
```

**Karakter Dönüşümleri:**
- ı → i, ğ → g, ü → u, ş → s, ö → o, ç → c
- Özel karakterler kaldırılır
- Boşluklar tire (-) ile değiştirilir
- Birden fazla tire tek tireye düşürülür

---

#### 2. `sync_runner.py`

**Güncellenmiş Fonksiyon:** `_update_product()`

```python
def _update_product(shopify_api, sentos_api, sentos_product, existing_product, sync_mode):
    # ✅ ÖZEL: SEO Alt Metinli Resimler modu
    if sync_mode == "SEO Alt Metinli Resimler":
        result = shopify_api.update_product_media_seo(shopify_gid, product_name)
        # Sadece SEO güncelleme yapılır, başka hiçbir işlem yapılmaz
        return all_changes
    
    # Diğer sync modları normal çalışır...
```

---

## 🚀 GraphQL Mutation

Modül şu Shopify GraphQL mutation'ını kullanır:

```graphql
mutation updateMedia($media: [UpdateMediaInput!]!, $productId: ID!) {
    productUpdateMedia(media: $media, productId: $productId) {
        media {
            id
            alt
        }
        mediaUserErrors {
            field
            message
        }
    }
}
```

**Variables:**
```json
{
  "media": [
    {
      "id": "gid://shopify/MediaImage/123456789",
      "alt": "Büyük Beden Kısa Kollu Bisiklet Yaka Baskılı T-shirt 303734"
    }
  ],
  "productId": "gid://shopify/Product/987654321"
}
```

---

## 📈 Performans

### Örnek İşlem Süresi:

**Test Modu (20 ürün):**
- Ürün başına ortalama 5 resim
- Toplam 100 resim güncellemesi
- Her resim arası 0.3 saniye
- **Toplam süre:** ~30-45 saniye

**Tam Sync (1000 ürün):**
- Ürün başına ortalama 5 resim
- Toplam 5000 resim güncellemesi
- **Toplam süre:** ~25-40 dakika

### Rate Limit Koruması:
- ✅ Her resim güncellemesi arası 0.3 saniye bekleme
- ✅ Shopify API limitlerini aşmaz
- ✅ Thread-safe çalışma

---

## 🎨 Log Mesajları

### Başarılı Güncelleme:
```
🎯 SEO Modu: Sadece resim ALT text'leri güncelleniyor...
  ✅ Resim 1/5 ALT text güncellendi: 'Büyük Beden T-shirt 303734'
  ✅ Resim 2/5 ALT text güncellendi: 'Büyük Beden T-shirt 303734'
  ✅ Resim 3/5 ALT text zaten güncel: Büyük Beden T-shirt 303734
✅ SEO Güncelleme: 4/5 resim ALT text güncellendi
```

### Resim Bulunamadığında:
```
✅ SEO Güncelleme: Güncellenecek resim bulunamadı
```

### Hata Durumunda:
```
❌ SEO Hatası: Shopify API hatası - Rate limit exceeded
```

---

## ⚠️ Önemli Notlar

### 1. Sadece ALT Text Güncellenir
- ❌ Resim dosya ismi CDN tarafından otomatik oluşturulur
- ❌ Shopify API ile direkt filename değiştirilemez
- ✅ ALT text SEO için yeterlidir (Google, ALT text'i kullanır)

### 2. Mevcut Resimleri Korur
- ❌ Hiçbir resim silinmez
- ❌ Hiçbir yeni resim eklenmez
- ❌ Resim sıralaması değiştirilmez
- ✅ Sadece metadata güncellenir

### 3. Güvenli Çalışma
- ✅ Ürün bilgileri değiştirilmez
- ✅ Stok bilgileri dokunulmaz
- ✅ Fiyatlar etkilenmez
- ✅ Kategoriler korunur

---

## 🔍 SEO Faydaları

### Google için:
1. ✅ **Image Search** - Resimler ürün ismi ile aranabilir
2. ✅ **Accessibility** - Görme engelliler için uygun
3. ✅ **Rich Snippets** - Google'da zengin sonuçlar
4. ✅ **Page Speed** - Hafif metadata, hızlı yüklenme

### Örnek Google Sonucu:
```
Büyük Beden Kısa Kollu Bisiklet Yaka Baskılı T-shirt 303734
vervegrand.com › products › t-shirt-303734
[RESİM] - ALT: "Büyük Beden Kısa Kollu Bisiklet Yaka Baskılı T-shirt 303734"
```

---

## 🧪 Test Senaryoları

### Test 1: Tek Ürün
1. Test modunu aç (ilk 20 ürün)
2. SEO Alt Metinli Resimler modunu seç
3. Sync'i başlat
4. ✅ Her ürünün tüm resimlerinin ALT text'i ürün ismi olmalı

### Test 2: ALT Text Kontrolü
1. Shopify admin paneline git
2. Bir ürünün resimlerine tıkla
3. "Edit" butonuna bas
4. ✅ ALT text alanında ürün ismi görülmeli

### Test 3: Tekrar Sync
1. Aynı ürünleri tekrar sync et
2. ✅ "ALT text zaten güncel" mesajı almalısın
3. ✅ Gereksiz API çağrısı yapılmamalı

---

## 📝 Versiyon Notları

**Versiyon:** 1.0  
**Tarih:** 6 Ekim 2025  
**Durum:** ✅ Production Ready

### Değişiklikler:
- ✅ Yeni `update_product_media_seo()` fonksiyonu eklendi
- ✅ SEO dostu filename generator eklendi
- ✅ Sync runner'a özel SEO modu entegrasyonu
- ✅ Rate limit koruması eklendi
- ✅ Detaylı log mesajları

### Bilinen Sınırlamalar:
- Shopify API ile dosya ismi direkt değiştirilemez (CDN limitasyonu)
- Sadece IMAGE tipindeki medyalar desteklenir (VIDEO/3D model değil)
- Maksimum 250 resim/ürün işlenebilir (Shopify API limiti)

---

## 🆘 Sorun Giderme

### "Güncellenecek resim bulunamadı"
**Çözüm:** Ürünün hiç resmi yoksa bu normal. Önce resim ekleyin.

### "Rate limit exceeded"
**Çözüm:** Bekleme süresi otomatik artar. Birkaç dakika bekleyin.

### "ALT text güncellenemedi"
**Çözüm:** Shopify API erişim izinlerini kontrol edin (write_products gerekli).

---

## 📞 Destek

Sorun yaşarsanız:
1. Log dosyalarını kontrol edin
2. Shopify API durumunu kontrol edin
3. Test modunda küçük bir grup ile test edin

**İletişim:** GitHub Issues
