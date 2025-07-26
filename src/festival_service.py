import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
from api_integrations import get_live_festivals_from_apis

logger = logging.getLogger(__name__)

def get_ongoing_festivals() -> List[Dict[str, Any]]:
    """
    Get ongoing and upcoming festivals in Montreal using real APIs
    
    Returns:
        List[Dict[str, Any]]: List of festival dictionaries
    """
    try:
        # Get live festival data from real APIs
        festivals = get_live_festivals_from_apis()
        
        if not festivals:
            logger.warning("No live festivals found from APIs, using fallback data")
            return _get_fallback_festivals()
        
        logger.info(f"Successfully retrieved {len(festivals)} live festivals from APIs")
        return festivals
        
    except Exception as e:
        logger.error(f"Error getting ongoing festivals: {e}")
        return _get_fallback_festivals()

def _get_fallback_festivals() -> List[Dict[str, Any]]:
    """Return fallback festival data when APIs fail"""
    return [
        {
            'name': 'Montreal Jazz Festival',
            'venue': 'Quartier des Spectacles',
            'address': 'Quartier des Spectacles, Montreal, QC H2X 1X8',
            'start_date': '2024-06-27T18:00:00',
            'end_date': '2024-07-06T23:00:00',
            'url': 'https://www.montrealjazzfest.com',
            'source': 'Fallback Data',
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
            'source': 'Fallback Data',
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
            'source': 'Fallback Data',
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
            'source': 'Fallback Data',
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
            'source': 'Fallback Data',
            'category': 'food',
            'price': '$20-80 CAD',
            'metro': 'Place-d\'Armes'
        }
    ] 