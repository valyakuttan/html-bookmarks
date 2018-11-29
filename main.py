# main.py

import glob
import os
import os.path
from itertools import chain, islice, starmap
from getpass import getpass

from jsonbookmarks import load_bookmarks_from_json
from markdownbookmarks import load_bookmarks_from_markdown
from gistbookmarks import (retrieve_bookmarks_from_github,
                           bookmarked_date)
from htmltemplate import html_output


def list_of_json_files(path):
    return glob.glob(path + "/*.json")


def split_every(n, iterable):
    it = iter(iterable)
    chunk = list(islice(it, n))
    while chunk:
        yield chunk
        chunk = list(islice(it, n))


def main(username,
         password,
         json_files_path,
         html_directory,
         bookmark_file_name_prefix,
         number_of_bookmark_entries):

    files = list_of_json_files(json_files_path)
    json_bookmarks = []
    for file_name in files:
        with open(file_name) as f:
            json_bookmarks.append(load_bookmarks_from_json(f))

    ms = retrieve_bookmarks_from_github(username, password)
    mds = map(lambda m: (m[1], bookmarked_date(m[0])), ms)
    md_bookmarks = starmap(load_bookmarks_from_markdown, mds)

    bookmarks = chain(*json_bookmarks, *md_bookmarks)
    sorted_bookmarks = sorted(bookmarks,
                              key=lambda b: b.date_added)

    if not os.path.isdir(html_directory):
        os.mkdir(html_directory)

    number_of_bookmark_entries = 25
    bookmark_file_name_prefix = "bookmark"

    counter = 0
    for bs in split_every(number_of_bookmark_entries,
                          sorted_bookmarks):
        counter += 1
        c = str(counter).zfill(2)
        my_title = "{0}-{1}".format(bookmark_file_name_prefix, c)

        page = html_output(bs, my_title)
        oname = "{0}/{1}.html".format(html_directory, my_title)
        with open(oname, "w") as f:
            f.write(page)


if __name__ == "__main__":
    json_files_path = ("/home/valyakuttan/Downloads/"
                       "Bookmarks/data/bookmarks")
    html_directory = "html"
    number_of_bookmark_entries = 25
    bookmark_file_name_prefix = "bookmark"

    username = input("Username: ")
    password = getpass()

    main(
        username=username,
        password=password,
        json_files_path=json_files_path,
        html_directory=html_directory,
        bookmark_file_name_prefix=bookmark_file_name_prefix,
        number_of_bookmark_entries=number_of_bookmark_entries)
