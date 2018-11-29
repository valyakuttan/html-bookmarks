# gistbookmarks.py

import re
from datetime import datetime, timezone
from itertools import chain
from functools import reduce

from github3 import login


__all__ = ["retrieve_bookmarks_from_github", "bookmarked_date"]


def retrieve_bookmarks_from_github(username, password):
    """
    Return an iterable of(gist_file_name, gist_markdown_content)
    pairs from Github.
    """
    gh = login(username, password)
    gists = filter(lambda g: contains_bookmark(g), gh.gists())
    gist_bookmarks = map(GistBookmark, gists)

    xss = map(lambda g: g.markdown_bookmarks, gist_bookmarks)
    return reduce(chain, xss)


BOOKMARKS_FILE_NAME = re.compile(r"Bookmarks_"
                                 r"(?P<day>\d{2})_"
                                 r"(?P<month>\d{2})_"
                                 r"(?P<year>\d{4}).md",
                                 re.IGNORECASE)


def bookmarked_date(file_name):
    """
    Return date at which bookmark created, which is encoded
    in the file name, as a dateime object.
    """
    m = BOOKMARKS_FILE_NAME.match(file_name)
    if m:
        xs = [m.group("year"), m.group("month"), m.group("day")]
        return datetime(*map(int, xs), tzinfo=timezone.utc)
    else:
        return datetime(1970, 1, 1, tzinfo=timezone.utc)


class GistBookmark:
    def __init__(self, gist):
        self.gist = gist

        xs = self.gist.files.items()
        self.bookmarks = {
            k: v for k, v in xs if is_bookmark(k)
        }

    @property
    def date_created(self):
        "Return date at which gist created as a dateime object."
        return self.gist.created_at

    @property
    def markdown_bookmarks(self):
        """
        Return an iterable of (file name, markdown data) pairs.
        """
        def get_content(o):
            bs = o.content()
            return bs.decode("utf-8")

        xs = self.bookmarks.items()
        return map(lambda x: (x[0], get_content(x[1])), xs)

    @property
    def formatted_date(self):
        return ("( {0:%A} {0:%B}"
                " {0:%d} {0:%Y} )").format(self.date_created)

    def __str__(self):
        bookmarks = ", ".join(self.bookmarks.keys())
        return "{0} {1}".format(bookmarks,
                                self.formatted_date)

    def __repr__(self):
        bookmarks = ", ".join(self.bookmarks.keys())
        return "{0} {1}".format(bookmarks,
                                self.formatted_date)


def contains_bookmark(gist):
    files = gist.files.keys()
    return any(map(is_bookmark, files))


def is_bookmark(file_name):
    return BOOKMARKS_FILE_NAME.match(file_name)
