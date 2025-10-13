# operations/sales_analytics.py
"""
Sentos Satış Analizi Modülü
E-Ticaret kanalından satış verilerini çeker ve detaylı analiz yapar
"""

import logging
from datetime import datetime, timedelta
from collections import defaultdict

class SalesAnalytics:
    """Satış verilerini analiz eden sınıf"""
    
    def __init__(self, sentos_api):
        """
        Args:
            sentos_api: SentosAPI instance
        """
        self.sentos_api = sentos_api
    
    def analyze_sales_data(self, start_date=None, end_date=None, marketplace=None, 
                          progress_callback=None):
        """
        Satış verilerini çeker ve detaylı analiz yapar
        
        Args:
            start_date: Başlangıç tarihi (YYYY-MM-DD)
            end_date: Bitiş tarihi (YYYY-MM-DD)
            marketplace: Pazar yeri filtresi
            progress_callback: İlerleme callback fonksiyonu
            
        Returns:
            dict: Detaylı analiz sonuçları
        """
        
        if progress_callback:
            progress_callback({
                'message': '📊 Satış verileri çekiliyor...',
                'progress': 0
            })
        
        # Tüm siparişleri çek
        all_orders = self.sentos_api.get_all_sales_orders(
            start_date=start_date,
            end_date=end_date,
            marketplace=marketplace,
            progress_callback=progress_callback
        )
        
        if progress_callback:
            progress_callback({
                'message': '📈 Veriler analiz ediliyor...',
                'progress': 50
            })
        
        # Analiz yap
        analysis = self._analyze_orders(all_orders, progress_callback)
        
        if progress_callback:
            progress_callback({
                'message': '✅ Analiz tamamlandı!',
                'progress': 100
            })
        
        return analysis
    
    def _analyze_orders(self, orders, progress_callback=None):
        """
        Sipariş listesini detaylı analiz eder
        
        Returns:
            dict: {
                'summary': {...},           # Özet istatistikler
                'by_marketplace': {...},    # Pazar yeri bazında
                'by_date': {...},          # Tarih bazında
                'by_product': {...},       # Ürün bazında
                'returns': {...},          # İade analizi
                'profitability': {...}     # Karlılık analizi
            }
        """
        
        # Veri yapıları
        summary = {
            'total_orders': 0,
            'gross_quantity': 0,
            'gross_revenue': 0,
            'return_quantity': 0,
            'return_amount': 0,
            'net_quantity': 0,
            'net_revenue': 0,
            'total_cost': 0,
            'gross_profit': 0,
            'profit_margin': 0
        }
        
        by_marketplace = defaultdict(lambda: {
            'order_count': 0,
            'gross_quantity': 0,
            'gross_revenue': 0,
            'return_quantity': 0,
            'return_amount': 0,
            'net_quantity': 0,
            'net_revenue': 0,
            'total_cost': 0,
            'gross_profit': 0
        })
        
        by_date = defaultdict(lambda: {
            'order_count': 0,
            'gross_quantity': 0,
            'gross_revenue': 0,
            'return_quantity': 0,
            'return_amount': 0,
            'net_quantity': 0,
            'net_revenue': 0
        })
        
        by_product = defaultdict(lambda: {
            'product_name': '',
            'sku': '',
            'quantity_sold': 0,
            'quantity_returned': 0,
            'net_quantity': 0,
            'gross_revenue': 0,
            'return_amount': 0,
            'net_revenue': 0,
            'unit_cost': 0,
            'total_cost': 0,
            'gross_profit': 0,
            'profit_margin': 0
        })
        
        returns_data = {
            'total_returns': 0,
            'return_rate': 0,
            'top_returned_products': []
        }
        
        # Siparişleri işle
        total = len(orders)
        for idx, order in enumerate(orders):
            if progress_callback and idx % 100 == 0:
                progress_callback({
                    'message': f'📈 Sipariş {idx + 1}/{total} analiz ediliyor...',
                    'progress': 50 + int((idx / total) * 50)
                })
            
            self._process_order(
                order, 
                summary, 
                by_marketplace, 
                by_date, 
                by_product
            )
        
        # İade oranını hesapla
        if summary['gross_quantity'] > 0:
            returns_data['total_returns'] = summary['return_quantity']
            returns_data['return_rate'] = (summary['return_quantity'] / summary['gross_quantity']) * 100
        
        # En çok iade alan ürünleri bul
        products_with_returns = [
            {
                'product_name': data['product_name'],
                'sku': data['sku'],
                'return_quantity': data['quantity_returned'],
                'return_rate': (data['quantity_returned'] / data['quantity_sold'] * 100) if data['quantity_sold'] > 0 else 0
            }
            for data in by_product.values()
            if data['quantity_returned'] > 0
        ]
        returns_data['top_returned_products'] = sorted(
            products_with_returns, 
            key=lambda x: x['return_quantity'], 
            reverse=True
        )[:20]
        
        # Net değerleri hesapla
        summary['net_quantity'] = summary['gross_quantity'] - summary['return_quantity']
        summary['net_revenue'] = summary['gross_revenue'] - summary['return_amount']
        summary['gross_profit'] = summary['net_revenue'] - summary['total_cost']
        
        if summary['net_revenue'] > 0:
            summary['profit_margin'] = (summary['gross_profit'] / summary['net_revenue']) * 100
        
        # Pazar yeri bazında net hesaplamalar
        for mp_data in by_marketplace.values():
            mp_data['net_quantity'] = mp_data['gross_quantity'] - mp_data['return_quantity']
            mp_data['net_revenue'] = mp_data['gross_revenue'] - mp_data['return_amount']
            mp_data['gross_profit'] = mp_data['net_revenue'] - mp_data['total_cost']
            if mp_data['net_revenue'] > 0:
                mp_data['profit_margin'] = (mp_data['gross_profit'] / mp_data['net_revenue']) * 100
        
        # Tarih bazında net hesaplamalar
        for date_data in by_date.values():
            date_data['net_quantity'] = date_data['gross_quantity'] - date_data['return_quantity']
            date_data['net_revenue'] = date_data['gross_revenue'] - date_data['return_amount']
        
        # Ürün bazında karlılık hesapla
        for product_data in by_product.values():
            product_data['net_quantity'] = product_data['quantity_sold'] - product_data['quantity_returned']
            product_data['net_revenue'] = product_data['gross_revenue'] - product_data['return_amount']
            product_data['gross_profit'] = product_data['net_revenue'] - product_data['total_cost']
            if product_data['net_revenue'] > 0:
                product_data['profit_margin'] = (product_data['gross_profit'] / product_data['net_revenue']) * 100
        
        # Karlılık özeti
        profitability = {
            'total_cost': summary['total_cost'],
            'gross_profit': summary['gross_profit'],
            'profit_margin': summary['profit_margin'],
            'top_profitable_products': self._get_top_profitable_products(by_product, top_n=20),
            'low_margin_products': self._get_low_margin_products(by_product, threshold=10, top_n=20)
        }
        
        return {
            'summary': summary,
            'by_marketplace': dict(by_marketplace),
            'by_date': dict(sorted(by_date.items())),
            'by_product': dict(by_product),
            'returns': returns_data,
            'profitability': profitability
        }
    
    def _process_order(self, order, summary, by_marketplace, by_date, by_product):
        """Tek bir siparişi işler ve istatistiklere ekler"""
        
        # Debug: İlk siparişin yapısını logla
        if summary['total_orders'] == 0:
            logging.info(f"Örnek sipariş yapısı: {order}")
        
        # Temel bilgiler - Sentos API field isimleri
        order_status = order.get('status', order.get('orderStatus', 'UNKNOWN'))
        
        # Marketplace için farklı olası field isimlerini kontrol et
        marketplace = (
            order.get('marketplace') or 
            order.get('marketPlace') or 
            order.get('channel') or 
            order.get('salesChannel') or
            'UNKNOWN'
        )
        
        # Tarih için farklı olası field isimlerini kontrol et
        order_date = (
            order.get('createdDate') or 
            order.get('orderDate') or 
            order.get('date') or
            ''
        )
        if order_date and len(order_date) >= 10:
            order_date = order_date[:10]  # YYYY-MM-DD formatına çevir
        else:
            order_date = 'UNKNOWN'
        
        # İade mi kontrol et
        is_return = order_status.upper() in ['RETURNED', 'CANCELLED', 'REFUNDED', 'IPTAL', 'IADE']
        
        # Sipariş sayısı
        summary['total_orders'] += 1
        by_marketplace[marketplace]['order_count'] += 1
        by_date[order_date]['order_count'] += 1
        
        # Sipariş kalemleri - Farklı olası field isimlerini kontrol et
        items = (
            order.get('items') or 
            order.get('orderItems') or 
            order.get('products') or 
            []
        )
        
        for item in items:
            # Miktar
            quantity = (
                item.get('quantity') or 
                item.get('qty') or 
                item.get('amount') or 
                0
            )
            
            # Birim fiyat
            unit_price = float(
                item.get('unitPrice') or 
                item.get('price') or 
                item.get('salePrice') or 
                0
            )
            
            # Toplam fiyat
            item_total = float(
                item.get('totalPrice') or 
                item.get('total') or 
                (quantity * unit_price)
            )
            
            # Maliyet bilgisi (eğer varsa)
            unit_cost = float(
                item.get('unitCost') or 
                item.get('cost') or 
                item.get('buyPrice') or 
                0
            )
            total_cost = unit_cost * quantity
            
            # Ürün bilgileri
            product_name = (
                item.get('productName') or 
                item.get('name') or 
                item.get('title') or 
                'Bilinmeyen Ürün'
            )
            
            sku = (
                item.get('sku') or 
                item.get('productCode') or 
                item.get('barcode') or 
                ''
            )
            
            product_key = f"{sku}_{product_name}" if sku else product_name
            
            if not by_product[product_key]['product_name']:
                by_product[product_key]['product_name'] = product_name
                by_product[product_key]['sku'] = sku
                by_product[product_key]['unit_cost'] = unit_cost
            
            if is_return:
                # İade
                summary['return_quantity'] += quantity
                summary['return_amount'] += item_total
                
                by_marketplace[marketplace]['return_quantity'] += quantity
                by_marketplace[marketplace]['return_amount'] += item_total
                
                by_date[order_date]['return_quantity'] += quantity
                by_date[order_date]['return_amount'] += item_total
                
                by_product[product_key]['quantity_returned'] += quantity
                by_product[product_key]['return_amount'] += item_total
            else:
                # Normal satış
                summary['gross_quantity'] += quantity
                summary['gross_revenue'] += item_total
                summary['total_cost'] += total_cost
                
                by_marketplace[marketplace]['gross_quantity'] += quantity
                by_marketplace[marketplace]['gross_revenue'] += item_total
                by_marketplace[marketplace]['total_cost'] += total_cost
                
                by_date[order_date]['gross_quantity'] += quantity
                by_date[order_date]['gross_revenue'] += item_total
                
                by_product[product_key]['quantity_sold'] += quantity
                by_product[product_key]['gross_revenue'] += item_total
                by_product[product_key]['total_cost'] += total_cost
    
    def _get_top_profitable_products(self, by_product, top_n=20):
        """En karlı ürünleri döndürür"""
        products = [
            {
                'product_name': data['product_name'],
                'sku': data['sku'],
                'net_quantity': data['net_quantity'],
                'net_revenue': data['net_revenue'],
                'total_cost': data['total_cost'],
                'gross_profit': data['gross_profit'],
                'profit_margin': data['profit_margin']
            }
            for data in by_product.values()
            if data['net_quantity'] > 0
        ]
        
        return sorted(products, key=lambda x: x['gross_profit'], reverse=True)[:top_n]
    
    def _get_low_margin_products(self, by_product, threshold=10, top_n=20):
        """Düşük marjlı ürünleri döndürür"""
        products = [
            {
                'product_name': data['product_name'],
                'sku': data['sku'],
                'net_quantity': data['net_quantity'],
                'net_revenue': data['net_revenue'],
                'total_cost': data['total_cost'],
                'gross_profit': data['gross_profit'],
                'profit_margin': data['profit_margin']
            }
            for data in by_product.values()
            if data['net_quantity'] > 0 and data['profit_margin'] < threshold
        ]
        
        return sorted(products, key=lambda x: x['profit_margin'])[:top_n]
