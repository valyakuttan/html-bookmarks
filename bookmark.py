# bookmark.py
from datetime import timedelta, timezone, datetime


# Unix Epoch
Epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)


class Bookmark:
    def __init__(self, title, url, micro_seconds=0):
        self.url = url
        self.title = title
        self.date_added = Epoch + timedelta(
            microseconds=micro_seconds
        )

    @property
    def formatted_date(self):
        return ("{0:%A} {0:%B} {0:%d} {0:%Y}").format(
            self.date_added
        )

    def __str__(self):
        return "({0.title}, {0.url})".format(self)

    def __repr__(self):
        return "({0.title}, {0.url})".format(self)
