# 🐛 BUG FIX: Kategori ID Format Hatası

## 🔍 Tespit Edilen Sorun

**Önerilen kategoriler kabul edilmiyordu çünkü YANLIŞ FORMAT kullanılıyordu!**

### Kod İncelemesi Sonucu:

```python
# ❌ YANLIŞ (Önceki kod):
category_keywords = {
    't-shirt': 'gid://shopify/TaxonomyCategory/aa-2-6-14',  # ← GID formatı
}

# Mutation'da:
"category": suggested_category['id']  # ← GID'yi doğrudan gönderiyordu
```

### Shopify API Bekledikleri:

| Durum | Beklenen Format | Örnek |
|-------|----------------|-------|
| **GraphQL Query** (taxonomyCategory) | GID formatı | `gid://shopify/TaxonomyCategory/aa-2-6-14` |
| **GraphQL Mutation** (productUpdate) | Sadece ID | `aa-2-6-14` |

### Hata Sebep:

1. Dictionary'de GID formatında saklıyorduk: `gid://shopify/TaxonomyCategory/aa-2-6-14`
2. Query için GID gerekiyor ✅ → DOĞRU
3. **AMA** Mutation için sadece ID gerekiyor ❌ → YANLIŞ!

```
Query çağrısı:  "gid://shopify/TaxonomyCategory/aa-2-6-14" ✅
                           ↓
Mutation gönderir:  "gid://shopify/TaxonomyCategory/aa-2-6-14" ❌ (HATA!)
Mutation bekler:    "aa-2-6-14" ✅ (DOĞRU!)
```

## ✅ Çözüm

### Değişiklik 1: Dictionary'de Sadece ID Sakla

```python
# ✅ DOĞRU (Yeni kod):
category_keywords = {
    't-shirt': 'aa-2-6-14',  # ← Sadece taxonomy ID
    'tişört': 'aa-2-6-14',
    'bluz': 'aa-2-6-2',
    # ... diğerleri
}
```

### Değişiklik 2: Query İçin GID Formatı Oluştur

```python
# Query GID bekliyor, onu oluştur:
for keyword, category_id in category_keywords.items():
    if keyword in title_lower:
        category_gid = f"gid://shopify/TaxonomyCategory/{category_id}"  # ← GID oluştur
        
        cat_result = self.execute_graphql(category_query, {"id": category_gid})
        suggested_category = cat_result.get('taxonomyCategory')
        
        if suggested_category:
            # Mutation için sadece ID'yi sakla
            suggested_category['taxonomy_id'] = category_id  # ← aa-2-6-14
            # ...
```

### Değişiklik 3: Mutation'da Sadece ID Kullan

```python
# ❌ ÖNCE (YANLIŞ):
result = self.execute_graphql(
    category_mutation,
    {
        "input": {
            "id": product_gid,
            "category": suggested_category['id']  # ← GID gönderiyordu! HATA!
        }
    }
)

# ✅ SONRA (DOĞRU):
result = self.execute_graphql(
    category_mutation,
    {
        "input": {
            "id": product_gid,
            "category": suggested_category['taxonomy_id']  # ← Sadece ID! DOĞRU!
        }
    }
)
```

## 📊 Çalışma Akışı

### ÖNCE (HATA):

```
1. Keyword bulundu: "t-shirt"
   ↓
2. Dictionary'den: "gid://shopify/TaxonomyCategory/aa-2-6-14"
   ↓
3. Query gönder: "gid://shopify/TaxonomyCategory/aa-2-6-14" ✅
   ↓
4. Cevap geldi: {
     "id": "gid://shopify/TaxonomyCategory/aa-2-6-14",
     "fullName": "Apparel > Clothing > Tops > T-shirts"
   }
   ↓
5. Mutation gönder: "category": "gid://shopify/TaxonomyCategory/aa-2-6-14" ❌
   ↓
6. SHOPIFY: "Kategori set edilemedi, format yanlış!" ❌
```

### SONRA (DOĞRU):

```
1. Keyword bulundu: "t-shirt"
   ↓
2. Dictionary'den: "aa-2-6-14"
   ↓
3. GID oluştur: "gid://shopify/TaxonomyCategory/aa-2-6-14"
   ↓
4. Query gönder: "gid://shopify/TaxonomyCategory/aa-2-6-14" ✅
   ↓
5. Cevap geldi: {
     "id": "gid://shopify/TaxonomyCategory/aa-2-6-14",
     "fullName": "Apparel > Clothing > Tops > T-shirts"
   }
   ↓
6. taxonomy_id sakla: "aa-2-6-14"
   ↓
7. Mutation gönder: "category": "aa-2-6-14" ✅
   ↓
8. SHOPIFY: "Kategori başarıyla set edildi!" ✅
```

## 🎯 Beklenen Sonuç

### Shopify Admin'de:

**ÖNCE:**
```
Kategori: Snowboard'lar Kayak ve Snowboard içinde ❌
Önerilen: T-Shirts Clothing Tops içinde
(Öneri kabul edilmiyor, çünkü mutation hatalı format kullanıyor)
```

**SONRA:**
```
Kategori: T-Shirts Clothing Tops içinde ✅
Meta alanlar: Renk, Geometrik, Boyut (otomatik eklendi) ✅
(Öneri başarıyla kabul edildi ve uygulandı!)
```

## 📝 Güncellenen Dosyalar

- ✅ `connectors/shopify_api.py`
  - `get_product_recommendations()` fonksiyonu:
    - ✅ Dictionary'de GID kaldırıldı, sadece ID saklanıyor
    - ✅ Query için dinamik GID oluşturuluyor
    - ✅ `taxonomy_id` alanı eklendi
  - `update_product_category_and_metafields()` fonksiyonu:
    - ✅ Mutation'da `suggested_category['taxonomy_id']` kullanılıyor
    - ✅ GID yerine sadece ID gönderiliyor

## 🧪 Test Etmek İçin

```powershell
streamlit run streamlit_app.py
```

1. "Otomatik Kategori ve Meta Alan" sayfasına git
2. Test modu + DRY RUN aktif
3. **"🎯 Shopify Önerilerini Kullan"** işaretli
4. "Güncellemeyi Başlat"

### Beklenen Log:

```
📦 Test Ürün: 'Kadın Kırmızı V Yaka T-shirt'
🎯 Önerilen kategori bulundu: Apparel > Clothing > Tops > T-shirts ('t-shirt' kelimesinden)
📊 Shopify Önerileri:
   Kategori: Apparel > Clothing > Tops > T-shirts
   Önerilen Attribute'ler: Renk, Geometrik, Boyut

[GraphQL Mutation Gönderiliyor]
Input: {
  "id": "gid://shopify/Product/...",
  "category": "aa-2-6-14"  ← SADECE ID, GID YOK!
}

✅ Shopify önerisi kategori set edildi: Apparel > Clothing > Tops > T-shirts
   ➕ Shopify önerisi eklendi: Geometrik (geometrik)
   ➕ Shopify önerisi eklendi: Boyut (boyut)
✅ 74 meta alan güncellendi
```

---

**TL;DR:** Kategori ID'sini GID formatıyla mutation'a gönderiyorduk, ama Shopify **sadece taxonomy ID** istiyor! Format düzeltildi: `gid://shopify/TaxonomyCategory/aa-2-6-14` → `aa-2-6-14` 🎉
