#!/usr/bin/env python3
"""
Test script for CaffiAIne Agentic AI System
This script tests the core functionality and Gemini API integration.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test basic Gemini API functionality"""
    try:
        import google.generativeai as genai
        
        # Check for API key
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("❌ Error: GOOGLE_API_KEY not found in environment variables")
            print("Please set your Google Gemini API key in a .env file")
            return False
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-1.5-pro')
        
        # Test simple generation
        response = model.generate_content("Hello, this is a test. Please respond with 'Test successful' if you can see this message.")
        
        if response.text:
            print("✅ Gemini API test successful!")
            print(f"Response: {response.text}")
            return True
        else:
            print("❌ Gemini API test failed: No response received")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        return False

def test_imports():
    """Test that all modules can be imported"""
    try:
        from planner import plan, prioritize_tasks
        from executor import execute_task, get_executor
        from memory import get_memory_manager, store_conversation
        from main import AgenticAI
        
        print("✅ All module imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_memory_system():
    """Test memory system functionality"""
    try:
        from memory import get_memory_manager
        
        memory_manager = get_memory_manager()
        
        # Test storing and retrieving
        memory_manager.store_conversation("Test input", "Test response")
        conversations = memory_manager.recall_conversations(limit=1)
        
        if conversations:
            print("✅ Memory system test successful!")
            return True
        else:
            print("❌ Memory system test failed: No conversations retrieved")
            return False
            
    except Exception as e:
        print(f"❌ Memory system test failed: {e}")
        return False

def test_planner():
    """Test planner functionality"""
    try:
        from planner import plan
        
        # Test basic planning
        tasks = plan("Test user input")
        
        if tasks and isinstance(tasks, list):
            print("✅ Planner test successful!")
            print(f"Generated {len(tasks)} tasks")
            return True
        else:
            print("❌ Planner test failed: No tasks generated")
            return False
            
    except Exception as e:
        print(f"❌ Planner test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running CaffiAIne System Tests")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Gemini API Test", test_gemini_api),
        ("Memory System Test", test_memory_system),
        ("Planner Test", test_planner),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the setup and try again.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
