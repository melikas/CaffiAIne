import logging
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz
import re

from planner import plan, prioritize_tasks, validate_task_dependencies
from executor import execute_task, search_festival_information, get_festival_location, get_festival_directions, estimate_festival_cost
from memory import (
    store_conversation, store_task_result, recall_conversations, 
    recall_task_results, get_user_preferences, get_memory_manager
)
from festival_service import get_ongoing_festivals
from ui_helper import get_ui

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Montreal timezone
MONTREAL_TZ = pytz.timezone('America/Montreal')

class MontrealFestivalAssistant:
    def __init__(self):
        """Initialize the Montreal Festival Assistant with real-time data"""
        self.memory_manager = get_memory_manager()
        self.ui = get_ui()
        logger.info("Montreal Festival Assistant initialized with real-time data")
    
    def get_current_montreal_time(self) -> datetime:
        """Get current time in Montreal timezone"""
        return datetime.now(MONTREAL_TZ)
    
    def show_ongoing_festivals(self):
        """Display currently ongoing festivals from real APIs"""
        try:
            festivals = get_ongoing_festivals()
            self.ui.show_ongoing_festivals(festivals)
            
        except Exception as e:
            logger.error(f"Error showing ongoing festivals: {e}")
            print("❌ Error loading ongoing festivals")
    
    def get_festivals_by_criteria(self, category: str, day: str, time: str) -> List[Dict[str, Any]]:
        """Get festivals matching category, day, and time criteria using real data"""
        try:
            festivals = get_ongoing_festivals()
            matching_festivals = []
            
            logger.info(f"Searching for {category} festivals on {day} at {time}")
            logger.info(f"Total festivals available: {len(festivals)}")
            
            # If no specific day/time criteria, return all festivals of the category
            if day.lower() in ['any', 'all', ''] and time.lower() in ['any', 'all', '']:
                for festival in festivals:
                    if category.lower() in festival['name'].lower() or category.lower() in festival.get('category', '').lower():
                        matching_festivals.append(festival)
                logger.info(f"Found {len(matching_festivals)} festivals for category '{category}'")
                return matching_festivals
            
            # Convert day and time to datetime for comparison
            target_datetime = self._parse_datetime(day, time)
            
            for festival in festivals:
                # Check if festival matches category (case-insensitive)
                category_match = (category.lower() in festival['name'].lower() or 
                                category.lower() in festival.get('category', '').lower())
                
                # Check if festival is happening on the specified day/time
                time_match = self._is_festival_at_time(festival, target_datetime)
                
                # If category matches, include the festival regardless of time
                if category_match:
                    matching_festivals.append(festival)
                    logger.info(f"Added festival: {festival['name']} (category match)")
            
            logger.info(f"Found {len(matching_festivals)} matching festivals")
            return matching_festivals
            
        except Exception as e:
            logger.error(f"Error getting festivals by criteria: {e}")
            return []
    
    def _parse_datetime(self, day: str, time: str) -> datetime:
        """Parse day and time into datetime object with Montreal timezone"""
        try:
            current_time = self.get_current_montreal_time()
            
            # Convert to lowercase for processing
            day_lower = day.lower()
            time_lower = time.lower()
            
            # Handle different day formats
            if day_lower in ['today', 'now']:
                target_date = current_time.date()
            elif day_lower in ['tomorrow']:
                target_date = (current_time + timedelta(days=1)).date()
            elif day_lower in ['tonight']:
                target_date = current_time.date()
                time_lower = 'evening'  # Default to evening for tonight
            elif day_lower in ['monday', 'mon']:
                target_date = self._get_next_weekday(0)
            elif day_lower in ['tuesday', 'tue']:
                target_date = self._get_next_weekday(1)
            elif day_lower in ['wednesday', 'wed']:
                target_date = self._get_next_weekday(2)
            elif day_lower in ['thursday', 'thu']:
                target_date = self._get_next_weekday(3)
            elif day_lower in ['friday', 'fri']:
                target_date = self._get_next_weekday(4)
            elif day_lower in ['saturday', 'sat']:
                target_date = self._get_next_weekday(5)
            elif day_lower in ['sunday', 'sun']:
                target_date = self._get_next_weekday(6)
            else:
                # Try to parse as date
                try:
                    target_date = datetime.strptime(day, "%Y-%m-%d").date()
                except:
                    # If parsing fails, use today
                    target_date = current_time.date()
            
            # Parse time
            if time_lower in ['morning', 'am']:
                target_time = datetime.strptime("09:00", "%H:%M").time()
            elif time_lower in ['afternoon', 'pm']:
                target_time = datetime.strptime("14:00", "%H:%M").time()
            elif time_lower in ['evening', 'night']:
                target_time = datetime.strptime("19:00", "%H:%M").time()
            else:
                # Try to parse as time
                try:
                    target_time = datetime.strptime(time, "%H:%M").time()
                except:
                    # Default to current time if parsing fails
                    target_time = current_time.time()
            
            # Combine date and time with Montreal timezone
            naive_datetime = datetime.combine(target_date, target_time)
            return MONTREAL_TZ.localize(naive_datetime)
            
        except Exception as e:
            logger.error(f"Error parsing datetime: {e}")
            return self.get_current_montreal_time()
    
    def _get_next_weekday(self, weekday: int) -> datetime.date:
        """Get the next occurrence of a weekday in Montreal timezone"""
        today = self.get_current_montreal_time().date()
        days_ahead = weekday - today.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return today + timedelta(days=days_ahead)
    
    def _is_festival_at_time(self, festival: Dict[str, Any], target_datetime: datetime) -> bool:
        """Check if festival is happening at the specified time with timezone awareness"""
        try:
            # Parse festival dates with timezone awareness
            start_date_str = festival['start_date'].replace('Z', '+00:00')
            end_date_str = festival['end_date'].replace('Z', '+00:00')
            
            # Handle different date formats
            if 'T' in start_date_str:
                start_date = datetime.fromisoformat(start_date_str)
            else:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                start_date = MONTREAL_TZ.localize(start_date)
            
            if 'T' in end_date_str:
                end_date = datetime.fromisoformat(end_date_str)
            else:
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                end_date = MONTREAL_TZ.localize(end_date)
            
            # Ensure all datetimes are timezone-aware
            if start_date.tzinfo is None:
                start_date = MONTREAL_TZ.localize(start_date)
            if end_date.tzinfo is None:
                end_date = MONTREAL_TZ.localize(end_date)
            if target_datetime.tzinfo is None:
                target_datetime = MONTREAL_TZ.localize(target_datetime)
            
            # Check if festival is happening at the target time
            return start_date <= target_datetime <= end_date
            
        except Exception as e:
            logger.error(f"Error checking festival time: {e}")
            return False
    
    def _is_festival_currently_ongoing(self, festival: Dict[str, Any]) -> bool:
        """Check if festival is currently ongoing"""
        try:
            current_time = self.get_current_montreal_time()
            return self._is_festival_at_time(festival, current_time)
        except Exception as e:
            logger.error(f"Error checking if festival is ongoing: {e}")
            return False
    
    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        Process user input for Montreal festival information using real-time data
        
        Args:
            user_input (str): User's festival request
            
        Returns:
            Dict[str, Any]: Complete response with festival details
        """
        try:
            logger.info(f"Processing festival request: {user_input}")
            
            # Parse input for category, day, time
            category, day, time = self._parse_user_input(user_input)
            
            # Get matching festivals from real APIs
            matching_festivals = self.get_festivals_by_criteria(category, day, time)
            
            if not matching_festivals:
                return {
                    'user_input': user_input,
                    'final_response': f"No festivals found for {category} on {day} at {time}. Try different criteria or check ongoing festivals.",
                    'festivals_found': 0,
                    'data_source': 'Real-time APIs'
                }
            
            # Generate real-time response for each matching festival
            responses = []
            for festival in matching_festivals:
                response = self._generate_festival_response(festival)
                responses.append(response)
            
            final_response = "\n\n".join(responses)
            
            # Store conversation in memory
            store_conversation(user_input, final_response, [])
            
            return {
                'user_input': user_input,
                'final_response': final_response,
                'festivals_found': len(matching_festivals),
                'matching_festivals': matching_festivals,
                'data_source': 'Real-time APIs'
            }
            
        except Exception as e:
            logger.error(f"Error processing festival request: {e}")
            error_response = f"I apologize, but I encountered an error: {str(e)}"
            store_conversation(user_input, error_response)
            
            return {
                'user_input': user_input,
                'error': str(e),
                'final_response': error_response
            }
    
    def _parse_user_input(self, user_input: str) -> tuple:
        """Parse user input to extract category, day, and time"""
        # Default values
        category = "music"
        day = "today"
        time = "evening"
        
        # English keyword mapping
        category_keywords = {
            'music': ['music', 'concert', 'jazz', 'rock', 'pop'],
            'film': ['film', 'movie', 'cinema', 'documentary'],
            'food': ['food', 'culinary', 'wine', 'beer', 'taste'],
            'art': ['art', 'exhibition', 'gallery', 'museum'],
            'comedy': ['comedy', 'standup', 'humor'],
            'dance': ['dance', 'ballet', 'performance']
        }
        
        # English day keywords
        day_keywords = {
            'today': ['today', 'now'],
            'tomorrow': ['tomorrow'],
            'tonight': ['tonight'],
            'monday': ['monday', 'mon'],
            'tuesday': ['tuesday', 'tue'],
            'wednesday': ['wednesday', 'wed'],
            'thursday': ['thursday', 'thu'],
            'friday': ['friday', 'fri'],
            'saturday': ['saturday', 'sat'],
            'sunday': ['sunday', 'sun']
        }
        
        # English time keywords
        time_keywords = {
            'morning': ['morning', 'am'],
            'afternoon': ['afternoon', 'pm'],
            'evening': ['evening', 'night'],
            'night': ['night']
        }
        
        # Convert input to lowercase for processing
        input_lower = user_input.lower()
        words = input_lower.split()
        
        # Look for category keywords
        found_category = False
        for word in words:
            for cat, keywords in category_keywords.items():
                if word in keywords:
                    category = cat
                    found_category = True
                    break
            if found_category:
                break
        
        # If no category found, try to infer from the input
        if not found_category:
            if any(word in input_lower for word in ['music', 'concert', 'jazz']):
                category = 'music'
            elif any(word in input_lower for word in ['food', 'culinary', 'restaurant']):
                category = 'food'
            elif any(word in input_lower for word in ['comedy', 'humor', 'standup']):
                category = 'comedy'
            elif any(word in input_lower for word in ['art', 'exhibition', 'gallery']):
                category = 'art'
            elif any(word in input_lower for word in ['dance', 'ballet']):
                category = 'dance'
            elif any(word in input_lower for word in ['film', 'movie', 'cinema']):
                category = 'film'
        
        # Look for day keywords
        found_day = False
        for word in words:
            for day_name, keywords in day_keywords.items():
                if word in keywords:
                    day = day_name
                    found_day = True
                    break
            if found_day:
                break
        
        # Look for time keywords
        found_time = False
        for word in words:
            for time_name, keywords in time_keywords.items():
                if word in keywords:
                    time = time_name
                    found_time = True
                    break
            if found_time:
                break
        
        # If no specific time found, try to infer from current time
        if not found_time:
            current_hour = self.get_current_montreal_time().hour
            if 6 <= current_hour < 12:
                time = 'morning'
            elif 12 <= current_hour < 17:
                time = 'afternoon'
            elif 17 <= current_hour < 22:
                time = 'evening'
            else:
                time = 'night'
        
        logger.info(f"Parsed input: category='{category}', day='{day}', time='{time}'")
        return category, day, time
    
    def _generate_festival_response(self, festival: Dict[str, Any]) -> str:
        """Generate real-time response for a specific festival using API data with timezone awareness"""
        try:
            current_time = self.get_current_montreal_time()
            is_ongoing = self._is_festival_currently_ongoing(festival)
            
            # Format current time for display
            current_time_str = current_time.strftime("%Y-%m-%d %H:%M %Z")
            
            # Use Gemini API with real festival data
            prompt = f"""
            Provide EXACT, CONCISE information for this Montreal festival:
            
            Festival: {festival['name']}
            Venue: {festival['venue']}
            Address: {festival['address']}
            Dates: {festival['start_date']} to {festival['end_date']}
            Category: {festival.get('category', 'N/A')}
            Price: {festival.get('price', 'N/A')}
            Metro: {festival.get('metro', 'N/A')}
            Source: {festival['source']}
            Current Montreal Time: {current_time_str}
            Is Currently Ongoing: {is_ongoing}
            
            Provide ONLY 3 key points:
            1. [Festival name and exact venue]
            2. [Google Maps address for navigation]
            3. [Cost estimation in CAD - tickets, transport, food]
            
            Keep each point under 20 words. Be specific and actionable.
            Include current time context if relevant.
            """
            
            result = execute_task(prompt, {
                'location': 'Montreal, Canada',
                'festival_focus': True,
                'real_time_data': True,
                'current_time': current_time_str,
                'is_ongoing': is_ongoing
            })
            
            if result['status'] == 'success':
                return result['response']
            else:
                # Fallback response using API data with timezone info
                status_emoji = "🟢" if is_ongoing else "🟡"
                status_text = "ONGOING NOW" if is_ongoing else "UPCOMING"
                
                return f"""
{status_emoji} {festival['name']} ({status_text})
📍 Venue: {festival['venue']}
🗺️  Address: {festival['address']} (Google Maps)
💰 Estimated Cost: {festival.get('price', '$50-150 CAD')} (varies by event)
🚇 Metro: {festival.get('metro', 'Multiple stations')}
📊 Source: {festival['source']} (Real-time data)
🕐 Current Montreal Time: {current_time_str}
                """
                
        except Exception as e:
            logger.error(f"Error generating festival response: {e}")
            return f"Error getting information for {festival['name']}"
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and statistics"""
        return {
            'memory_stats': self.memory_manager.get_memory_stats(),
            'recent_conversations': recall_conversations(limit=5),
            'user_preferences': get_user_preferences(),
            'data_sources': 'Real-time APIs (Ticketmaster, Eventbrite, Meetup, Facebook, Google Places)'
        }

def main():
    """Main function to run the Montreal Festival Assistant with real-time data"""
    # Check for API key
    if not os.getenv('GOOGLE_API_KEY'):
        print("❌ Error: GOOGLE_API_KEY not found in environment variables")
        print("Please set your Google Gemini API key in a .env file:")
        print("GOOGLE_API_KEY=your_api_key_here")
        return
    
    # Initialize the festival assistant
    assistant = MontrealFestivalAssistant()
    
    # Show system status
    status = assistant.get_system_status()
    print(f"🎭 Montreal Festival Assistant - Real-Time Data")
    print("=" * 60)
    print(f"📊 System Status:")
    print(f"   - Total conversations: {status['memory_stats']['total_conversations']}")
    print(f"   - Total task results: {status['memory_stats']['total_task_results']}")
    print(f"   - User preferences: {status['memory_stats']['total_user_preferences']}")
    print(f"   - Data sources: {status['data_sources']}")
    print()
    
    # Main application loop
    while True:
        try:
            # Get user selection through UI
            category, day, time = assistant.ui.get_user_selection()
            
            if category == 'quit':
                print("👋 Goodbye! Enjoy your Montreal festivals!")
                break
            
            elif category == 'ongoing':
                assistant.show_ongoing_festivals()
                input("\nPress Enter to continue...")
                continue
            
            elif category is None:
                continue
            
            elif day is None and time is None:
                # Quick search with text input
                result = assistant.process_user_input(category)
            else:
                # Guided search with specific criteria
                search_input = f"{category} {day} {time}"
                result = assistant.process_user_input(search_input)
            
            # Show results
            assistant.ui.show_festival_results(result)
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Enjoy your Montreal festivals!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
