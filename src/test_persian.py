#!/usr/bin/env python3
"""
Test Persian/Farsi input functionality
"""

from main import MontrealFestivalAssistant

def test_persian_input():
    """Test Persian input functionality"""
    print("🧪 Testing Persian/Farsi Input")
    print("=" * 40)
    
    assistant = MontrealFestivalAssistant()
    
    # Test Persian inputs
    test_inputs = [
        "موزیک امشب",
        "موسیقی امشب",
        "غذا امشب",
        "کمدی امشب",
        "هنر امشب",
        "music tonight",
        "food tonight",
        "comedy tonight"
    ]
    
    for user_input in test_inputs:
        print(f"\n🔍 Testing: '{user_input}'")
        result = assistant.process_user_input(user_input)
        
        festivals_found = result.get('festivals_found', 0)
        print(f"Found: {festivals_found} festivals")
        
        if festivals_found > 0:
            matching_festivals = result.get('matching_festivals', [])
            for festival in matching_festivals:
                print(f"  ✅ {festival['name']} ({festival.get('category', 'N/A')})")
        else:
            print("  ❌ No festivals found")

if __name__ == "__main__":
    test_persian_input() 