"""
System verification script
Run this to check if your environment is set up correctly.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def check_python_version():
    """Check Python version."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (need 3.9+)")
        return False


def check_dependencies():
    """Check if required packages are installed."""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'streamlit',
        'langchain',
        'openai',
        'chromadb',
        'yaml',
        'dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n   Run: pip install -r requirements.txt")
        return False
    return True


def check_env_file():
    """Check if .env file exists."""
    print("\n🔑 Checking environment configuration...")
    env_path = Path(__file__).parent.parent / '.env'
    
    if env_path.exists():
        print("   ✅ .env file exists")
        
        # Check for API keys
        with open(env_path, 'r') as f:
            content = f.read()
            
        if 'OPENAI_API_KEY' in content and 'your_' not in content.lower():
            print("   ✅ OpenAI API key configured")
            return True
        else:
            print("   ⚠️  API keys not configured in .env")
            print("   Edit .env and add your API keys")
            return False
    else:
        print("   ❌ .env file not found")
        print("   Run: cp .env.example .env")
        print("   Then edit .env with your API keys")
        return False


def check_config_files():
    """Check if configuration files exist."""
    print("\n⚙️  Checking configuration files...")
    
    config_files = [
        'config/config.yaml',
        'config/agents.yaml'
    ]
    
    all_exist = True
    for config_file in config_files:
        path = Path(__file__).parent.parent / config_file
        if path.exists():
            print(f"   ✅ {config_file}")
        else:
            print(f"   ❌ {config_file} (missing)")
            all_exist = False
    
    return all_exist


def check_directories():
    """Check if required directories exist."""
    print("\n📁 Checking directory structure...")
    
    directories = [
        'data/documents',
        'data/evaluation',
        'logs'
    ]
    
    for directory in directories:
        path = Path(__file__).parent.parent / directory
        if path.exists():
            print(f"   ✅ {directory}")
        else:
            print(f"   ⚠️  {directory} (will be created automatically)")
            path.mkdir(parents=True, exist_ok=True)
    
    return True


def test_import_modules():
    """Test importing project modules."""
    print("\n🧪 Testing project modules...")
    
    modules = [
        ('src.utils', 'ConfigLoader'),
        ('src.agents', 'AgentManager'),
        ('src.rag', 'RAGManager'),
        ('src.llm', 'LLMFactory')
    ]
    
    all_ok = True
    for module_name, class_name in modules:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"   ✅ {module_name}.{class_name}")
        except Exception as e:
            print(f"   ❌ {module_name}.{class_name}: {str(e)}")
            all_ok = False
    
    return all_ok


def check_sample_data():
    """Check if sample data exists."""
    print("\n📄 Checking sample data...")
    
    sample_files = [
        'data/documents/sample_ai_document.md',
        'data/documents/getting_started.md',
        'data/evaluation/sample_test_set.json'
    ]
    
    for sample_file in sample_files:
        path = Path(__file__).parent.parent / sample_file
        if path.exists():
            print(f"   ✅ {sample_file}")
        else:
            print(f"   ⚠️  {sample_file} (missing)")
    
    return True


def main():
    """Run all checks."""
    print("=" * 60)
    print("🔍 CHATBOT TEMPLATE - SYSTEM VERIFICATION")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("Config Files", check_config_files),
        ("Directories", check_directories),
        ("Project Modules", test_import_modules),
        ("Sample Data", check_sample_data)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} {name}")
    
    print("=" * 60)
    print(f"Result: {passed}/{total} checks passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All checks passed! You're ready to go!")
        print("\nNext steps:")
        print("1. Run: python scripts/init_vectordb.py")
        print("2. Run: streamlit run app.py")
        print("3. Open http://localhost:8501 in your browser")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Create .env file: cp .env.example .env")
        print("- Add API keys to .env file")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
