# giststreams.py


import re
from datetime import datetime, timezone
from itertools import chain, starmap
from functools import partial

from github3 import login

from markdownstreams import mk_markdownbookmark


__all__ = ["gist_streams"]


def gist_streams(username, password):
    gistbookmarks = gist_bookmarks(username, password)
    xs = map(lambda g: (g.markdown_content, g.bookmarked_date),
             gistbookmarks)

    mdbookmarks = starmap(mk_markdownbookmark, xs)
    return map(lambda m: m.bookmarks, mdbookmarks)


def gist_bookmarks(username, password):
    gh = login(username, password)
    gists = gh.gists()
    gist_bookmarks = map(gist_to_gistbookmarks, gists)
    return chain(*gist_bookmarks)


def gist_to_gistbookmarks(gist):
    if gist and gist.files:
        xs = gist.files
        bookmark_files = filter(is_bookmark, xs.keys())
        f = partial(mk_gistbookmark, gist=gist)

        return map(f, bookmark_files)
    else:
        return iter([])


def mk_gistbookmark(bookmark_file_name, gist):
    return GistBookmark(gist, bookmark_file_name)


class GistBookmark:
    def __init__(self, gist, gist_file_name):
        self.gist = gist
        self.gist_file_name = gist_file_name

    @property
    def markdown_content(self):
        """
        Return markdown content of the gist bookmark.
        """
        files = self.gist.files
        if self.gist_file_name in files:
            stream_object = files[self.gist_file_name]
            byte_stream = stream_object.content()
            return byte_stream.decode("utf-8")
        else:
            return ""

    @property
    def bookmarked_date(self):
        """
        Return date at which bookmark created, which is encoded
        in the file name, as a dateime object.
        """
        m = BOOKMARKS_FILE_NAME.match(self.gist_file_name)
        if m:
            xs = [m.group("year"),
                  m.group("month"),
                  m.group("day")]
            return datetime(*map(int, xs), tzinfo=timezone.utc)
        else:
            return datetime(1970, 1, 1, tzinfo=timezone.utc)

    def __str__(self):
        return "{0}".format(self.gist_file_name)

    def __repr__(self):
        return "{0}".format(self.gist_file_name)


BOOKMARKS_FILE_NAME = re.compile(r"Bookmarks_"
                                 r"(?P<day>\d{2})_"
                                 r"(?P<month>\d{2})_"
                                 r"(?P<year>\d{4}).md",
                                 re.IGNORECASE)


def contains_bookmark(gist):
    files = gist.files.keys()
    return any(map(is_bookmark, files))


def is_bookmark(file_name):
    return BOOKMARKS_FILE_NAME.match(file_name)
