# 🎯 TAXONOMY ATTRIBUTES vs CUSTOM METAFIELDS - AÇIKLAMA

## 📌 Durum Analizi

Resimlerde gördüğünüz meta alanlar **2 farklı tip**:

### 1️⃣ Shopify Taxonomy Attributes (Standart Alanlar)
Shopify'ın kategori sistemine bağlı otomatik gelen alanlar:

**Elbise kategorisi için**:
- ✅ Renk
- ✅ Boyut  
- ✅ Kumaş
- ✅ Yaş Grubu
- ✅ Giysi özellikleri
- ✅ Elbise etkinliği
- ✅ Elbise stili
- ✅ **Yaka Çizgisi** (Neckline)
- ✅ Etek/Elbise uzunluk türü
- ✅ **Kol Uzunluğu Tipi** (Sleeve Length)
- ✅ Hedef Cinsiyet

**Pantolon kategorisi için**:
- ✅ Renk
- ✅ Boyut
- ✅ Kumaş
- ✅ Fit
- ✅ **Pantolon uzunluğu türü**
- ✅ **Bel Yükseltme** (Rise)
- ✅ Hedef Cinsiyet

### 2️⃣ Custom Metafields (Bizim Oluşturduğumuz)
Kodumuzda tanımladığımız custom alanlar:

- `custom.renk`
- `custom.yaka_tipi`
- `custom.kol_tipi`
- `custom.boy`
- `custom.pacha_tipi`
- `custom.bel_tipi`

## ❌ Sorun

**Taxonomy attribute'ler** ve **custom metafield'lar** **FARKLI ŞEY**LER!

```
Shopify Taxonomy:
  Yaka Çizgisi (Neckline)          ≠  custom.yaka_tipi
  Kol Uzunluğu Tipi (Sleeve Length) ≠  custom.kol_tipi
  Bel Yükseltme (Rise)             ≠  custom.bel_tipi
```

**Biz ne yapıyoruz:**
- `custom.yaka_tipi` = "V Yaka" yazıyoruz ✅
- Ama bu **"Yaka Çizgisi"** alanına gitmiyor ❌

**Shopify ne bekliyor:**
- **Taxonomy attribute "Neckline"** = "V-Neck" 
- Bu alan kategori ile otomatik gelir ✅
- Ama biz değer yazmıyoruz ❌

## ✅ Çözümler

### Çözüm 1: Sadece Kategori Set Et (Mevcut Durum)
```
✅ Kategori set edilir (örn: T-Shirts - aa-1-13-8)
✅ Taxonomy attribute'ler otomatik görünür
❌ Değerler boş kalır (manuel doldurulmalı)
```

**Avantaj**: Basit, hızlı  
**Dezavantaj**: Alanlar görünür ama boş

### Çözüm 2: Custom Metafield Kullan (Şu Anki Kod)
```
✅ Kategori set edilir
✅ Custom metafield'lara değer yazılır (custom.yaka_tipi = "V Yaka")
❌ Taxonomy attribute'ler boş kalır (farklı alanlar)
```

**Avantaj**: Bizim kontrolümüzde custom alanlar  
**Dezavantaj**: Taxonomy standart alanları doldurmuyor

### Çözüm 3: İKİSİNİ DE YAP! (ÖNERİLEN) ⭐
```
✅ Kategori set edilir → Taxonomy attributes görünür
✅ Custom metafield'lara değer yazılır → Bizim alanlar dolu
✅ Taxonomy attribute'lere DE değer yazılır → Standart alanlar dolu
```

**Avantaj**: Hem Shopify standartları hem custom alanlar dolu  
**Dezavantaj**: Daha karmaşık API kullanımı gerekir

## 🔧 Çözüm 3'ü Nasıl Uygularız?

### Adım 1: Taxonomy Attribute Mapping

```python
# custom key -> Shopify taxonomy attribute
attribute_mapping = {
    'yaka_tipi': {
        'taxonomy_name': 'Neckline',
        'values': {
            'V Yaka': 'V-Neck',
            'Bisiklet Yaka': 'Crew Neck',
            'Polo Yaka': 'Polo',
            'Boğazlı': 'Turtleneck',
        }
    },
    'kol_tipi': {
        'taxonomy_name': 'Sleeve Length',
        'values': {
            'Uzun Kol': 'Long Sleeve',
            'Kısa Kol': 'Short Sleeve',
            'Kolsuz': 'Sleeveless',
        }
    },
    'boy': {
        'taxonomy_name': 'Length',  # veya 'Skirt/Dress Length Type'
        'values': {
            'Maxi': 'Maxi',
            'Midi': 'Midi',
            'Mini': 'Mini',
        }
    },
    'bel_tipi': {
        'taxonomy_name': 'Rise',
        'values': {
            'Yüksek Bel': 'High Rise',
            'Normal Bel': 'Regular Rise',
            'Düşük Bel': 'Low Rise',
        }
    }
}
```

### Adım 2: Taxonomy Attribute'lere Yaz

**Mevcut durum** (sadece custom metafield):
```python
metafields = [
    {'namespace': 'custom', 'key': 'yaka_tipi', 'value': 'V Yaka', 'type': 'single_line_text_field'}
]

shopify_api.update_product_metafields(product_gid, metafields)
```

**Yeni yaklaşım** (hem custom hem taxonomy):
```python
# 1. Custom metafield'lara yaz (mevcut)
metafields = [
    {'namespace': 'custom', 'key': 'yaka_tipi', 'value': 'V Yaka', 'type': 'single_line_text_field'}
]
shopify_api.update_product_metafields(product_gid, metafields)

# 2. Taxonomy attribute'lere de yaz (YENİ!)
taxonomy_attrs = map_to_taxonomy(metafields)  # [{'name': 'Neckline', 'value': 'V-Neck'}]
shopify_api.update_taxonomy_attributes(product_gid, taxonomy_attrs)
```

### Adım 3: API Implementation

Shopify'da taxonomy attribute'lere yazmak için iki yol var:

#### Yol 1: productSet Mutation (2024-10 API)
```graphql
mutation productSet($input: ProductSetInput!) {
    productSet(input: $input) {
        product {
            id
            category {
                id
            }
        }
        userErrors {
            field
            message
        }
    }
}
```

**Input**:
```json
{
  "input": {
    "id": "gid://shopify/Product/123",
    "productOptions": [...],
    "standardizedProductType": {
      "productTaxonomyNodeId": "gid://shopify/TaxonomyCategory/aa-1-13-8"
    }
  }
}
```

#### Yol 2: Metafield ile (Daha Basit)
Shopify'ın taxonomy attribute'leri aslında özel bir namespace'de metafield olarak saklanıyor olabilir.

## 📝 ŞİMDİLİK YAPILACAKLAR

### 1. Kategori Set Ediliyor mu? → ✅ EVET
```python
result = shopify_api.update_product_category_and_metafields(
    product_gid=gid,
    category=category,
    metafields=metafields
)
```
Kategori başarıyla set ediliyor → Taxonomy attributes **görünüyor** ✅

### 2. Custom Metafield'lar Yazılıyor mu? → ✅ EVET  
```python
metafields = [
    {'namespace': 'custom', 'key': 'yaka_tipi', 'value': 'V Yaka'}
]
```
Custom metafield'lar başarıyla yazılıyor ✅

### 3. Taxonomy Attribute'ler Dolu mu? → ❌ HAYIR
```
Yaka Çizgisi: (boş)
Kol Uzunluğu Tipi: (boş)
```
Taxonomy attribute'lere değer yazılmıyor ❌

## 🎯 Sonuç ve Öneriler

### Kısa Vadede (Mevcut Sistem)
1. ✅ Kategori otomatik set ediliyor → Taxonomy alanlar görünüyor
2. ✅ Custom metafield'lar doluyor → Kendi alanlarımız var
3. ⚠️ Taxonomy alanları **manuel doldurulmalı**

**Kullanıcı ne yapmalı:**
- Shopify Admin'de ürüne git
- Taxonomy attribute'leri (Yaka Çizgisi, Kol Uzunluğu vb.) **elle doldur**
- VEYA custom metafield'lardan (custom.yaka_tipi) değerleri kopyala

### Uzun Vadede (Geliştirilecek)
1. ✅ Taxonomy attribute mapping ekle
2. ✅ Türkçe → İngilizce değer çevirisi (V Yaka → V-Neck)
3. ✅ `productSet` veya özel metafield ile taxonomy attribute'lere yaz
4. ✅ Hem custom hem taxonomy alanları otomatik doldur

## 💡 Geçici Çözüm

Şimdilik **en iyi yaklaşım**:

1. **Kategoriyi set et** → Taxonomy alanlar görünür ✅
2. **Custom metafield'ları doldur** → Değerler güvende ✅
3. **Taxonomy alanları Shopify bulk editor ile toplu doldur**:
   - Shopify Admin → Products → Bulk Editor
   - Custom alanlardan taxonomy alanlara kopyala
   - VEYA CSV export → düzenle → import

## 🚀 Gelecek Implementasyon

```python
# TODO: Eklenecek fonksiyon
def sync_custom_to_taxonomy_attributes(product_gid, metafields):
    """
    Custom metafield değerlerini taxonomy attribute'lere senkronize eder.
    
    custom.yaka_tipi = "V Yaka" → Neckline = "V-Neck"
    """
    mapping = load_taxonomy_mapping()
    
    for mf in metafields:
        if mf['key'] in mapping:
            taxonomy_name = mapping[mf['key']]['taxonomy_name']
            taxonomy_value = mapping[mf['key']]['values'].get(mf['value'])
            
            if taxonomy_value:
                set_taxonomy_attribute(product_gid, taxonomy_name, taxonomy_value)
```

Şimdilik sistem **%80 çalışıyor** - sadece taxonomy attribute'ler manuel doldurulmalı!
