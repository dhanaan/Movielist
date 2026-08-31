import requests

class TMDBClient:
    def __init__(self, access_token: str):
        self.base_url = "https://api.themoviedb.org/3"
        self.image_url = "https://image.tmdb.org/t/p/original"
        self.access_token = access_token
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
    
    def search(self, query: str, query_type="movie", page: int = 1):
        url = f"{self.base_url}/search/{query_type}"
        params = {"query": query, "language": "en-US", "page": page}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def genre(self, query_type: str):
        url = f"{self.base_url}/genre/{query_type}/list"
        params = {"language": "en-US"}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()