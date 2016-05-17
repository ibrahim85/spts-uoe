import json
from os import listdir
from os.path import isfile, join

def parse_json(file_name, parse_function):
    """Parses the given JSON file using the given parsing function"""

    with open(file_name) as data_file:
        json_obj = json.load(data_file)

    return parse_function(json_obj)

def parse_dir(path, parse_function):
    """Parses all files in the given directory using the given parsing function in each file"""

    file_names = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

    return [parse_json(file_name, parse_function) for file_name in file_names]

