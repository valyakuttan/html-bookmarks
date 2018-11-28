# main.py

import glob
import os
import os.path
from itertools import chain, islice, starmap

from jsonbookmarks import load_bookmarks_from_json
from markdownbookmarks import load_bookmarks_from_markdown
from gistbookmarks import retrieve_bookmarks_from_github
from htmltemplate import html_output


def list_of_json_files(path):
    return glob.glob(path + "/*.json")


def split_every(n, iterable):
    it = iter(iterable)
    chunk = list(islice(it, n))
    while chunk:
        yield chunk
        chunk = list(islice(it, n))


if __name__ == "__main__":
    path = "/home/valyakuttan/Downloads/Bookmarks/data/bookmarks"
    files = list_of_json_files(path)

    json_bookmarks = []
    for file_name in files:
        with open(file_name) as f:
            json_bookmarks.append(load_bookmarks_from_json(f))

    mds = retrieve_bookmarks_from_github("valyakuttan",
                                         "$github4fun!")
    md_bookmarks = starmap(load_bookmarks_from_markdown, mds)

    bookmarks = chain(*json_bookmarks, *md_bookmarks)
    sorted_bookmarks = sorted(bookmarks,
                              key=lambda b: b.date_added)

    directory = "html"
    if not os.path.isdir(directory):
        os.mkdir(directory)

    csize, oprefix = 25, "bookmark"
    counter = 0
    for bs in split_every(csize, sorted_bookmarks):
        counter += 1
        c = str(counter).zfill(2)
        my_title = "{0}-{1}".format(oprefix, c)

        page = html_output(bs, my_title)
        oname = "{0}/{1}.html".format(directory, my_title)
        with open(oname, "w") as f:
            f.write(page)
