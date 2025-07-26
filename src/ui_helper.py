import os
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, List

class FestivalUI:
    def __init__(self):
        """Initialize the Festival UI helper"""
        self.categories = {
            '1': 'music',
            '2': 'film', 
            '3': 'food',
            '4': 'art',
            '5': 'comedy'
        }
        
        self.days = {
            '1': 'today',
            '2': 'tomorrow',
            '3': 'monday',
            '4': 'tuesday', 
            '5': 'wednesday',
            '6': 'thursday',
            '7': 'friday',
            '8': 'saturday',
            '9': 'sunday'
        }
        
        self.times = {
            '1': 'morning',
            '2': 'afternoon',
            '3': 'evening',
            '4': 'night'
        }
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_header(self):
        """Show the application header"""
        self.clear_screen()
        print("🎭 Montreal Festival Assistant")
        print("=" * 50)
        print("Find Real-Time Festival Information!")
        print("=" * 50)
        print()
    
    def show_categories(self) -> str:
        """Show category selection menu"""
        print("📂 SELECT FESTIVAL CATEGORY:")
        print("-" * 30)
        for key, category in self.categories.items():
            print(f"{key}. {category.upper()}")
        print("0. Back to main menu")
        print()
        
        while True:
            choice = input("Enter your choice (1-5): ").strip()
            if choice == '0':
                return None
            elif choice in self.categories:
                return self.categories[choice]
            else:
                print("❌ Invalid choice. Please try again.")
    
    def show_calendar(self) -> str:
        """Show calendar for day selection"""
        print("📅 SELECT DAY:")
        print("-" * 30)
        
        # Show current week
        today = datetime.now()
        print(f"Today: {today.strftime('%A, %B %d, %Y')}")
        print()
        
        for key, day in self.days.items():
            if day in ['today', 'tomorrow']:
                if day == 'today':
                    display_day = f"Today ({today.strftime('%A')})"
                else:
                    tomorrow = today + timedelta(days=1)
                    display_day = f"Tomorrow ({tomorrow.strftime('%A')})"
            else:
                # Calculate the next occurrence of this weekday
                weekday_map = {
                    'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                    'friday': 4, 'saturday': 5, 'sunday': 6
                }
                target_weekday = weekday_map[day]
                days_ahead = target_weekday - today.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                target_date = today + timedelta(days=days_ahead)
                display_day = f"{day.title()} ({target_date.strftime('%B %d')})"
            
            print(f"{key}. {display_day}")
        
        print("0. Back to category selection")
        print()
        
        while True:
            choice = input("Enter your choice (1-9): ").strip()
            if choice == '0':
                return None
            elif choice in self.days:
                return self.days[choice]
            else:
                print("❌ Invalid choice. Please try again.")
    
    def show_time_picker(self) -> str:
        """Show time selection menu"""
        print("🕐 SELECT TIME:")
        print("-" * 30)
        for key, time in self.times.items():
            time_display = {
                'morning': 'Morning (9:00 AM - 12:00 PM)',
                'afternoon': 'Afternoon (12:00 PM - 5:00 PM)', 
                'evening': 'Evening (5:00 PM - 9:00 PM)',
                'night': 'Night (9:00 PM - 12:00 AM)'
            }
            print(f"{key}. {time_display[time]}")
        
        print("0. Back to day selection")
        print()
        
        while True:
            choice = input("Enter your choice (1-4): ").strip()
            if choice == '0':
                return None
            elif choice in self.times:
                return self.times[choice]
            else:
                print("❌ Invalid choice. Please try again.")
    
    def show_festival_results(self, result: Dict[str, Any]):
        """Show festival search results"""
        print("\n" + "=" * 60)
        print("🎭 FESTIVAL SEARCH RESULTS")
        print("=" * 60)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return
        
        festivals_found = result.get('festivals_found', 0)
        data_source = result.get('data_source', 'Real-time APIs')
        
        if festivals_found == 0:
            print("❌ No festivals found matching your criteria.")
            print("💡 Try different category, day, or time.")
            print(f"📊 Data source: {data_source}")
        else:
            print(f"✅ Found {festivals_found} festival(s):")
            print(f"📊 Data source: {data_source}")
            print()
            
            # Show detailed results
            matching_festivals = result.get('matching_festivals', [])
            for i, festival in enumerate(matching_festivals, 1):
                print(f"{i}. 🎭 {festival['name']}")
                print(f"   📍 Venue: {festival['venue']}")
                print(f"   🗺️  Address: {festival['address']}")
                print(f"   📅 Dates: {festival['start_date']} to {festival['end_date']}")
                print(f"   🎭 Category: {festival.get('category', 'N/A').upper()}")
                print(f"   💰 Price: {festival.get('price', 'N/A')}")
                print(f"   🚇 Metro: {festival.get('metro', 'N/A')}")
                print(f"   📊 Source: {festival['source']}")
                print()
        
        # Show AI response if available
        if 'final_response' in result and result['final_response']:
            print("🤖 AI Response:")
            print(result['final_response'])
            print()
    
    def show_ongoing_festivals(self, festivals: List[Dict[str, Any]]):
        """Show currently ongoing festivals"""
        print("\n" + "=" * 60)
        print("🎪 CURRENTLY AVAILABLE FESTIVALS")
        print("=" * 60)
        
        if not festivals:
            print("❌ No festivals currently available.")
            print("💡 This might be due to:")
            print("   - No API keys configured")
            print("   - Network connectivity issues")
            print("   - No events happening right now")
            return
        
        print(f"✅ Found {len(festivals)} festival(s) available:")
        print()
        
        # Group by category
        categories = {}
        for festival in festivals:
            cat = festival.get('category', 'other')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(festival)
        
        for category, events in categories.items():
            print(f"🎭 {category.upper()} ({len(events)} events):")
            for event in events:
                print(f"   • {event['name']}")
                print(f"     📍 {event['venue']}")
                print(f"     💰 {event.get('price', 'N/A')}")
                print(f"     📊 Source: {event['source']}")
            print()
        
        print("💡 Use the search function to find specific festivals!")
        print("🔍 Try searching by category, day, or time.")
    
    def show_main_menu(self):
        """Show the main menu"""
        print("🏠 MAIN MENU:")
        print("-" * 30)
        print("1. Search Festivals")
        print("2. View Ongoing Festivals") 
        print("3. Quick Search")
        print("4. Help")
        print("5. Exit")
        print()
    
    def get_user_selection(self) -> tuple:
        """Get user selection through UI"""
        self.show_header()
        self.show_main_menu()
        
        while True:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                return self._guided_search()
            elif choice == '2':
                return ('ongoing', None, None)
            elif choice == '3':
                return self._quick_search()
            elif choice == '4':
                self._show_help()
                continue
            elif choice == '5':
                return ('quit', None, None)
            else:
                print("❌ Invalid choice. Please try again.")
    
    def _guided_search(self) -> tuple:
        """Guided search through UI"""
        self.show_header()
        print("🔍 GUIDED FESTIVAL SEARCH")
        print("=" * 40)
        
        # Step 1: Category selection
        category = self.show_categories()
        if category is None:
            return (None, None, None)
        
        # Step 2: Day selection
        day = self.show_calendar()
        if day is None:
            return (None, None, None)
        
        # Step 3: Time selection
        time = self.show_time_picker()
        if time is None:
            return (None, None, None)
        
        return (category, day, time)
    
    def _quick_search(self) -> tuple:
        """Quick search with text input"""
        self.show_header()
        print("⚡ QUICK SEARCH")
        print("=" * 30)
        print("Enter: [category] [day] [time]")
        print("Examples: music today evening")
        print()
        
        user_input = input("Enter your search: ").strip()
        if user_input.lower() in ['back', 'cancel', 'exit']:
            return (None, None, None)
        
        return (user_input, None, None)
    
    def _show_help(self):
        """Show help information"""
        self.show_header()
        print("❓ HELP & INSTRUCTIONS")
        print("=" * 40)
        print("🎭 Montreal Festival Assistant helps you find:")
        print("• Real-time festival information")
        print("• Exact venue locations")
        print("• Google Maps directions")
        print("• Cost estimates in CAD")
        print()
        print("📂 Available Categories:")
        for key, category in self.categories.items():
            print(f"   {key}. {category.upper()}")
        print()
        print("🕐 Available Times:")
        for key, time in self.times.items():
            print(f"   {key}. {time.title()}")
        print()
        print("💡 Tips:")
        print("• Use 'ongoing' to see current festivals")
        print("• Try different combinations for better results")
        print("• All costs are in Canadian Dollars (CAD)")
        print()
        input("Press Enter to continue...")

# Global UI instance
_ui = None

def get_ui():
    """Get or create the global UI instance"""
    global _ui
    if _ui is None:
        _ui = FestivalUI()
    return _ui 