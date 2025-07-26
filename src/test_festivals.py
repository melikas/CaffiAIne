#!/usr/bin/env python3
"""
Test script to verify real-time festival data
"""

import os
import sys
from dotenv import load_dotenv
from real_time_data import get_real_time_festivals
from datetime import datetime

# Load environment variables
load_dotenv()

def test_festival_data():
    """Test the festival data collection"""
    print("🎭 Testing Real-Time Festival Data Collection")
    print("=" * 60)
    
    try:
        # Get real-time festivals
        festivals = get_real_time_festivals()
        
        if not festivals:
            print("❌ No festivals found!")
            return False
        
        print(f"✅ Found {len(festivals)} festivals!")
        print()
        
        # Display festivals
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
        
        # Test categories
        categories = {}
        for festival in festivals:
            cat = festival.get('category', 'other')
            categories[cat] = categories.get(cat, 0) + 1
        
        print("📊 Category Breakdown:")
        for cat, count in categories.items():
            print(f"   {cat.upper()}: {count} festivals")
        
        print()
        print("✅ Festival data collection test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing festival data: {e}")
        return False

def test_current_festivals():
    """Test for currently ongoing festivals"""
    print("\n🎪 Testing for Currently Ongoing Festivals")
    print("=" * 50)
    
    try:
        festivals = get_real_time_festivals()
        current_date = datetime.now()
        
        ongoing_festivals = []
        for festival in festivals:
            try:
                start_date = datetime.fromisoformat(festival['start_date'].replace('Z', '+00:00'))
                end_date = datetime.fromisoformat(festival['end_date'].replace('Z', '+00:00'))
                
                if start_date <= current_date <= end_date:
                    ongoing_festivals.append(festival)
            except:
                continue
        
        if ongoing_festivals:
            print(f"✅ Found {len(ongoing_festivals)} currently ongoing festivals:")
            for festival in ongoing_festivals:
                print(f"   • {festival['name']} at {festival['venue']}")
        else:
            print("ℹ️  No currently ongoing festivals found")
            print("   (This is normal - most festivals are seasonal)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing current festivals: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Montreal Festival Assistant - Data Test Suite")
    print("=" * 60)
    
    # Test festival data
    test1 = test_festival_data()
    
    # Test current festivals
    test2 = test_current_festivals()
    
    print("\n" + "=" * 60)
    if test1 and test2:
        print("🎉 All tests passed! Festival data is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    print("\n💡 Tips:")
    print("- The system now has real Montreal festival data")
    print("- Festivals are categorized by type (music, food, art, etc.)")
    print("- Each festival includes venue, address, and metro information")
    print("- Price ranges and dates are included")

if __name__ == "__main__":
    main() 