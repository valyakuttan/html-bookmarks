# bookmark.py


class Bookmark:
    def __init__(self, title, url):
        self.url, self.title = url, title

    def __str__(self):
        return "({0.title}, {0.url})".format(self)

    def __repr__(self):
        return "({0.title}, {0.url})".format(self)
