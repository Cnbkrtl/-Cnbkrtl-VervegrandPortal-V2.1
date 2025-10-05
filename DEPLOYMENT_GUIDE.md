# 🚀 VervegrandPortal V2 - Deployment Rehberi

## 📋 İçindekiler

1. [Ön Hazırlık](#on-hazirlik)
2. [Lokal Kurulum](#lokal-kurulum)
3. [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
4. [Secrets Yapılandırması](#secrets-yapilandirmasi)
5. [Testing & Validation](#testing-validation)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Ön Hazırlık

### Gerekli Bilgiler

#### 1. Shopify API Credentials
```yaml
SHOPIFY_STORE: "your-store.myshopify.com"
SHOPIFY_TOKEN: "shpat_xxxxxxxxxxxxx"
SHOPIFY_DESTINATION_STORE: "destination-store.myshopify.com"  # Opsiyonel
SHOPIFY_DESTINATION_TOKEN: "shpat_yyyyyyyyyyyyyy"  # Opsiyonel
```

**Nasıl Alınır:**
1. Shopify Admin → Apps → Develop apps
2. "Create an app" butonuna tıkla
3. App adı: "Vervegrand Sync"
4. Admin API access scopes seç:
   - `read_products`
   - `write_products`
   - `read_inventory`
   - `write_inventory`
   - `read_orders`
   - `write_orders`
5. Install app → Access token'ı kopyala

#### 2. Sentos API Credentials
```yaml
SENTOS_API_URL: "https://your-sentos-instance.com/api"
SENTOS_API_KEY: "your-api-key"
SENTOS_API_SECRET: "your-api-secret"
SENTOS_COOKIE: "PHPSESSID=xxxxxxxxxx; other_cookie=yyyyyy"
```

**Cookie Nasıl Alınır:**
1. Chrome/Firefox Developer Tools aç (F12)
2. Network tab'ına git
3. Sentos paneline giriş yap
4. Herhangi bir request seç
5. Headers → Cookie değerini kopyala

#### 3. Google Sheets API (Opsiyonel)
```json
{
  "type": "service_account",
  "project_id": "your-project",
  "private_key_id": "xxxxx",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "your-sa@project.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
```

**Nasıl Oluşturulur:**
1. [Google Cloud Console](https://console.cloud.google.com)
2. "Create Project" → Proje adı gir
3. APIs & Services → Enable APIs
   - Google Sheets API
   - Google Drive API
4. Credentials → Create Credentials → Service Account
5. JSON key indir

---

## 💻 Lokal Kurulum

### 1. Depoyu Klonla
```bash
git clone https://github.com/Cnbkrtl/VervegrandPortal-V2.git
cd VervegrandPortal-V2
```

### 2. Virtual Environment Oluştur
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Dependencies Kur
```bash
pip install -r requirements.txt
```

### 4. Secrets Dosyası Oluştur

**Windows:**
```bash
mkdir .streamlit
notepad .streamlit\secrets.toml
```

**macOS/Linux:**
```bash
mkdir -p .streamlit
nano .streamlit/secrets.toml
```

**İçerik:**
```toml
# Shopify Credentials
SHOPIFY_STORE = "your-store.myshopify.com"
SHOPIFY_TOKEN = "shpat_xxxxx"

# Sentos Credentials
SENTOS_API_URL = "https://your-sentos.com/api"
SENTOS_API_KEY = "your-key"
SENTOS_API_SECRET = "your-secret"
SENTOS_COOKIE = "PHPSESSID=xxxxx"

# Encryption Key (Generate new one!)
FERNET_KEY = "your-fernet-key-here"

# Google Sheets (Optional)
GCP_SERVICE_ACCOUNT_JSON = '''
{
  "type": "service_account",
  ...
}
'''
```

### 5. Fernet Key Oluştur
```bash
python generate_keys.py
```

Çıktıdaki `FERNET_KEY` değerini kopyala ve `secrets.toml`'a yapıştır.

### 6. Uygulamayı Çalıştır
```bash
streamlit run streamlit_app.py
```

Tarayıcı otomatik açılacak: `http://localhost:8501`

---

## ☁️ Streamlit Cloud Deployment

### 1. GitHub Repository Hazırla

#### .gitignore Oluştur
```gitignore
# Secrets
.streamlit/secrets.toml
*.env
config_local.yaml

# Cache
__pycache__/
*.pyc
*.pyo
.pytest_cache/
data_cache/

# Logs
logs/*.log
*.db

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
```

#### Repository Push
```bash
git add .
git commit -m "Initial deployment"
git push origin main
```

### 2. Streamlit Cloud Setup

1. [share.streamlit.io](https://share.streamlit.io) hesap aç
2. "New app" → GitHub repository seç
3. Settings:
   - **Main file path:** `streamlit_app.py`
   - **Python version:** 3.11
   - **Branch:** main

### 3. Secrets Yapılandır

Streamlit Cloud → Your app → Settings → Secrets

**Tüm secrets.toml içeriğini kopyala-yapıştır:**
```toml
SHOPIFY_STORE = "..."
SHOPIFY_TOKEN = "..."
SENTOS_API_URL = "..."
# ... (tüm credentials)
```

**⚠️ ÖNEMLİ:** 
- Tırnak işaretlerini koru (`"..."`)
- Multi-line JSON için `'''` kullan
- Boşlukları koru

### 4. Deploy

"Deploy!" butonuna tıkla → 2-3 dakika bekle → ✅ Canlı!

---

## 🔐 Secrets Yapılandırması

### Zorunlu Secrets (Minimum)

```toml
# Shopify - Mutlaka gerekli
SHOPIFY_STORE = "store-name.myshopify.com"
SHOPIFY_TOKEN = "shpat_xxxxxxxxx"

# Sentos - Mutlaka gerekli
SENTOS_API_URL = "https://api.sentos.com.tr"
SENTOS_API_KEY = "your-key"
SENTOS_API_SECRET = "your-secret"

# Encryption - Mutlaka gerekli
FERNET_KEY = "generated-fernet-key"
```

### Opsiyonel Secrets

```toml
# Shopify Transfer (Mağaza transferi için)
SHOPIFY_DESTINATION_STORE = "destination.myshopify.com"
SHOPIFY_DESTINATION_TOKEN = "shpat_yyyyyy"

# Sentos Cookie (Resim senkronizasyonu için)
SENTOS_COOKIE = "PHPSESSID=xxxxx; path=/; domain=.sentos.com.tr"

# Google Sheets (Fiyat yönetimi için)
GCP_SERVICE_ACCOUNT_JSON = '''
{
  "type": "service_account",
  "project_id": "vervegrand-sync",
  ...
}
'''
```

---

## ✅ Testing & Validation

### 1. Lokal Test

```bash
# Test modunda çalıştır (ilk 20 ürün)
streamlit run streamlit_app.py
```

**Test Checklist:**
- [ ] Login sayfası açılıyor mu?
- [ ] Credentials doğru mu? (Settings sayfası)
- [ ] API connections başarılı mı?
- [ ] Dashboard verileri yükleniyor mu?
- [ ] Test sync çalışıyor mu? (10-20 ürün)

### 2. Production Test

**1. Staged Rollout:**
```
1. Sadece 10 ürün sync
2. Sonuçları kontrol et
3. 100 ürün sync
4. 24 saat izle
5. Full sync
```

**2. Monitor:**
- Logs sayfasından hataları izle
- Dashboard'da metrikleri kontrol et
- Shopify Admin'de ürünleri doğrula

---

## 🐛 Troubleshooting

### Hata: "Module not found"

**Çözüm:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Hata: "Shopify API Error 401"

**Sebep:** Access token geçersiz veya expired

**Çözüm:**
1. Shopify Admin → Apps → Vervegrand Sync
2. Yeni token oluştur
3. `secrets.toml` güncelle
4. Uygulamayı restart et

### Hata: "Rate limit exceeded"

**Sebep:** Çok fazla istek

**Çözüm:**
1. `max_workers` değerini azalt (Settings → Sync)
2. Batch size'ı düşür (kod içinde)
3. Test mode aktif et
4. 1-2 saat bekle

### Hata: "Sentos Cookie expired"

**Sebep:** Cookie süresi dolmuş

**Çözüm:**
1. Sentos'a tekrar giriş yap
2. Yeni cookie al (F12 → Network)
3. `secrets.toml` güncelle
4. App restart

### Hata: "Fernet key invalid"

**Sebep:** Encryption key hatalı

**Çözüm:**
```bash
# Yeni key oluştur
python generate_keys.py

# secrets.toml güncelle
FERNET_KEY = "yeni-key-buraya"

# Cache temizle
rm -rf data_cache/*
```

### Hata: "Streamlit Cloud build failed"

**Sebep:** requirements.txt veya Python version uyumsuz

**Çözüm:**
1. Python version: 3.11 seç
2. requirements.txt kontrol et:
   ```txt
   streamlit>=1.28.0
   requests>=2.31.0
   pandas>=2.0.0
   ```
3. Rebuild

---

## 📊 Performance Tuning

### Optimize Settings

```python
# Düşük Trafik (Gece Sync'i)
max_workers = 5
batch_size = 50

# Normal Trafik
max_workers = 2
batch_size = 25

# Yüksek Trafik (Peak Hours)
max_workers = 1
batch_size = 10
```

### Monitoring Commands

```bash
# Log dosyası izle
tail -f logs/sync_logs.db

# Cache boyutu kontrol
du -sh data_cache/

# Memory usage
ps aux | grep streamlit
```

---

## 🚀 Production Checklist

**Pre-Deployment:**
- [ ] Tüm secrets doğru yapılandırıldı
- [ ] Test sync başarılı (20 ürün)
- [ ] Error handling test edildi
- [ ] Backup alındı (mevcut veriler)

**Deployment:**
- [ ] GitHub push yapıldı
- [ ] Streamlit Cloud build başarılı
- [ ] Secrets sync edildi
- [ ] Health check geçildi

**Post-Deployment:**
- [ ] İlk sync tamamlandı
- [ ] Loglar kontrol edildi
- [ ] Dashboard metrikleri doğru
- [ ] 24 saat monitoring

---

## 📞 Destek

**Geliştirici:** Can Bakırtel  
**Email:** cnbkrtl11@gmail.com  
**GitHub:** [@Cnbkrtl](https://github.com/Cnbkrtl)

**Dokümantasyon:**
- [README.md](README.md)
- [IYILESTIRME_RAPORU.md](IYILESTIRME_RAPORU.md)
- [Shopify API Docs](https://shopify.dev/docs/api/admin-graphql)

---

**🎉 Başarılar! Production'a hazırsınız!**
