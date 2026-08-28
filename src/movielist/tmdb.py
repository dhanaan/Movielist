import requests

class TMDBClient:
    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p/original"

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

    def search(self, query: str, query_type="movie", page: int = 1):
        url = f"{self.BASE_URL}/search/{query_type}"
        params = {"query": query, "language": "en-US", "page": page}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def genre(self, query_type: str):
        url = f"{self.BASE_URL}/genre/{query_type}/list"
        params = {"language": "en-US"}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()