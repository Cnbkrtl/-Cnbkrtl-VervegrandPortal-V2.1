"""
🏷️ Otomatik Kategori ve Meta Alan Yönetim Sistemi

Ürün başlığından otomatik kategori tespiti ve kategori bazlı meta alanlarını doldurur.
Shopify'da manuel işlem yapmadan kategori ve meta alanlarını otomatik günceller.
"""

import re
import logging
from typing import Dict, List, Optional, Tuple

class CategoryMetafieldManager:
    """
    Kategori tespit ve meta alan yönetimi için merkezi sınıf.
    """
    
    # Kategori tespit için anahtar kelimeler (öncelik sırasına göre)
    CATEGORY_KEYWORDS = {
        'Elbise': ['elbise', 'dress'],
        'T-shirt': ['t-shirt', 'tshirt', 'tişört', 'tisort'],
        'Bluz': ['bluz', 'blouse', 'gömlek'],
        'Pantolon': ['pantolon', 'pants', 'jean', 'kot'],
        'Şort': ['şort', 'sort', 'short'],
        'Etek': ['etek', 'skirt'],
        'Ceket': ['ceket', 'jacket', 'mont', 'kaban'],
        'Kazak': ['kazak', 'sweater', 'hırka', 'hirka', 'cardigan'],
        'Tunik': ['tunik', 'tunic'],
        'Yelek': ['yelek', 'vest'],
        'Şal': ['şal', 'sal', 'scarf', 'atkı', 'atki'],
        'Takım': ['takım', 'takim', 'suit', 'set'],
        'Mayo': ['mayo', 'bikini', 'swimsuit'],
        'Gecelik': ['gecelik', 'pijama', 'nightgown'],
        'Kaban': ['kaban', 'palto', 'coat'],
        'Tulum': ['tulum', 'jumpsuit', 'overall']
    }
    
    # Her kategori için meta alan şablonları
    # Shopify'daki standart meta alanlarına göre düzenlenmiştir
    CATEGORY_METAFIELDS = {
        'Elbise': {
            'custom.yaka_tipi': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'yaka_tipi',
                'description': 'Yaka tipi (V yaka, Bisiklet yaka, Halter vb.)'
            },
            'custom.kol_tipi': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'kol_tipi',
                'description': 'Kol tipi (Kısa kol, Uzun kol, Kolsuz vb.)'
            },
            'custom.boy': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'boy',
                'description': 'Elbise boyu (Mini, Midi, Maxi, Diz üstü vb.)'
            },
            'custom.desen': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'desen',
                'description': 'Desen (Çiçekli, Düz, Leopar, Çizgili vb.)'
            },
            'custom.kullanim_alani': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'kullanim_alani',
                'description': 'Kullanım alanı (Günlük, Gece, Kokteyl vb.)'
            }
        },
        'T-shirt': {
            'custom.yaka_tipi': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'yaka_tipi',
                'description': 'Yaka tipi (V yaka, Bisiklet yaka, Polo vb.)'
            },
            'custom.kol_tipi': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'kol_tipi',
                'description': 'Kol tipi (Kısa kol, Uzun kol vb.)'
            },
            'custom.desen': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'desen',
                'description': 'Desen (Baskılı, Düz, Çizgili vb.)'
            }
        },
        'Bluz': {
            'custom.yaka_tipi': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'yaka_tipi',
                'description': 'Yaka tipi (V yaka, Hakim yaka, Gömlek yaka vb.)'
            },
            'custom.kol_tipi': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'kol_tipi',
                'description': 'Kol tipi (Kısa kol, Uzun kol, 3/4 kol vb.)'
            },
            'custom.desen': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'desen',
                'description': 'Desen'
            }
        },
        'Pantolon': {
            'custom.pacha_tipi': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'pacha_tipi',
                'description': 'Paça tipi (Dar paça, Bol paça, İspanyol paça vb.)'
            },
            'custom.bel_tipi': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'bel_tipi',
                'description': 'Bel tipi (Yüksek bel, Normal bel, Düşük bel vb.)'
            },
            'custom.boy': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'boy',
                'description': 'Pantolon boyu (Uzun, 7/8, Capri vb.)'
            }
        },
        'Şort': {
            'custom.boy': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'boy',
                'description': 'Şort boyu (Mini, Midi, Bermuda vb.)'
            },
            'custom.bel_tipi': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'bel_tipi',
                'description': 'Bel tipi (Yüksek bel, Normal bel vb.)'
            }
        },
        'Etek': {
            'custom.boy': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'boy',
                'description': 'Etek boyu (Mini, Midi, Maxi vb.)'
            },
            'custom.model': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'model',
                'description': 'Model (Kalem, Pileli, A kesim vb.)'
            }
        },
        'Ceket': {
            'custom.kol_tipi': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'kol_tipi',
                'description': 'Kol tipi (Uzun kol, Kısa kol vb.)'
            },
            'custom.kapanma_tipi': {
                'type': 'single_line_text_field',
                'namespace': 'custom',
                'key': 'kapanma_tipi',
                'description': 'Kapanma tipi (Fermuarlı, Düğmeli, Çıtçıtlı vb.)'
            }
        }
    }
    
    @staticmethod
    def detect_category(product_title: str) -> Optional[str]:
        """
        Ürün başlığından kategori tespit eder.
        
        Args:
            product_title: Ürün başlığı
            
        Returns:
            Tespit edilen kategori veya None
        """
        if not product_title:
            return None
        
        title_lower = product_title.lower()
        
        # Öncelik sırasına göre kontrol et
        for category, keywords in CategoryMetafieldManager.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in title_lower:
                    logging.info(f"Kategori tespit edildi: '{category}' (Anahtar: '{keyword}')")
                    return category
        
        logging.warning(f"'{product_title}' için kategori tespit edilemedi")
        return None
    
    @staticmethod
    def extract_metafield_values(product_title: str, category: str) -> Dict[str, str]:
        """
        Ürün başlığından meta alan değerlerini çıkarır.
        
        Args:
            product_title: Ürün başlığı
            category: Tespit edilen kategori
            
        Returns:
            Meta alan değerleri (key: value)
        """
        values = {}
        title_lower = product_title.lower()
        
        # Ortak kalıplar
        patterns = {
            'yaka_tipi': [
                (r'v\s*yaka', 'V Yaka'),
                (r'bisiklet\s*yaka', 'Bisiklet Yaka'),
                (r'hakim\s*yaka', 'Hakim Yaka'),
                (r'polo\s*yaka', 'Polo Yaka'),
                (r'balıkçı\s*yaka', 'Balıkçı Yaka'),
                (r'halter', 'Halter'),
                (r'kayık\s*yaka', 'Kayık Yaka'),
                (r'gömlek\s*yaka', 'Gömlek Yaka'),
            ],
            'kol_tipi': [
                (r'uzun\s*kol', 'Uzun Kol'),
                (r'kısa\s*kol', 'Kısa Kol'),
                (r'kolsuz', 'Kolsuz'),
                (r'3/4\s*kol', '3/4 Kol'),
                (r'yarım\s*kol', 'Yarım Kol'),
            ],
            'boy': [
                (r'mini', 'Mini'),
                (r'midi', 'Midi'),
                (r'maxi', 'Maxi'),
                (r'diz\s*üst', 'Diz Üstü'),
                (r'diz\s*alt', 'Diz Altı'),
                (r'bilekli', 'Bilekli'),
            ],
            'desen': [
                (r'leopar', 'Leopar'),
                (r'çiçek', 'Çiçekli'),
                (r'düz\s*renk', 'Düz'),
                (r'çizgi', 'Çizgili'),
                (r'desenli', 'Desenli'),
                (r'baskı', 'Baskılı'),
                (r'puantiye', 'Puantiyeli'),
                (r'kareli', 'Kareli'),
            ],
            'pacha_tipi': [
                (r'dar\s*paça', 'Dar Paça'),
                (r'bol\s*paça', 'Bol Paça'),
                (r'ispanyol\s*paça', 'İspanyol Paça'),
                (r'düz\s*paça', 'Düz Paça'),
            ],
            'bel_tipi': [
                (r'yüksek\s*bel', 'Yüksek Bel'),
                (r'normal\s*bel', 'Normal Bel'),
                (r'düşük\s*bel', 'Düşük Bel'),
            ]
        }
        
        # Her meta alan için değer çıkar
        for field, pattern_list in patterns.items():
            for pattern, value in pattern_list:
                if re.search(pattern, title_lower):
                    values[field] = value
                    logging.info(f"Meta alan çıkarıldı: {field} = '{value}'")
                    break  # İlk eşleşmeyi al
        
        return values
    
    @staticmethod
    def get_metafields_for_category(category: str) -> Dict[str, dict]:
        """
        Belirtilen kategori için meta alan şablonlarını döndürür.
        
        Args:
            category: Kategori adı
            
        Returns:
            Meta alan şablonları
        """
        return CategoryMetafieldManager.CATEGORY_METAFIELDS.get(category, {})
    
    @staticmethod
    def prepare_metafields_for_shopify(
        category: str, 
        product_title: str,
        product_description: str = ""
    ) -> List[Dict]:
        """
        Shopify GraphQL için metafield input formatını hazırlar.
        
        Args:
            category: Ürün kategorisi
            product_title: Ürün başlığı
            product_description: Ürün açıklaması
            
        Returns:
            Shopify metafield input listesi
        """
        metafield_templates = CategoryMetafieldManager.get_metafields_for_category(category)
        extracted_values = CategoryMetafieldManager.extract_metafield_values(product_title, category)
        
        shopify_metafields = []
        
        for field_key, template in metafield_templates.items():
            # Meta alan key'ini çıkar (custom.yaka_tipi -> yaka_tipi)
            key = template['key']
            
            # Çıkarılan değerler içinde varsa kullan
            if key in extracted_values:
                value = extracted_values[key]
                
                shopify_metafields.append({
                    'namespace': template['namespace'],
                    'key': template['key'],
                    'value': value,
                    'type': template['type']
                })
                
                logging.info(f"Shopify metafield hazırlandı: {template['namespace']}.{template['key']} = '{value}'")
        
        return shopify_metafields
    
    @staticmethod
    def get_category_summary() -> Dict[str, int]:
        """
        Kategori istatistiklerini döndürür.
        
        Returns:
            Kategori adı ve meta alan sayısı
        """
        summary = {}
        for category, metafields in CategoryMetafieldManager.CATEGORY_METAFIELDS.items():
            summary[category] = len(metafields)
        return summary


# Kullanım örneği
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test
    test_titles = [
        "Büyük Beden Uzun Kollu Leopar Desenli Diz Üstü Elbise 285058",
        "Büyük Beden Bisiklet Yaka Yarım Kollu Düz Renk T-shirt 303734",
        "Büyük Beden V Yaka Kısa Kol Çiçekli Bluz 256478",
        "Büyük Beden Yüksek Bel Dar Paça Siyah Pantolon 123456"
    ]
    
    for title in test_titles:
        print(f"\n{'='*60}")
        print(f"Ürün: {title}")
        print(f"{'='*60}")
        
        # Kategori tespit
        category = CategoryMetafieldManager.detect_category(title)
        print(f"Kategori: {category}")
        
        if category:
            # Meta alanları hazırla
            metafields = CategoryMetafieldManager.prepare_metafields_for_shopify(category, title)
            print(f"\nOluşturulan Meta Alanlar ({len(metafields)}):")
            for mf in metafields:
                print(f"  - {mf['namespace']}.{mf['key']} = '{mf['value']}'")
