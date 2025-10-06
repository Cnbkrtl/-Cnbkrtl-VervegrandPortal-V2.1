"""Test script for updated CategoryMetafieldManager"""
from utils.category_metafield_manager import CategoryMetafieldManager

print("=" * 80)
print("GÜNCELLENMIŞ KATEGORİ VE META ALAN SİSTEMİ")
print("=" * 80)

# Kategori özeti
summary = CategoryMetafieldManager.get_category_summary()
print(f"\n✅ Toplam {len(summary)} kategori destekleniyor:\n")

for cat, count in sorted(summary.items()):
    print(f"  • {cat:20} : {count} meta alan")

# Test örnekleri
print("\n" + "=" * 80)
print("TEST ÖRNEKLERİ")
print("=" * 80)

test_titles = [
    "Büyük Beden Uzun Kollu Leopar Desenli Diz Üstü Elbise 285058",
    "Büyük Beden Boğazlı Kazak Düz Renk",
    "Büyük Beden Kapüşonlu Sweatshirt",
    "Büyük Beden Jogger Lastikli Paça",
    "Büyük Beden Mont Fermuarlı Kapüşonlu",
    "Büyük Beden Hırka Düğmeli Uzun",
    "Büyük Beden Tayt Yüksek Bel Spor",
]

for title in test_titles:
    print(f"\n{'─' * 80}")
    print(f"Ürün: {title}")
    print(f"{'─' * 80}")
    
    category = CategoryMetafieldManager.detect_category(title)
    print(f"Kategori: {category}")
    
    if category:
        metafields = CategoryMetafieldManager.prepare_metafields_for_shopify(category, title)
        if metafields:
            print(f"Tespit edilen meta alanlar ({len(metafields)}):")
            for mf in metafields:
                print(f"  ✓ {mf['key']:20} = {mf['value']}")
        else:
            print("  (Meta alan tespit edilemedi)")

print("\n" + "=" * 80)
print("✅ Test tamamlandı!")
print("=" * 80)
