# 🏷️ Otomatik Kategori ve Meta Alan - Hızlı Başlangıç

## 🚀 5 Dakikada Başlayın!

### 1️⃣ Streamlit Uygulamasını Başlatın

```bash
streamlit run streamlit_app.py
```

### 2️⃣ Sayfayı Açın

Sol menüden: **"15_Otomatik_Kategori_Meta_Alan"**

### 3️⃣ Önizleme Yapın

1. ✅ **Test Modu** aktif bırakın (ilk 20 ürün)
2. 🔍 **"👁️ Önizleme Yap"** butonuna tıklayın
3. Sonuçları inceleyin

### 4️⃣ DRY RUN ile Test Edin

1. ✅ **DRY RUN** aktif bırakın
2. 🚀 **"Güncellemeyi Başlat"** butonuna tıklayın
3. Hangi kategori ve meta alanların güncelleneceğini görün

### 5️⃣ Gerçek Güncelleme Yapın

1. ❌ **DRY RUN**'ı kapatın
2. ✅ **Kategori güncelle** aktif
3. ✅ **Meta alanları güncelle** aktif
4. 🚀 **"Güncellemeyi Başlat"** butonuna tıklayın

---

## 📖 Ne Yapar?

### Giriş (Manuel İşlem)
```
Ürün: "Büyük Beden Uzun Kollu V Yaka Leopar Desenli Diz Üstü Elbise 285058"

Shopify Admin'de:
1. Kategori seç: [    ] ← Manuel
2. Yaka tipi: [    ] ← Manuel
3. Kol tipi: [    ] ← Manuel
4. Boy: [    ] ← Manuel
5. Desen: [    ] ← Manuel

❌ 5+ alan, her ürün için 2-3 dakika!
```

### Çıkış (Otomatik İşlem)
```
Ürün: "Büyük Beden Uzun Kollu V Yaka Leopar Desenli Diz Üstü Elbise 285058"

Otomatik tespit:
✅ Kategori: Elbise
✅ Yaka tipi: V Yaka
✅ Kol tipi: Uzun Kol
✅ Boy: Diz Üstü
✅ Desen: Leopar

⚡ Tüm alanlar otomatik dolduruldu!
```

---

## 📊 Desteklenen Kategoriler

| Kategori | Örnek Başlık | Meta Alan |
|----------|--------------|-----------|
| **Elbise** | "Uzun Kollu V Yaka Elbise" | Yaka, Kol, Boy, Desen |
| **T-shirt** | "Bisiklet Yaka Kısa Kol T-shirt" | Yaka, Kol, Desen |
| **Bluz** | "Hakim Yaka Uzun Kol Bluz" | Yaka, Kol, Desen |
| **Pantolon** | "Yüksek Bel Dar Paça Pantolon" | Bel, Paça, Boy |
| **Şort** | "Yüksek Bel Mini Şort" | Bel, Boy |
| **Etek** | "Midi Kalem Etek" | Boy, Model |
| **Ceket** | "Fermuarlı Uzun Kol Ceket" | Kol, Kapanma |

Ve daha fazlası...

---

## ⚙️ Önemli Ayarlar

### Test Modu
- ✅ **Aktif:** İlk 20 ürün işlenir (güvenli test)
- ❌ **Kapalı:** Tüm ürünler işlenir

### DRY RUN
- ✅ **Aktif:** Sadece gösterir, Shopify'a yazmaz
- ❌ **Kapalı:** Shopify'a gerçekten yazar

### Güncelleme Seçenekleri
- 📦 **Kategori güncelle:** Product Type alanını doldurur
- 🏷️ **Meta alanları güncelle:** Custom metafields doldurur

---

## 🎯 Örnek Akış

### Adım 1: Önizleme
```
[Önizleme Yap] butonuna tıkla

Sonuç:
✅ Toplam Ürün: 20
✅ Kategori Tespit Edildi: 18
✅ Başarı Oranı: 90%

Ürün Örnekleri:
- "Uzun Kollu Elbise 123" → Kategori: Elbise, Kol: Uzun Kol
- "V Yaka T-shirt 456" → Kategori: T-shirt, Yaka: V Yaka
- "Dar Paça Pantolon 789" → Kategori: Pantolon, Paça: Dar Paça
```

### Adım 2: DRY RUN Test
```
[Güncellemeyi Başlat] butonuna tıkla (DRY RUN aktif)

Sonuç:
🔍 Elbise: Uzun Kollu V Yaka Elbise
   Kategori: Elbise | Meta: yaka_tipi: V Yaka, kol_tipi: Uzun Kol

🔍 T-shirt: Bisiklet Yaka Kısa Kol T-shirt
   Kategori: T-shirt | Meta: yaka_tipi: Bisiklet Yaka, kol_tipi: Kısa Kol

⚠️ DRY RUN - Shopify'a yazılmadı
```

### Adım 3: Gerçek Güncelleme
```
DRY RUN'ı kapat → [Güncellemeyi Başlat]

Sonuç:
✅ Elbise: Uzun Kollu V Yaka Elbise
   Kategori: Elbise | Meta: 2 alan güncellendi

✅ T-shirt: Bisiklet Yaka Kısa Kol T-shirt
   Kategori: T-shirt | Meta: 2 alan güncellendi

✅ 18 ürün başarıyla güncellendi!
```

---

## ❓ Sık Sorulan Sorular

### Kategori tespit edilemedi ne yapmalıyım?

Ürün başlığına kategori anahtar kelimesi ekleyin:
- ✅ "**Elbise** 123" 
- ✅ "Uzun Kollu **T-shirt** 456"
- ✅ "V Yaka **Bluz** 789"

### Meta alanlar boş kalıyor?

Başlığa detay ekleyin:
- ✅ "**Uzun Kollu** **V Yaka** Elbise"
- ✅ "**Yüksek Bel** **Dar Paça** Pantolon"

### Tüm ürünleri güncellemek güvenli mi?

1. İlk önce **Test Modu** (20 ürün) ile deneyin
2. Sonucu kontrol edin
3. Başarı oranı >%80 ise tüm ürünleri güncelleyin

---

## 📈 Performans

- **20 ürün:** ~10 saniye
- **100 ürün:** ~60 saniye
- **1000 ürün:** ~10 dakika

---

## ✅ Başarı İpuçları

1. ✅ **Açıklayıcı başlıklar kullanın**
   - ❌ "Elbise 123"
   - ✅ "Uzun Kollu V Yaka Leopar Desenli Elbise 123"

2. ✅ **Test modu ile başlayın**
   - İlk 20 ürünü test edin
   - Sonuçları kontrol edin
   - Sonra tümünü güncelleyin

3. ✅ **DRY RUN kullanın**
   - Önce test edin
   - Sonuçları inceleyin
   - Sonra gerçek güncelleme yapın

4. ✅ **Loglara bakın**
   - Hangi kategori tespit edildi?
   - Hangi meta alanlar çıkarıldı?
   - Hata varsa nedenini görün

---

## 🎓 Daha Fazla Bilgi

Detaylı kullanım için: **OTOMATIK_KATEGORI_META_ALAN_KILAVUZU.md**

---

**Artık hazırsınız! Başlayın ve zamanınızı kurtarın! 🚀**
