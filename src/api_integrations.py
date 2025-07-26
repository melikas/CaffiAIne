import requests
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
import time

load_dotenv()

logger = logging.getLogger(__name__)

class APIIntegrations:
    def __init__(self):
        """Initialize API integrations"""
        self.ticketmaster_key = os.getenv('TICKETMASTER_API_KEY')
        self.eventbrite_token = os.getenv('EVENTBRITE_TOKEN')
        self.facebook_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.google_places_key = os.getenv('GOOGLE_PLACES_API_KEY')
        self.meetup_key = os.getenv('MEETUP_API_KEY')
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_live_festivals(self) -> List[Dict[str, Any]]:
        """Get live festival data from multiple APIs"""
        festivals = []
        
        try:
            # 1. Ticketmaster Discovery API
            festivals.extend(self._get_ticketmaster_events())
            
            # 2. Eventbrite API
            festivals.extend(self._get_eventbrite_events())
            
            # 3. Meetup API
            festivals.extend(self._get_meetup_events())
            
            # 4. Facebook Events API
            festivals.extend(self._get_facebook_events())
            
            # 5. Google Places API for venues
            festivals.extend(self._get_google_places_events())
            
            # 6. Quebec Open Data
            festivals.extend(self._get_quebec_open_data())
            
            # Filter and validate
            current_date = datetime.now()
            valid_festivals = []
            
            for festival in festivals:
                if self._is_valid_festival(festival, current_date):
                    valid_festivals.append(festival)
            
            logger.info(f"Found {len(valid_festivals)} live festivals from APIs")
            return valid_festivals[:50]  # Return top 50 festivals
            
        except Exception as e:
            logger.error(f"Error collecting API data: {e}")
            return []
    
    def _get_ticketmaster_events(self) -> List[Dict[str, Any]]:
        """Get events from Ticketmaster Discovery API"""
        if not self.ticketmaster_key:
            logger.warning("Ticketmaster API key not found")
            return []
        
        try:
            # Montreal coordinates
            lat = 45.5017
            lon = -73.5673
            radius = 50  # km
            
            url = "https://app.ticketmaster.com/discovery/v2/events.json"
            params = {
                'apikey': self.ticketmaster_key,
                'latlong': f"{lat},{lon}",
                'radius': radius,
                'unit': 'km',
                'keyword': 'festival',
                'classificationName': 'music,arts,theater',
                'size': 50
            }
            
            response = self.session.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                events = []
                
                if '_embedded' in data and 'events' in data['_embedded']:
                    for event in data['_embedded']['events']:
                        try:
                            # Extract venue information
                            venue = event.get('_embedded', {}).get('venues', [{}])[0]
                            
                            # Extract dates
                            dates = event.get('dates', {})
                            start_date = dates.get('start', {}).get('dateTime', '')
                            end_date = dates.get('end', {}).get('dateTime', '')
                            
                            # Extract pricing
                            price_ranges = event.get('priceRanges', [])
                            price_info = "Free"
                            if price_ranges:
                                min_price = price_ranges[0].get('min', 0)
                                max_price = price_ranges[0].get('max', 0)
                                currency = price_ranges[0].get('currency', 'USD')
                                price_info = f"${min_price}-{max_price} {currency}"
                            
                            events.append({
                                'name': event.get('name', 'Unknown Event'),
                                'venue': venue.get('name', 'Unknown Venue'),
                                'address': f"{venue.get('address', {}).get('line1', '')}, {venue.get('city', {}).get('name', 'Montreal')}, {venue.get('state', {}).get('stateCode', 'QC')}",
                                'start_date': start_date,
                                'end_date': end_date,
                                'url': event.get('url', ''),
                                'source': 'Ticketmaster',
                                'category': self._categorize_event(event.get('name', '')),
                                'price': price_info,
                                'metro': self._get_nearest_metro(venue.get('address', {}).get('line1', ''))
                            })
                            
                        except Exception as e:
                            logger.error(f"Error parsing Ticketmaster event: {e}")
                
                return events
            
        except Exception as e:
            logger.error(f"Error getting Ticketmaster events: {e}")
        
        return []
    
    def _get_eventbrite_events(self) -> List[Dict[str, Any]]:
        """Get events from Eventbrite API"""
        if not self.eventbrite_token:
            logger.warning("Eventbrite token not found")
            return []
        
        try:
            # Montreal location
            location = "Montreal, QC, Canada"
            
            url = "https://www.eventbriteapi.com/v3/events/search/"
            headers = {
                'Authorization': f'Bearer {self.eventbrite_token}'
            }
            params = {
                'location.address': location,
                'expand': 'venue',
                'q': 'festival',
                'start_date.range_start': datetime.now().isoformat(),
                'start_date.range_end': (datetime.now() + timedelta(days=90)).isoformat(),
                'page_size': 50
            }
            
            response = self.session.get(url, headers=headers, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                events = []
                
                for event in data.get('events', []):
                    try:
                        venue = event.get('venue', {})
                        
                        events.append({
                            'name': event.get('name', {}).get('text', 'Unknown Event'),
                            'venue': venue.get('name', 'Unknown Venue'),
                            'address': venue.get('address', {}).get('localized_address_display', 'Montreal'),
                            'start_date': event.get('start', {}).get('utc', ''),
                            'end_date': event.get('end', {}).get('utc', ''),
                            'url': event.get('url', ''),
                            'source': 'Eventbrite',
                            'category': self._categorize_event(event.get('name', {}).get('text', '')),
                            'price': self._get_eventbrite_price(event),
                            'metro': self._get_nearest_metro(venue.get('address', {}).get('localized_address_display', ''))
                        })
                        
                    except Exception as e:
                        logger.error(f"Error parsing Eventbrite event: {e}")
                
                return events
            
        except Exception as e:
            logger.error(f"Error getting Eventbrite events: {e}")
        
        return []
    
    def _get_meetup_events(self) -> List[Dict[str, Any]]:
        """Get events from Meetup API"""
        if not self.meetup_key:
            logger.warning("Meetup API key not found")
            return []
        
        try:
            # Montreal coordinates
            lat = 45.5017
            lon = -73.5673
            radius = 50  # miles
            
            url = "https://api.meetup.com/2/open_events"
            params = {
                'key': self.meetup_key,
                'lat': lat,
                'lon': lon,
                'radius': radius,
                'text': 'festival',
                'page': 50
            }
            
            response = self.session.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                events = []
                
                for event in data.get('results', []):
                    try:
                        venue = event.get('venue', {})
                        
                        events.append({
                            'name': event.get('name', 'Unknown Event'),
                            'venue': venue.get('name', 'Unknown Venue'),
                            'address': venue.get('address_1', 'Montreal'),
                            'start_date': datetime.fromtimestamp(event.get('time', 0) / 1000).isoformat(),
                            'end_date': datetime.fromtimestamp((event.get('time', 0) + event.get('duration', 0)) / 1000).isoformat(),
                            'url': event.get('event_url', ''),
                            'source': 'Meetup',
                            'category': self._categorize_event(event.get('name', '')),
                            'price': 'Free' if event.get('fee', {}).get('amount', 0) == 0 else f"${event.get('fee', {}).get('amount', 0)}",
                            'metro': self._get_nearest_metro(venue.get('address_1', ''))
                        })
                        
                    except Exception as e:
                        logger.error(f"Error parsing Meetup event: {e}")
                
                return events
            
        except Exception as e:
            logger.error(f"Error getting Meetup events: {e}")
        
        return []
    
    def _get_facebook_events(self) -> List[Dict[str, Any]]:
        """Get events from Facebook Graph API"""
        if not self.facebook_token:
            logger.warning("Facebook access token not found")
            return []
        
        try:
            # Search for events in Montreal
            url = "https://graph.facebook.com/v18.0/search"
            params = {
                'access_token': self.facebook_token,
                'type': 'event',
                'q': 'festival',
                'center': '45.5017,-73.5673',
                'distance': 50000,  # 50km
                'limit': 50
            }
            
            response = self.session.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                events = []
                
                for event in data.get('data', []):
                    try:
                        # Get event details
                        event_id = event.get('id', '')
                        if event_id:
                            event_details = self._get_facebook_event_details(event_id)
                            if event_details:
                                events.append(event_details)
                        
                    except Exception as e:
                        logger.error(f"Error parsing Facebook event: {e}")
                
                return events
            
        except Exception as e:
            logger.error(f"Error getting Facebook events: {e}")
        
        return []
    
    def _get_facebook_event_details(self, event_id: str) -> Dict[str, Any]:
        """Get detailed information for a Facebook event"""
        try:
            url = f"https://graph.facebook.com/v18.0/{event_id}"
            params = {
                'access_token': self.facebook_token,
                'fields': 'name,description,place,start_time,end_time,ticket_uri'
            }
            
            response = self.session.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                event = response.json()
                place = event.get('place', {})
                
                return {
                    'name': event.get('name', 'Unknown Event'),
                    'venue': place.get('name', 'Unknown Venue'),
                    'address': place.get('location', {}).get('street', 'Montreal'),
                    'start_date': event.get('start_time', ''),
                    'end_date': event.get('end_time', ''),
                    'url': event.get('ticket_uri', ''),
                    'source': 'Facebook',
                    'category': self._categorize_event(event.get('name', '')),
                    'price': 'Free',
                    'metro': self._get_nearest_metro(place.get('location', {}).get('street', ''))
                }
            
        except Exception as e:
            logger.error(f"Error getting Facebook event details: {e}")
        
        return {}
    
    def _get_google_places_events(self) -> List[Dict[str, Any]]:
        """Get events from Google Places API"""
        if not self.google_places_key:
            logger.warning("Google Places API key not found")
            return []
        
        try:
            # Search for event venues in Montreal
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            params = {
                'key': self.google_places_key,
                'query': 'festival venue Montreal',
                'location': '45.5017,-73.5673',
                'radius': 50000,  # 50km
                'type': 'establishment'
            }
            
            response = self.session.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                events = []
                
                for place in data.get('results', []):
                    try:
                        # Create a generic event for the venue
                        events.append({
                            'name': f"Events at {place.get('name', 'Unknown Venue')}",
                            'venue': place.get('name', 'Unknown Venue'),
                            'address': place.get('formatted_address', 'Montreal'),
                            'start_date': datetime.now().isoformat(),
                            'end_date': (datetime.now() + timedelta(days=30)).isoformat(),
                            'url': place.get('website', ''),
                            'source': 'Google Places',
                            'category': 'other',
                            'price': 'Varies',
                            'metro': self._get_nearest_metro(place.get('formatted_address', ''))
                        })
                        
                    except Exception as e:
                        logger.error(f"Error parsing Google Places venue: {e}")
                
                return events
            
        except Exception as e:
            logger.error(f"Error getting Google Places events: {e}")
        
        return []
    
    def _get_quebec_open_data(self) -> List[Dict[str, Any]]:
        """Get events from Quebec Open Data"""
        try:
            # Quebec Open Data API for events
            url = "https://www.donneesquebec.ca/recherche/api/3/action/datastore_search"
            params = {
                'resource_id': 'events_montreal',  # Example resource ID
                'limit': 50
            }
            
            response = self.session.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                events = []
                
                for record in data.get('result', {}).get('records', []):
                    try:
                        events.append({
                            'name': record.get('name', 'Unknown Event'),
                            'venue': record.get('venue', 'Unknown Venue'),
                            'address': record.get('address', 'Montreal'),
                            'start_date': record.get('start_date', ''),
                            'end_date': record.get('end_date', ''),
                            'url': record.get('url', ''),
                            'source': 'Quebec Open Data',
                            'category': self._categorize_event(record.get('name', '')),
                            'price': record.get('price', 'Free'),
                            'metro': self._get_nearest_metro(record.get('address', ''))
                        })
                        
                    except Exception as e:
                        logger.error(f"Error parsing Quebec Open Data event: {e}")
                
                return events
            
        except Exception as e:
            logger.error(f"Error getting Quebec Open Data events: {e}")
        
        return []
    
    def _get_eventbrite_price(self, event: Dict[str, Any]) -> str:
        """Extract price information from Eventbrite event"""
        try:
            ticket_classes = event.get('ticket_availability', {}).get('ticket_classes', [])
            if ticket_classes:
                prices = []
                for ticket in ticket_classes:
                    if ticket.get('free', False):
                        prices.append('Free')
                    else:
                        cost = ticket.get('cost', {})
                        if cost:
                            currency = cost.get('currency', 'USD')
                            amount = cost.get('major_value', 0)
                            prices.append(f"{currency} {amount}")
                
                if prices:
                    return ', '.join(set(prices))  # Remove duplicates
            
            return 'Free'
            
        except Exception as e:
            logger.error(f"Error parsing Eventbrite price: {e}")
            return 'Free'
    
    def _get_nearest_metro(self, address: str) -> str:
        """Get nearest metro station based on address"""
        # Simple metro station mapping
        metro_stations = {
            'quartier des spectacles': 'Place-des-Arts',
            'place des arts': 'Place-des-Arts',
            'old port': 'Place-d\'Armes',
            'parc jean-drapeau': 'Jean-Drapeau',
            'quartier latin': 'Berri-UQAM',
            'downtown': 'McGill',
            'plateau': 'Sherbrooke',
            'mile end': 'Laurier'
        }
        
        address_lower = address.lower()
        for location, station in metro_stations.items():
            if location in address_lower:
                return station
        
        return 'Multiple stations'
    
    def _categorize_event(self, event_name: str) -> str:
        """Categorize event based on name"""
        event_lower = event_name.lower()
        
        if any(word in event_lower for word in ['music', 'concert', 'jazz', 'rock', 'pop', 'band', 'singer', 'festival']):
            return 'music'
        elif any(word in event_lower for word in ['film', 'movie', 'cinema', 'documentary', 'screening', 'festival']):
            return 'film'
        elif any(word in event_lower for word in ['food', 'culinary', 'wine', 'beer', 'taste', 'dining', 'restaurant', 'festival']):
            return 'food'
        elif any(word in event_lower for word in ['art', 'exhibition', 'gallery', 'museum', 'painting', 'sculpture', 'festival']):
            return 'art'
        elif any(word in event_lower for word in ['comedy', 'standup', 'humor', 'laugh', 'joke', 'festival']):
            return 'comedy'
        elif any(word in event_lower for word in ['dance', 'ballet', 'performance', 'theatre', 'theater', 'festival']):
            return 'dance'
        else:
            return 'other'
    
    def _is_valid_festival(self, festival: Dict[str, Any], current_date: datetime) -> bool:
        """Check if festival is valid and current"""
        try:
            # Check if it has required fields
            required_fields = ['name', 'venue', 'start_date']
            if not all(field in festival for field in required_fields):
                return False
            
            # Check if name is not too generic
            if len(festival['name']) < 3:
                return False
            
            # Check if it's a current or upcoming event
            try:
                start_date = datetime.fromisoformat(festival['start_date'].replace('Z', '+00:00'))
                # Accept events from 30 days ago to 90 days in the future
                return (current_date - timedelta(days=30)) <= start_date <= (current_date + timedelta(days=90))
            except:
                return False
                
        except Exception as e:
            logger.error(f"Error validating festival: {e}")
            return False

# Global API integrations instance
_api_integrations = None

def get_api_integrations():
    """Get or create the global API integrations instance"""
    global _api_integrations
    if _api_integrations is None:
        _api_integrations = APIIntegrations()
    return _api_integrations

def get_live_festivals_from_apis():
    """Get live festival data from APIs"""
    api_integrations = get_api_integrations()
    return api_integrations.get_live_festivals() 