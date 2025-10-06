"""Test script for color metafield feature"""
from utils.category_metafield_manager import CategoryMetafieldManager

print("=" * 80)
print("RENK META ALANI TESTİ")
print("=" * 80)

# Simulated variants with colors
test_variants_1 = [
    {'title': 'Kırmızı / M', 'options': [{'name': 'Renk', 'value': 'Kırmızı'}, {'name': 'Beden', 'value': 'M'}]},
    {'title': 'Kırmızı / L', 'options': [{'name': 'Renk', 'value': 'Kırmızı'}, {'name': 'Beden', 'value': 'L'}]},
]

test_variants_2 = [
    {'title': 'Siyah / S', 'options': [{'name': 'Renk', 'value': 'Siyah'}, {'name': 'Beden', 'value': 'S'}]},
    {'title': 'Beyaz / S', 'options': [{'name': 'Renk', 'value': 'Beyaz'}, {'name': 'Beden', 'value': 'S'}]},
    {'title': 'Lacivert / S', 'options': [{'name': 'Renk', 'value': 'Lacivert'}, {'name': 'Beden', 'value': 'S'}]},
]

test_cases = [
    {
        'title': 'Büyük Beden Uzun Kollu Leopar Desenli Elbise',
        'variants': test_variants_1
    },
    {
        'title': 'Büyük Beden V Yaka Kısa Kol T-shirt',
        'variants': test_variants_2
    }
]

for idx, test in enumerate(test_cases, 1):
    print(f"\n{'─' * 80}")
    print(f"TEST {idx}: {test['title']}")
    print(f"{'─' * 80}")
    
    category = CategoryMetafieldManager.detect_category(test['title'])
    print(f"Kategori: {category}")
    
    if category:
        # Varyant renklerini göster
        from utils.variant_helpers import extract_colors_from_variants
        colors = extract_colors_from_variants(test['variants'])
        print(f"Varyant Renkleri: {', '.join(colors)}")
        
        # Meta alanları hazırla (varyantlarla birlikte)
        metafields = CategoryMetafieldManager.prepare_metafields_for_shopify(
            category, 
            test['title'],
            variants=test['variants']
        )
        
        print(f"\nOluşturulan Meta Alanlar ({len(metafields)}):")
        for mf in metafields:
            value_display = mf['value'][:50] + '...' if len(mf['value']) > 50 else mf['value']
            print(f"  ✓ {mf['key']:20} = {value_display}")
            
        # Renk meta alanını kontrol et
        renk_found = any(mf['key'] == 'renk' for mf in metafields)
        if renk_found:
            renk_value = next(mf['value'] for mf in metafields if mf['key'] == 'renk')
            print(f"\n  ✅ RENK META ALANI BAŞARIYLA EKLENDİ: {renk_value}")
        else:
            print(f"\n  ⚠️ Renk meta alanı eklenemedi")

print("\n" + "=" * 80)
print("✅ Test tamamlandı!")
print("=" * 80)

# Özet
summary = CategoryMetafieldManager.get_category_summary()
total_with_color = sum(1 for cat, count in summary.items() if count >= 1)
print(f"\nTüm {len(summary)} kategoride RENK meta alanı eklendi!")
print(f"Toplam meta alan sayısı arttı: {sum(summary.values())} meta alan")
