#!/usr/bin/env python3
"""
Demo script showing real-time festival data collection
"""

import os
import sys
from dotenv import load_dotenv
from festival_service import get_ongoing_festivals
from datetime import datetime
import time

# Load environment variables
load_dotenv()

def demo_real_time_data():
    """Demo the real-time festival data collection"""
    print("🎭 Montreal Festival Assistant - Real-Time Data Demo")
    print("=" * 70)
    
    print("\n📡 Collecting real-time festival data...")
    start_time = time.time()
    
    # Get festivals from all available sources
    festivals = get_ongoing_festivals()
    
    end_time = time.time()
    collection_time = end_time - start_time
    
    print(f"⏱️  Data collection completed in {collection_time:.2f} seconds")
    print(f"📊 Found {len(festivals)} festivals")
    
    if not festivals:
        print("\n❌ No festivals found!")
        print("This could be because:")
        print("- No API keys are configured")
        print("- APIs are not returning data")
        print("- Network connectivity issues")
        return
    
    # Display festivals by category
    categories = {}
    for festival in festivals:
        cat = festival.get('category', 'other')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(festival)
    
    print(f"\n📋 Festivals by Category:")
    for category, events in categories.items():
        print(f"\n🎭 {category.upper()} ({len(events)} events):")
        for event in events:
            print(f"   • {event['name']}")
            print(f"     📍 {event['venue']}")
            print(f"     💰 {event.get('price', 'N/A')}")
            print(f"     📊 Source: {event['source']}")
    
    # Show sample detailed festival
    if festivals:
        print(f"\n🎪 Sample Festival Details:")
        sample = festivals[0]
        print(f"   Name: {sample['name']}")
        print(f"   Venue: {sample['venue']}")
        print(f"   Address: {sample['address']}")
        print(f"   Dates: {sample['start_date']} to {sample['end_date']}")
        print(f"   Category: {sample.get('category', 'N/A').upper()}")
        print(f"   Price: {sample.get('price', 'N/A')}")
        print(f"   Metro: {sample.get('metro', 'N/A')}")
        print(f"   Info: {sample['url']}")
        print(f"   Source: {sample['source']}")

def demo_search_functionality():
    """Demo the search functionality"""
    print("\n🔍 Demo Search Functionality")
    print("=" * 40)
    
    # Simulate user searches
    search_queries = [
        "music festivals",
        "food events",
        "art exhibitions",
        "comedy shows",
        "dance performances"
    ]
    
    festivals = get_ongoing_festivals()
    
    for query in search_queries:
        print(f"\n🔎 Searching for: '{query}'")
        
        # Simple search simulation
        matching_festivals = []
        query_lower = query.lower()
        
        for festival in festivals:
            festival_name = festival['name'].lower()
            festival_category = festival.get('category', '').lower()
            
            if (query_lower in festival_name or 
                query_lower in festival_category or
                any(word in festival_name for word in query_lower.split())):
                matching_festivals.append(festival)
        
        if matching_festivals:
            print(f"   ✅ Found {len(matching_festivals)} matching festivals:")
            for festival in matching_festivals[:3]:  # Show top 3
                print(f"      • {festival['name']} ({festival.get('category', 'N/A')})")
        else:
            print(f"   ❌ No festivals found for '{query}'")

def demo_api_status():
    """Show API status and recommendations"""
    print("\n🔌 API Status & Recommendations")
    print("=" * 40)
    
    api_keys = {
        'Ticketmaster': os.getenv('TICKETMASTER_API_KEY'),
        'Eventbrite': os.getenv('EVENTBRITE_TOKEN'),
        'Meetup': os.getenv('MEETUP_API_KEY'),
        'Facebook': os.getenv('FACEBOOK_ACCESS_TOKEN'),
        'Google Places': os.getenv('GOOGLE_PLACES_API_KEY')
    }
    
    configured_apis = [name for name, key in api_keys.items() if key]
    
    if configured_apis:
        print("✅ Configured APIs:")
        for api in configured_apis:
            print(f"   • {api}")
    else:
        print("❌ No external APIs configured")
        print("   The system is using fallback data")
    
    print(f"\n💡 To get real-time data, configure these APIs:")
    print("   • Ticketmaster Discovery API")
    print("   • Eventbrite API")
    print("   • Meetup API")
    print("   • Facebook Graph API")
    print("   • Google Places API")
    print("\n📖 See api_setup_guide.md for detailed setup instructions")

def main():
    """Run the demo"""
    print("🎭 Montreal Festival Assistant - Real-Time Data Demo")
    print("=" * 70)
    
    # Demo 1: Real-time data collection
    demo_real_time_data()
    
    # Demo 2: Search functionality
    demo_search_functionality()
    
    # Demo 3: API status
    demo_api_status()
    
    print("\n" + "=" * 70)
    print("🎉 Demo Complete!")
    print("\n💡 Next Steps:")
    print("   1. Set up API keys for real-time data")
    print("   2. Run the main application: python main.py")
    print("   3. Test the full festival assistant")
    
    print("\n🔗 Useful Links:")
    print("   • API Setup Guide: api_setup_guide.md")
    print("   • Test API Connections: python test_api_connections.py")
    print("   • Main Application: python main.py")

if __name__ == "__main__":
    main() 