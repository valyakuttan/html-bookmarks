# gistbookmarks.py

from github3 import login


class GistBookmark:
    def __init__(self, gist):
        self.gist = gist

        xs = self.gist.files.items()
        self.bookmarks = {
            k: v for k, v in xs if is_bookmark(k)
        }

    @property
    def date_created(self):
        return self.gist.created_at

    @property
    def markdown(self):
        def get_content(o):
            bs = o.content()
            return bs.decode("utf-8")

        contents = map(get_content, self.bookmarks.values())
        return "".join(contents)

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


def retrieve_bookmarks_from_github(username, password):
    "Return a list of (markdown, date) pair."
    gh = login(username, password)
    gists = filter(lambda g: contains_bookmark(g), gh.gists())
    bookmarks = map(GistBookmark, gists)

    return map(lambda g: (g.markdown, g.date_created), bookmarks)


def contains_bookmark(gist):
    files = gist.files.keys()
    return any(map(is_bookmark, files))


def is_bookmark(file_name):
    return file_name.startswith("Bookmark")


if __name__ == "__main__":
    bookmarks = retrieve_bookmarks_from_github("valyakuttan",
                                               "$github4fun!")

    print("=============================================")

    for b in bookmarks:
        print("=============================================")
        print()
        print(b)
        print()
        print("=============================================")

    print("=============================================")
