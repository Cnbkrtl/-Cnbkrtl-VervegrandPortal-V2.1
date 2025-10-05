# 🚀 CI/CD Pipeline - Hızlı Başlangıç

## 📖 CI/CD Nedir? (1 Dakikada Anla)

**Eski Yöntem:**
```
Kod Yaz → Manuel Test → Sunucuya Yükle → Elle Kontrol → Sorun Varsa Düzelt
⏱️ Süre: 30-60 dakika
🐛 Risk: Yüksek (insan hatası)
```

**CI/CD ile:**
```
Kod Yaz → Git Push → Otomatik Test → Otomatik Deploy
⏱️ Süre: 5-10 dakika
🛡️ Risk: Düşük (hatalı kod deploy olmaz)
```

---

## ⚡ 5 Dakikada Kurulum

### 1. GitHub Secrets Ekle
```
GitHub Repo → Settings → Secrets and variables → Actions → New secret
```

**Gerekli Secrets:**
- `SHOPIFY_STORE`: vervegrand.myshopify.com
- `SHOPIFY_ACCESS_TOKEN`: shpat_xxxxx

### 2. Workflow Dosyasını Push Et
```powershell
git add .github/workflows/ci-cd.yml
git commit -m "feat: CI/CD pipeline eklendi"
git push origin main
```

### 3. Pipeline'ı İzle
```
GitHub Repo → Actions sekmesi → İlk workflow'u göreceksiniz
```

**Tamamlandı!** 🎉

---

## 🎯 Pipeline Ne Yapar?

| Job | Süre | Açıklama |
|-----|------|----------|
| 🔍 Kod Kalitesi | ~1 dk | Format, syntax, complexity |
| 🔒 Güvenlik | ~2 dk | Dependency scan, secret leak |
| 🧪 Unit Tests | ~2 dk | Fonksiyon testleri |
| 🔗 Integration | ~1 dk | API bağlantı testleri |
| 🚀 Deploy | ~2 dk | Production deployment |
| **TOPLAM** | **~8 dk** | Otomatik! |

---

## 📊 Pipeline Senaryoları

### ✅ Başarılı Deploy
```
Git Push → Testler Geçti → Deploy Başarılı → Email Bildirimi
```

### ❌ Test Hatası
```
Git Push → Test Başarısız → Deploy İPTAL → Hata Raporu
```

### ⚠️ Güvenlik Uyarısı
```
Git Push → Güvenlik Uyarısı → Manuel Onay → Deploy
```

---

## 🔧 Kullanım Örnekleri

### Özellik Geliştirme (Feature Branch)
```powershell
# 1. Yeni branch oluştur
git checkout -b feature/yeni-ozellik

# 2. Kod yaz ve test et
# ...

# 3. Push et (sadece testler çalışır)
git push origin feature/yeni-ozellik

# 4. Pull Request aç
# GitHub → Pull Requests → New PR

# 5. Testler geçerse merge et
# main branch'e deploy olur
```

### Hotfix (Acil Düzeltme)
```powershell
# 1. Hotfix branch
git checkout -b hotfix/kritik-hata

# 2. Düzelt ve commit
git commit -m "fix: kritik hata düzeltildi"

# 3. main'e merge
git checkout main
git merge hotfix/kritik-hata
git push origin main

# 4. Otomatik deploy (5-8 dk)
```

---

## 📚 Detaylı Dokümantasyon

- 📖 **[CI_CD_KILAVUZU.md](./CI_CD_KILAVUZU.md)** → Tam kılavuz
- 🧪 **[tests/](./tests/)** → Test örnekleri
- ⚙️ **[.github/workflows/ci-cd.yml](./.github/workflows/ci-cd.yml)** → Pipeline config

---

## 💡 Sık Kullanılan Komutlar

```powershell
# Workflow'u manuel başlat
gh workflow run ci-cd.yml

# Son çalışma durumunu gör
gh run list --workflow=ci-cd.yml

# Çalışan pipeline'ı izle
gh run watch

# Test sonuçlarını göster
pytest tests/ -v

# Coverage raporu
pytest tests/ --cov=. --cov-report=html
open htmlcov/index.html
```

---

## 🆘 Sorun Giderme

### Pipeline Başlamıyor
```
Kontrol: .github/workflows/ci-cd.yml dosyası main branch'de mi?
Çözüm: git push origin main
```

### Test Hataları
```
Kontrol: pytest tests/ -v (local'de çalışıyor mu?)
Çözüm: Testleri local'de düzelt, sonra push et
```

### Deploy Başarısız
```
Kontrol: GitHub Secrets doğru mu?
Çözüm: Settings → Secrets → Değerleri kontrol et
```

---

## 📊 Status Badge

README'nize ekleyin:

```markdown
[![CI/CD](https://github.com/Cnbkrtl/VervegrandPortal-V2/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Cnbkrtl/VervegrandPortal-V2/actions)
```

---

## 🎓 Sonraki Adımlar

1. ✅ **Şimdi:** Pipeline'ı kur (yukarıdaki 5 dakikalık adımlar)
2. 📝 **Bu Hafta:** İlk testleri yaz (tests/test_shopify_api.py örneğinden başla)
3. 🚀 **Bu Ay:** Coverage'ı %80'e çıkar
4. 🔔 **Gelecek:** Slack/Discord bildirim ekle

---

**Hazırladı:** GitHub Copilot  
**Tarih:** 4 Ekim 2025  
**İletişim:** [GitHub Issues](https://github.com/Cnbkrtl/VervegrandPortal-V2/issues)
