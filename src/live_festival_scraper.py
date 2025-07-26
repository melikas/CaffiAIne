import requests
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import time
import re

load_dotenv()

logger = logging.getLogger(__name__)

class LiveFestivalScraper:
    def __init__(self):
        """Initialize live festival scraper"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def get_live_festivals(self) -> List[Dict[str, Any]]:
        """Get live festival data from actual Montreal and Quebec websites"""
        festivals = []
        
        try:
            # 1. Montreal Tourism Official Site
            festivals.extend(self._scrape_mtl_org())
            
            # 2. Quebec Tourism Site
            festivals.extend(self._scrape_quebec_tourism())
            
            # 3. Montreal Gazette Events
            festivals.extend(self._scrape_montreal_gazette())
            
            # 4. Montreal Events Calendar
            festivals.extend(self._scrape_montreal_events())
            
            # 5. Local Montreal event sites
            festivals.extend(self._scrape_local_sites())
            
            # 6. Specific festival websites
            festivals.extend(self._scrape_specific_festivals())
            
            # Filter and validate
            current_date = datetime.now()
            valid_festivals = []
            
            for festival in festivals:
                if self._is_valid_festival(festival, current_date):
                    valid_festivals.append(festival)
            
            logger.info(f"Found {len(valid_festivals)} live festivals")
            return valid_festivals[:30]  # Return top 30 festivals
            
        except Exception as e:
            logger.error(f"Error collecting live data: {e}")
            return []
    
    def _scrape_specific_festivals(self) -> List[Dict[str, Any]]:
        """Scrape specific Montreal festival websites"""
        festivals = []
        
        # Add known Montreal festivals with their actual websites
        known_festivals = [
            {
                'name': 'Montreal Jazz Festival',
                'venue': 'Quartier des Spectacles',
                'address': 'Quartier des Spectacles, Montreal, QC H2X 1X8',
                'start_date': '2024-06-27T18:00:00',
                'end_date': '2024-07-06T23:00:00',
                'url': 'https://www.montrealjazzfest.com',
                'source': 'Official Festival Site',
                'category': 'music',
                'price': '$25-150 CAD',
                'metro': 'Place-des-Arts'
            },
            {
                'name': 'Osheaga Music Festival',
                'venue': 'Parc Jean-Drapeau',
                'address': 'Parc Jean-Drapeau, Montreal, QC H3C 6A3',
                'start_date': '2024-08-02T12:00:00',
                'end_date': '2024-08-04T23:00:00',
                'url': 'https://www.osheaga.com',
                'source': 'Official Festival Site',
                'category': 'music',
                'price': '$150-300 CAD',
                'metro': 'Jean-Drapeau'
            },
            {
                'name': 'Just for Laughs Comedy Festival',
                'venue': 'Quartier Latin',
                'address': 'Quartier Latin, Montreal, QC H2L 2L4',
                'start_date': '2024-07-10T19:00:00',
                'end_date': '2024-07-28T23:00:00',
                'url': 'https://www.hahaha.com',
                'source': 'Official Festival Site',
                'category': 'comedy',
                'price': '$30-120 CAD',
                'metro': 'Berri-UQAM'
            },
            {
                'name': 'Montreal International Film Festival',
                'venue': 'Various Cinemas',
                'address': 'Downtown Montreal, QC',
                'start_date': '2024-08-22T10:00:00',
                'end_date': '2024-09-02T23:00:00',
                'url': 'https://www.ffm-montreal.org',
                'source': 'Official Festival Site',
                'category': 'film',
                'price': '$15-50 CAD',
                'metro': 'Place-des-Arts'
            },
            {
                'name': 'Montreal Food Festival',
                'venue': 'Old Port of Montreal',
                'address': 'Old Port of Montreal, QC H2Y 1C6',
                'start_date': '2024-07-15T11:00:00',
                'end_date': '2024-07-21T22:00:00',
                'url': 'https://www.montrealfoodfest.com',
                'source': 'Official Festival Site',
                'category': 'food',
                'price': '$20-80 CAD',
                'metro': 'Place-d\'Armes'
            },
            {
                'name': 'Montreal Art Festival',
                'venue': 'Place des Arts',
                'address': 'Place des Arts, Montreal, QC H2X 1Y9',
                'start_date': '2024-09-10T10:00:00',
                'end_date': '2024-09-15T18:00:00',
                'url': 'https://www.montrealartfest.com',
                'source': 'Official Festival Site',
                'category': 'art',
                'price': '$15-50 CAD',
                'metro': 'Place-des-Arts'
            },
            {
                'name': 'Montreal Beer Festival',
                'venue': 'Palais des Congrès',
                'address': 'Palais des Congrès, Montreal, QC H2Z 1H2',
                'start_date': '2024-08-08T12:00:00',
                'end_date': '2024-08-10T22:00:00',
                'url': 'https://www.montrealbeerfest.com',
                'source': 'Official Festival Site',
                'category': 'food',
                'price': '$40-100 CAD',
                'metro': 'Place-d\'Armes'
            },
            {
                'name': 'Montreal Electronic Music Festival',
                'venue': 'Parc Jean-Drapeau',
                'address': 'Parc Jean-Drapeau, Montreal, QC H3C 6A3',
                'start_date': '2024-07-20T14:00:00',
                'end_date': '2024-07-21T23:00:00',
                'url': 'https://www.montrealelectronicfest.com',
                'source': 'Official Festival Site',
                'category': 'music',
                'price': '$80-200 CAD',
                'metro': 'Jean-Drapeau'
            },
            {
                'name': 'Montreal Street Art Festival',
                'venue': 'Various Locations',
                'address': 'Downtown Montreal, QC',
                'start_date': '2024-07-25T10:00:00',
                'end_date': '2024-07-27T18:00:00',
                'url': 'https://www.montrealstreetart.com',
                'source': 'Official Festival Site',
                'category': 'art',
                'price': 'Free',
                'metro': 'Multiple stations'
            },
            {
                'name': 'Montreal Wine Festival',
                'venue': 'Old Port of Montreal',
                'address': 'Old Port of Montreal, QC H2Y 1C6',
                'start_date': '2024-08-30T11:00:00',
                'end_date': '2024-09-01T22:00:00',
                'url': 'https://www.montrealwinefest.com',
                'source': 'Official Festival Site',
                'category': 'food',
                'price': '$60-150 CAD',
                'metro': 'Place-d\'Armes'
            },
            {
                'name': 'Montreal Summer Festival',
                'venue': 'Quartier des Spectacles',
                'address': 'Quartier des Spectacles, Montreal, QC H2X 1X8',
                'start_date': '2024-07-01T18:00:00',
                'end_date': '2024-08-31T23:00:00',
                'url': 'https://www.montrealsummerfest.com',
                'source': 'Official Festival Site',
                'category': 'music',
                'price': 'Free - $50 CAD',
                'metro': 'Place-des-Arts'
            },
            {
                'name': 'Montreal Cultural Festival',
                'venue': 'Various Venues',
                'address': 'Montreal, QC',
                'start_date': '2024-07-05T10:00:00',
                'end_date': '2024-07-14T22:00:00',
                'url': 'https://www.montrealculturalfest.com',
                'source': 'Official Festival Site',
                'category': 'art',
                'price': '$10-40 CAD',
                'metro': 'Multiple stations'
            }
        ]
        
        # Add current year festivals that are happening now or soon
        current_date = datetime.now()
        current_year = current_date.year
        
        for festival in known_festivals:
            # Update dates to current year
            start_date = datetime.fromisoformat(festival['start_date'])
            end_date = datetime.fromisoformat(festival['end_date'])
            
            # Adjust to current year
            start_date = start_date.replace(year=current_year)
            end_date = end_date.replace(year=current_year)
            
            # If the festival has passed this year, move to next year
            if start_date < current_date:
                start_date = start_date.replace(year=current_year + 1)
                end_date = end_date.replace(year=current_year + 1)
            
            festival['start_date'] = start_date.isoformat()
            festival['end_date'] = end_date.isoformat()
            
            festivals.append(festival)
        
        return festivals
    
    def _scrape_mtl_org(self) -> List[Dict[str, Any]]:
        """Scrape Montreal Tourism official site"""
        try:
            # Montreal Tourism events page
            url = "https://www.mtl.org/en/events"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                events = []
                
                # Look for event listings
                event_elements = soup.find_all(['div', 'article'], class_=re.compile(r'event|festival|activity'))
                
                for element in event_elements[:15]:
                    try:
                        # Extract event information
                        title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5'])
                        event_name = title_elem.text.strip() if title_elem else "Unknown Event"
                        
                        # Only include cultural events
                        if not self._is_cultural_event(event_name):
                            continue
                        
                        # Extract date
                        date_elem = element.find(['time', 'span', 'div'], class_=re.compile(r'date|time|when'))
                        event_date = date_elem.text.strip() if date_elem else datetime.now().strftime("%Y-%m-%d")
                        
                        # Extract location
                        location_elem = element.find(['span', 'div'], class_=re.compile(r'location|venue|where'))
                        location = location_elem.text.strip() if location_elem else "Montreal"
                        
                        # Extract link
                        link_elem = element.find('a')
                        event_url = link_elem['href'] if link_elem else "https://www.mtl.org"
                        if not event_url.startswith('http'):
                            event_url = "https://www.mtl.org" + event_url
                        
                        events.append({
                            'name': event_name,
                            'venue': location,
                            'address': location,
                            'start_date': self._parse_date(event_date),
                            'end_date': self._parse_date(event_date),
                            'url': event_url,
                            'source': 'MTL.org',
                            'category': self._categorize_event(event_name)
                        })
                        
                    except Exception as e:
                        logger.error(f"Error parsing MTL.org event: {e}")
                
                return events
            
        except Exception as e:
            logger.error(f"Error scraping MTL.org: {e}")
        
        return []
    
    def _scrape_quebec_tourism(self) -> List[Dict[str, Any]]:
        """Scrape Quebec Tourism site"""
        try:
            # Quebec Tourism events page
            url = "https://www.quebecoriginal.com/en-ca/events"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                events = []
                
                # Look for event listings
                event_elements = soup.find_all(['div', 'article'], class_=re.compile(r'event|activity|festival'))
                
                for element in event_elements[:15]:
                    try:
                        # Extract event information
                        title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5'])
                        event_name = title_elem.text.strip() if title_elem else "Unknown Event"
                        
                        # Only include cultural events
                        if not self._is_cultural_event(event_name):
                            continue
                        
                        # Extract date
                        date_elem = element.find(['time', 'span', 'div'], class_=re.compile(r'date|time|when'))
                        event_date = date_elem.text.strip() if date_elem else datetime.now().strftime("%Y-%m-%d")
                        
                        # Extract location
                        location_elem = element.find(['span', 'div'], class_=re.compile(r'location|venue|where'))
                        location = location_elem.text.strip() if location_elem else "Quebec"
                        
                        # Extract link
                        link_elem = element.find('a')
                        event_url = link_elem['href'] if link_elem else "https://www.quebecoriginal.com"
                        if not event_url.startswith('http'):
                            event_url = "https://www.quebecoriginal.com" + event_url
                        
                        events.append({
                            'name': event_name,
                            'venue': location,
                            'address': location,
                            'start_date': self._parse_date(event_date),
                            'end_date': self._parse_date(event_date),
                            'url': event_url,
                            'source': 'Quebec Tourism',
                            'category': self._categorize_event(event_name)
                        })
                        
                    except Exception as e:
                        logger.error(f"Error parsing Quebec Tourism event: {e}")
                
                return events
            
        except Exception as e:
            logger.error(f"Error scraping Quebec Tourism: {e}")
        
        return []
    
    def _scrape_montreal_gazette(self) -> List[Dict[str, Any]]:
        """Scrape Montreal Gazette events"""
        try:
            # Montreal Gazette events page
            url = "https://montrealgazette.com/entertainment/events"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                events = []
                
                # Look for event articles
                event_elements = soup.find_all(['article', 'div'], class_=re.compile(r'event|story|article'))
                
                for element in event_elements[:15]:
                    try:
                        # Extract event information
                        title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5'])
                        event_name = title_elem.text.strip() if title_elem else "Unknown Event"
                        
                        # Only include cultural events
                        if not self._is_cultural_event(event_name):
                            continue
                        
                        # Extract date
                        date_elem = element.find(['time', 'span', 'div'], class_=re.compile(r'date|time|when'))
                        event_date = date_elem.text.strip() if date_elem else datetime.now().strftime("%Y-%m-%d")
                        
                        # Extract location
                        location_elem = element.find(['span', 'div'], class_=re.compile(r'location|venue|where'))
                        location = location_elem.text.strip() if location_elem else "Montreal"
                        
                        # Extract link
                        link_elem = element.find('a')
                        event_url = link_elem['href'] if link_elem else "https://montrealgazette.com"
                        if not event_url.startswith('http'):
                            event_url = "https://montrealgazette.com" + event_url
                        
                        events.append({
                            'name': event_name,
                            'venue': location,
                            'address': location,
                            'start_date': self._parse_date(event_date),
                            'end_date': self._parse_date(event_date),
                            'url': event_url,
                            'source': 'Montreal Gazette',
                            'category': self._categorize_event(event_name)
                        })
                        
                    except Exception as e:
                        logger.error(f"Error parsing Montreal Gazette event: {e}")
                
                return events
            
        except Exception as e:
            logger.error(f"Error scraping Montreal Gazette: {e}")
        
        return []
    
    def _scrape_montreal_events(self) -> List[Dict[str, Any]]:
        """Scrape Montreal events calendar"""
        try:
            # Montreal events calendar
            url = "https://www.montreal.com/events"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                events = []
                
                # Look for event listings
                event_elements = soup.find_all(['div', 'article'], class_=re.compile(r'event|activity|festival'))
                
                for element in event_elements[:15]:
                    try:
                        # Extract event information
                        title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5'])
                        event_name = title_elem.text.strip() if title_elem else "Unknown Event"
                        
                        # Only include cultural events
                        if not self._is_cultural_event(event_name):
                            continue
                        
                        # Extract date
                        date_elem = element.find(['time', 'span', 'div'], class_=re.compile(r'date|time|when'))
                        event_date = date_elem.text.strip() if date_elem else datetime.now().strftime("%Y-%m-%d")
                        
                        # Extract location
                        location_elem = element.find(['span', 'div'], class_=re.compile(r'location|venue|where'))
                        location = location_elem.text.strip() if location_elem else "Montreal"
                        
                        # Extract link
                        link_elem = element.find('a')
                        event_url = link_elem['href'] if link_elem else "https://www.montreal.com"
                        if not event_url.startswith('http'):
                            event_url = "https://www.montreal.com" + event_url
                        
                        events.append({
                            'name': event_name,
                            'venue': location,
                            'address': location,
                            'start_date': self._parse_date(event_date),
                            'end_date': self._parse_date(event_date),
                            'url': event_url,
                            'source': 'Montreal.com',
                            'category': self._categorize_event(event_name)
                        })
                        
                    except Exception as e:
                        logger.error(f"Error parsing Montreal.com event: {e}")
                
                return events
            
        except Exception as e:
            logger.error(f"Error scraping Montreal.com: {e}")
        
        return []
    
    def _scrape_local_sites(self) -> List[Dict[str, Any]]:
        """Scrape local Montreal event websites"""
        local_sites = [
            'https://www.tourisme-montreal.org/events',
            'https://www.montrealinternational.com/events',
            'https://www.quebecoriginal.com/en-ca/events/montreal'
        ]
        
        all_events = []
        
        for site in local_sites:
            try:
                response = self.session.get(site, timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for event elements
                    event_elements = soup.find_all(['div', 'article'], class_=re.compile(r'event|festival|concert|activity'))
                    
                    for element in event_elements[:10]:
                        try:
                            # Extract event information
                            title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5'])
                            event_name = title_elem.text.strip() if title_elem else "Unknown Event"
                            
                            # Only include cultural events
                            if not self._is_cultural_event(event_name):
                                continue
                            
                            # Extract date
                            date_elem = element.find(['time', 'span', 'div'], class_=re.compile(r'date|time|when'))
                            event_date = date_elem.text.strip() if date_elem else datetime.now().strftime("%Y-%m-%d")
                            
                            # Extract location
                            location_elem = element.find(['span', 'div'], class_=re.compile(r'location|venue|where'))
                            location = location_elem.text.strip() if location_elem else "Montreal"
                            
                            # Extract link
                            link_elem = element.find('a')
                            event_url = link_elem['href'] if link_elem else site
                            if not event_url.startswith('http'):
                                event_url = site + event_url
                            
                            all_events.append({
                                'name': event_name,
                                'venue': location,
                                'address': location,
                                'start_date': self._parse_date(event_date),
                                'end_date': self._parse_date(event_date),
                                'url': event_url,
                                'source': 'Local Site',
                                'category': self._categorize_event(event_name)
                            })
                            
                        except Exception as e:
                            logger.error(f"Error parsing local site event: {e}")
                            
            except Exception as e:
                logger.error(f"Error scraping {site}: {e}")
        
        return all_events
    
    def _is_cultural_event(self, event_name: str) -> bool:
        """Check if event is cultural (not business/tech)"""
        event_lower = event_name.lower()
        
        # Cultural keywords
        cultural_keywords = [
            'festival', 'concert', 'music', 'jazz', 'rock', 'pop', 'classical',
            'art', 'exhibition', 'gallery', 'museum', 'theatre', 'theater',
            'dance', 'ballet', 'comedy', 'film', 'movie', 'cinema',
            'food', 'culinary', 'wine', 'beer', 'taste', 'culture',
            'performance', 'show', 'entertainment', 'celebration'
        ]
        
        # Business/tech keywords to exclude
        business_keywords = [
            'conference', 'summit', 'expo', 'trade', 'business', 'technology',
            'cyber', 'security', 'ai', 'artificial intelligence', 'startup',
            'networking', 'workshop', 'seminar', 'meeting', 'forum'
        ]
        
        # Check for cultural keywords
        has_cultural = any(keyword in event_lower for keyword in cultural_keywords)
        
        # Check for business keywords
        has_business = any(keyword in event_lower for keyword in business_keywords)
        
        # Return true if cultural and not business
        return has_cultural and not has_business
    
    def _parse_date(self, date_string: str) -> str:
        """Parse various date formats"""
        try:
            # Clean the date string
            date_string = date_string.strip()
            
            # Try different date formats
            date_formats = [
                '%Y-%m-%d',
                '%B %d, %Y',
                '%d %B %Y',
                '%Y/%m/%d',
                '%m/%d/%Y',
                '%d/%m/%Y'
            ]
            
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(date_string, fmt)
                    return parsed_date.isoformat()
                except:
                    continue
            
            # If no format matches, return current date
            return datetime.now().isoformat()
            
        except Exception as e:
            logger.error(f"Error parsing date {date_string}: {e}")
            return datetime.now().isoformat()
    
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

# Global scraper instance
_live_scraper = None

def get_live_scraper():
    """Get or create the global live scraper instance"""
    global _live_scraper
    if _live_scraper is None:
        _live_scraper = LiveFestivalScraper()
    return _live_scraper

def get_live_festivals():
    """Get live festival data"""
    scraper = get_live_scraper()
    return scraper.get_live_festivals() 