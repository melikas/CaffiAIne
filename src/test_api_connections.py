#!/usr/bin/env python3
"""
Test script to verify API connections for real-time festival data
"""

import os
import sys
from dotenv import load_dotenv
from api_integrations import get_api_integrations
from datetime import datetime
import time

# Load environment variables
load_dotenv()

def test_api_connections():
    """Test all API connections"""
    print("🔌 Testing API Connections for Real-Time Festival Data")
    print("=" * 70)
    
    api = get_api_integrations()
    results = {}
    
    # Test Ticketmaster API
    print("\n🎫 Testing Ticketmaster Discovery API...")
    try:
        ticketmaster_events = api._get_ticketmaster_events()
        results['Ticketmaster'] = {
            'status': '✅ Working',
            'events_found': len(ticketmaster_events),
            'sample_events': ticketmaster_events[:3] if ticketmaster_events else []
        }
        print(f"   ✅ Found {len(ticketmaster_events)} events")
    except Exception as e:
        results['Ticketmaster'] = {
            'status': '❌ Failed',
            'error': str(e),
            'events_found': 0
        }
        print(f"   ❌ Error: {str(e)[:50]}...")
    
    # Test Eventbrite API
    print("\n🎪 Testing Eventbrite API...")
    try:
        eventbrite_events = api._get_eventbrite_events()
        results['Eventbrite'] = {
            'status': '✅ Working',
            'events_found': len(eventbrite_events),
            'sample_events': eventbrite_events[:3] if eventbrite_events else []
        }
        print(f"   ✅ Found {len(eventbrite_events)} events")
    except Exception as e:
        results['Eventbrite'] = {
            'status': '❌ Failed',
            'error': str(e),
            'events_found': 0
        }
        print(f"   ❌ Error: {str(e)[:50]}...")
    
    # Test Meetup API
    print("\n👥 Testing Meetup API...")
    try:
        meetup_events = api._get_meetup_events()
        results['Meetup'] = {
            'status': '✅ Working',
            'events_found': len(meetup_events),
            'sample_events': meetup_events[:3] if meetup_events else []
        }
        print(f"   ✅ Found {len(meetup_events)} events")
    except Exception as e:
        results['Meetup'] = {
            'status': '❌ Failed',
            'error': str(e),
            'events_found': 0
        }
        print(f"   ❌ Error: {str(e)[:50]}...")
    
    # Test Facebook API
    print("\n📘 Testing Facebook Graph API...")
    try:
        facebook_events = api._get_facebook_events()
        results['Facebook'] = {
            'status': '✅ Working',
            'events_found': len(facebook_events),
            'sample_events': facebook_events[:3] if facebook_events else []
        }
        print(f"   ✅ Found {len(facebook_events)} events")
    except Exception as e:
        results['Facebook'] = {
            'status': '❌ Failed',
            'error': str(e),
            'events_found': 0
        }
        print(f"   ❌ Error: {str(e)[:50]}...")
    
    # Test Google Places API
    print("\n🗺️  Testing Google Places API...")
    try:
        google_events = api._get_google_places_events()
        results['Google Places'] = {
            'status': '✅ Working',
            'events_found': len(google_events),
            'sample_events': google_events[:3] if google_events else []
        }
        print(f"   ✅ Found {len(google_events)} venues")
    except Exception as e:
        results['Google Places'] = {
            'status': '❌ Failed',
            'error': str(e),
            'events_found': 0
        }
        print(f"   ❌ Error: {str(e)[:50]}...")
    
    # Test Quebec Open Data
    print("\n🇨🇦 Testing Quebec Open Data...")
    try:
        quebec_events = api._get_quebec_open_data()
        results['Quebec Open Data'] = {
            'status': '✅ Working',
            'events_found': len(quebec_events),
            'sample_events': quebec_events[:3] if quebec_events else []
        }
        print(f"   ✅ Found {len(quebec_events)} events")
    except Exception as e:
        results['Quebec Open Data'] = {
            'status': '❌ Failed',
            'error': str(e),
            'events_found': 0
        }
        print(f"   ❌ Error: {str(e)[:50]}...")
    
    return results

def test_combined_data():
    """Test the combined API data collection"""
    print("\n🌐 Testing Combined API Data Collection...")
    print("=" * 50)
    
    try:
        start_time = time.time()
        
        # Get combined data from all APIs
        api = get_api_integrations()
        all_events = api.get_live_festivals()
        
        end_time = time.time()
        collection_time = end_time - start_time
        
        print(f"⏱️  Data collection completed in {collection_time:.2f} seconds")
        print(f"📊 Total events found: {len(all_events)}")
        
        if all_events:
            print("\n📋 Sample Events:")
            for i, event in enumerate(all_events[:5], 1):
                print(f"   {i}. {event['name']}")
                print(f"      📍 {event['venue']}")
                print(f"      🎭 {event.get('category', 'N/A').upper()}")
                print(f"      📊 Source: {event['source']}")
                print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing combined data: {e}")
        return False

def check_api_keys():
    """Check which API keys are configured"""
    print("\n🔑 Checking API Key Configuration")
    print("=" * 40)
    
    api_keys = {
        'Ticketmaster': os.getenv('TICKETMASTER_API_KEY'),
        'Eventbrite': os.getenv('EVENTBRITE_TOKEN'),
        'Meetup': os.getenv('MEETUP_API_KEY'),
        'Facebook': os.getenv('FACEBOOK_ACCESS_TOKEN'),
        'Google Places': os.getenv('GOOGLE_PLACES_API_KEY'),
        'Google Gemini': os.getenv('GOOGLE_API_KEY')
    }
    
    for api_name, key in api_keys.items():
        if key:
            print(f"   ✅ {api_name}: Configured")
        else:
            print(f"   ❌ {api_name}: Not configured")
    
    configured_count = sum(1 for key in api_keys.values() if key)
    total_count = len(api_keys)
    
    print(f"\n📊 API Key Status: {configured_count}/{total_count} configured")
    
    if configured_count == 0:
        print("\n⚠️  No API keys configured!")
        print("Please set up your API keys in the .env file")
        print("See api_setup_guide.md for detailed instructions")
    elif configured_count < total_count:
        print(f"\nℹ️  {total_count - configured_count} API keys missing")
        print("The system will work with available APIs")
    else:
        print("\n🎉 All API keys configured!")

def main():
    """Run all API tests"""
    print("🧪 API Connection Test Suite")
    print("=" * 70)
    
    # Check API keys
    check_api_keys()
    
    # Test individual API connections
    results = test_api_connections()
    
    # Test combined data collection
    combined_success = test_combined_data()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 API Test Results Summary")
    print("=" * 70)
    
    working_apis = 0
    total_events = 0
    
    for api_name, result in results.items():
        status = result['status']
        events = result['events_found']
        print(f"{api_name}: {status} ({events} events)")
        
        if '✅' in status:
            working_apis += 1
        total_events += events
    
    print(f"\n📈 Overall Results:")
    print(f"   Working APIs: {working_apis}/{len(results)}")
    print(f"   Total Events Found: {total_events}")
    
    if combined_success:
        print("   Combined Data Collection: ✅ Working")
    else:
        print("   Combined Data Collection: ❌ Failed")
    
    print("\n💡 Recommendations:")
    if working_apis == 0:
        print("   - Set up at least one API key for real-time data")
        print("   - See api_setup_guide.md for setup instructions")
    elif working_apis < len(results):
        print("   - Consider adding more API keys for better coverage")
        print("   - The system will work with available APIs")
    else:
        print("   - All APIs working! You have comprehensive data coverage")
    
    print("\n🚀 Next Steps:")
    print("   - Run the main application to test the full system")
    print("   - The system will use available APIs for real-time data")

if __name__ == "__main__":
    main() 