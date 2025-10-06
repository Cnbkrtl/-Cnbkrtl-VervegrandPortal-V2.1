# 🔍 ÇOKLU KAYNAK META ALAN ÇIKARMA SİSTEMİ

## 📌 Genel Bakış

1000+ ürün için akıllı meta alan doldurma sistemi. Ürün bilgilerini 4 farklı kaynaktan öncelik sırasına göre çıkarır.

## 🌟 4 Katmanlı Veri Kaynağı

### Katman 1: Shopify AI Önerileri (En Yüksek Öncelik)
- **Kaynak**: `shopify_api.get_product_recommendations(product_gid)`
- **Format**: `recommended_attributes` listesi
- **Örnek**:
```json
{
  "recommended_attributes": [
    {
      "name": "Yaka Tipi",
      "values": [
        {"name": "V Yaka", "confidence": 0.95}
      ]
    }
  ]
}
```
- **Avantaj**: Shopify'ın yapay zekası en doğru önerileri sağlar
- **Kullanım**: Eğer Shopify öneri veriyorsa, bu değer diğer tüm kaynakları ezer

### Katman 2: Varyant Bilgileri
- **Kaynak**: `product['variants']` - Her varyantın `selectedOptions` listesi
- **Çıkarılan Bilgiler**:
  - **Renk**: Tüm varyantlardan renk seçenekleri (zaten mevcuttu)
  - **Beden**: Size/Beden seçeneklerinden beden listesi
  - **Kumaş**: Material/Kumaş seçeneklerinden kumaş tipi
- **Örnek**:
```python
variants = [
  {
    'sku': 'PROD-001-S-RED',
    'options': [
      {'name': 'Beden', 'value': 'S'},
      {'name': 'Renk', 'value': 'Kırmızı'},
      {'name': 'Kumaş', 'value': 'Pamuklu'}
    ]
  }
]
```
- **Avantaj**: Varyant seçenekleri genellikle doğru ve yapılandırılmıştır

### Katman 3: Ürün Başlığı (Regex Pattern Matching)
- **Kaynak**: `product['title']`
- **Yöntem**: Genişletilmiş regex pattern'leri ile eşleştirme
- **Çıkarılan Alanlar**:
  - Yaka Tipi (19 pattern)
  - Kol Tipi (9 pattern)
  - Boy (12 pattern)
  - Desen (18 pattern)
  - Paça Tipi (7 pattern)
  - Bel Tipi (6 pattern)
  - Kapanma Tipi (8 pattern)
  - Kapüşonlu (3 pattern)
  - Kullanım Alanı (9 pattern)
  - Cep (2 pattern)
  - Model (7 pattern)
  - Kumaş (14 pattern)
  - Stil (9 pattern)

**Örnek Pattern**:
```python
'yaka_tipi': [
    (r'boğazlı\s*yaka', 'Boğazlı Yaka'),
    (r'v\s*yaka', 'V Yaka'),
    (r'bisiklet\s*yaka', 'Bisiklet Yaka'),
    # ... 16 pattern daha
]
```

### Katman 4: Ürün Açıklaması (Son Çare)
- **Kaynak**: `product['description']`
- **Yöntem**: Başlıktaki pattern'ler açıklamada da aranır
- **Kullanım**: Sadece önceki 3 katmanda bulunamayan alanlar için
- **Avantaj**: Başlıkta eksik olan bilgiler açıklamada olabilir

## 📊 Öncelik Sistemi

```
Shopify AI Öneri > Varyant Bilgisi > Başlık > Açıklama
```

**Örnek Senaryo**:
1. Shopify "V Yaka" öneriyor → ✅ Kullan
2. Shopify öneri yok, varyantlarda "Yuvarlak Yaka" var → ✅ Kullan  
3. Varyantlarda yok, başlıkta "bisiklet yaka" var → ✅ Kullan
4. Hiçbirinde yok, açıklamada "hakim yaka" var → ✅ Kullan
5. Hiçbirinde yok → ❌ Meta alan boş

## 🔧 Kod Yapısı

### 1. `category_metafield_manager.py`

#### `extract_metafield_values()`
```python
def extract_metafield_values(
    product_title: str, 
    category: str,
    product_description: str = "",
    variants: List[Dict] = None,
    shopify_recommendations: Dict = None
) -> Dict[str, str]:
    """
    4 katmanlı meta alan çıkarma
    
    Returns:
        {'yaka_tipi': 'V Yaka', 'kol_tipi': 'Uzun Kol', ...}
    """
```

#### `prepare_metafields_for_shopify()`
```python
def prepare_metafields_for_shopify(
    category: str, 
    product_title: str,
    product_description: str = "",
    variants: List[Dict] = None,
    shopify_recommendations: Dict = None
) -> List[Dict]:
    """
    Shopify GraphQL formatında metafield listesi hazırlar
    
    Returns:
        [
            {
                'namespace': 'custom',
                'key': 'yaka_tipi',
                'value': 'V Yaka',
                'type': 'single_line_text_field'
            }
        ]
    """
```

### 2. `shopify_api.py`

#### `load_all_products_for_cache()` - Güncellenmiş
```graphql
query getProductsForCache($cursor: String) {
  products(first: 50, after: $cursor) {
    edges {
      node {
        id
        title
        description  # ✅ YENİ EKLENDI
        variants(first: 100) {
          edges {
            node {
              sku
              selectedOptions {  # ✅ YENİ EKLENDI
                name
                value
              }
            }
          }
        }
      }
    }
  }
}
```

**Önbellek Verisi**:
```python
product_data = {
    'id': 12345,
    'gid': 'gid://shopify/Product/12345',
    'title': 'Uzun Kollu V Yaka T-shirt',
    'description': 'Pamuklu kumaştan üretilmiş...', # ✅ YENİ
    'variants': [  # ✅ GÜÇLENDIRILDI
        {
            'sku': 'TSHIRT-001-S',
            'options': [
                {'name': 'Beden', 'value': 'S'},
                {'name': 'Renk', 'value': 'Beyaz'}
            ]
        }
    ]
}
```

### 3. `pages/15_Otomatik_Kategori_Meta_Alan.py`

#### Önizleme & Güncelleme Kodu
```python
# Shopify önerilerini al
shopify_recommendations = None
try:
    recommendations_data = shopify_api.get_product_recommendations(gid)
    if recommendations_data:
        shopify_recommendations = recommendations_data
except Exception as e:
    logging.warning(f"Shopify önerileri alınamadı: {e}")

# Meta alanları hazırla (TÜM KAYNAKLARLA)
metafields = CategoryMetafieldManager.prepare_metafields_for_shopify(
    category=category,
    product_title=title,
    product_description=description,  # ✅ YENİ
    variants=variants,
    shopify_recommendations=shopify_recommendations  # ✅ YENİ
)
```

## 🧪 Test Senaryoları

### Senaryo 1: Shopify Önerisi Var
```python
# INPUT
title = "Uzun Kollu Bluz"
shopify_recommendations = {
    'recommended_attributes': [
        {'name': 'kol_tipi', 'values': [{'name': 'Uzun Kol'}]}
    ]
}

# OUTPUT
{'kol_tipi': 'Uzun Kol'}  # ✨ Shopify'dan alındı
```

### Senaryo 2: Varyantlardan Çıkarma
```python
# INPUT
title = "Kadın Bluz"  # Yaka tipi yok
variants = [
    {
        'options': [
            {'name': 'Kumaş', 'value': 'Pamuklu'},
            {'name': 'Beden', 'value': 'M'}
        ]
    }
]

# OUTPUT
{'kumaş': 'Pamuklu', 'beden': 'M'}  # 🎨 Varyantlardan çıkarıldı
```

### Senaryo 3: Başlıktan Çıkarma
```python
# INPUT
title = "Büyük Beden Uzun Kollu Leopar Desenli Diz Üstü Elbise"

# OUTPUT
{
    'kol_tipi': 'Uzun Kol',     # 📝 Başlıktan
    'desen': 'Leopar',          # 📝 Başlıktan
    'boy': 'Diz Üstü'           # 📝 Başlıktan
}
```

### Senaryo 4: Açıklamadan Çıkarma
```python
# INPUT
title = "Kadın Elbise"  # Minimal bilgi
description = "V yakalı ve fermuarlı tasarım"

# OUTPUT
{
    'yaka_tipi': 'V Yaka',           # 📄 Açıklamadan
    'kapanma_tipi': 'Fermuarlı'      # 📄 Açıklamadan
}
```

### Senaryo 5: Karma (Tüm Katmanlar)
```python
# INPUT
title = "Uzun Kollu Leopar Desenli Elbise"
description = "Fermuarlı kapanma"
variants = [{'options': [{'name': 'Kumaş', 'value': 'Viskon'}]}]
shopify_recommendations = {
    'recommended_attributes': [
        {'name': 'yaka_tipi', 'values': [{'name': 'Bisiklet Yaka'}]}
    ]
}

# OUTPUT (Katman önceliği ile)
{
    'yaka_tipi': 'Bisiklet Yaka',    # ✨ Shopify (1. öncelik)
    'kumaş': 'Viskon',                # 🎨 Varyant (2. öncelik)
    'kol_tipi': 'Uzun Kol',           # 📝 Başlık (3. öncelik)
    'desen': 'Leopar',                # 📝 Başlık (3. öncelik)
    'kapanma_tipi': 'Fermuarlı'       # 📄 Açıklama (4. öncelik)
}
```

## 📈 Performans & Ölçeklenebilirlik

### 1000+ Ürün için Optimizasyonlar

1. **Önbellekleme**: Ürün verileri tek seferde yüklenir
2. **Batch İşleme**: 50 ürün/sorgu ile GraphQL pagination
3. **Rate Limiting**: Her sorgu arasında 0.5s bekleme
4. **Lazy Loading**: Shopify önerileri sadece gerektiğinde çağrılır

### Tahmini İşlem Süresi
- **1000 ürün**: ~15-20 dakika
- **Ürün yükleme**: ~5 dakika (50 ürün/sorgu × 0.5s)
- **Shopify önerileri**: Ürün başına +0.5s (isteğe bağlı)
- **Meta alan çıkarma**: Ürün başına ~0.1s (local işlem)
- **Shopify'a yazma**: Ürün başına ~1s

## 🔍 Loglama ve Debug

Tüm katmanlar detaylı log kaydeder:

```python
logging.info(f"✨ Shopify önerisinden alındı: {key} = '{value}'")
logging.info(f"🎨 Varyantlardan renk çıkarıldı: '{color_value}'")
logging.info(f"📏 Varyantlardan beden çıkarıldı: '{beden_value}'")
logging.info(f"🧵 Varyantlardan kumaş çıkarıldı: '{fabric_value}'")
logging.info(f"📝 Başlıktan çıkarıldı: {field} = '{value}'")
logging.info(f"📄 Açıklamadan çıkarıldı: {field} = '{value}'")
```

## 🚀 Kullanım

### Streamlit Arayüzünden

1. **Önizleme**: "👁️ Önizleme Yap" butonu
   - İlk 10 ürünü gösterir
   - Tüm katmanları test eder
   - Shopify önerilerini dener

2. **Güncelleme**: "🚀 Güncellemeyi Başlat" butonu
   - Test modu: İlk 20 ürün
   - Tam mod: Tüm ürünler
   - Dry Run: Sadece önizle, yazma

### Programatik Kullanım

```python
from utils.category_metafield_manager import CategoryMetafieldManager

# Kategori tespit et
category = CategoryMetafieldManager.detect_category("Uzun Kollu T-shirt")

# Meta alanları hazırla
metafields = CategoryMetafieldManager.prepare_metafields_for_shopify(
    category=category,
    product_title="Uzun Kollu V Yaka Leopar Desenli T-shirt",
    product_description="Pamuklu kumaştan üretilmiş",
    variants=[
        {
            'sku': 'TSHIRT-001-S',
            'options': [
                {'name': 'Beden', 'value': 'S'},
                {'name': 'Kumaş', 'value': 'Pamuklu'}
            ]
        }
    ],
    shopify_recommendations={
        'recommended_attributes': [
            {'name': 'yaka_tipi', 'values': [{'name': 'V Yaka'}]}
        ]
    }
)

# Shopify'a yaz
shopify_api.update_product_category_and_metafields(
    product_gid="gid://shopify/Product/12345",
    category=category,
    metafields=metafields
)
```

## ✅ Tamamlanan Değişiklikler

### `utils/category_metafield_manager.py`
- ✅ `extract_metafield_values()` - 5 parametre alıyor (eski 2)
- ✅ 4 katmanlı extraction logic implementasyonu
- ✅ Shopify AI recommendation parser
- ✅ Variant option extractor (renk, beden, kumaş)
- ✅ Enhanced title patterns (100+ pattern)
- ✅ Description fallback parser
- ✅ `prepare_metafields_for_shopify()` - Tüm parametreleri geçiyor

### `connectors/shopify_api.py`
- ✅ `load_all_products_for_cache()` - Description ve variant options eklendi
- ✅ GraphQL query genişletildi
- ✅ Product cache yapısı güncellendi

### `pages/15_Otomatik_Kategori_Meta_Alan.py`
- ✅ Önizleme kısmı - Shopify recommendations çağrısı eklendi
- ✅ Güncelleme kısmı - Tüm parametreler geçiliyor
- ✅ Description ve recommendations entegrasyonu

## 📝 Notlar

1. **Shopify Önerileri**: API limitleri nedeniyle her ürün için öneri çekmek yavaş olabilir. Gerekirse devre dışı bırakılabilir.

2. **HTML Açıklama**: `description` HTML içerebilir. Pattern matching sırasında HTML etiketleri sorun çıkarmaz (lower case comparison yapılıyor).

3. **Varyant Seçenekleri**: Varyant option isimleri Türkçe veya İngilizce olabilir. Her iki dilde kontrol yapılıyor:
   - `['material', 'kumaş', 'kumaş tipi', 'fabric']`
   - `['size', 'beden', 'boyut']`
   - `['color', 'renk']`

4. **Eksik Alanlar**: Bir meta alan hiçbir kaynakta bulunamazsa, Shopify'a gönderilmez (boş değer yerine hiç eklenmez).

## 🎯 Sonuç

Bu sistem ile 1000+ ürün için otomatik meta alan doldurma artık mümkün:
- ✅ Shopify'ın AI önerilerini kullanır
- ✅ Varyant bilgilerinden yararlanır
- ✅ Başlık ve açıklamadan akıllıca çıkarır
- ✅ Öncelik sistemi ile en doğru veriyi seçer
- ✅ Ölçeklenebilir ve performanslı
