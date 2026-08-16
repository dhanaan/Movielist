from dataclasses import dataclass, field
import json

@dataclass
class Liblary:
    json_path: str = "liblary.json"
    liblary_data: list = field(default_factory=list)

    def write(self):
        with open(self.json_path, 'w') as file:
            json.dump(self.liblary_data, file)

    def read(self):
        try:
            with open(self.json_path, 'r') as file:
                self.liblary_data = json.load(file)
        except json.JSONDecodeError:
            self.liblary_data = []
        except FileNotFoundError:
            self.write()
            

    def liblary_index(self, id):
        for i, item in enumerate(self.liblary_data):
            if item['id'] == id:
                return i
        return None
          
    def get_data(self, index):
        return self.liblary_data[index]
        
    def is_watched(self, id):
        find = self.liblary_index(id)
        if find is not None:
            return self.liblary_data[find]['is_watched']
        return None
        
    def add_item(self, item):
        self.liblary_data.append(item)
        self.liblary_data[-1]['is_watched'] = False
        self.write()

    def remove_item(self, index):
        self.liblary_data.pop(index)
        self.write()

    def change_is_watched(self, index):
        if self.liblary_data[index]["is_watched"] == True:
            self.liblary_data[index]["is_watched"] = False
        else:
            self.liblary_data[index]["is_watched"] = True
        self.write()

