import requests

class TMDBAPIError(Exception):
    """Raised when the TMDB API returns an error response"""
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data

class TMDBConnectionError(TMDBAPIError):
    """
    Raised for network-level failures (timeout, DNS, connection refused, etc).

    NOTE: subclass of TMDBAPIError, always except this BEFORE TMDBAPIError,
    or the parent will silently swallow it.
    """ 
    pass

class TMDBClient:
    def __init__(self, access_token: str):
        self.base_url = "https://api.themoviedb.org/3"
        self.image_url = "https://image.tmdb.org/t/p/original"
        self._access_token = access_token
        self._headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self._access_token}"
        }

    def change_access_token(self, new_token):
        self._access_token = new_token
        self._headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self._access_token}"
        }

    def _request(self, method: str, path: str, **kwargs):
        url = f'{self.base_url}{path}'
        try:
            response = requests.request(method, url, headers=self._headers, **kwargs)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                data = response.json()
            except ValueError:
                data = {}
            raise TMDBAPIError(
                data.get("status_message", str(e)),
                status_code=response.status_code,
                response_data=data,
            ) from e
            
        except requests.exceptions.RequestException as e:
            # network errors, timeouts, connection issues
            raise TMDBConnectionError(f"Request failed: {e}") from e
        return response.json()
    
    def authentication(self):
        return self._request("GET", "/authentication")
    
    def search(self, query: str, query_type="movie", page: int = 1):
        params = {"query": query, "language": "en-US", "page": page}
        return self._request("GET", f"/search/{query_type}", params=params)

    def genre(self, query_type: str):
        params = {"language": "en-US"}
        return self._request("GET", f"/genre/{query_type}/list", params=params)

    def get_data(self, id, query_type="movie"):
        return self._request("GET", f'/{query_type}/{id}')
