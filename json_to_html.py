# json_to_html.py

import glob

from bookmark import Bookmark


def list_of_json_files(path):
    return glob.glob(path + "/*.json")


def to_list(d):
    if "_store" in d:
        return [
            Bookmark(v['_bookmarkTitle'], v['_bookmarkUrl'])
            for v in d["_store"]["store"].values()
        ]
    else:
        return {}


if __name__ == "__main__":
    import json

    path = "/home/valyakuttan/Downloads/Bookmarks/data/bookmarks"
    json_files = list_of_json_files(path)
    file_name = json_files[100]

    with open(file_name) as f:
        x = json.load(f)
        print(to_list(x))
