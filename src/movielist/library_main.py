import movielist.storage as storage

def autosave(func) -> function:
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        storage.write(self.json_path, self.library_data)
        return result
    return wrapper

class Library:
    def __init__(self, json_path):
        self.library_data: list = list([])
        self.json_path: str = json_path

    def read(self):
        self.library_data = storage.read(self.json_path)

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

