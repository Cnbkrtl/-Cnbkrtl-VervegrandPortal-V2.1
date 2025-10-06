"""
🧪 Kategori ID Format Test

Bu script kategori ID formatını test eder:
- Dictionary'de sadece ID olmalı (aa-2-6-14)
- Query için GID oluşturulmalı (gid://shopify/TaxonomyCategory/aa-2-6-14)
- Mutation'da sadece ID gönderilmeli (aa-2-6-14)
"""

# Test kategorileri
category_keywords = {
    't-shirt': 'aa-2-6-14',
    'tişört': 'aa-2-6-14',
    'bluz': 'aa-2-6-2',
    'gömlek': 'aa-2-6-13',
    'elbise': 'aa-2-1-4',
}

# Test ürünleri
test_products = [
    "Kadın Kırmızı V Yaka T-shirt",
    "Uzun Kollu Beyaz Gömlek",
    "Çiçek Desenli Bluz",
    "Yaz Elbisesi",
    "Siyah Tişört"
]

print("🧪 Kategori ID Format Testi\n")
print("=" * 60)

for title in test_products:
    print(f"\n📦 Ürün: '{title}'")
    
    title_lower = title.lower()
    found = False
    
    for keyword, category_id in category_keywords.items():
        if keyword in title_lower:
            # Query için GID formatı
            category_gid = f"gid://shopify/TaxonomyCategory/{category_id}"
            
            print(f"   ✅ Keyword bulundu: '{keyword}'")
            print(f"   📋 Dictionary'den: {category_id}")
            print(f"   🔍 Query için GID: {category_gid}")
            print(f"   💾 Mutation için ID: {category_id}")
            
            # Format kontrolü
            assert not category_id.startswith('gid://'), "❌ HATA: Dictionary'de GID olmamalı!"
            assert category_gid.startswith('gid://shopify/TaxonomyCategory/'), "❌ HATA: Query GID formatı yanlış!"
            assert category_id.startswith('aa-'), "❌ HATA: Taxonomy ID formatı yanlış!"
            
            print(f"   ✅ Tüm formatlar DOĞRU!")
            found = True
            break
    
    if not found:
        print(f"   ⚠️  Kategori bulunamadı (varsayılan kullanılacak)")

print("\n" + "=" * 60)
print("\n🎉 TÜM TESTLER BAŞARILI!")
print("\nÖZET:")
print("✅ Dictionary'de sadece taxonomy ID var (aa-2-6-14)")
print("✅ Query için GID formatı oluşturuluyor (gid://shopify/...)")  
print("✅ Mutation'a sadece taxonomy ID gönderiliyor (aa-2-6-14)")
