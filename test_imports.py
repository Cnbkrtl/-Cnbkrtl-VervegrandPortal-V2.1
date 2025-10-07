#!/usr/bin/env python
# test_imports.py - Import sorunlarını test et

import sys
import os

# Proje kök dizinini ekle
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

print("🔍 Import Test Başlıyor...\n")
print(f"Python Path: {project_root}\n")

# Test 1: Temel modüller
print("✓ Test 1: Temel modüller")
try:
    import config_manager
    print("  ✅ config_manager")
except Exception as e:
    print(f"  ❌ config_manager: {e}")

try:
    from gsheets_manager import GoogleSheetsManager
    print("  ✅ gsheets_manager")
except Exception as e:
    print(f"  ❌ gsheets_manager: {e}")

try:
    from log_manager import LogManager
    print("  ✅ log_manager")
except Exception as e:
    print(f"  ❌ log_manager: {e}")

try:
    import utils
    print("  ✅ utils")
except Exception as e:
    print(f"  ❌ utils: {e}")

# Test 2: Connectors
print("\n✓ Test 2: Connectors")
try:
    from connectors.shopify_api import ShopifyAPI
    print("  ✅ connectors.shopify_api")
except Exception as e:
    print(f"  ❌ connectors.shopify_api: {e}")

try:
    from connectors.sentos_api import SentosAPI
    print("  ✅ connectors.sentos_api")
except Exception as e:
    print(f"  ❌ connectors.sentos_api: {e}")

# Test 3: Operations
print("\n✓ Test 3: Operations")
try:
    from operations import core_sync
    print("  ✅ operations.core_sync")
except Exception as e:
    print(f"  ❌ operations.core_sync: {e}")

try:
    from operations import media_sync
    print("  ✅ operations.media_sync")
except Exception as e:
    print(f"  ❌ operations.media_sync: {e}")

try:
    from operations import stock_sync
    print("  ✅ operations.stock_sync")
except Exception as e:
    print(f"  ❌ operations.stock_sync: {e}")

# Test 4: Sync Runner
print("\n✓ Test 4: Sync Runner")
try:
    import sync_runner
    print("  ✅ sync_runner")
except Exception as e:
    print(f"  ❌ sync_runner: {e}")

print("\n✅ Test Tamamlandı!")
