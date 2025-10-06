"""Test import script to verify module loading"""
import sys
import os

# Same setup as in pages
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print(f"Project root: {project_root}")
print(f"Python path first entry: {sys.path[0]}")
print(f"Utils directory exists: {os.path.exists(os.path.join(project_root, 'utils'))}")
print()

try:
    from utils.category_metafield_manager import CategoryMetafieldManager
    print("✓ SUCCESS: CategoryMetafieldManager imported successfully!")
    print(f"Class: {CategoryMetafieldManager}")
except Exception as e:
    print(f"❌ FAILED: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
