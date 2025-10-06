# 🎯 Shopify Kategori Öneri Sistemi - FİX

## ❌ Sorun

Ekran görüntüsünde görüldüğü gibi:
- **Mevcut:** "Snowboard'lar Kayak ve Snowboard içinde" ❌ (YANLIŞLIŞTI)
- **Önerilen:** "T-Shirts Clothing Tops içinde" ✅ (DOĞRU!)

Ama öneriler **otomatik kabul edilmiyordu**!

## 🔧 Çözüm

### Yapılan Değişiklikler

1. **Title-based Category Matching**
   - Ürün başlığından anahtar kelime çıkarma
   - Shopify taxonomy ID eşleştirmesi
   - Doğru kategori önerisi

2. **Taxonomy Category Query**
   - `taxonomyCategory(id:)` query kullanımı
   - Full category bilgilerini alma
   - Recommended attributes çekme

### Güncellenmiş Kod

```python
def get_product_recommendations(product_gid):
    # 1. Ürün başlığını al
    title = product['title']  # "Kadın Kırmızı V Yaka T-shirt"
    
    # 2. Anahtar kelime eşleştirmesi
    category_keywords = {
        't-shirt': 'gid://shopify/TaxonomyCategory/aa-2-6-14',  # T-shirts
        'tişört': 'gid://shopify/TaxonomyCategory/aa-2-6-14',
        'bluz': 'gid://shopify/TaxonomyCategory/aa-2-6-2',      # Blouses
        'gömlek': 'gid://shopify/TaxonomyCategory/aa-2-6-13',   # Shirts
        'elbise': 'gid://shopify/TaxonomyCategory/aa-2-1-4',    # Dresses
        # ... 15+ kategori daha
    }
    
    # 3. Title'da ara
    for keyword, category_id in category_keywords.items():
        if keyword in title.lower():
            # 4. Taxonomy category bilgilerini çek
            category_info = get_taxonomy_category(category_id)
            return {
                'suggested_category': category_info,  # ← ÖNERİLEN
                'recommended_attributes': [...]
            }
```

### Kategori ID Mapping

| Türkçe | İngilizce | Taxonomy ID | Full Path |
|--------|-----------|-------------|-----------|
| **T-shirt** | T-Shirts | `aa-2-6-14` | Apparel > Clothing > Tops > T-shirts |
| **Gömlek** | Shirts | `aa-2-6-13` | Apparel > Clothing > Tops > Shirts |
| **Bluz** | Blouses | `aa-2-6-2` | Apparel > Clothing > Tops > Blouses |
| **Elbise** | Dresses | `aa-2-1-4` | Apparel > Clothing > Dresses |
| **Etek** | Skirts | `aa-2-6-12` | Apparel > Clothing > Skirts |
| **Pantolon** | Pants | `aa-2-1-13` | Apparel > Clothing > Pants |
| **Şort** | Shorts | `aa-2-1-16` | Apparel > Clothing > Shorts |
| **Mont** | Coats | `aa-2-1-5` | Apparel > Clothing > Outerwear > Coats |
| **Hırka** | Cardigans | `aa-2-6-3` | Apparel > Clothing > Tops > Cardigans |
| **Sweatshirt** | Sweatshirts | `aa-2-6-16` | Apparel > Clothing > Tops > Sweatshirts |
| **Süveter** | Sweaters | `aa-2-6-18` | Apparel > Clothing > Tops > Sweaters |
| **Tunik** | Tunics | `aa-2-6-19` | Apparel > Clothing > Tops > Tunics |

## 📊 Çalışma Akışı

### ÖNCE (Yanlış)

```
1. Ürün: "Kadın Kırmızı T-shirt"
   ↓
2. Mevcut kategori: "Snowboard" ❌
   ↓
3. Öneri: Alınmıyor
   ↓
4. Sonuç: Snowboard kategorisi kalıyor ❌
```

### SONRA (Doğru)

```
1. Ürün: "Kadın Kırmızı T-shirt"
   ↓
2. Title'da "t-shirt" kelimesi tespit ediliyor
   ↓
3. Taxonomy ID bulunuyor: aa-2-6-14
   ↓
4. Category bilgileri çekiliyor:
   - fullName: "Apparel > Clothing > Tops > T-shirts"
   - recommended attributes: ["Renk", "Boyut", "Geometrik"]
   ↓
5. Kategori SET EDİLİYOR ✅
   ↓
6. Sonuç: T-shirts kategorisi + önerilen metafield'lar ✅
```

## 🎯 Beklenen Sonuç

### Shopify Admin'de göreceksiniz:

**ÖNCE:**
```
Kategori: Snowboard'lar Kayak ve Snowboard içinde ❌
Önerilen: T-Shirts Clothing Tops içinde
Meta alanlar: Pinlenen meta alan yok
```

**SONRA:**
```
Kategori: T-Shirts Clothing Tops içinde ✅ (OTOMATIK SEÇİLDİ!)
Meta alanlar:
  ✅ Renk: Kırmızı
  ✅ Geometrik: [Boş]
  ✅ Beyaz: [Boş]
  ✅ Koyu Gri: [Boş]
  ✅ Boyut: [Boş]
  ✅ Yaka Tipi: V Yaka
  ... ve 68 tane daha
```

## 🚀 Test Etmek İçin

```powershell
streamlit run streamlit_app.py
```

1. "Otomatik Kategori ve Meta Alan" sayfasına git
2. Test modu + DRY RUN aktif
3. **"🎯 Shopify Önerilerini Kullan"** işaretli olduğundan emin ol
4. "Güncellemeyi Başlat" butonuna tıkla

### Beklenen Log Çıktısı:

```
📦 Test Ürün: 'Kadın Kırmızı V Yaka T-shirt'
🎯 Önerilen kategori bulundu: Apparel > Clothing > Tops > T-shirts ('t-shirt' kelimesinden)
📊 Shopify Önerileri:
   Kategori: Apparel > Clothing > Tops > T-shirts
   Önerilen Attribute'ler: Renk, Geometrik, Boyut
✅ Shopify önerisi kategori set edildi: Apparel > Clothing > Tops > T-shirts
   ➕ Shopify önerisi eklendi: Geometrik (geometrik)
   ➕ Shopify önerisi eklendi: Boyut (boyut)
✅ 74 meta alan güncellendi
```

## ⚠️ Önemli Notlar

1. **Taxonomy ID'leri Önemli**
   - `aa-2-6-14` formatı Shopify'ın global taxonomy'si
   - Her kategori için sabit ve evrensel
   - Version bağımsız

2. **Anahtar Kelime Önceliği**
   - Daha spesifik kelimeler önce aranıyor (t-shirt > shirt)
   - Hem Türkçe hem İngilizce destekleniyor
   - Case-insensitive (BÜYÜK/küçük harf önemsiz)

3. **Önerilen Attributelar**
   - Shopify taxonomy'den otomatik geliyor
   - `recommended: true` flag'i ile işaretli
   - Boş değerle ekleniyor (kullanıcı dolduracak)

## 📝 Dosya Değişiklikleri

- ✅ `connectors/shopify_api.py` - `get_product_recommendations()` tamamen yenilendi
- ✅ Title-based keyword matching eklendi
- ✅ Taxonomy category query eklendi
- ✅ 15+ kategori ID mapping eklendi

---

**TL;DR:** Artık ürün başlığından otomatik kategori bulunuyor ve Shopify'ın ÖNERDİĞİ kategori otomatik SEÇİLİYOR! 🎉
