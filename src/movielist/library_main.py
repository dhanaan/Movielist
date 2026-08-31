from dataclasses import dataclass, field
from platformdirs import user_data_path
import json

def default_library_path() -> str:
    data_dir = user_data_path("Movielist")
    data_dir.mkdir(parents=True, exist_ok=True)
    return f'{data_dir}/library.json'

def autosave(func) -> function:
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.write()
        return result
    return wrapper

@dataclass
class Library:
    json_path: str = field(default_factory=default_library_path)
    library_data: list = field(default_factory=list)

    def write(self):
        with open(self.json_path, 'w') as file:
            json.dump(self.library_data, file)

    def read(self):
        try:
            with open(self.json_path, 'r') as file:
                self.library_data = json.load(file)
        except json.JSONDecodeError:
            self.library_data = []
        except FileNotFoundError:
            self.write()
            

    def library_index(self, id):
        for i, item in enumerate(self.library_data):
            if item['id'] == id:
                return i
        return None

    def __len__(self):
        return len(self.library_data)
          
    def get_data(self, index):
        return self.library_data.get(index)
        
    def is_watched(self, id):
        find = self.library_index(id)
        if find is not None:
            return self.library_data[find]['is_watched']
        return None

    @autosave
    def add_item(self, item):
        self.library_data.append(item)
        self.library_data[-1]['is_watched'] = False

    @autosave
    def remove_item(self, index):
        self.library_data.pop(index)

    @autosave
    def change_is_watched(self, index):
        watched = self.library_data[index]["is_watched"]
        self.library_data[index]["is_watched"] = not watched

