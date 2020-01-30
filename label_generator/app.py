import os
from pathlib import Path

import jinja2
from bottle import get, post, request, run, static_file, default_app

HERE = Path(__file__).parent

JINJA_ENV = jinja2.Environment(
    loader=jinja2.loaders.FileSystemLoader(str(HERE / "templates"))
)


@get("/")
def index():
    return static_file("index.html", root=str(HERE / "static"))


@post("/")
def create_label():
    print(request.forms)
    title = request.forms.get("title")
    parts = request.forms.get("parts")
    print(title)
    print(parts)


app = default_app()

if __name__ == "__main__":
    if os.getenv("DEBUG") == "label-generator":
        run(host="localhost", port="8982", debug=True)
