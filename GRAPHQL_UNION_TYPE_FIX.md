# 🔧 GraphQL Union Type Hatası - FIX

## ❌ Hata Mesajı

```
GraphQL Error: Selections can't be made directly on unions 
(see selections on TaxonomyCategoryAttribute)
```

**Sorun:** `TaxonomyCategoryAttribute` bir **union type** olduğu için doğrudan field'larına erişemiyoruz!

## 🔍 Kök Sebep

### GraphQL Union Type Nedir?

Union type, birden fazla farklı tipi temsil edebilen bir GraphQL type'dır. Shopify'ın `TaxonomyCategoryAttribute` union'ı:

```graphql
union TaxonomyCategoryAttribute = TaxonomyValue | TaxonomyAttribute
```

Bu şu demek:
- `TaxonomyValue`: Enum değerler (örn: "Kırmızı", "Mavi", "L", "XL")
- `TaxonomyAttribute`: Text/Number değerler (örn: "Beden", "Renk")

### Neden Hata Verdi?

```graphql
# ❌ YANLIŞ (Eski kod):
attributes(first: 50) {
    edges {
        node {
            name          # ← Union'da direkt field erişimi YASAK!
            recommended   # ← Hata burada!
        }
    }
}
```

GraphQL şöyle diyor: 
> "Bu `node` bir `TaxonomyValue` mı yoksa `TaxonomyAttribute` mi? Ben bilemem, sen söyle!"

## ✅ Çözüm: Inline Fragments

Union type'larda **inline fragment** kullanmalıyız:

```graphql
# ✅ DOĞRU (Yeni kod):
attributes(first: 50) {
    edges {
        node {
            ... on TaxonomyValue {      # ← "Eğer TaxonomyValue ise..."
                name
                recommended
            }
            ... on TaxonomyAttribute {  # ← "Eğer TaxonomyAttribute ise..."
                name
                recommended
            }
        }
    }
}
```

Bu syntax şu anlama geliyor:
- **`... on TaxonomyValue`**: "Node TaxonomyValue type'ındaysa, name ve recommended field'larını getir"
- **`... on TaxonomyAttribute`**: "Node TaxonomyAttribute type'ındaysa, name ve recommended field'larını getir"

## 📝 Yapılan Değişiklikler

### 1️⃣ `getProductInfo` Query'si

**Dosya:** `connectors/shopify_api.py` - `get_product_recommendations()` fonksiyonu

**ÖNCE:**
```graphql
query getProductInfo($id: ID!) {
    product(id: $id) {
        category {
            attributes(first: 50) {
                edges {
                    node {
                        name          # ❌ Direkt erişim
                        recommended   # ❌ Hata!
                    }
                }
            }
        }
    }
}
```

**SONRA:**
```graphql
query getProductInfo($id: ID!) {
    product(id: $id) {
        category {
            attributes(first: 50) {
                edges {
                    node {
                        ... on TaxonomyValue {      # ✅ Inline fragment
                            name
                            recommended
                        }
                        ... on TaxonomyAttribute {  # ✅ Inline fragment
                            name
                            recommended
                        }
                    }
                }
            }
        }
    }
}
```

### 2️⃣ `getCategoryInfo` Query'si

**Dosya:** `connectors/shopify_api.py` - `get_product_recommendations()` fonksiyonu

**ÖNCE:**
```graphql
query getCategoryInfo($id: ID!) {
    taxonomyCategory(id: $id) {
        attributes(first: 50) {
            edges {
                node {
                    name          # ❌ Direkt erişim
                    recommended   # ❌ Hata!
                }
            }
        }
    }
}
```

**SONRA:**
```graphql
query getCategoryInfo($id: ID!) {
    taxonomyCategory(id: $id) {
        attributes(first: 50) {
            edges {
                node {
                    ... on TaxonomyValue {      # ✅ Inline fragment
                        name
                        recommended
                    }
                    ... on TaxonomyAttribute {  # ✅ Inline fragment
                        name
                        recommended
                    }
                }
            }
        }
    }
}
```

## 🎓 GraphQL Union Type Kuralları

### Kural 1: Direkt Field Erişimi Yasak

```graphql
# ❌ YANLIŞ:
node {
    name
}
```

### Kural 2: Inline Fragment Kullan

```graphql
# ✅ DOĞRU:
node {
    ... on Type1 {
        name
    }
    ... on Type2 {
        name
    }
}
```

### Kural 3: Tüm Union Member'ları İçin Fragment Ekle

Eğer union 3 tip içeriyorsa, 3'ü için de fragment ekle:

```graphql
node {
    ... on Type1 { name }
    ... on Type2 { name }
    ... on Type3 { name }
}
```

## 📊 Shopify Taxonomy Attribute Types

### TaxonomyValue

Enum değerler için kullanılır:

```json
{
  "__typename": "TaxonomyValue",
  "name": "Renk",
  "recommended": true,
  "value": {
    "id": "gid://shopify/TaxonomyValue/...",
    "name": "Kırmızı"
  }
}
```

### TaxonomyAttribute

Text/Number değerler için kullanılır:

```json
{
  "__typename": "TaxonomyAttribute",
  "name": "Beden",
  "recommended": true
}
```

## 🧪 Test Sonucu

### ÖNCE (HATA):
```
ERROR: Selections can't be made directly on unions
(see selections on TaxonomyCategoryAttribute)
```

### SONRA (BAŞARILI):
```
🎯 Önerilen kategori bulundu: Apparel > Clothing > Tops > T-shirts
📊 Shopify Önerileri:
   Kategori: T-shirts
   Önerilen Attribute'ler: Renk, Geometrik, Boyut
✅ Kategori set edildi!
```

## 📚 Kaynaklar

- [GraphQL Union Types Documentation](https://graphql.org/learn/schema/#union-types)
- [Shopify Admin API - Product Category](https://shopify.dev/docs/api/admin-graphql/latest/objects/Product#field-product-category)
- [Shopify Taxonomy Attributes](https://shopify.dev/docs/api/admin-graphql/latest/unions/TaxonomyCategoryAttribute)

## ✅ Özet

**SORUN:** Union type'da direkt field erişimi yapıyorduk ❌

**ÇÖZÜM:** Inline fragment kullanıyoruz ✅

```diff
- node {
-     name
-     recommended
- }

+ node {
+     ... on TaxonomyValue {
+         name
+         recommended
+     }
+     ... on TaxonomyAttribute {
+         name
+         recommended
+     }
+ }
```

---

**TL;DR:** GraphQL union type'larda `... on TypeName` syntax'ı kullanmak zorunludur! 🚀
