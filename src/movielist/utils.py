import subprocess
import os
import movielist.storage as storage
from movielist.tmdb import TMDBClient

def show_banner():
    print(r"""
  __  __         _     _ _    _   
 |  \/  |_____ _(_)___| (_)__| |_ 
 | |\/| / _ \ V / / -_) | (_-<  _|
 |_|  |_\___/\_/|_\___|_|_/__/\__|
    """)

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
            full_genre[str(res["id"])] = res["name"]

        for res in movie_result:
            full_genre[str(res["id"])] = res["name"]

        storage.write(json_path, full_genre)
        return full_genre
    else:
        return result

def format_rating(rating):
    rounded = round(rating, 1)
    if rounded == int(rounded):
        return str(int(rounded))
    return str(rounded)