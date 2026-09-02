import webbrowser, time
from movielist.input_ext import take_input
from movielist.tmdb import TMDBClient, TMDBAPIError, TMDBConnectionError
from movielist.library_main import Library
from movielist.utils import show_banner, clear, load_genres, format_rating, print_error, looks_like_jwt
import movielist.storage as storage
import sys

class App:
    def __init__(self):
        self.API = storage.read("api.json")
        self.client = TMDBClient(self.API)

    def setup(self):
        self.library = Library(json_path="library.json")
        self.genre_list = load_genres("genres.json", self.client)

    def change_api(self, new: str):
        self.API = new
        self.client.change_access_token(self.API)

    @staticmethod
    def enter_to_continue():
        take_input("Press Enter to try again: ")

    def show_details(self, item):
        is_a_movie = item.get('title') is not None
        title = item['title' if is_a_movie else 'name']
        original_title = item['original_title' if is_a_movie else 'original_name']
        overview = item.get('overview', '')
        rating = format_rating(item.get('vote_average'))
        genre = item.get('genre_ids', [])
        release_date = item.get('release_date' if is_a_movie else 'first_air_date', '')
        poster_path = item.get('poster_path', '')
        item_id = item.get('id')

        while True:
            clear()
            print(title if title == original_title else f'{title} ({original_title})')
            print(f'★ {rating}/10 | {", ".join([self.genre_list.get(str(g)) for g in genre])} | {release_date}')
            print("-----------------------------")
            print(overview or "No description.")
            print("-----------------------------")
            is_watched = self.library.is_watched(item_id)
            if is_watched is not None:
                print(f"In library | {'👁  Watched' if is_watched else '👁  Not Watched'}")
            else:
                print("Not in library")

            print()
            print("[q] back | [p] poster | [l] add/remove to library | [c] change watched state")
            usr = take_input("$ ", choices=['q', 'p', 'l', 'c'])
            match usr:
                case 'q':
                    clear()
                    return
                case 'p':
                    if poster_path is not None:
                        webbrowser.open(f'{self.client.image_url}{poster_path}')
                case 'l':
                    index = self.library.library_index(item_id)
                    if index is None:
                        self.library.add_item(item)
                    else:
                        self.library.remove_item(index)
                case 'c':
                    index = self.library.library_index(item_id)
                    if index is None:
                        self.library.add_item(item)
                        index = self.library.library_index(item_id)
                    self.library.change_is_watched(index)

    def search_in_app(self):
        print("search engine")
        print("[q] back | [m] movies | [s] tv-series/anime")
        query_type_short = {
            'm':'movie',
            's':'tv',
            'q':'return'
        }

        query_type = take_input("$ ", choices=query_type_short.keys())
        if query_type == 'q':
            return
        
        query = take_input("search > ")
        page = 1
        result_cache = {}

        while True:
            clear()
            print(f'search > {query}')
            time_start = time.perf_counter()
            if result_cache.get(page) is None:
                while result_cache.get(page) is None:
                    try:
                        result = self.client.search(query, query_type=query_type_short[query_type], page=page)
                        result_cache[page] = result
                    except TMDBConnectionError as e:
                        print_error(e)
                        self.enter_to_continue()
                    except TMDBAPIError as e:
                        print_error(e)
                        self.enter_to_continue()
                    clear()
                    print(f"search > {query}")
            else:
                result = result_cache.get(page)

            total_page = result["total_pages"]
            full_result = result["results"]
            result_len = len(full_result)
            for i, res in enumerate(full_result, 1):
                print(f'{i}. {res['title'] if query_type == 'm' else res['name']} ({res['release_date'][:4] if query_type == 'm' else res['first_air_date']}) [★ {format_rating(res['vote_average'])}/10]')
            time_end = time.perf_counter()

            print()
            print(f'[page {page}/{total_page}] [{result_len} results in {time_end - time_start:.3f}]')
            print("[q] back | [n] next | [p] previous | [number] select")
            usr = take_input("$ ", choices=['q', 'n', 'p'] + list(map(str, range(1, result_len + 1))))
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
                    self.show_details(item)

    def see_library(self):
        clear()
        self.library.read()
        print("library > ")
        while True:
            if not self.library.library_data:
                print("Nothing in your library..")
            else:
                for i, item in enumerate(self.library.library_data, 1):
                    is_a_movie = item.get('title') != None
                    print(f'{i}. {item['title'] if is_a_movie else item['name']} ({item['release_date'][:4] if is_a_movie else item['first_air_date']}) [★ {format_rating(item['vote_average'])}/10] {'👁' if item['is_watched'] else ''}')
            
            print()
            print("[q] back | [number] select")
            usr = take_input("$ ", choices=['q'] + list(map(str, range(1, len(self.library) + 1))))
            match usr:
                case 'q':
                    return
                case _:
                    item = self.library.library_data[int(usr) - 1]
                    self.show_details(item)


    def try_authenticate(self, show_mesage = True):
        if not looks_like_jwt(self.API):
            if show_mesage: print_error("ERROR: Access Token is not valid.")
            return [False, TMDBAPIError]
        
        # REMEMBER TMDBConnectionError is a child of TMDBAPIError so order correctly, if not the parent will catch them
        try:
            self.client.authentication()
            return [True, None]
        except TMDBConnectionError as e:
            if show_mesage: print_error(e)
            return [False, TMDBConnectionError]
        except TMDBAPIError as e:
            if show_mesage: print_error(e)
            return [False, TMDBAPIError]

    def authenticate(self):
        api_changed = False
        first_time = self.API == [] or self.API == None # default at first is this
        auth = self.try_authenticate(show_mesage=not first_time)
        valid = auth[0]

        if not valid:
            valid_method = auth[1]
            if first_time:
                show_banner()
                print("Welcome to Movielist!")
                print("For info about this step, check out https://github.com/dhanaan/Movielist/blob/main/SETUP.md")
                print()

        while not valid:
            if valid_method is TMDBAPIError:
                self.change_api(take_input("Enter TMDB API Read Access Token: "))
            else:
                self.enter_to_continue()

            auth = self.try_authenticate()
            valid = auth[0]
            valid_method = auth[1]

            api_changed = True

        if api_changed: storage.write("api.json", self.API)

    def start(self):
        self.setup()
        while True:
            clear()
            show_banner()
            print("Welcome to Movielist!")
            print("[s] to search")
            print("[l] to see your library")
            print("[q] to quit")
            usr = take_input("$ ", choices=['s', 'l', 'q'])
            match usr:
                case 'q':
                    sys.exit()
                case 'l':
                    self.see_library()
                case 's':
                    self.search_in_app()

def main():
    app = App()
    app.authenticate()
    app.start()

if __name__ == "__main__":
    main()