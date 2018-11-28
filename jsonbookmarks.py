# jsonbookmarks.py

import json

from bookmark import mk_bookmark


__all__ = ["load_bookmarks_from_json"]


def load_bookmarks_from_json(stream):
    "Return an iterable of bookmarks from a json stream."
    data = json.load(stream)
    return json_to_bookmarks(data)


def json_to_bookmarks(cloud):
    if "_store" in cloud:
        return map(json_to_bookmark,
                   cloud["_store"]["store"].values())
    else:
        return []


def json_to_bookmark(json):
    return mk_bookmark(json["_bookmarkTitle"],
                       json["_bookmarkUrl"],
                       json["_bookmarkTags"],
                       json["_bookmarkDateAdded"])


if __name__ == "__main__":

    path = "/home/valyakuttan/Downloads/Bookmarks/data/bookmarks"
    file_name = path + "/bookmark-cloud-0.jsonon"

    with open(file_name) as f:
        x = json.load(f)
        bs = json_to_bookmarks(x)
        tags = [b.tags_string for b in bs]

        print(bs)
        print()
        print(tags)
