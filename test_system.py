"""
Test Script for Content Intelligence Analyzer
Run this script to verify all components are working correctly
"""

import sys
import importlib

def check_imports():
    """Check if all required packages are installed"""
    print("🔍 Checking required packages...")
    
    required_packages = [
        'streamlit',
        'bs4',  # BeautifulSoup
        'requests',
        'PyPDF2',
        'docx',
        'pandas',
        'openpyxl'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    print("\n✅ All required packages are installed!")
    return True

def check_files():
    """Check if all required files exist"""
    print("\n🔍 Checking required files...")
    
    import os
    
    required_files = [
        'content_analyzer.py',
        'analysis_modules.py',
        'requirements.txt',
        'README.md',
        'QUICK_START.md'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - NOT FOUND")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    
    print("\n✅ All required files are present!")
    return True

def test_data_directory():
    """Check if data directory can be created"""
    print("\n🔍 Testing data directory creation...")
    
    import os
    from pathlib import Path
    
    try:
        data_dir = Path("analyzer_data")
        data_dir.mkdir(exist_ok=True)
        
        # Try to create a test file
        test_file = data_dir / "test.txt"
        test_file.write_text("test")
        test_file.unlink()
        
        print("  ✅ Data directory is working")
        return True
    except Exception as e:
        print(f"  ❌ Error with data directory: {str(e)}")
        return False

def test_basic_functions():
    """Test basic functionality"""
    print("\n🔍 Testing basic functions...")
    
    try:
        from analysis_modules import (
            analyze_funnel_stage,
            extract_entities,
            analyze_keyword_optimization
        )
        
        # Test content
        test_content = """
        This is a test article about content marketing and SEO optimization.
        Learn how to improve your content strategy with these best practices.
        We'll cover keyword research, content creation, and performance tracking.
        """
        
        # Test funnel analysis
        funnel_result = analyze_funnel_stage(test_content)
        if 'primary_stage' in funnel_result:
            print(f"  ✅ Funnel analysis works (Stage: {funnel_result['primary_stage']})")
        else:
            print("  ❌ Funnel analysis failed")
            return False
        
        # Test entity extraction
        entity_result = extract_entities(test_content)
        if 'total_words' in entity_result:
            print(f"  ✅ Entity extraction works ({entity_result['total_words']} words)")
        else:
            print("  ❌ Entity extraction failed")
            return False
        
        # Test keyword analysis
        keywords = ['content marketing', 'SEO']
        keyword_result = analyze_keyword_optimization(test_content, keywords)
        if 'keyword_analysis' in keyword_result:
            print(f"  ✅ Keyword analysis works")
        else:
            print("  ❌ Keyword analysis failed")
            return False
        
        print("\n✅ All basic functions are working!")
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing functions: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🚀 Content Intelligence Analyzer - System Check")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Package Check", check_imports()))
    results.append(("File Check", check_files()))
    results.append(("Data Directory", test_data_directory()))
    results.append(("Function Tests", test_basic_functions()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All tests passed! Your system is ready.")
        print("\nTo start the application, run:")
        print("  streamlit run content_analyzer.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("Check the error messages and install missing dependencies.")
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
