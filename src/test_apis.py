#!/usr/bin/env python3
"""
Test script for Montreal Festival Assistant APIs
"""

import os
import sys
from dotenv import load_dotenv
from festival_service import get_festival_service

# Load environment variables
load_dotenv()

def test_api_keys():
    """Test if API keys are properly configured"""
    print("🔑 Testing API Key Configuration")
    print("=" * 50)
    
    # Check Google Gemini API
    google_key = os.getenv('GOOGLE_API_KEY')
    if google_key:
        print("✅ Google Gemini API key found")
    else:
        print("❌ Google Gemini API key missing")
    
    # Check Eventbrite API
    eventbrite_key = os.getenv('EVENTBRITE_TOKEN')
    if eventbrite_key:
        print("✅ Eventbrite API token found")
    else:
        print("⚠️  Eventbrite API token missing (optional)")
    
    # Check Ticketmaster API
    ticketmaster_key = os.getenv('TICKETMASTER_KEY')
    if ticketmaster_key:
        print("✅ Ticketmaster API key found")
    else:
        print("⚠️  Ticketmaster API key missing (optional)")
    
    # Check Montreal API
    montreal_key = os.getenv('MONTREAL_API_KEY')
    if montreal_key:
        print("✅ Montreal API key found")
    else:
        print("⚠️  Montreal API key missing (optional)")
    
    print()

def test_festival_service():
    """Test the festival service functionality"""
    print("🎭 Testing Festival Service")
    print("=" * 50)
    
    try:
        service = get_festival_service()
        festivals = service.get_ongoing_festivals()
        
        if festivals:
            print(f"✅ Found {len(festivals)} festivals")
            print("\n📋 Available Festivals:")
            for i, festival in enumerate(festivals, 1):
                print(f"{i}. {festival['name']} - {festival['venue']}")
        else:
            print("⚠️  No festivals found (using fallback data)")
            
    except Exception as e:
        print(f"❌ Error testing festival service: {e}")
    
    print()

def test_api_connections():
    """Test actual API connections"""
    print("🌐 Testing API Connections")
    print("=" * 50)
    
    service = get_festival_service()
    
    # Test Eventbrite
    if service.eventbrite_token:
        try:
            festivals = service._get_eventbrite_festivals()
            print(f"✅ Eventbrite API: {len(festivals)} festivals found")
        except Exception as e:
            print(f"❌ Eventbrite API error: {e}")
    else:
        print("⚠️  Eventbrite API not configured")
    
    # Test Ticketmaster
    if service.ticketmaster_key:
        try:
            festivals = service._get_ticketmaster_festivals()
            print(f"✅ Ticketmaster API: {len(festivals)} festivals found")
        except Exception as e:
            print(f"❌ Ticketmaster API error: {e}")
    else:
        print("⚠️  Ticketmaster API not configured")
    
    # Test Local Data
    try:
        festivals = service._get_montreal_local_festivals()
        print(f"✅ Local Data: {len(festivals)} festivals available")
    except Exception as e:
        print(f"❌ Local data error: {e}")
    
    print()

def main():
    """Run all API tests"""
    print("🧪 Montreal Festival Assistant - API Test Suite")
    print("=" * 60)
    
    # Test API keys
    test_api_keys()
    
    # Test festival service
    test_festival_service()
    
    # Test API connections
    test_api_connections()
    
    print("🎉 API testing completed!")
    print("\n💡 Tips:")
    print("- Make sure your .env file is in the src directory")
    print("- Check that your API keys are correct")
    print("- Some APIs may require registration and approval")
    print("- The system will work with just the Google Gemini API")

if __name__ == "__main__":
    main() 