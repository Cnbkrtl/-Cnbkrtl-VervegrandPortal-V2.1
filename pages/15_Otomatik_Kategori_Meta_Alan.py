"""
🏷️ Otomatik Kategori ve Meta Alan Güncelleme

Ürün başlıklarından otomatik kategori tespiti yaparak 
Shopify kategori ve meta alanlarını otomatik doldurur.
"""

import streamlit as st
import sys
import os

# Proje ana dizinini path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from connectors.shopify_api import ShopifyAPI
import config_manager
from utils.category_metafield_manager import CategoryMetafieldManager
import logging
import time

st.set_page_config(
    page_title="Otomatik Kategori ve Meta Alan",
    page_icon="🏷️",
    layout="wide"
)

st.title("🏷️ Otomatik Kategori ve Meta Alan Güncelleme")
st.markdown("---")

# Kullanıcı giriş kontrolü
if "authentication_status" not in st.session_state or not st.session_state.get("authentication_status"):
    st.warning("⚠️ Lütfen önce giriş yapın.")
    st.stop()

username = st.session_state.get("username", "guest")

# API anahtarlarını yükle
user_keys = config_manager.load_all_user_keys(username)

if not user_keys.get("shopify_store") or not user_keys.get("shopify_token"):
    st.error("❌ Shopify API bilgileri eksik! Lütfen Settings sayfasından ekleyin.")
    st.stop()

# Bilgilendirme
st.info("""
### 🎯 Bu Modül Ne Yapar?

**Sorun:** Shopify'da her ürün için kategori ve meta alanlarını manuel doldurmak çok zaman alıyor.

**Çözüm:** Bu modül ürün başlıklarından otomatik olarak:
1. 📦 **Kategori tespit eder** (T-shirt, Elbise, Bluz, Pantolon, Şort vb.)
2. 🏷️ **Kategoriye uygun meta alanları belirler** (Yaka tipi, Kol tipi, Boy, Desen vb.)
3. ✨ **Ürün başlığından değerleri çıkarır** (V Yaka, Uzun Kol, Mini, Leopar vb.)
4. 💾 **Shopify'a otomatik yazar** (GraphQL API ile)

**Örnek:**
- Başlık: "Büyük Beden Uzun Kollu V Yaka Leopar Desenli Diz Üstü Elbise 285058"
- Kategori: **Elbise** ✅
- Meta Alanlar:
  - `custom.yaka_tipi` = "V Yaka" ✅
  - `custom.kol_tipi` = "Uzun Kol" ✅
  - `custom.boy` = "Diz Üstü" ✅
  - `custom.desen` = "Leopar" ✅
""")

st.markdown("---")

# Kategori istatistikleri göster
st.markdown("### 📊 Desteklenen Kategoriler ve Meta Alanları")

col1, col2 = st.columns([1, 2])

with col1:
    category_summary = CategoryMetafieldManager.get_category_summary()
    
    summary_data = []
    for category, count in category_summary.items():
        summary_data.append({
            'Kategori': category,
            'Meta Alan Sayısı': count
        })
    
    st.dataframe(summary_data, use_container_width=True, hide_index=True)

with col2:
    selected_category = st.selectbox(
        "Kategori Detayları",
        options=list(category_summary.keys())
    )
    
    if selected_category:
        metafields = CategoryMetafieldManager.get_metafields_for_category(selected_category)
        
        st.markdown(f"**{selected_category}** kategorisi için meta alanlar:")
        for field_key, field_info in metafields.items():
            st.markdown(f"- `{field_info['key']}`: {field_info['description']}")

st.markdown("---")

# Güncelleme Ayarları
st.markdown("### ⚙️ Güncelleme Ayarları")

col1, col2, col3 = st.columns(3)

with col1:
    test_mode = st.checkbox("🧪 Test Modu (İlk 20 ürün)", value=True)
    
with col2:
    dry_run = st.checkbox("🔍 DRY RUN (Sadece göster, güncelleme)", value=True)

with col3:
    update_category = st.checkbox("📦 Kategori güncelle", value=True)
    update_metafields = st.checkbox("🏷️ Meta alanları güncelle", value=True)

st.markdown("---")

# Önizleme Butonu
if st.button("👁️ Önizleme Yap", type="secondary"):
    with st.spinner("Ürünler yükleniyor ve analiz ediliyor..."):
        try:
            shopify_api = ShopifyAPI(
                user_keys["shopify_store"],
                user_keys["shopify_token"]
            )
            
            # Ürünleri yükle
            shopify_api.load_all_products_for_cache()
            
            # Unique ürünleri al
            unique_products = {}
            for product_data in shopify_api.product_cache.values():
                gid = product_data.get('gid')
                if gid and gid not in unique_products:
                    unique_products[gid] = product_data
            
            products = list(unique_products.values())[:20 if test_mode else len(unique_products)]
            
            st.success(f"✅ {len(products)} ürün yüklendi")
            
            # Önizleme tablosu
            preview_data = []
            
            for product in products[:10]:  # İlk 10 ürünü göster
                title = product.get('title', '')
                gid = product.get('gid', '')
                
                # Kategori tespit
                category = CategoryMetafieldManager.detect_category(title)
                
                if category:
                    # Meta alanları hazırla
                    metafields = CategoryMetafieldManager.prepare_metafields_for_shopify(category, title)
                    
                    metafield_summary = ', '.join([f"{mf['key']}: {mf['value']}" for mf in metafields])
                    
                    preview_data.append({
                        'Ürün': title[:50] + '...' if len(title) > 50 else title,
                        'Kategori': category,
                        'Meta Alanlar': metafield_summary if metafield_summary else 'Yok'
                    })
                else:
                    preview_data.append({
                        'Ürün': title[:50] + '...' if len(title) > 50 else title,
                        'Kategori': '❌ Tespit edilemedi',
                        'Meta Alanlar': '-'
                    })
            
            st.dataframe(preview_data, use_container_width=True, hide_index=True)
            
            # İstatistikler
            total_with_category = sum(1 for p in products if CategoryMetafieldManager.detect_category(p.get('title', '')))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Toplam Ürün", len(products))
            with col2:
                st.metric("Kategori Tespit Edildi", total_with_category)
            with col3:
                st.metric("Başarı Oranı", f"{(total_with_category/len(products)*100):.1f}%")
            
        except Exception as e:
            st.error(f"❌ Hata: {str(e)}")

# Güncelleme Butonu
st.markdown("---")

if st.button("🚀 Güncellemeyi Başlat", type="primary", disabled=(not update_category and not update_metafields)):
    if dry_run:
        st.warning("⚠️ DRY RUN modu aktif - Değişiklikler Shopify'a yazılmayacak")
    
    with st.spinner("Güncelleme yapılıyor..."):
        try:
            shopify_api = ShopifyAPI(
                user_keys["shopify_store"],
                user_keys["shopify_token"]
            )
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Ürünleri yükle
            status_text.text("📦 Ürünler yükleniyor...")
            shopify_api.load_all_products_for_cache()
            
            # Unique ürünleri al
            unique_products = {}
            for product_data in shopify_api.product_cache.values():
                gid = product_data.get('gid')
                if gid and gid not in unique_products:
                    unique_products[gid] = product_data
            
            products = list(unique_products.values())[:20 if test_mode else len(unique_products)]
            
            status_text.text(f"✅ {len(products)} ürün yüklendi")
            
            # Sonuçlar
            stats = {
                'total': len(products),
                'updated': 0,
                'skipped': 0,
                'failed': 0
            }
            
            results_container = st.container()
            
            with results_container:
                st.markdown("### 📊 Güncelleme Sonuçları:")
                results_placeholder = st.empty()
                
                results_html = ""
                
                for idx, product in enumerate(products):
                    gid = product.get('gid')
                    title = product.get('title', 'Bilinmeyen')
                    
                    progress = (idx + 1) / len(products)
                    progress_bar.progress(progress)
                    status_text.text(f"[{idx + 1}/{len(products)}] {title[:50]}...")
                    
                    # Kategori tespit
                    category = CategoryMetafieldManager.detect_category(title)
                    
                    if not category:
                        stats['skipped'] += 1
                        results_html += f"""
                        <div style='padding: 8px; margin: 3px 0; border-left: 3px solid #ffc107; background: #fff8e1;'>
                            <small>⏭️ Kategori tespit edilemedi: <b>{title[:60]}</b></small>
                        </div>
                        """
                        results_placeholder.markdown(results_html, unsafe_allow_html=True)
                        continue
                    
                    # Meta alanları hazırla
                    metafields = CategoryMetafieldManager.prepare_metafields_for_shopify(category, title)
                    
                    if dry_run:
                        # DRY RUN: Sadece göster
                        stats['updated'] += 1
                        metafield_list = ', '.join([f"{mf['key']}: {mf['value']}" for mf in metafields])
                        
                        results_html += f"""
                        <div style='padding: 8px; margin: 3px 0; border-left: 3px solid #2196f3; background: #e3f2fd;'>
                            <small>🔍 <b>{title[:60]}</b></small><br>
                            <small>&nbsp;&nbsp;&nbsp;&nbsp;Kategori: <b>{category}</b> | Meta: {metafield_list}</small>
                        </div>
                        """
                    else:
                        # GERÇEK GÜNCELLEME
                        try:
                            result = shopify_api.update_product_category_and_metafields(
                                gid,
                                category if update_category else None,
                                metafields if update_metafields else []
                            )
                            
                            if result.get('success'):
                                stats['updated'] += 1
                                results_html += f"""
                                <div style='padding: 8px; margin: 3px 0; border-left: 3px solid #4caf50; background: #e8f5e9;'>
                                    <small>✅ <b>{title[:60]}</b></small><br>
                                    <small>&nbsp;&nbsp;&nbsp;&nbsp;Kategori: <b>{category}</b> | Meta: {len(metafields)} alan güncellendi</small>
                                </div>
                                """
                            else:
                                stats['failed'] += 1
                                results_html += f"""
                                <div style='padding: 8px; margin: 3px 0; border-left: 3px solid #f44336; background: #ffebee;'>
                                    <small>❌ <b>{title[:60]}</b></small><br>
                                    <small>&nbsp;&nbsp;&nbsp;&nbsp;Hata: {result.get('message', 'Bilinmeyen')}</small>
                                </div>
                                """
                            
                            time.sleep(0.5)  # Rate limit
                            
                        except Exception as e:
                            stats['failed'] += 1
                            results_html += f"""
                            <div style='padding: 8px; margin: 3px 0; border-left: 3px solid #f44336; background: #ffebee;'>
                                <small>❌ <b>{title[:60]}</b></small><br>
                                <small>&nbsp;&nbsp;&nbsp;&nbsp;Hata: {str(e)}</small>
                            </div>
                            """
                    
                    results_placeholder.markdown(results_html, unsafe_allow_html=True)
            
            # Özet
            st.markdown("---")
            st.markdown("### 📊 Özet:")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Toplam", stats['total'])
            with col2:
                st.metric("Güncellendi", stats['updated'])
            with col3:
                st.metric("Atlandı", stats['skipped'])
            with col4:
                st.metric("Hata", stats['failed'])
            
            if dry_run:
                st.warning("💡 DRY RUN moduydu - Gerçek güncelleme için DRY RUN'ı kapatıp tekrar çalıştırın.")
            elif stats['updated'] > 0:
                st.success(f"✅ {stats['updated']} ürün başarıyla güncellendi!")
            
            progress_bar.progress(1.0)
            status_text.text("✅ Tamamlandı!")
            
        except Exception as e:
            st.error(f"❌ Hata: {str(e)}")
            import traceback
            with st.expander("Detaylı Hata"):
                st.code(traceback.format_exc())

# Yardım bölümü
with st.expander("❓ Yardım ve İpuçları"):
    st.markdown("""
    ### Kategori Tespit Kuralları
    
    Sistem ürün başlığında şu anahtar kelimeleri arar:
    
    - **Elbise:** elbise, dress
    - **T-shirt:** t-shirt, tshirt, tişört
    - **Bluz:** bluz, blouse, gömlek
    - **Pantolon:** pantolon, pants, jean, kot
    - **Şort:** şort, short
    - **Etek:** etek, skirt
    - **Ceket:** ceket, jacket, mont, kaban
    - Ve daha fazlası...
    
    ### Meta Alan Çıkarma
    
    Başlıktan otomatik çıkarılan değerler:
    
    - **Yaka:** V yaka, Bisiklet yaka, Hakim yaka vb.
    - **Kol:** Uzun kol, Kısa kol, Kolsuz vb.
    - **Boy:** Mini, Midi, Maxi, Diz üstü vb.
    - **Desen:** Leopar, Çiçekli, Düz, Çizgili vb.
    - **Paça:** Dar paça, Bol paça vb.
    - **Bel:** Yüksek bel, Normal bel vb.
    
    ### İpuçları
    
    1. ✅ İlk önce **Test Modu** ve **DRY RUN** ile deneyin
    2. ✅ Önizleme yaparak sonuçları kontrol edin
    3. ✅ Ürün başlıklarının açıklayıcı olması önemli
    4. ✅ Kategori tespit edilemezse başlığı düzenleyin
    """)
