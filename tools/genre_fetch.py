import json
import os
from dotenv import load_dotenv
from movielist.tmdb import TMDBClient
from pprint import pprint
load_dotenv()

# run this script to get a fresh genre.json list
# genres rarely changes so fetching them once in a while is fine
# after that change the genre.py, and assign the result to ALL variable

target_path = "genre.json"
client = TMDBClient(os.getenv("TMDB_API_KEY"))
tv_result = client.genre('tv')['genres']
pprint(tv_result)
movie_result = client.genre('movie')['genres']
pprint(movie_result)
full_genre = {}
for res in tv_result:
    full_genre[res["id"]] = res["name"]
    
for res in movie_result:
    full_genre[res["id"]] = res["name"]

with open(target_path, "w") as file:
    json.dump(full_genre, file)