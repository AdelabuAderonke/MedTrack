# test_import.py
try:
    from flask_restx import Api
    print("✅ Import successful!")
    print(f"flask-restx version: {Api.__module__}")
except ImportError as e:
    print(f"❌ Import failed: {e}")