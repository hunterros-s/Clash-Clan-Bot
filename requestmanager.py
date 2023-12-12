import requests
from utils import *

class RequestManager():
    """Manage requests to the COC (Clash of Clans) API.

    This class handles interactions with the COC API by setting
    default header and making requests to specified URLs.
    """
    def __init__(self):
        """Initialize the RequestManager."""
        self.header = {}
    
    def set_header(self, header):
        """Set the header for the request.

        Args:
            header (dict): The header to set for the request.
        """
        self.header = header
    
    def get_header(self):
        """Return the header.

        Returns:
            dict: The currently set header for the request.
        """
        return self.header

    def request(self, url, timeout=10):  # Timeout set to 10 seconds by default
        """Make a request to the specified URL and return data.

        Args:
            url (str): The URL to which the request will be made.
            timeout (int, optional): Timeout for the request in seconds. Defaults to 10.

        Returns:
            dict: The JSON data received from the API.

        Raises:
            ValueError: If the response is not valid JSON.
        """
        try:
            response = requests.get(url, headers=self.get_header(), timeout=timeout)
            
            if response.status_code == 200:
                if response.text:
                    try:
                        return response.json()
                    except ValueError:
                        raise ValueError("ERROR: Response is not valid JSON")
                else:
                    raise ValueError("ERROR: Got empty response")
            else:
                raise requests.HTTPError(f"ERROR: Request failed with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            error(f"Request failed: {str(e)}")

# Need to parse reponse better:
"""
	
Error: response status is 503

Response body
Download
{
  "reason": "inMaintenance",
  "message": "API is currently in maintenance, please come back later"
}
"""