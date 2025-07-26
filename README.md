# 🎭 Montreal Festival Assistant

A real-time festival information system that provides live data about Montreal festivals, events, and cultural activities. The system integrates multiple APIs to deliver accurate, up-to-date information about festivals, including venue details, pricing, directions, and cost estimations.

## 🌟 Features

### Real-Time Data Collection
- **Ticketmaster Discovery API** - Major events and concerts
- **Eventbrite API** - Local events and festivals  
- **Meetup API** - Community events and meetups
- **Facebook Graph API** - Social events and gatherings
- **Google Places API** - Venue and location data
- **Quebec Open Data** - Government event data

### Smart Search & Filtering
- **Category-based search** (Music, Food, Art, Comedy, Dance, Film)
- **Date and time filtering** (Today, Tomorrow, specific days)
- **Location-based results** (Montreal area)
- **Price range filtering**

### Comprehensive Information
- **Festival names and descriptions**
- **Exact venue addresses**
- **Google Maps integration** for directions
- **Cost estimations** (tickets, transport, food)
- **Metro station information**
- **Real-time pricing** from multiple sources

### User-Friendly Interface
- **Interactive console UI** with menus
- **Calendar-style date selection**
- **Category-based browsing**
- **Quick search functionality**

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd src
pip install -r requirements.txt
```

### 2. Set Up API Keys (Optional)
For real-time data, create a `.env` file in the project root:

```env
# Required for AI responses
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional - for real-time data
TICKETMASTER_API_KEY=your_ticketmaster_api_key_here
EVENTBRITE_TOKEN=your_eventbrite_token_here
MEETUP_API_KEY=your_meetup_api_key_here
FACEBOOK_ACCESS_TOKEN=your_facebook_token_here
GOOGLE_PLACES_API_KEY=your_google_places_api_key_here
```

### 3. Run the Application
```bash
cd src
python main.py
```

### 4. Test API Connections
```bash
python test_api_connections.py
```

### 5. View Demo
```bash
python demo_with_real_data.py
```

## 📋 API Setup Guide

For detailed instructions on setting up each API, see:
- [API Setup Guide](src/api_setup_guide.md)

### Available APIs:
1. **Ticketmaster Discovery API** - Free tier, 5000 requests/day
2. **Eventbrite API** - Free tier, 2000 requests/hour  
3. **Meetup API** - Free, 200 requests/hour
4. **Facebook Graph API** - Free tier, 200 requests/hour
5. **Google Places API** - Free tier, 1000 requests/day

## 🎯 Usage Examples

### Search by Category
```
Input: "music festivals"
Output: 
🎵 Montreal Jazz Festival
📍 Quartier des Spectacles, Montreal
🗺️ Google Maps: https://maps.google.com/...
💰 Cost: $25-150 CAD (tickets) + $10-20 CAD (transport)
```

### Search by Date
```
Input: "food events tomorrow"
Output:
🍽️ Montreal Food Festival  
📍 Old Port of Montreal
🗺️ Google Maps: https://maps.google.com/...
💰 Cost: $20-80 CAD (tickets) + $8-15 CAD (transport)
```

### Search by Time
```
Input: "art exhibitions evening"
Output:
🎨 Montreal Art Festival
📍 Place des Arts, Montreal
🗺️ Google Maps: https://maps.google.com/...
💰 Cost: $15-50 CAD (tickets) + $5-10 CAD (metro)
```

## 🏗️ System Architecture

### Core Components

1. **API Integrations** (`api_integrations.py`)
   - Real-time data collection from multiple sources
   - Error handling and fallback mechanisms
   - Data validation and filtering

2. **Festival Service** (`festival_service.py`)
   - Centralized festival data management
   - Search and filtering logic
   - Fallback data when APIs unavailable

3. **Main Application** (`main.py`)
   - User interface and interaction
   - Search processing and result formatting
   - Integration with AI for enhanced responses

4. **UI Helper** (`ui_helper.py`)
   - Console-based user interface
   - Menu system and navigation
   - Result display formatting

### Data Flow

```
User Input → Main App → Festival Service → API Integrations
                ↓
            AI Processing → Formatted Response → User
```

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY` - Required for AI responses
- `TICKETMASTER_API_KEY` - Optional, for live event data
- `EVENTBRITE_TOKEN` - Optional, for local events
- `MEETUP_API_KEY` - Optional, for community events
- `FACEBOOK_ACCESS_TOKEN` - Optional, for social events
- `GOOGLE_PLACES_API_KEY` - Optional, for venue data

### Fallback System
When APIs are unavailable or not configured, the system uses:
- Curated Montreal festival database
- Major festivals (Jazz Fest, Osheaga, etc.)
- Basic venue and pricing information

## 📊 Data Sources

### Real-Time APIs
- **Ticketmaster** - Major concerts and events
- **Eventbrite** - Local festivals and activities
- **Meetup** - Community gatherings
- **Facebook** - Social events
- **Google Places** - Venue information
- **Quebec Open Data** - Government events

### Fallback Data
- Montreal Jazz Festival
- Osheaga Music Festival
- Just for Laughs Comedy Festival
- Montreal International Film Festival
- Montreal Food Festival

## 🧪 Testing

### Test API Connections
```bash
python test_api_connections.py
```

### Test Festival Data
```bash
python test_festivals.py
```

### Test Live Scraper
```bash
python test_live_scraper.py
```

### Demo Application
```bash
python demo_with_real_data.py
```

## 📈 Performance

### Response Times
- **API Data**: 2-5 seconds (depending on API response)
- **Fallback Data**: <1 second
- **AI Processing**: 1-3 seconds

### Data Accuracy
- **Real-time APIs**: Live data from official sources
- **Fallback Data**: Curated, verified information
- **AI Enhancement**: Context-aware responses

## 🔒 Security

- API keys stored in environment variables
- No sensitive data in code
- Rate limiting and error handling
- Secure API authentication

## 🚀 Deployment

### Local Development
```bash
git clone <repository>
cd CaffiAIne/src
pip install -r requirements.txt
python main.py
```

### Production
- Set up all required API keys
- Configure environment variables
- Monitor API usage and costs
- Implement proper error handling

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the [API Setup Guide](src/api_setup_guide.md)
2. Run the test scripts to diagnose issues
3. Review the demo for usage examples

## 🎉 What's New

### Latest Updates
- ✅ Real-time API integrations
- ✅ Comprehensive festival database
- ✅ Interactive console UI
- ✅ AI-powered responses
- ✅ Google Maps integration
- ✅ Cost estimation features
- ✅ Metro station information
- ✅ Category-based search

The Montreal Festival Assistant now provides **real-time, accurate festival information** with comprehensive coverage of Montreal's vibrant cultural scene! 🎭


