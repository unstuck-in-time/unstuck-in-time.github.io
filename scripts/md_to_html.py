import klembord
import markdown
from collections import OrderedDict
from bs4 import BeautifulSoup
import pyperclip
from marko import Markdown

f_name = "../content/posts/about.md"


def main():
    file = open(f_name, "r")
    content = file.read()
    file.close()
    html = markdown.markdown(content, extensions=["footnotes"])
    f = open("test.html", "w")
    f.write(html)
    f.close()


if __name__ == "__main__":
    main()
