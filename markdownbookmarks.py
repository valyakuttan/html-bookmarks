# markdownbookmarks.py

import re
from functools import partial


from bookmark import mk_bookmark


__all__ = ["load_bookmarks_from_markdown"]


def load_bookmarks_from_markdown(markdown, date_created=0):
    "Return an iterable of bookmarks from a markdown stream."
    md = markdown.strip()
    entries = re.split(r"\n\n+", md)
    md2bm = partial(markdown_entry_to_bookmark,
                    date_created=date_created)

    bookmarks = map(md2bm, entries)
    return filter(lambda b: b.url, bookmarks)


def markdown_entry_to_bookmark(entry, date_created):
    md = entry.strip()
    xs = re.split(r"\n", md)

    if len(xs) == 2:
        bm = bm_from_md(xs[0].strip())

        tags = bookmark_tags(xs[1].strip())
        bm.tags = tags

        bm.date_added = date_created
        return bm

    elif len(xs) == 1:
        bm = bm_from_md(xs[0])
        bm.date_added = date_created
        return bm

    else:
        return mk_bookmark("", "")


def bm_from_md(markdown):
    md = markdown.strip()
    title, url = title_and_url(md)
    bm = mk_bookmark(title.strip(), url.strip())
    return bm


TAGS = re.compile(r"\[(?P<tags>.+)\]\(\)")


def bookmark_tags(line):
    m = TAGS.match(line)
    if m:
        tags = m.group("tags").strip(",")
        return [x.strip() for x in tags.split(",")]
    else:
        return []


TITLE_AND_URL = re.compile(r"\[(?P<title>.+)\]"
                           r"\((?P<url>.+)\)")


def title_and_url(line):
    m = TITLE_AND_URL.match(line)
    if m:
        title, url = m.group("title"), m.group("url")
        return title.strip(), url.strip()
    else:
        return "Title", ""
