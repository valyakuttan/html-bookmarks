# bookmark.py
from datetime import timedelta, timezone, datetime

# Unix Epoch
Epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)


class Bookmark:
    def __init__(self, title, url, tags=None, micro_seconds=0):
        self.url = url
        self.title = title
        self.tags = tags if tags else []
        self.date_added = Epoch + timedelta(
            microseconds=micro_seconds
        )

    @property
    def tags_string(self):
        tags = ", ".join(self.tags)
        return "[ {0} ]".format(tags) if tags else ""

    @property
    def formatted_date(self):
        return ("( {0:%A} {0:%B}"
                " {0:%d} {0:%Y} )").format(self.date_added)

    def __str__(self):
        fs = ("({0.title} "
              "{0.url} "
              "{0.tags!s} "
              "{0.date_added!s})")
        return fs.format(self)

    def __repr__(self):
        fs = ("({0.title} "
              "{0.url} "
              "{0.tags!r} "
              "{0.date_added!r})")
        return fs.format(self)
