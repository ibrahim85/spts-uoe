import json
import logging
from os import listdir
from os.path import isfile, join


def parse_dir(path, parse_function, sort_fn=None, percentage_to_parse=1, filter_fn=None):
    """Parses all files in the given directory using the given parsing function in each file"""

    logging.info('parsing dir %s' % path)
    file_names = get_file_list(path, filter_fn, sort_fn)

    return parse_json_files(file_names, parse_function, percentage_to_parse)

def get_file_list(path, filter_fn=None, sort_fn=None):
    """Get the files in the given directory"""

    # retrieve the file names and apply filtering (if any)
    file_names = [join(path, f) for f in listdir(path) if isfile(join(path, f))
                  and (filter_fn is None or filter_fn(f))]

    # sort file names using the comparator (if any)
    if sort_fn is not None:
        file_names.sort(key=sort_fn)

    return file_names;

def parse_json_files(file_names, parse_function, percentage_to_parse=1):
    """Parses the files using the given parsing function in each file"""

    # parse only the first N files
    max_files = int(round(len(file_names) * percentage_to_parse))
    logging.info('parsing the first %i files' % max_files)

    return [parse_json_file(file_name, parse_function) for file_name in file_names[:max_files]]


def parse_json_file(file_name, parse_function):
    """Parses the given JSON file using the given parsing function"""

    logging.debug('parsing %s' % file_name)
    try:
        with open(file_name) as data_file:
            json_obj = json.load(data_file)
        return parse_function(json_obj)
    except:
        logging.error('error when parsing %s' % file_name)
        return []
