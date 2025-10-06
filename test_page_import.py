"""Test script to simulate how the page imports modules"""
import sys
import os

# Simulate being in the pages directory
os.chdir(os.path.join(os.path.dirname(__file__), 'pages'))

# Simulate Streamlit's sys.path with 'streamlit_app.py' entry (the bug)
sys.path.insert(0, 'streamlit_app.py')

# Now run the same import logic as the page
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

print(f"Original sys.path (first 3): {sys.path[:3]}")

# Clean sys.path (remove file names, keep only directories)
sys.path = [p for p in sys.path if (p == '' or (os.path.exists(p) and os.path.isdir(p)))]
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print(f"Cleaned sys.path (first 3): {sys.path[:3]}")
print(f"Project root: {project_root}")

# Try the import
try:
    from utils.category_metafield_manager import CategoryMetafieldManager
    print("\n✅ SUCCESS: Normal import worked!")
    print(f"Class: {CategoryMetafieldManager}")
except (ImportError, ModuleNotFoundError) as e:
    print(f"\n⚠️ Normal import failed: {e}")
    print("Trying alternative import method...")
    
    # Alternative import
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "category_metafield_manager",
        os.path.join(project_root, "utils", "category_metafield_manager.py")
    )
    category_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(category_module)
    CategoryMetafieldManager = category_module.CategoryMetafieldManager
    
    print("✅ SUCCESS: Alternative import worked!")
    print(f"Class: {CategoryMetafieldManager}")
