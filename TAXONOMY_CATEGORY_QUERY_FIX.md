# 🔧 taxonomyCategory Query Hatası - FIX

## ❌ Hata

```
Field 'taxonomyCategory' doesn't exist on type 'QueryRoot'
```

**Sorun:** Shopify GraphQL API'da `taxonomyCategory(id:)` adında direkt bir query **YOK**!

## 🔍 Kök Sebep

### Yanlış Varsayım

Kod şunu yapmaya çalışıyordu:
```graphql
query getCategoryInfo($id: ID!) {
    taxonomyCategory(id: $id) {  # ← BU QUERY YOK!
        id
        fullName
        name
        attributes { ... }
    }
}
```

### Shopify API Gerçeği

Shopify'da sadece şu yollar var:
1. **`taxonomy.categories`** - Filtreleme ile kategori listesi (ama ID ile direkt getirme yok)
2. **`product.category`** - Ürünün mevcut kategorisi (zaten alıyoruz)

**Sonuç:** Kategori bilgilerini ID ile direkt query edemiyoruz!

## ✅ Çözüm: Static Mapping

Gereksiz query yerine **static mapping** kullanıyoruz:

### 1️⃣ Kategori Adlarını Manuel Tanımla

```python
category_names = {
    'aa-2-6-14': 'Apparel > Clothing > Tops > T-shirts',
    'aa-2-6-2': 'Apparel > Clothing > Tops > Blouses',
    'aa-2-1-4': 'Apparel > Clothing > Dresses',
    'aa-2-6-13': 'Apparel > Clothing > Tops > Shirts',
    'aa-2-6-12': 'Apparel > Clothing > Skirts',
    'aa-2-1-13': 'Apparel > Clothing > Pants',
    'aa-2-1-16': 'Apparel > Clothing > Shorts',
    'aa-2-1-5': 'Apparel > Clothing > Outerwear > Coats & Jackets',
    'aa-2-6-3': 'Apparel > Clothing > Tops > Cardigans',
    'aa-2-6-16': 'Apparel > Clothing > Tops > Sweatshirts',
    'aa-2-6-18': 'Apparel > Clothing > Tops > Sweaters',
    'aa-2-6-19': 'Apparel > Clothing > Tops > Tunics',
}
```

### 2️⃣ Keyword'den Direkt Kategori Oluştur

```python
# ÖNCE (YANLIŞ):
category_gid = f"gid://shopify/TaxonomyCategory/{category_id}"
cat_result = self.execute_graphql(category_query, {"id": category_gid})  # ← HATA!
suggested_category = cat_result.get('taxonomyCategory')

# SONRA (DOĞRU):
suggested_taxonomy_id = category_id
category_full_name = category_names.get(category_id, f'Category {category_id}')

suggested_category = {
    'id': f"gid://shopify/TaxonomyCategory/{suggested_taxonomy_id}",
    'taxonomy_id': suggested_taxonomy_id,  # ← Mutation için
    'fullName': category_full_name,
    'name': category_full_name.split(' > ')[-1]  # ← Son kısım (örn: "T-shirts")
}
```

## 📊 Çalışma Akışı

### ❌ ÖNCE (HATA):

```
1. Title'da keyword bul: "t-shirt"
   ↓
2. Dictionary'den taxonomy ID al: "aa-2-6-14"
   ↓
3. GID oluştur: "gid://shopify/TaxonomyCategory/aa-2-6-14"
   ↓
4. GraphQL query gönder: taxonomyCategory(id: ...) ❌
   ↓
5. HATA: "Field 'taxonomyCategory' doesn't exist on type 'QueryRoot'"
```

### ✅ SONRA (DOĞRU):

```
1. Title'da keyword bul: "t-shirt"
   ↓
2. Dictionary'den taxonomy ID al: "aa-2-6-14"
   ↓
3. Static mapping'den full name al: "Apparel > Clothing > Tops > T-shirts"
   ↓
4. Suggested category objesi oluştur (query YOK!)
   ↓
5. taxonomy_id'yi mutation için sakla: "aa-2-6-14"
   ↓
6. Mutation'da kullan ✅
```

## 📝 Yapılan Değişiklikler

### `connectors/shopify_api.py` - `get_product_recommendations()`

**DEĞİŞİKLİK 1:** taxonomyCategory query kaldırıldı

```diff
- category_gid = f"gid://shopify/TaxonomyCategory/{category_id}"
- category_query = """
-     query getCategoryInfo($id: ID!) {
-         taxonomyCategory(id: $id) {
-             id
-             fullName
-             name
-             attributes { ... }
-         }
-     }
- """
- cat_result = self.execute_graphql(category_query, {"id": category_gid})
- suggested_category = cat_result.get('taxonomyCategory')
```

**DEĞİŞİKLİK 2:** Static mapping eklendi

```diff
+ suggested_taxonomy_id = category_id
+ category_names = {
+     'aa-2-6-14': 'Apparel > Clothing > Tops > T-shirts',
+     'aa-2-6-2': 'Apparel > Clothing > Tops > Blouses',
+     # ... 10+ kategori daha
+ }
+ category_full_name = category_names.get(category_id, f'Category {category_id}')
```

**DEĞİŞİKLİK 3:** Manuel category objesi oluştur

```diff
+ suggested_category = {
+     'id': f"gid://shopify/TaxonomyCategory/{suggested_taxonomy_id}",
+     'taxonomy_id': suggested_taxonomy_id,
+     'fullName': category_full_name,
+     'name': category_full_name.split(' > ')[-1]
+ }
```

**DEĞİŞİKLİK 4:** Attribute'leri mevcut category'den al

```diff
- attrs_source = suggested_category or current_category
- if attrs_source and attrs_source.get('attributes'):
+ if current_category and current_category.get('attributes'):
      for edge in current_category['attributes']['edges']:
```

## 🎯 Neden Static Mapping?

### Avantajlar:

1. **Hız:** Gereksiz GraphQL query yok ✅
2. **Basitlik:** Kod daha basit ve anlaşılır ✅
3. **Kontrol:** Tam olarak hangi kategorilerin desteklendiğini biliyoruz ✅
4. **Hata Yok:** taxonomyCategory query hatası çözüldü ✅

### Dezavantajlar:

1. **Manuel Güncelleme:** Yeni kategori eklemek için kod güncellemesi gerekli
2. **Sınırlı Kapsam:** Sadece tanımlı kategoriler destekleniyor (şu an 12 kategori)

**Ama:** Zaten keyword-based matching kullanıyoruz, yani otomatik olarak tüm kategorileri destekleyemiyoruz. Static mapping daha pratik!

## 📚 Desteklenen Kategoriler

| Taxonomy ID | Full Name | Keyword'ler |
|-------------|-----------|-------------|
| `aa-2-6-14` | Apparel > Clothing > Tops > T-shirts | t-shirt, tshirt, tişört |
| `aa-2-6-2` | Apparel > Clothing > Tops > Blouses | blouse, bluz |
| `aa-2-1-4` | Apparel > Clothing > Dresses | dress, elbise |
| `aa-2-6-13` | Apparel > Clothing > Tops > Shirts | shirt, gömlek |
| `aa-2-6-12` | Apparel > Clothing > Skirts | skirt, etek |
| `aa-2-1-13` | Apparel > Clothing > Pants | pants, pantolon |
| `aa-2-1-16` | Apparel > Clothing > Shorts | shorts, şort |
| `aa-2-1-5` | Apparel > Clothing > Outerwear > Coats | coat, jacket, mont |
| `aa-2-6-3` | Apparel > Clothing > Tops > Cardigans | cardigan, hırka |
| `aa-2-6-16` | Apparel > Clothing > Tops > Sweatshirts | sweatshirt, hoodie |
| `aa-2-6-18` | Apparel > Clothing > Tops > Sweaters | sweater, süveter |
| `aa-2-6-19` | Apparel > Clothing > Tops > Tunics | tunic, tunik |

## 🎓 Shopify Taxonomy Query Gerçeği

Shopify API'da taxonomy query şu şekilde:

```graphql
query {
  taxonomy {
    categories(search: "T-shirt") {  # ← search ile filtreleme
      edges {
        node {
          id
          fullName
          name
        }
      }
    }
  }
}
```

**Ama:**
- ID ile direkt query **YOK** ❌
- Search her zaman birden fazla sonuç döner
- Tam olarak istediğimiz kategoriyi bulmak garanti değil

**Sonuç:** Static mapping daha güvenilir ve hızlı!

## ✅ Özet

**SORUN:** `taxonomyCategory(id:)` query'si Shopify API'da yok

**ÇÖZÜM:** Static mapping ile kategori bilgilerini tutuyoruz

**SONUÇ:**
- ✅ Gereksiz GraphQL query kaldırıldı
- ✅ Hata çözüldü
- ✅ Kod daha hızlı ve basit
- ✅ 12 kategori destekleniyor

---

**TL;DR:** `taxonomyCategory` query yok! Bunun yerine static mapping kullanıyoruz: keyword → taxonomy ID → manuel full name. Daha hızlı, daha basit! 🚀
