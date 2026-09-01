import subprocess
import os
import movielist.storage as storage
from movielist.tmdb import TMDBClient

def clear():
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

def load_genres(json_path: str, Client: TMDBClient):
    result = storage.read(json_path)
    if result is None:
        client = Client
        tv_result = client.genre('tv')['genres']
        movie_result = client.genre('movie')['genres']
        full_genre = {}

        for res in tv_result:
            full_genre[res["id"]] = res["name"]

        for res in movie_result:
            full_genre[res["id"]] = res["name"]

        storage.write(json_path, full_genre)
        return full_genre
    else:
        return result

