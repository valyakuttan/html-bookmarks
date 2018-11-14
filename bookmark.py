# bookmark.py
from datetime import timedelta


class Bookmark:
    def __init__(self, title, url, micro_seconds=0):
        self.url = url
        self.title = title
        self.delta = timedelta(microseconds=micro_seconds)

    def __str__(self):
        return "({0.title}, {0.url})".format(self)

    def __repr__(self):
        return "({0.title}, {0.url})".format(self)
