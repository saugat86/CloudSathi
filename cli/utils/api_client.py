"""API client for CloudSathi backend."""
import os
from typing import Dict, Any, Optional
import requests
from requests.exceptions import RequestException, ConnectionError, Timeout


class APIClient:
    """Client for interacting with CloudSathi API."""

    def __init__(self, base_url: Optional[str] = None):
        """Initialize API client.
        
        Args:
            base_url: Base URL for the API. Defaults to http://localhost:8000
        """
        self.base_url = base_url or os.getenv("CLOUDSATHI_API_URL", "http://localhost:8000")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def get_aws_costs(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get AWS cost data.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Dictionary containing cost data
            
        Raises:
            RequestException: If API request fails
        """
        url = f"{self.base_url}/api/aws/costs"
        params = {"start_date": start_date, "end_date": end_date}
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except ConnectionError as exc:
            raise RequestException(
                f"Failed to connect to API at {self.base_url}. "
                "Is the server running?"
            ) from exc
        except Timeout as exc:
            raise RequestException("Request timed out") from exc
        except RequestException as exc:
            if hasattr(exc, 'response') and exc.response is not None:
                try:
                    error_detail = exc.response.json().get('detail', str(exc))
                except Exception:
                    error_detail = exc.response.text or str(exc)
                raise RequestException(f"API Error: {error_detail}") from exc
            raise

    def get_azure_costs(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get Azure cost data.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Dictionary containing cost data
            
        Raises:
            RequestException: If API request fails
        """
        url = f"{self.base_url}/api/azure/costs"
        params = {"start_date": start_date, "end_date": end_date}
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except ConnectionError as exc:
            raise RequestException(
                f"Failed to connect to API at {self.base_url}. "
                "Is the server running?"
            ) from exc
        except Timeout as exc:
            raise RequestException("Request timed out") from exc
        except RequestException as exc:
            if hasattr(exc, 'response') and exc.response is not None:
                try:
                    error_detail = exc.response.json().get('detail', str(exc))
                except Exception:
                    error_detail = exc.response.text or str(exc)
                raise RequestException(f"API Error: {error_detail}") from exc
            raise

    def get_recommendation(self, cost_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get cost optimization recommendation.
        
        Args:
            cost_data: Dictionary containing cost information
            
        Returns:
            Dictionary containing recommendation
            
        Raises:
            RequestException: If API request fails
        """
        url = f"{self.base_url}/api/recommendations"
        payload = {"cost_data": cost_data}
        
        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except ConnectionError as exc:
            raise RequestException(
                f"Failed to connect to API at {self.base_url}. "
                "Is the server running?"
            ) from exc
        except Timeout as exc:
            raise RequestException("Request timed out") from exc
        except RequestException as exc:
            if hasattr(exc, 'response') and exc.response is not None:
                try:
                    error_detail = exc.response.json().get('detail', str(exc))
                except Exception:
                    error_detail = exc.response.text or str(exc)
                raise RequestException(f"API Error: {error_detail}") from exc
            raise

    def health_check(self) -> bool:
        """Check if API is reachable.
        
        Returns:
            True if API is reachable, False otherwise
        """
        try:
            response = self.session.get(f"{self.base_url}/docs", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
