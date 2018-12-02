# template_helper.py

from jinja2 import Environment, FileSystemLoader


__all__ = ["html_output"]


def html_output(my_list, my_title, my_list_title="",
                TEMPLATE_FILE="site.html",
                searchpath="templates/"):
    TEMPLATE_FILE = TEMPLATE_FILE
    templateLoader = FileSystemLoader(searchpath="templates/")
    templateEnv = Environment(loader=templateLoader)
    template = templateEnv.get_template(TEMPLATE_FILE)

    return template.render(list=my_list,
                           title=my_title,
                           list_title=my_list_title)
