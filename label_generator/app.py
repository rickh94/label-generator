import os
import tempfile
from pathlib import Path

import jinja2
import weasyprint
from bottle import get, post, request, run, static_file, default_app

HERE = Path(__file__).parent

JINJA_ENV = jinja2.Environment(
    loader=jinja2.loaders.FileSystemLoader(str(HERE / "templates"))
)
main_template = JINJA_ENV.get_template("labels.html")


@get("/")
def index():
    return static_file("index.html", root=str(HERE / "static"))


@post("/")
def create_label():
    title = request.forms.get("title")
    parts = request.forms.get("parts")
    parts = parts.replace("\r", "").split("\n")
    title_words = title.split(" ")
    if len(title_words) == 1:
        title_prefix = title[:2]
    else:
        title_prefix = "".join(word[0].upper() for word in title_words)
    part_labels = [f"{title_prefix}-{part_name}" for part_name in parts]
    all_labels = [title] + part_labels
    label_rows = []
    prev_index = 0
    for i in range(3, len(all_labels) + 2, 3):
        label_rows.append(all_labels[prev_index:i])
        prev_index = i
    output_dir = render_page(label_rows)
    return static_file(
        "labels.pdf",
        root=output_dir,
        mimetype="application/pdf",
        download=f"{title.replace(' ', '')}-labels.pdf",
    )


def render_page(label_rows):
    tmpdir = Path(tempfile.mkdtemp())
    html = main_template.render(label_rows=label_rows)
    tmp_out = tmpdir / "output.html"
    with tmp_out.open("w") as html_file:
        html_file.write(html)
    filename = str(tmpdir / f"labels.pdf")
    weasyprint.HTML(filename=str(tmp_out)).write_pdf(filename)
    return tmpdir


app = default_app()

if __name__ == "__main__":
    if os.getenv("DEBUG") == "label-generator":
        run(host="localhost", port="8982", debug=True)
