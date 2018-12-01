# template_helper.py

from jinja2 import Environment, FileSystemLoader


__all__ = ["html_output"]


# Load template file templates/site.html
TEMPLATE_FILE = "site.html"
templateLoader = FileSystemLoader(searchpath="templates/")
templateEnv = Environment(loader=templateLoader)
template = templateEnv.get_template(TEMPLATE_FILE)


def html_output(my_list, my_title, my_list_title=""):
    return template.render(list=my_list,
                           title=my_title,
                           list_title=my_list_title)
