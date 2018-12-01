# main.py


from itertools import islice, chain
from functools import reduce

from jsonstreams import json_bookmarks
from giststreams import gist_streams
from htmltemplate import html_output


def combine_streams(xss, xs=None):
    if not xs:
        xs = iter([])
    return reduce(chain, xss, xs)


def is_empty(it):
    first = None
    try:
        first = next(it)
        return False, chain([first], it)
    except StopIteration:
        return True, it


def chunks_of(n, iterable):
    it = iter(iterable)

    chunk = islice(it, n)
    empty, chunk = is_empty(chunk)
    while not empty:
        yield chunk
        chunk = islice(it, n)
        empty, chunk = is_empty(chunk)


def output_chunks(count, xs, html_directory,
                  bookmark_file_name_prefix):
    c = str(count).zfill(2)
    my_title = "{0}_{1}".format(bookmark_file_name_prefix, c)
    page = html_output(xs, my_title)
    oname = "{0}/{1}.html".format(html_directory, my_title)
    with open(oname, "w") as f:
        f.write(page)


def main(username, password, json_files_path, html_directory,
         bookmark_file_name_prefix, number_of_bookmark_entries):

    jsonbookmarks = json_bookmarks(json_files_path)
    bookmarks = combine_streams(jsonbookmarks)

    gistbookmarks = gist_streams(username, password)
    bookmarks = combine_streams(gistbookmarks, bookmarks)

    sorted_bookmarks = sorted(bookmarks,
                              key=lambda b: b.date_added)

    xss = chunks_of(number_of_bookmark_entries, sorted_bookmarks)
    for c, xs in enumerate(xss, 1):
        output_chunks(c, xs, html_directory,
                      bookmark_file_name_prefix)


if __name__ == "__main__":
    import getpass
    import os
    import os.path

    print("Github Login")
    username = input("Username: ")
    password = getpass.getpass()

    json_files_path = ("/home/valyakuttan/Downloads/"
                       "Bookmarks/data/bookmarks")

    html_directory = "html"
    if not os.path.isdir(html_directory):
        os.mkdir(html_directory)

    number_of_bookmark_entries = 25
    bookmark_file_name_prefix = "bookmark"

    main(username=username, password=password,
         json_files_path=json_files_path,
         html_directory=html_directory,
         bookmark_file_name_prefix=bookmark_file_name_prefix,
         number_of_bookmark_entries=number_of_bookmark_entries)
