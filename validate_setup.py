#!/usr/bin/env python3
"""
Setup validation script for ArXiv Research Agent
Run this to ensure everything is properly configured
"""
import sys
import os
from typing import List, Tuple

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_python_version() -> Tuple[bool, str]:
    """Check if Python version is compatible"""
    required_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version >= required_version:
        return True, f"✅ Python {sys.version.split()[0]} (compatible)"
    else:
        return False, f"❌ Python {sys.version.split()[0]} (requires 3.8+)"

def check_dependencies() -> List[Tuple[bool, str]]:
    """Check if all required dependencies are installed"""
    dependencies = [
        ('gradio', 'Gradio web interface'),
        ('requests', 'HTTP requests'),
        ('feedparser', 'ArXiv XML parsing'),
        ('sklearn', 'Machine learning utilities'),
        ('fitz', 'PDF processing (PyMuPDF)'),
        ('PIL', 'Image processing (Pillow)')
    ]
    
    results = []
    for module, description in dependencies:
        try:
            __import__(module)
            results.append((True, f"✅ {description}"))
        except ImportError:
            results.append((False, f"❌ {description} - Missing: {module}"))
    
    return results

def check_imports() -> List[Tuple[bool, str]]:
    """Check if all project modules can be imported"""
    imports = [
        ('config.config', 'Configuration management'),
        ('src.arxiv_agent.core.models', 'Core data models'),
        ('src.arxiv_agent.core.agent', 'Main agent'),
        ('src.arxiv_agent.analysis.query_analyzer', 'Query analyzer'),
        ('src.arxiv_agent.analysis.visual_extractor', 'Visual extractor'),
        ('src.arxiv_agent.search.enhanced_search', 'Enhanced search'),
        ('src.arxiv_agent.ui.gradio_interface', 'Gradio interface')
    ]
    
    results = []
    for module, description in imports:
        try:
            __import__(module)
            results.append((True, f"✅ {description}"))
        except ImportError as e:
            results.append((False, f"❌ {description} - Error: {str(e)[:50]}..."))
    
    return results

def check_configuration() -> List[Tuple[bool, str]]:
    """Check configuration settings"""
    results = []
    
    try:
        from config.config import Config
        config = Config()
        
        # Check API key configuration
        if config.OPENROUTER_API_KEY and not config.OPENROUTER_API_KEY.startswith("your-"):
            results.append((True, "✅ OpenRouter API key configured"))
        else:
            results.append((False, "⚠️  OpenRouter API key not configured (required)"))
        
        if config.SERPER_API_KEY and not config.SERPER_API_KEY.startswith("your-"):
            results.append((True, "✅ Serper API key configured"))
        else:
            results.append((True, "ℹ️  Serper API key not configured (optional)"))
        
        # Check basic configuration
        results.append((True, f"✅ LLM Model: {config.LLM_MODEL}"))
        results.append((True, f"✅ Server Port: {config.GRADIO_SERVER_PORT}"))
        
    except Exception as e:
        results.append((False, f"❌ Configuration error: {str(e)}"))
    
    return results

def check_file_structure() -> List[Tuple[bool, str]]:
    """Check if required files and directories exist"""
    required_paths = [
        ('src/', 'Source directory'),
        ('config/', 'Configuration directory'),
        ('main.py', 'Main entry point'),
        ('requirements.txt', 'Dependencies file'),
        ('README.md', 'Documentation'),
        ('src/arxiv_agent/', 'Main package'),
        ('src/arxiv_agent/core/', 'Core modules'),
        ('src/arxiv_agent/search/', 'Search modules'),
        ('src/arxiv_agent/analysis/', 'Analysis modules'),
        ('src/arxiv_agent/ui/', 'UI modules')
    ]
    
    results = []
    for path, description in required_paths:
        if os.path.exists(path):
            results.append((True, f"✅ {description}"))
        else:
            results.append((False, f"❌ {description} - Missing: {path}"))
    
    return results

def run_basic_functionality_test() -> Tuple[bool, str]:
    """Run a basic functionality test"""
    try:
        from src.arxiv_agent.analysis.query_analyzer import QueryAnalyzer
        
        analyzer = QueryAnalyzer()
        analysis = analyzer.analyze_query("test query about machine learning")
        
        if hasattr(analysis, 'intent') and hasattr(analysis, 'complexity'):
            return True, "✅ Basic functionality test passed"
        else:
            return False, "❌ Basic functionality test failed - Invalid analysis result"
    
    except Exception as e:
        return False, f"❌ Basic functionality test failed: {str(e)}"

def main():
    """Main validation function"""
    print("🔬 ArXiv Research Agent - Setup Validation")
    print("=" * 50)
    
    all_checks_passed = True
    
    # Check Python version
    print("\n📋 Python Version Check:")
    passed, message = check_python_version()
    print(f"  {message}")
    if not passed:
        all_checks_passed = False
    
    # Check dependencies
    print("\n📦 Dependency Check:")
    for passed, message in check_dependencies():
        print(f"  {message}")
        if not passed:
            all_checks_passed = False
    
    # Check file structure
    print("\n📁 File Structure Check:")
    for passed, message in check_file_structure():
        print(f"  {message}")
        if not passed:
            all_checks_passed = False
    
    # Check imports
    print("\n🔗 Import Check:")
    for passed, message in check_imports():
        print(f"  {message}")
        if not passed:
            all_checks_passed = False
    
    # Check configuration
    print("\n⚙️  Configuration Check:")
    for passed, message in check_configuration():
        print(f"  {message}")
        if not passed and "required" in message:
            all_checks_passed = False
    
    # Run basic functionality test
    print("\n🧪 Functionality Test:")
    passed, message = run_basic_functionality_test()
    print(f"  {message}")
    if not passed:
        all_checks_passed = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_checks_passed:
        print("🎉 All checks passed! Your setup looks good.")
        print("\n💡 Next steps:")
        print("  1. Copy env.example to .env and configure your API keys")
        print("  2. Run 'python main.py' to start the application")
        print("  3. Open http://localhost:7861 in your browser")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\n💡 Common solutions:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Set API keys in environment or config.py")
        print("  3. Ensure Python 3.8+ is installed")
    
    return all_checks_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 