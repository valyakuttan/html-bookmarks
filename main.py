# main.py

import json

from json_to_html import list_of_json_files, to_list
from template_helper import html_output


if __name__ == "__main__":
    path = "/home/valyakuttan/Downloads/Bookmarks/data/bookmarks"
    files = list_of_json_files(path)

    my_list = []

    for file_name in files:
        with open(file_name) as f:
            data = json.load(f)
            my_list += to_list(data)

    counter = 0
    oprefix = "bookmark"

    while my_list:
        counter += 1
        c = str(counter).zfill(3)
        my_title = "{0}-{1}".format(oprefix, c)

        chunk_size = 25
        lst = my_list[:chunk_size]
        my_list = my_list[chunk_size:]

        page = html_output(lst, my_title)
        oname = "html/{0}.html".format(my_title)
        with open(oname, "w") as f:
            f.write(page)
