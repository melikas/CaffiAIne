import logging
import os
from typing import Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai
from festival_service import get_ongoing_festivals

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def execute_task(task_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Execute a task using Gemini API with real festival data
    
    Args:
        task_description (str): Description of the task to execute
        context (Dict[str, Any]): Additional context for the task
        
    Returns:
        Dict[str, Any]: Task execution results
    """
    try:
        logger.info(f"Executing task: {task_description}")
        
        # Get real festival data from APIs
        festivals = get_ongoing_festivals()
        
        # Create context with real data
        festival_context = {
            'location': 'Montreal, Canada',
            'festival_focus': True,
            'available_festivals': festivals,
            'total_festivals': len(festivals),
            'data_sources': 'Real-time APIs (Ticketmaster, Eventbrite, Meetup, Facebook, Google Places)'
        }
        
        if context:
            festival_context.update(context)
        
        # Create enhanced prompt with real data
        enhanced_prompt = f"""
        You are a Montreal Festival Assistant. Provide EXACT, CONCISE information for festival requests.
        
        AVAILABLE REAL-TIME FESTIVAL DATA:
        {_format_festival_data(festivals)}
        
        USER REQUEST: {task_description}
        
        CONTEXT: {festival_context}
        
        REQUIREMENTS:
        1. Use ONLY the real festival data provided above
        2. Provide EXACT venue addresses for Google Maps
        3. Give specific cost estimations in CAD
        4. Include metro station information
        5. Keep responses under 5 points, each under 20 words
        6. Format: [Festival name], [Venue], [Google Maps address], [Cost in CAD], [Metro station]
        
        If no matching festivals found, suggest alternatives or explain why.
        """
        
        # Use Gemini API
        model = genai.GenerativeModel('models/gemini-1.5-pro')
        response = model.generate_content(enhanced_prompt)
        
        result = {
            'status': 'success',
            'response': response.text,
            'model_used': 'models/gemini-1.5-pro',
            'real_time_data_used': True,
            'festivals_available': len(festivals),
            'data_sources': festival_context['data_sources']
        }
        
        logger.info(f"Task executed successfully with {len(festivals)} real festivals")
        return result
        
    except Exception as e:
        logger.error(f"Error executing task: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'response': f"I apologize, but I encountered an error: {str(e)}"
        }

def _format_festival_data(festivals: list) -> str:
    """Format festival data for the prompt"""
    if not festivals:
        return "No festivals currently available."
    
    formatted_data = []
    for festival in festivals:
        formatted_data.append(f"""
        Festival: {festival['name']}
        Venue: {festival['venue']}
        Address: {festival['address']}
        Category: {festival.get('category', 'N/A')}
        Price: {festival.get('price', 'N/A')}
        Metro: {festival.get('metro', 'N/A')}
        Dates: {festival['start_date']} to {festival['end_date']}
        Source: {festival['source']}
        """)
    
    return "\n".join(formatted_data)

def search_festival_information(query: str) -> Dict[str, Any]:
    """Search for festival information using real-time data"""
    return execute_task(f"Search for festivals matching: {query}", {
        'task_type': 'search',
        'query': query
    })

def get_festival_location(festival_name: str) -> Dict[str, Any]:
    """Get specific festival location and details"""
    return execute_task(f"Get location and details for: {festival_name}", {
        'task_type': 'location',
        'festival_name': festival_name
    })

def get_festival_directions(festival_name: str) -> Dict[str, Any]:
    """Get directions to a specific festival"""
    return execute_task(f"Get directions to: {festival_name}", {
        'task_type': 'directions',
        'festival_name': festival_name
    })

def estimate_festival_cost(festival_name: str) -> Dict[str, Any]:
    """Estimate total cost for attending a festival"""
    return execute_task(f"Estimate total cost for: {festival_name}", {
        'task_type': 'cost_estimation',
        'festival_name': festival_name
    })
