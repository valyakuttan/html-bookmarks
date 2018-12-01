# markdownstreams.py


import re

from bookmark import mk_bookmark


__all__ = ["mk_markdownbookmark"]


def mk_markdownbookmark(markdown, date_added):
    return MarkdownBookmark(markdown, date_added)


class MarkdownBookmark:
    def __init__(self, markdown, date_added):
        self.markdown = markdown
        self.date_added = date_added

    @property
    def bookmarks(self):
        def md2bm(entry):
            bm = markdown_entry_to_bookmark(entry)
            bm.date_added = self.date_added
            return bm

        if self.markdown:
            md = self.markdown.strip()
            entries = re.split(r"\n\n+", md)
            bms = map(md2bm, entries)

            return filter(lambda b: b.url, bms)
        else:
            return iter([])

    def __str__(self):
        return "{0} ({1})".format(self.markdown, self.date_added)

    def __repr__(self):
        return "{0} ({1})".format(self.markdown, self.date_added)


def markdown_entry_to_bookmark(entry):
    md = entry.strip()
    xs = re.split(r"\n", md)

    if len(xs) == 2:
        bm = bm_from_md(xs[0].strip())

        tags = bookmark_tags(xs[1].strip())
        bm.tags = tags
        return bm

    elif len(xs) == 1:
        bm = bm_from_md(xs[0])
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
