import json
from pprint import pprint 
import requests
import os
from dotenv import load_dotenv

load_dotenv()
with open('mock.json', 'r') as file:
    data = json.load(file)

pprint(data["results"][0]["title"])

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv("TMDB_API_KEY")}"
}

pprint(requests.get("https://api.themoviedb.org/3/authentication", headers=headers))
