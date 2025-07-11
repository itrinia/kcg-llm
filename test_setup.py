#!/usr/bin/env python3
"""
Test script to verify the KCG LLM Chatbot setup
"""

import sys
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'torch',
        'transformers', 
        'numpy',
        'pandas',
        'requests',
        'jupyter'
    ]
    
    print("Testing package imports...")
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} - OK")
        except ImportError as e:
            print(f"❌ {package} - FAILED: {e}")
            return False
    return True

def test_ollama():
    """Test Ollama connection"""
    print("\nTesting Ollama connection...")
    try:
        import ollama
        models = ollama.list()
        print(f"✅ Ollama connection successful")
        print(f"Available models: {[model['name'] for model in models['models']]}")
        return True
    except ImportError:
        print("❌ Ollama package not installed. Run: pip install ollama")
        return False
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("Make sure Ollama app is running on your Mac")
        return False

def main():
    print("=" * 50)
    print("KCG LLM Chatbot Setup Test")
    print("=" * 50)
    
    # Test Python version
    print(f"Python version: {sys.version}")
    
    # Test imports
    imports_ok = test_imports()
    
    # Test Ollama
    ollama_ok = test_ollama()
    
    print("\n" + "=" * 50)
    if imports_ok and ollama_ok:
        print("✅ All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Start Jupyter: jupyter notebook")
        print("2. Open chat.ipynb to start developing your chatbot")
        print("3. Pull a model: ollama pull mistral")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    print("=" * 50)

if __name__ == "__main__":
    main() 