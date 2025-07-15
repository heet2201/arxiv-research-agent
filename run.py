#!/usr/bin/env python3
"""
Quick run script for ArXiv Research Agent
Alternative to main.py with additional checks
"""
import sys
import os

def main():
    """Main function with pre-flight checks"""
    print("🚀 Starting ArXiv Research Agent...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    
    # Add src to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        # Import and run main
        from main import main as main_func
        main_func()
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\n💡 Try running:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 For help, run:")
        print("   python validate_setup.py")
        sys.exit(1)

if __name__ == "__main__":
    main() 