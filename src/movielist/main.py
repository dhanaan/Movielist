import time
import textwrap

from movielist.input_ext import take_input
from movielist.tmdb import TMDBClient, TMDBAPIError, TMDBConnectionError
from movielist.library_main import Library
from movielist.utils import *
import movielist.storage as storage

class App:
    def __init__(self):
        self.API: str = storage.read("api.json")
        self.client: TMDBClient = TMDBClient(self.API)

    def setup(self):
        self.library = Library(json_path="library.json")
        #self.genre_list = load_genres("genres.json", self.client) not needed now, used when genre is in ids instead of name

    def access_token_changed(self, new: str):
        self.API = new
        self.client.change_access_token(self.API)

    @staticmethod
    def enter_to_continue():
        take_input("Press Enter to try again: ")
        print()

    def edit_note(self, title: str, previous_note: str) -> str:
        clear()
        print(f"{HEADER}Add note for {title}")
        if previous_note:
            print("Previous note: (Ctrl+Shift+C to copy, Ctrl+Shift+V to paste)")
            print(previous_note)
            print()
        return take_input("~> ")

    def get_full_item(self, id: int, is_a_movie: bool):
        if self.library.library_index(id) is None:
            while True:
                try:
                    return self.client.get_data(id, "movie" if is_a_movie else "tv")
                except TMDBConnectionError as e:
                    print_error(e)
                    self.enter_to_continue()
                except TMDBAPIError as e:
                    print_error(e)
                    self.enter_to_continue()
        else:
            return self.library.get_data_by_id(id)


    def show_details(self, id: int, is_a_movie: bool):
        item = self.get_full_item(id, is_a_movie) # will loop until get the data

        if is_a_movie:
            title = item.get('title', '')
            og_title = item.get('original_title', '')
            release_date = item.get('release_date', '')
            runtime = item.get("runtime", 0)
            revenue = item.get("revenue", 0)
            budget = item.get('budget', 0)
        else:
            title = item.get('name', '')
            og_title = item.get('original_name', '')
            first_year = item.get("first_air_date", '')[:4]
            last_year = item.get("last_air_date", '')[:4]
            release_date = f'{first_year} - {last_year}' if (first_year or last_year) else ''
            number_of_episodes = item.get('number_of_episodes', 0)
            number_of_seasons = item.get('number_of_seasons', 0)
            season = f'{number_of_seasons} seasons / {number_of_episodes} episodes'

        links = []
        title_bar = []
        header_bar = []

        overview = item.get('overview', 'No description.')
        rating = item.get('vote_average', 0)
        genres = [g.get('name', '') for g in item.get('genres', [])]
        status = item.get('status', '')
        companies = [c.get('name', '') for c in item.get('production_companies', [])]
        tagline = item.get('tagline', '')
        poster_path = item.get('poster_path', '')
        homepage = item.get("homepage", '')
        imdb = item.get('imdb_id', '')

        # LINKS
        if poster_path: links.append(link_it("[Poster]",f'{self.client.image_url}{poster_path}'))
        if homepage: links.append(link_it("[Official website]", f"{homepage}"))
        if imdb: links.append(link_it("[IMDB]", f'https://imdb.com/title/{imdb}'))
        links.append(link_it("[TMDB]", f'https://themoviedb.com/{"movie" if is_a_movie else "tv"}/{id}'))
        
        # TITLE BAR
        if title == og_title:
            title_bar.append(title)
        else:
            title_bar.append(f'{title} ({og_title})')

        if status not in ("Released", "Ended"): title_bar.append(status)

        if is_a_movie:
            if runtime: title_bar.append(format_runtime(runtime))
        else:
            title_bar.append(season)

        # HEADER BAR
        if rating: header_bar.append(f'★ {format_rating(rating)}/10')
        if genres: header_bar.append(", ".join(genres))
        if release_date: header_bar.append(release_date)
        
        while True:
            clear()
            print(f"{HEADER}" + " | ".join(title_bar))
            print(f"{WARN}" + " | ".join(header_bar))
            print(f"{DIM}------------------------------------------------------")
            if tagline:
                print(f'{WARN}~ "{tagline}"')
                print(f"{DIM}======================================================")
            print(textwrap.fill(overview))
            print(f"{DIM}------------------------------------------------------")
            print(f"{LINK}" + " ".join(links))

            if companies: print(textwrap.fill(f"Companies: {', '.join(companies)}"))
            if is_a_movie and budget and revenue:
                    print(f'{SUCCESS}Budget: ${budget:,} / Revenue: ${revenue:,}')
            print()

            # IS WATCHED
            if self.library.library_index(id) is not None:
                is_watched = self.library.is_watched(id)
                print(f"{SUCCESS if is_watched else WARN}In library | {'👁  Watched' if is_watched else '👁  Not Watched'}")
            else:
                print(f"{DIM}Not in library")

            # USER NOTES
            note = self.library.get_note(id)
            if note:
                print(f"\n{HEADER}Note:")
                print(textwrap.fill(note))

            print()
            print(menu(("q", "back"), ("l", "add/remove to library"), ("c", "change watched state"), ("n", "add/change notes")))
            usr = take_input("$ ", choices=['q', 'l', 'c', 'n'])
            match usr:
                case 'q':
                    clear()
                    return
                case 'l':
                    index = self.library.library_index(id)
                    if index is None:
                        self.library.add_item(item)
                    else:
                        self.library.remove_item(index)
                case 'c':
                    index = self.make_sure_item_in_library(id, item)
                    self.library.change_is_watched(index)
                case 'n':
                    index = self.make_sure_item_in_library(id, item)
                    self.library.change_note(index, self.edit_note(title, note))

    def make_sure_item_in_library(self, id: int, item):
        index = self.library.library_index(id)
        if index is None:
            self.library.add_item(item)
            index = self.library.library_index(id)
        return index

    def search_in_app(self):
        clear()
        print(f"{HEADER}search engine > ")
        print(menu(("q", "back"), ("m", "movies"), ("s", "tv-series/anime")))
        query_type_short = {
            'm':'movie',
            's':'tv',
            'q':'back'
        }

        query_type = take_input("$ ", choices=query_type_short.keys())
        if query_type == 'q':
            return

        clear()
        print(f"{HEADER}{"movies" if query_type == 'm' else "tv-series"} search > ")
        query = take_input("$ ")
        result_cache = {}
        show_page = 0
        cache_result = []
        raw_cache = []
        next_api_page = True
        api_page = 1

        while True:
            clear()
            print(f'{HEADER}search > {query}')
            if result_cache.get(api_page) is None:
                while result_cache.get(api_page) is None:
                    try:
                        result = self.client.search(query, query_type=query_type_short[query_type], page=api_page)
                        result_cache[api_page] = result
                    except TMDBConnectionError as e:
                        print_error(e)
                        self.enter_to_continue()
                    except TMDBAPIError as e:
                        print_error(e)
                        self.enter_to_continue()
                    clear()
                    print(f"{HEADER}search > {query}")
            else:
                result = result_cache.get(api_page)

            total_api_page = result["total_pages"]
            total_results = result["total_results"]
            full_result = result["results"]

            if next_api_page:
                for i, res in enumerate(full_result, len(cache_result) + 1):
                    date = res.get('release_date') if query_type == 'm' else res.get('first_air_date')
                    year = date[:4] if date else '????'
                    cache_result.append(f'{i}. {res['title'] if query_type == 'm' else res['name']} ({year}) [{WARN}★ {format_rating(res['vote_average'])}/10{Style.RESET_ALL}]')
                    raw_cache.append(res)
                    next_api_page = False

            if (show_page + 1) * 10 > len(cache_result) and api_page < total_api_page:
                next_api_page = True
                api_page += 1
                continue

            page_items = cache_result[show_page * 10 : show_page * 10 + 10]
            for line in page_items:
                print(line)

            number_choices = [str(n) for n in range(show_page * 10 + 1, show_page * 10 + len(page_items) + 1)]

            print()
            local_total_pages = -(-total_results // 10)   # ceil division, no import needed
            print(f'{DIM}[page {show_page + 1}/{local_total_pages}]')
            print(menu(("q", "back"), ("n", "next"), ("p", "previous"), ("number", "select")))
            usr = take_input("$ ", choices=['q', 'n', 'p'] + number_choices)
            match usr:
                case 'q':
                    return
                case 'n':
                    if (show_page + 1) * 10 < len(cache_result) or api_page < total_api_page:
                        show_page += 1
                case 'p':
                    if show_page > 0:
                        show_page -= 1
                case _:
                    item = raw_cache[int(usr) - 1]
                    item_id = item.get("id")
                    item_a_movie = item.get('title') is not None
                    self.show_details(item_id, item_a_movie)

    def see_library(self):
        clear()
        self.library.read()
        page = 0
        max_page = 0

        if not self.library.library_data:
            print(f"{WARN}Nothing in your library..")
            self.enter_to_continue()
            return

        while True:
            clear()
            print(f"{HEADER}library > ")

            cache = []
            for i, item in enumerate(self.library.library_data, 1):
                is_a_movie = item.get('title') is not None
                watched = item.get('is_watched', False)
                cache.append(f'{i}. {item['title'] if is_a_movie else item['name']} ({item['release_date'][:4] if is_a_movie else item['first_air_date']}) [{WARN}★ {format_rating(item['vote_average'])}/10{Style.RESET_ALL}] {SUCCESS + "👁" if watched else ""}')

            max_page = -(-len(cache) // 10) - 1   # ceil division, then convert to 0-indexed
            
            page_items = cache[page * 10 : page * 10 + 10]
            for line in page_items:
                print(line)
            print(f'{DIM}[page {page + 1}/{max_page + 1}]')
            print(menu(("q", "back"), ("n", "next"), ("p", "previous"), ("number", "select")))
            number_choices = [str(n) for n in range(page * 10 + 1, page * 10 + len(page_items) + 1)]
            usr = take_input("$ ", choices=['q', 'n', 'p'] + number_choices)
            match usr:
                case 'q':
                    return
                case 'n':
                    page = min(page + 1, max_page)
                case 'p':
                    page = max(page - 1, 0)
                case _:
                    item = self.library.library_data[int(usr) - 1]
                    item_id = item.get("id")
                    item_a_movie = item.get('title') is not None
                    self.show_details(item_id, item_a_movie)

    def authenticate(self, show_mesage = True):
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

    def check_access_token(self):
        api_changed = False
        first_time = self.API == [] or self.API == None # default at first is this
        auth = self.authenticate(show_mesage=not first_time)
        valid = auth[0]

        if not valid:
            valid_method = auth[1]
            if first_time:
                show_banner()
                print(f"{HEADER}Welcome to Movielist!")
                print(f"For info about this step, check out {LINK}https://github.com/dhanaan/Movielist/blob/main/SETUP.md")
                print()

        while not valid:
            if valid_method is TMDBAPIError:
                self.access_token_changed(take_input("Enter TMDB API Read Access Token: "))
            else:
                self.enter_to_continue()

            auth = self.authenticate()
            valid = auth[0]
            valid_method = auth[1]

            api_changed = True

        if api_changed: storage.write("api.json", self.API)

    def options(self):
        while True:
            clear()
            print(f"{HEADER}options > ")
            print(menu(("a", "change TMDB Access Token")))
            print(menu(("q", "back")))
            usr = take_input("$ ", choices=['a', 'q'])
            match usr:
                case 'q':
                    return
                case 'a':
                    clear()
                    self.access_token_changed(None)
                    self.check_access_token()
                    return

    def start(self):
        self.setup()
        while True:
            clear()
            show_banner()
            print(f"{HEADER}Welcome to Movielist!")
            print(menu(("s", "search")))
            print(menu(("l", "library")))
            print(menu(("o", "options")))
            print(menu(("q", "quit")))
            usr = take_input("$ ", choices=['s', 'l','o', 'q'])
            match usr:
                case 'q':
                    return
                case 'l':
                    self.see_library()
                case 's':
                    self.search_in_app()
                case 'o':
                    self.options()

def main():
    app = App()
    app.check_access_token()
    app.start()

if __name__ == "__main__":
    main()