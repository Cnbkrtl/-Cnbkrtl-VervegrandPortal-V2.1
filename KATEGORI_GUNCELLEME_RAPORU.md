# Kategori ve Meta Alan Sistemi Güncellemesi

## Yapılan Değişiklikler

### ✅ RENK META ALANI EKLENDİ! (YENİ)

**Tüm 18 kategoriye** otomatik renk meta alanı eklendi! 
- Renk bilgisi varyantlardan otomatik olarak çıkarılır
- Birden fazla renk varsa virgülle ayrılmış liste halinde kaydedilir
- Örnek: "Kırmızı, Beyaz, Siyah"

### Yeni Eklenen Kategoriler (10 adet)

Sitenizden aldığımız koleksiyon verilerine göre aşağıdaki kategoriler eklendi:

1. **Gömlek** - 3 meta alan
2. **Mont** - 4 meta alan
3. **Hırka** - 3 meta alan
4. **Sweatshirt** - 3 meta alan
5. **Süveter** - 2 meta alan
6. **Jogger** - 3 meta alan
7. **Eşofman Altı** - 3 meta alan
8. **Tayt** - 3 meta alan

### Güncellenmiş Kategoriler

- **Kazak** - Boğazlı yaka ve balıkçı yaka desteği eklendi
- **Ceket** - Kapanma tipi meta alanı eklendi
- **Tunik** - Daha detaylı meta alanlar

## Toplam Kategori Kapsamı

✅ **18 farklı kategori** destekleniyor
✅ **71 meta alan** tanımlı (her kategoride RENK dahil!)
✅ Otomatik tespit ve doldurma
✅ Varyantlardan renk bilgisi çıkarma

## Desteklenen Kategoriler

| Kategori | Meta Alan Sayısı | Desteklenen Meta Alanlar |
|----------|------------------|--------------------------|
| Elbise | 6 | **Renk**, Yaka tipi, Kol tipi, Boy, Desen, Kullanım alanı |
| T-shirt | 4 | **Renk**, Yaka tipi, Kol tipi, Desen |
| Bluz | 4 | **Renk**, Yaka tipi, Kol tipi, Desen |
| Gömlek | 4 | **Renk**, Yaka tipi, Kol tipi, Desen |
| Pantolon | 4 | **Renk**, Paça tipi, Bel tipi, Boy |
| Jogger | 4 | **Renk**, Bel tipi, Paça tipi, Cep |
| Eşofman Altı | 4 | **Renk**, Bel tipi, Paça tipi, Kullanım alanı |
| Tayt | 4 | **Renk**, Bel tipi, Boy, Kullanım alanı |
| Şort | 3 | **Renk**, Boy, Bel tipi |
| Etek | 3 | **Renk**, Boy, Model |
| Ceket | 3 | **Renk**, Kol tipi, Kapanma tipi |
| Mont | 5 | **Renk**, Kol tipi, Kapanma tipi, Boy, Kapüşonlu |
| Hırka | 4 | **Renk**, Kol tipi, Kapanma tipi, Boy |
| Sweatshirt | 4 | **Renk**, Kol tipi, Kapüşonlu, Desen |
| Kazak | 4 | **Renk**, Yaka tipi, Kol tipi, Desen |
| Süveter | 3 | **Renk**, Yaka tipi, Kol tipi |
| Tunik | 4 | **Renk**, Yaka tipi, Kol tipi, Boy |
| Tulum | 4 | **Renk**, Kol tipi, Paça tipi, Boy |

## Geliştirilmiş Pattern Tanıma

Aşağıdaki özellikler artık otomatik olarak tespit ediliyor:

### Yaka Tipleri
- Boğazlı
- V Yaka
- Bisiklet Yaka
- Hakim Yaka
- Polo Yaka
- Balıkçı Yaka
- Halter
- Kayık Yaka
- Gömlek Yaka
- Klasik Yaka

### Kol Tipleri
- Uzun Kol
- Kısa Kol
- Kolsuz
- 3/4 Kol
- Yarım Kol

### Boy Özellikleri
- Maxi
- Midi
- Mini
- Diz Üstü
- Diz Altı
- Bilekli
- Uzun
- Orta
- Kısa

### Desen Tipleri
- Leopar
- Çiçekli
- Düz
- Çizgili
- Desenli
- Baskılı
- Logolu
- Puantiyeli
- Kareli
- Örgü

### Diğer Özellikler
- **Paça Tipleri**: Dar paça, Bol paça, İspanyol paça, Lastikli paça
- **Bel Tipleri**: Yüksek bel, Normal bel, Düşük bel, Lastikli, İpli
- **Kapanma Tipleri**: Fermuarlı, Düğmeli, Çıtçıtlı, Açık
- **Kapüşon**: Kapüşonlu, Kapüşonsuz
- **Kullanım Alanı**: Spor, Günlük, Gece, Kokteyl
- **Cep**: Cepli, Cepsiz
- **Model**: Kalem, Pileli, A Kesim, Balon

## Kullanım

Streamlit arayüzünden **"Otomatik Kategori ve Meta Alan"** sayfasına giderek:

1. Ürünleri seçin
2. "Analiz Et ve Önizle" butonuna tıklayın
3. Tespit edilen kategorileri ve meta alanları görün
4. "Shopify'a Uygula" ile değişiklikleri kaydedin

## Test Sonuçları

```
Örnek: "Büyük Beden Uzun Kollu Leopar Desenli Elbise" 
       Varyantlar: Kırmızı/M, Kırmızı/L
✓ Kategori: Elbise
✓ Meta Alanlar: 
  - Renk: Kırmızı (varyantlardan)
  - Kol tipi: Uzun Kol
  - Desen: Leopar

Örnek: "Büyük Beden V Yaka Kısa Kol T-shirt"
       Varyantlar: Siyah/S, Beyaz/S, Lacivert/S
✓ Kategori: T-shirt
✓ Meta Alanlar:
  - Renk: Beyaz, Lacivert, Siyah (varyantlardan)
  - Yaka tipi: V Yaka
  - Kol tipi: Kısa Kol

Örnek: "Büyük Beden Boğazlı Kazak Düz Renk"
✓ Kategori: Kazak
✓ Meta Alanlar: 
  - Renk: (varyantlardan otomatik)
  - Yaka tipi: Boğazlı
  - Desen: Düz

Örnek: "Büyük Beden Jogger Lastikli Paça"
✓ Kategori: Jogger
✓ Meta Alanlar: 
  - Renk: (varyantlardan otomatik)
  - Bel tipi: Lastikli
  - Paça tipi: Lastikli Paça
```

## Dosyalar

- `utils/category_metafield_manager.py` - Ana kategori ve meta alan yönetim sistemi (71 meta alan)
- `utils/variant_helpers.py` - Varyant renk çıkarma fonksiyonları (YENİ!)
- `pages/15_Otomatik_Kategori_Meta_Alan.py` - Streamlit arayüzü

---

**Güncelleme Tarihi**: 2025-10-06  
**Versiyon**: 2.4.0  
**Yeni Özellik**: Varyantlardan otomatik renk meta alanı!
