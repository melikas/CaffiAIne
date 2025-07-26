#!/usr/bin/env python3
"""
Quick test to verify festival search functionality
"""

from festival_service import get_ongoing_festivals
from main import MontrealFestivalAssistant

def test_festival_search():
    """Test the festival search functionality"""
    print("🧪 Testing Festival Search Functionality")
    print("=" * 50)
    
    # Get festivals
    festivals = get_ongoing_festivals()
    print(f"📊 Total festivals available: {len(festivals)}")
    
    if festivals:
        print("\n📋 Available Festivals:")
        for i, festival in enumerate(festivals, 1):
            print(f"{i}. {festival['name']} ({festival.get('category', 'N/A')})")
    
    # Test search functionality
    assistant = MontrealFestivalAssistant()
    
    # Test different searches
    test_searches = [
        "music festivals",
        "food events",
        "art exhibitions",
        "comedy shows"
    ]
    
    print("\n🔍 Testing Search Results:")
    for search_query in test_searches:
        print(f"\nSearching for: '{search_query}'")
        result = assistant.process_user_input(search_query)
        
        festivals_found = result.get('festivals_found', 0)
        print(f"Found: {festivals_found} festivals")
        
        if festivals_found > 0:
            matching_festivals = result.get('matching_festivals', [])
            for festival in matching_festivals:
                print(f"  • {festival['name']} ({festival.get('category', 'N/A')})")

if __name__ == "__main__":
    test_festival_search() 