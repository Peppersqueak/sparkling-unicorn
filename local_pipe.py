import json
import os

DB_PATH="db"



class ToDatabase:
    def __init__(self, file_name):
        self.file_name = file_name

    def convert_to_json(self, dictionary):
        json_file = json.dumps(dictionary)
        return self.send_to_db(json_file)

    def send_to_db(self, json_file):
        # This WILL overwrite old information if an edit is made
        filepath = os.path.join(DB_PATH, self.file_name + ".json")
        with open(filepath, "w") as file:
            file.write(json_file)


class FromDatabase:
    def __init__(self, name):
        self.name = name

    def grab_from_DB(self):
        json_file = os.path.join(DB_PATH, self.name + ".json")
        return self.json_to_array(json_file)

    def json_to_array(self, json_file):
        with open(json_file, 'r') as j:
            contents = json.loads(j.read())
            return contents
