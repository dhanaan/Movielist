import subprocess
import os
from colorama import init, Fore, Style

init(autoreset=True)

ERROR = Fore.RED
HEADER = Fore.CYAN + Style.BRIGHT
MENU = Fore.MAGENTA
SUCCESS = Fore.GREEN
WARN = Fore.YELLOW
LINK = Fore.BLUE
DIM = Style.DIM
RESET = Style.RESET_ALL

def show_banner():
    print(r"""
  __  __         _     _ _    _   
 |  \/  |_____ _(_)___| (_)__| |_ 
 | |\/| / _ \ V / / -_) | (_-<  _|
 |_|  |_\___/\_/|_\___|_|_/__/\__|
    """)

def clear():
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

# def load_genres(json_path: str, Client: TMDBClient) -> dict:
#     result = storage.read(json_path)
#     if result is None:
#         client = Client
#         tv_result = client.genre('tv')['genres']
#         movie_result = client.genre('movie')['genres']
#         full_genre = {}

#         for res in tv_result:
#             full_genre[str(res["id"])] = res["name"]

#         for res in movie_result:
#             full_genre[str(res["id"])] = res["name"]

#         storage.write(json_path, full_genre)
#         return full_genre
#     else:
#         return result

def format_rating(rating: int) -> str:
    rounded = round(rating, 1)
    if rounded == int(rounded):
        return str(int(rounded))
    return str(rounded)

def print_error(error_obj):
    if isinstance(error_obj, str):
        print(error_obj)
    else:
        if error_obj.status_code is None:
            print(f"{ERROR}ERROR: there is a network problem, check your connection and try again.")
        else:
            print(f"{ERROR}{error_obj.status_code} ERROR: {error_obj.response_data.get("status_message") or "No Information."}")

    
def looks_like_jwt(token: str) -> bool:
    """
    Cheap sanity check to catch empty input, accidental whitespace, or a
    pasted v3 API key instead of a v4 token.
    """
    token = str(token).strip()
    if not token or token.count(".") != 2 or len(token) < 100:
        return False
    else:
        return True

def format_runtime(min: int, convert_below_hour = True):
    if convert_below_hour:
        return f'{min // 60}h, {min % 60}min'

    if min >= 60:
        return f'{min // 60}h, {min % 60}min'
    
    return f'{min}min'


def link_it(text, url):
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

def menu(*items):
    parts = []
    for key, label in items:
        parts.append(f"{MENU}[{key}] {RESET}{label if label else ""}")
    return f" | ".join(parts)