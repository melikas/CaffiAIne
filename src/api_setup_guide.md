# API Setup Guide for Montreal Festival Assistant

This guide will help you set up all the required API keys to get real-time festival data from multiple sources.

## Required API Keys

### 1. Ticketmaster Discovery API
**Purpose**: Get live event data from Ticketmaster
**URL**: https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/

**Setup Steps**:
1. Go to https://developer.ticketmaster.com/
2. Create an account or sign in
3. Navigate to "My Apps" and create a new application
4. Get your API key from the application dashboard
5. Add to your `.env` file: `TICKETMASTER_API_KEY=your_api_key_here`

### 2. Eventbrite API
**Purpose**: Get event data from Eventbrite
**URL**: https://www.eventbrite.com/platform/api/

**Setup Steps**:
1. Go to https://www.eventbrite.com/platform/api-keys
2. Create an account or sign in
3. Generate a private token
4. Add to your `.env` file: `EVENTBRITE_TOKEN=your_token_here`

### 3. Meetup API
**Purpose**: Get event data from Meetup
**URL**: https://www.meetup.com/api/

**Setup Steps**:
1. Go to https://www.meetup.com/api/oauth/list/
2. Create an account or sign in
3. Register your application
4. Get your API key
5. Add to your `.env` file: `MEETUP_API_KEY=your_api_key_here`

### 4. Facebook Graph API
**Purpose**: Get event data from Facebook
**URL**: https://developers.facebook.com/docs/graph-api/

**Setup Steps**:
1. Go to https://developers.facebook.com/
2. Create an account or sign in
3. Create a new app
4. Add the "Events" permission
5. Generate an access token
6. Add to your `.env` file: `FACEBOOK_ACCESS_TOKEN=your_token_here`

### 5. Google Places API
**Purpose**: Get venue and location data
**URL**: https://developers.google.com/maps/documentation/places/web-service/overview

**Setup Steps**:
1. Go to https://console.cloud.google.com/
2. Create a project or select existing one
3. Enable the Places API
4. Create credentials (API key)
5. Add to your `.env` file: `GOOGLE_PLACES_API_KEY=your_api_key_here`

## Environment File Setup

Create a `.env` file in your project root with all the API keys:

```env
# Google Gemini API (required for AI responses)
GOOGLE_API_KEY=your_gemini_api_key_here

# Ticketmaster API
TICKETMASTER_API_KEY=your_ticketmaster_api_key_here

# Eventbrite API
EVENTBRITE_TOKEN=your_eventbrite_token_here

# Meetup API
MEETUP_API_KEY=your_meetup_api_key_here

# Facebook Graph API
FACEBOOK_ACCESS_TOKEN=your_facebook_token_here

# Google Places API
GOOGLE_PLACES_API_KEY=your_google_places_api_key_here
```

## API Rate Limits and Costs

### Ticketmaster Discovery API
- **Rate Limit**: 5000 requests per day
- **Cost**: Free tier available
- **Data**: Live event data, pricing, venue information

### Eventbrite API
- **Rate Limit**: 2000 requests per hour
- **Cost**: Free for basic usage
- **Data**: Event details, pricing, registration info

### Meetup API
- **Rate Limit**: 200 requests per hour
- **Cost**: Free
- **Data**: Local events and meetups

### Facebook Graph API
- **Rate Limit**: 200 requests per hour
- **Cost**: Free for basic usage
- **Data**: Public events and venue information

### Google Places API
- **Rate Limit**: 1000 requests per day (free tier)
- **Cost**: $0.017 per 1000 requests after free tier
- **Data**: Venue details, location information

## Testing API Connections

Run the test script to verify your API connections:

```bash
python test_api_connections.py
```

This will test each API and show you which ones are working.

## Security Notes

1. **Never commit your `.env` file** to version control
2. **Keep your API keys secure** and don't share them
3. **Monitor your API usage** to avoid unexpected charges
4. **Use environment variables** in production deployments

## Troubleshooting

### Common Issues:

1. **API Key Not Found**: Make sure your `.env` file is in the project root
2. **Rate Limit Exceeded**: Wait and try again later
3. **Authentication Failed**: Check your API key format
4. **No Data Returned**: Some APIs may not have events in your area

### Testing Individual APIs:

You can test each API individually:

```python
from api_integrations import get_api_integrations

api = get_api_integrations()

# Test Ticketmaster
ticketmaster_events = api._get_ticketmaster_events()
print(f"Found {len(ticketmaster_events)} Ticketmaster events")

# Test Eventbrite
eventbrite_events = api._get_eventbrite_events()
print(f"Found {len(eventbrite_events)} Eventbrite events")
```

## Data Sources Summary

The system will now get real-time data from:

1. **Ticketmaster** - Major events and concerts
2. **Eventbrite** - Local events and festivals
3. **Meetup** - Community events and meetups
4. **Facebook** - Social events and gatherings
5. **Google Places** - Venue and location data
6. **Quebec Open Data** - Government event data

This provides comprehensive coverage of Montreal's festival and event scene with real-time, accurate information. 