from dataclasses import dataclass, field
import json

@dataclass
class Library:
    json_path: str = "library.json"
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
        return self.library_data[index]
        
    def is_watched(self, id):
        find = self.library_index(id)
        if find is not None:
            return self.library_data[find]['is_watched']
        return None
        
    def add_item(self, item):
        self.library_data.append(item)
        self.library_data[-1]['is_watched'] = False
        self.write()

    def remove_item(self, index):
        self.library_data.pop(index)
        self.write()

    def change_is_watched(self, index):
        if self.library_data[index]["is_watched"] == True:
            self.library_data[index]["is_watched"] = False
        else:
            self.library_data[index]["is_watched"] = True
        self.write()

