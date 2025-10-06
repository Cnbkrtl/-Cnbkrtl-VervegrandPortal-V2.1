"""
Test script - Shopify Kategori Önerisi Sistemi
"""

import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from connectors.shopify_api import ShopifyAPI
from config_manager import ConfigManager

def test_category_suggestions():
    """Kategori öneri sistemini test et"""
    
    print("\n" + "="*80)
    print("TEST: Shopify Kategori Öneri Sistemi")
    print("="*80 + "\n")
    
    # Config yükle
    config = ConfigManager()
    user_keys = config.get_user_keys()
    
    shopify_api = ShopifyAPI(
        user_keys["shopify_store"],
        user_keys["shopify_token"]
    )
    
    # Test ürünleri
    test_products = [
        "Kadın Kırmızı V Yaka T-shirt",
        "Erkek Siyah Gömlek",
        "Kadın Mavi Elbise",
        "Çocuk Yeşil Bluz",
        "Kadın Beyaz Pantolon",
    ]
    
    for title in test_products:
        print(f"\n📦 Test Ürün: '{title}'")
        print("-" * 80)
        
        # Title'dan kelime ara
        title_lower = title.lower()
        
        category_keywords = {
            't-shirt': 'T-shirts',
            'tişört': 'T-shirts',
            'gömlek': 'Shirts',
            'shirt': 'Shirts',
            'elbise': 'Dresses',
            'dress': 'Dresses',
            'bluz': 'Blouses',
            'blouse': 'Blouses',
            'pantolon': 'Pants',
            'pants': 'Pants',
        }
        
        found_category = None
        for keyword, cat_name in category_keywords.items():
            if keyword in title_lower:
                found_category = cat_name
                print(f"✅ Tespit edilen kategori: {cat_name} ('{keyword}' kelimesinden)")
                break
        
        if not found_category:
            print("❌ Kategori tespit edilemedi")
    
    print("\n" + "="*80)
    print("✅ Test tamamlandı!")
    print("="*80 + "\n")

if __name__ == "__main__":
    test_category_suggestions()
