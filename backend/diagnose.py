#!/usr/bin/env python
"""
HerCare Diagnostic Script
========================
Checks if all required model files exist and are valid.

Run this script to troubleshoot model loading issues:
    python diagnose.py
"""

import os
import sys

def check_models():
    """Check if all required model files exist."""
    
    print("\n" + "="*60)
    print("🔍 HerCare Model Diagnostic Check")
    print("="*60 + "\n")
    
    # Define expected models
    models = {
        "CNN Model": "pcos_screener/model/model.h5",
        "Ensemble Model": "pcos_screener/model/pcos_ensemble_model.pkl",
        "Feature Scaler": "pcos_screener/model/scaler.pkl",
    }
    
    all_exist = True
    
    for model_name, model_path in models.items():
        abs_path = os.path.join(os.path.dirname(__file__), model_path)
        exists = os.path.exists(abs_path)
        
        if exists:
            size = os.path.getsize(abs_path)
            size_mb = size / 1024 / 1024
            status = "✅ FOUND"
            print(f"{status} {model_name}")
            print(f"   Path: {model_path}")
            print(f"   Size: {size_mb:.2f} MB")
        else:
            status = "❌ MISSING"
            all_exist = False
            print(f"{status} {model_name}")
            print(f"   Path: {model_path}")
            print(f"   Expected at: {abs_path}")
        
        print()
    
    return all_exist


def check_python_deps():
    """Check if required Python packages are installed."""
    
    print("="*60)
    print("📦 Python Dependencies Check")
    print("="*60 + "\n")
    
    deps = [
        ("Django", "django"),
        ("TensorFlow", "tensorflow"),
        ("Scikit-learn", "sklearn"),
        ("Pillow", "PIL"),
        ("Joblib", "joblib"),
        ("NumPy", "numpy"),
        ("Pandas", "pandas"),
    ]
    
    all_installed = True
    
    for display_name, import_name in deps:
        try:
            module = __import__(import_name)
            version = getattr(module, '__version__', 'unknown')
            status = "✅"
            print(f"{status} {display_name:20} v{version}")
        except ImportError:
            status = "❌"
            all_installed = False
            print(f"{status} {display_name:20} NOT INSTALLED")
    
    print()
    return all_installed


def check_dirs():
    """Check if required directories exist."""
    
    print("="*60)
    print("📁 Directory Structure Check")
    print("="*60 + "\n")
    
    dirs = {
        "Backend": ".",
        "PCOS Screener App": "pcos_screener",
        "Models Dir": "pcos_screener/model",
        "Data Dir": "pcos_screener/data",
        "Templates Dir": "pcos_screener/templates",
    }
    
    all_exist = True
    
    for dir_name, dir_path in dirs.items():
        abs_path = os.path.join(os.path.dirname(__file__), dir_path)
        exists = os.path.isdir(abs_path)
        status = "✅" if exists else "❌"
        
        print(f"{status} {dir_name:20} {dir_path}")
        if not exists:
            all_exist = False
    
    print()
    
    # Show model directory contents
    print("Contents of pcos_screener/model/:")
    model_dir = os.path.join(os.path.dirname(__file__), "pcos_screener/model")
    if os.path.exists(model_dir):
        files = os.listdir(model_dir)
        for file in files:
            file_path = os.path.join(model_dir, file)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                print(f"  - {file} ({size / 1024:.2f} KB)")
        if not files:
            print("  (directory is empty)")
    else:
        print(f"  (directory does not exist)")
    
    print()
    return all_exist


def main():
    """Run all diagnostic checks."""
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    models_ok = check_models()
    dirs_ok = check_dirs()
    deps_ok = check_python_deps()
    
    print("="*60)
    print("📋 Diagnostic Summary")
    print("="*60 + "\n")
    
    if models_ok and dirs_ok and deps_ok:
        print("✅ All checks passed!")
        print("\nYou can now run the Django server:")
        print("  python manage.py runserver")
        return 0
    else:
        print("❌ Some checks failed. See above for details.\n")
        
        if not models_ok:
            print("⚠️  Missing Model Files:")
            print("   The CNN model (model.h5) or other models are missing.")
            print("   You need to:")
            print("   1. Train or obtain the model file")
            print("   2. Place it in: pcos_screener/model/model.h5")
            print()
        
        if not deps_ok:
            print("⚠️  Missing Dependencies:")
            print("   Install missing packages with:")
            print("   pip install -r requirements.txt")
            print()
        
        if not dirs_ok:
            print("⚠️  Directory Structure Issue:")
            print("   Run this script from the backend directory")
            print()
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
