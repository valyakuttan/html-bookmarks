# template_helper.py

from jinja2 import Environment, FileSystemLoader


# Load template file templates/site.html
TEMPLATE_FILE = "site.html"
templateLoader = FileSystemLoader(searchpath="templates/")
templateEnv = Environment(loader=templateLoader)
template = templateEnv.get_template(TEMPLATE_FILE)


def html_output(my_list, my_title, my_list_title=""):
    return template.render(list=my_list,
                           title=my_title,
                           list_title=my_list_title)


if __name__ == "__main__":
    from bookmark import Bookmark

    # List for famous movie rendering
    movies = [
        Bookmark("The Hitchhiker's Guide to the Galaxy", "url"),
        Bookmark("Back to future", "url"),
        Bookmark("Matrix",  "url"),
    ]

    print(html_output(movies, "Movies", "Excellent"))
