import os
from dotenv import load_dotenv
from take_input import take_input
from tmdb import TMDBClient
import subprocess
import webbrowser
import time
from main_liblary import Liblary 
load_dotenv()


class App:
    def __init__(self):
        self.client = TMDBClient(os.getenv("TMDB_API_KEY"))
        self.liblary = Liblary()

    def show_details(self, title, original_title, overview, rating, genre, release_date, poster_path, id, item):
        while True:
            self.cls
            print(title if title == original_title else f'{title} ({original_title})')
            print(f'★ {round(int(rating))}/10 | {genre} | {release_date}')
            print("--------------")
            if overview:
                print(overview)
            else:
                print("No description.")
            print("--------------")
            self.liblary.read()
            is_watched = self.liblary.is_watched(id)
            if is_watched is not None:
                print(f'In liblary | {'Watched' if is_watched else 'Not Watched'}')
            else:
                print("Not in liblary")

            print("[q] back | [p] poster | [l] add/remove to liblary | [c] change watched state")
            usr = take_input("~ ", choices=['q', 'p', 'l', 'c'])
            match usr:
                case 'q':
                    self.cls
                    return
                case 'p':
                    webbrowser.open(f'{self.client.IMAGE_BASE_URL}{poster_path}')
                case 'l':
                    index = self.liblary.liblary_index(id)
                    if index is None:
                        self.liblary.add_item(item)
                    else:
                        self.liblary.remove_item(index)
                case 'c':
                    index = self.liblary.liblary_index(id)
                    if index is None:
                        self.liblary.add_item(item)
                        index = self.liblary.liblary_index(id)
                    self.liblary.change_is_watched(index)

    def search_in_app(self):
        self.cls
        print("search engine")
        print("[q] back | [m] movies | [s] tv-series/anime")
        query_type_short = {
            'm':'movie',
            's':'tv',
            'q':'return'
        }
        query_type = take_input("~ ", choices=query_type_short.keys())
        if query_type == 'q':
            return

        query = take_input("search > ")
        page = 1
        result_cache = {}

        while True:
            self.cls
            print(f'search > {query}')
            time_start = time.perf_counter()
            if result_cache.get(page) is None:
                result = self.client.search(query, query_type=query_type_short[query_type], page=page)
            else:
                result = result_cache.get(page)

            total_page = result["total_pages"]
            full_result = result["results"]
            result_len = len(full_result)
            for i, res in enumerate(full_result, 1):
                print(f'{i}. {res['title'] if query_type == 'm' else res['name']} ({res['release_date'][:4] if query_type == 'm' else res['first_air_date']}) [★ {round(int(res['vote_average']))}/10]')
            time_end = time.perf_counter()

            print()
            print(f'[page {page}/{total_page}] [{result_len} results in {time_end - time_start:.3f}]')
            print("[q] back | [n] next | [p] previous | [number] select")
            usr = take_input("~ ", choices=['q', 'n', 'p'] + list(map(str, range(1, result_len + 1))))
            match usr:
                case 'q':
                    return
                case 'n':
                    if page < total_page:
                        page += 1 
                    else:
                        print(f"Cannot go above {total_page}")
                case 'p':
                    if page > 1:
                        page -= 1 
                    else:
                        print("Cannot go below 1")
                case _:
                    item = full_result[int(usr) - 1]
                    self.show_details(title= item['title' if query_type == 'm' else 'name'], original_title=item['original_title' if query_type == 'm' else 'original_name'], overview=item['overview'], rating=item['vote_average'], genre=item['genre_ids'], release_date= item['release_date' if query_type == 'm' else 'first_air_date'], poster_path= item['poster_path'], id=item['id'], item=item)

    def see_liblary(self):
        while True:
            for i, item in enumerate(self.liblary.liblary_data, 1):
                is_a_movie = item.get('title') != None
                print(f'{i}. {item['title'] if is_a_movie else item['name']} ({item['release_date'][:4] if is_a_movie else item['first_air_date']}) [★ {round(int(item['vote_average']))}/10]')

         #print liblary, see the same thing but add eyes if watched, go to one of them and done. just use the saved data..
    # we should be able to choose by number and go, 

        

    def start(self):
        while True:
            self.cls
            print("Welcome to Movielist")
            print("[s] to search")
            print("[l] to see your liblary")
            print("[q] to quit")
            usr = take_input("~ ", choices=['s', 'l', 'q'])
            match usr:
                case 'q':
                    break
                case 'l':
                    self.see_liblary()
                case 's':
                    self.search_in_app()

    @property
    def cls(self):
        subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

def main():
    app = App()
    app.start()

if __name__ == "__main__":
    main()