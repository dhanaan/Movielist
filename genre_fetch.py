import json
import requests
import os
from dotenv import load_dotenv
from tmdb import TMDBClient
load_dotenv()

# run this script to get a fresh genre.json list

client = TMDBClient(os.getenv("TMDB_API_KEY"))
tv_result = client.genre('tv')['genres']
movie_result = client.genre('movie')['genres']
full_genre = {}
for res in tv_result:
    full_genre[res["id"]] = res["name"]
    
for res in movie_result:
    full_genre[res["id"]] = res["name"]

with open("genre.json", "w") as file:
    json.dump(full_genre, file)