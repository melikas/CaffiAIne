#!/usr/bin/env python3
"""
Setup script for CaffiAIne Agentic AI System
This script helps users set up the system quickly and easily.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_dependencies():
    """Install required dependencies"""
    try:
        print("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    print("📝 Creating .env file...")
    
    env_content = """# Google Gemini API Configuration
# Get your free API key from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional: Memory file location
MEMORY_FILE=agent_memory.json

# Optional: Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("⚠️  Please edit the .env file and add your Google Gemini API key")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def check_env_file():
    """Check if .env file is properly configured"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("⚠️  Warning: GOOGLE_API_KEY not set or using default value")
        print("Please edit the .env file and add your actual API key")
        return False
    
    print("✅ .env file is properly configured")
    return True

def run_tests():
    """Run system tests"""
    try:
        print("🧪 Running system tests...")
        result = subprocess.run([sys.executable, "test_gemini.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def show_next_steps():
    """Show next steps for the user"""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Edit the .env file and add your Google Gemini API key")
    print("2. Run: python test_gemini.py (to verify everything works)")
    print("3. Run: python main.py (to start the system)")
    print("\n💡 Example usage:")
    print("   python main.py")
    print("   # Then try: 'Search for information about AI'")

def main():
    """Main setup function"""
    print("🚀 CaffiAIne Agentic AI System Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create .env file
    if not create_env_file():
        return False
    
    # Check environment configuration
    check_env_file()
    
    # Run tests (optional, since API key might not be set yet)
    print("\n🔍 Running basic tests...")
    run_tests()
    
    # Show next steps
    show_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 