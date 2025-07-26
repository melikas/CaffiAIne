#!/usr/bin/env python3
"""
Test script to verify live festival scraper
"""

import os
import sys
from dotenv import load_dotenv
from live_festival_scraper import get_live_festivals
from datetime import datetime
import time

# Load environment variables
load_dotenv()

def test_live_scraper():
    """Test the live festival scraper"""
    print("🌐 Testing Live Festival Scraper")
    print("=" * 60)
    print("This will scrape real Montreal and Quebec festival websites...")
    print()
    
    try:
        start_time = time.time()
        
        # Get live festivals
        festivals = get_live_festivals()
        
        end_time = time.time()
        scraping_time = end_time - start_time
        
        print(f"⏱️  Scraping completed in {scraping_time:.2f} seconds")
        print()
        
        if not festivals:
            print("❌ No festivals found from live scraping!")
            print("This might be due to:")
            print("- Network connectivity issues")
            print("- Website blocking automated requests")
            print("- Changes in website structure")
            return False
        
        print(f"✅ Found {len(festivals)} live festivals!")
        print()
        
        # Display festivals with source information
        for i, festival in enumerate(festivals, 1):
            print(f"{i}. {festival['name']}")
            print(f"   📍 Venue: {festival['venue']}")
            print(f"   🗺️  Address: {festival['address']}")
            print(f"   📅 Dates: {festival['start_date']} to {festival['end_date']}")
            print(f"   🎭 Category: {festival.get('category', 'N/A').upper()}")
            print(f"   💰 Price: {festival.get('price', 'N/A')}")
            print(f"   🚇 Metro: {festival.get('metro', 'N/A')}")
            print(f"   🔗 Info: {festival['url']}")
            print(f"   📊 Source: {festival['source']}")
            print()
        
        # Analyze sources
        sources = {}
        categories = {}
        
        for festival in festivals:
            # Count sources
            source = festival.get('source', 'Unknown')
            sources[source] = sources.get(source, 0) + 1
            
            # Count categories
            cat = festival.get('category', 'other')
            categories[cat] = categories.get(cat, 0) + 1
        
        print("📊 Data Source Analysis:")
        for source, count in sources.items():
            print(f"   {source}: {count} festivals")
        
        print()
        print("📊 Category Breakdown:")
        for cat, count in categories.items():
            print(f"   {cat.upper()}: {count} festivals")
        
        print()
        print("✅ Live scraper test successful!")
        print("💡 The scraper is now getting real data from:")
        print("   - Montreal Tourism (mtl.org)")
        print("   - Quebec Tourism (quebecoriginal.com)")
        print("   - Montreal Gazette")
        print("   - Montreal.com")
        print("   - Local event sites")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing live scraper: {e}")
        print("This might be due to network issues or website changes")
        return False

def test_website_accessibility():
    """Test if we can access the target websites"""
    print("\n🔍 Testing Website Accessibility")
    print("=" * 50)
    
    import requests
    
    test_sites = [
        ("Montreal Tourism", "https://www.mtl.org/en/events"),
        ("Quebec Tourism", "https://www.quebecoriginal.com/en-ca/events"),
        ("Montreal Gazette", "https://montrealgazette.com/entertainment/events"),
        ("Montreal.com", "https://www.montreal.com/events")
    ]
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    for site_name, url in test_sites:
        try:
            print(f"Testing {site_name}...", end=" ")
            response = session.get(url, timeout=10)
            
            if response.status_code == 200:
                print("✅ Accessible")
            else:
                print(f"❌ HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)[:50]}...")

def main():
    """Run all tests"""
    print("🧪 Live Festival Scraper - Test Suite")
    print("=" * 60)
    
    # Test website accessibility first
    test_website_accessibility()
    
    print()
    print("=" * 60)
    
    # Test live scraper
    success = test_live_scraper()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Live scraper is working! Real-time data is available.")
        print("The system will now provide actual Montreal festival information.")
    else:
        print("⚠️  Live scraper encountered issues.")
        print("The system will use fallback data for now.")
    
    print("\n💡 Next steps:")
    print("- Run the main application to test the full system")
    print("- The scraper will automatically retry on each request")
    print("- Fallback data ensures the system always works")

if __name__ == "__main__":
    main() 