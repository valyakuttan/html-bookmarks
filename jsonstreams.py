# jsonstreams.py


import json
import glob

from bookmark import mk_bookmark


__all__ = ["json_bookmarks"]


def json_bookmarks(path):
    json_files = glob.glob(path + "/*.json")
    return map(load_bookmarks, json_files)


def load_bookmarks(file_name):
    json_data = {}
    with open(file_name) as f:
        json_data = json.load(f)

    return json_to_bookmarks(json_data)


def json_to_bookmarks(cloud):
    if "_store" in cloud:
        return map(json_to_bookmark,
                   cloud["_store"]["store"].values())
    else:
        return iter([])


def json_to_bookmark(json):
    return mk_bookmark(json["_bookmarkTitle"],
                       json["_bookmarkUrl"],
                       json["_bookmarkTags"],
                       json["_bookmarkDateAdded"])
