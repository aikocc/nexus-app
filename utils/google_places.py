"""
Google Places API integration module.
Handles address autocomplete, place details, and ACT-biased search.
"""

import optparse
import requests
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class GooglePlacesError(Exception):
    """Custom exception for Google Places API errors."""
    pass


class GooglePlacesClient:
    """Client for Google Places API operations."""
    
    # Canberra CBD coordinates (latitude, longitude)
    CANBERRA_CBD = "-35.2809,149.1300"
    
    # Default radius for ACT-biased search (50km)
    ACT_RADIUS = 50000
    
    def __init__(self, api_key: str):
        """
        Initialize the Google Places client.
        
        Args:
            api_key: Google Places API key
        """
        if not api_key:
            raise ValueError("Google Places API key is required")
        
        self.api_key = api_key
        self.autocomplete_url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
        self.details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    def _format_prediction(self, prediction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a Google Places prediction into a consistent structure.
        
        Args:
            prediction: Raw prediction from Google API
            
        Returns:
            Formatted suggestion dict
        """
        description = prediction.get("description", "")
        place_id = prediction.get("place_id", "")
        structured = prediction.get("structured_formatting", {})
        
        main_text = structured.get("main_text", "")
        secondary_text = structured.get("secondary_text", "")

        return {
            "description": description,
            "place_id": place_id,
            "main_text": main_text,
            "secondary_text": secondary_text,
        }
    
    def autocomplete_address(
        self,
        query: str,
        bias_to_act: bool = True,
        limit: int = 10,
        components: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get address autocomplete suggestions.
        
        Args:
            query: Search query (minimum 3 characters)
            bias_to_act: Whether to bias results towards ACT
            limit: Maximum number of results to return
            components: Additional Google Places components filter
            
        Returns:
            List of formatted suggestions
            
        Raises:
            GooglePlacesError: If API request fails
        """
        if not query or len(query) < 3:
            raise ValueError("Query must be at least 3 characters")
        
        params = {
            "input": query,
            "types": "address",
            "components": "country:au",  # Restrict to Australia
            "key": self.api_key
        }
        
        # Add ACT location bias if requested
        if bias_to_act:
            params.update({
                "location": self.CANBERRA_CBD,
                "radius": self.ACT_RADIUS,
                "strictbounds": False  # Allow results outside radius but bias towards ACT
            })
        
        # Add additional components if provided
        if components:
            components_str = "|".join([f"{k}:{v}" for k, v in components.items()])
            params["components"] = f"country:au|{components_str}"
        
        try:
            response = requests.get(self.autocomplete_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") != "OK":
                error_message = data.get("error_message", data.get("status", "Unknown error"))
                raise GooglePlacesError(f"Google Places API error: {error_message}")
            
            suggestions = []
            predictions = data.get("predictions", [])
            
            for prediction in predictions:
                suggestion = self._format_prediction(prediction)
                suggestions.append(suggestion)
            
            # Limit results
            return suggestions[:limit]
            
        except requests.RequestException as e:
            raise GooglePlacesError(f"Address lookup failed: {str(e)}")
        except Exception as e:
            if isinstance(e, GooglePlacesError):
                raise
            raise GooglePlacesError(f"Unexpected error: {str(e)}")
    
    def get_place_details(self, place_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a place.
        
        Args:
            place_id: Google Place ID
            
        Returns:
            Place details dict
            
        Raises:
            GooglePlacesError: If API request fails
        """
        if not place_id:
            raise ValueError("Place ID is required")
        
        params = {
            "place_id": place_id,
            "fields": "formatted_address,address_components,geometry,place_id,types",
            "key": self.api_key
        }
        
        try:
            response = requests.get(self.details_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") != "OK":
                raise GooglePlacesError(f"Google Places API error: {data.get('status')}")
            
            result = data.get("result", {})
            
            # Extract address components
            address_components = {}
            for component in result.get("address_components", []):
                types = component.get("types", [])
                long_name = component.get("long_name", "")
                short_name = component.get("short_name", "")
                
                for type_name in types:
                    address_components[type_name] = {
                        "long_name": long_name,
                        "short_name": short_name
                    }
            
            return {
                "formatted_address": result.get("formatted_address"),
                "place_id": result.get("place_id"),
                "address_components": address_components,
                "geometry": result.get("geometry"),
                "types": result.get("types", []),
                "postcode": address_components.get("postal_code", {}).get("long_name")
            }
            
        except requests.RequestException as e:
            raise GooglePlacesError(f"Place details lookup failed: {str(e)}")
        except Exception as e:
            if isinstance(e, GooglePlacesError):
                raise
            raise GooglePlacesError(f"Unexpected error: {str(e)}")


def create_google_places_client(api_key: Optional[str] = None) -> GooglePlacesClient:
    """
    Factory function to create a Google Places client.
    
    Args:
        api_key: Google Places API key (optional, can be set via config)
        
    Returns:
        GooglePlacesClient instance
    """
    if not api_key:
        # Fallback to environment variable
        api_key = os.environ.get('GOOGLE_PLACES_API_KEY')
    
    if not api_key:
        raise ValueError("Google Places API key not found")
    
    return GooglePlacesClient(api_key)