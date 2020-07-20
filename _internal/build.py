import os
import markdown2
import re
import json

try:
    from pathlib import Path
except:
    from pathlib2 import Path

LINK_DISCOVERY_REGEX = r"\[([^\]]*)\]\(([^)]+)\)"
PREDEFINED_LINK_DISCOVERY_REGEX = r"(\[[^\]]+]\:)\s*([^\s]+)"

root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", ".."))
source_dir = os.path.join(root_dir, "source")
rel_path_count = len(os.path.normpath(source_dir).split(os.sep))
target_dir = os.path.join(root_dir, "docs")
internal_dir = os.path.join(root_dir, "_internal")
template_html = os.path.join(internal_dir, "template.html")
config_file = os.path.join(internal_dir, "config.json")
gen_index = os.path.join(source_dir, "index.html")

css_file_src = os.path.join(internal_dir, "site.css")
css_file_source = os.path.join(source_dir, "site.css")
css_file = os.path.join(target_dir, "site.css")

TOC_ITEM_TEMPLATE = """
<a href="{relative_target_path}">
<div class="toc_content_div {selected} toc_content_div_l{level}">
 {title}
</div>
</a>
"""

TOC_TREE_TEMPLATE = """
<div class="toc_content_div toc_content_div_l{level}">
 {title}
</div>
"""

if os.path.exists(config_file):
    with open(config_file, "r", encoding="utf-8") as f:
        content = f.read()
        CONFIG = json.loads(content)
else:
    CONFIG = {}


class TemplateContext:
    def __init__(self, path, complete_path_list):
        self.complete_path_list = complete_path_list
        self.path = path
        self.relpath_compare = os.path.dirname(path)

    def get_title(self, target_path):
        return os.path.splitext(os.path.basename(target_path))[0]

    def get_nav_content(self):
        accumulated_html = ""
        navtuples = []

        for file in self.complete_path_list:
            level = len(os.path.normpath(file).split(os.path.sep)) - rel_path_count

            if not file == self.path:
                # self.path = source
                # file = target
                relpath = (
                    os.path.splitext(
                        os.path.sep.join(
                            os.path.normpath(os.path.relpath(file, self.path)).split(
                                os.path.sep
                            )[1:]
                        )
                    )[0]
                    + ".html"
                )

                # get the relative path to the file
                navtuples.append((relpath, self.get_title(file), level, False))

            else:
                relpath = "#"
                navtuples.append((relpath, self.get_title(file), level, True))

        for navtuple in navtuples:
            if navtuple[3]:
                suffix = "selected"
            else:
                suffix = ""

            accumulated_html += TOC_ITEM_TEMPLATE.format(
                relative_target_path=navtuple[0],
                title=navtuple[1],
                level=navtuple[2],
                selected=suffix,
            )

        return accumulated_html

    def get_populated_template(self):
        with open(self.path, "r", encoding="utf-8") as f:
            current_file_content = f.read()

        current_file_title = os.path.splitext(os.path.basename(self.path))[0]

        updated_content = update_content_relative_references(
            os.path.join(root_dir, "source"), self.path, current_file_content
        )
        converted_html = markdown2.markdown(updated_content)

        cssrelpath = os.path.sep.join(
            os.path.normpath(os.path.relpath(css_file_source, self.path)).split(os.path.sep)[
                1:
            ]
        )

        final_content = (
            get_template()
            .replace("{{nav_content}}", self.get_nav_content())
            .replace("{{content}}", converted_html)
            .replace("{{title}}", current_file_title)
            .replace("{{stylesheet}}", cssrelpath)
        )

        return final_content


def populate_index_content():
    if CONFIG["path_to_index"]:
        with open(
            os.path.abspath(os.path.join(internal_dir, CONFIG["path_to_index"])),
            "r",
            encoding="utf-8",
        ) as f:
            content = f.read()

        with open(gen_index, "w", encoding="utf-8") as f:
            f.write(content)


def populate_css():
    with open(css_file_src, "r", encoding="utf-8") as f:
        content = f.read()

    write_text("", css_file)

    with open(css_file, "w", encoding="utf-8") as f:
        f.write(content)


def get_template():
    with open(template_html, "r", encoding="utf-8") as f:
        return f.read()


def is_relative_link(link_value, readme_location):
    link_without_location = link_value
    if link_without_location.find("#") > 0:
        link_without_location = link_without_location[
            0 : link_without_location.find("#")
        ]

    try:
        return os.path.exists(
            os.path.abspath(
                os.path.join(os.path.dirname(readme_location), link_without_location)
            )
        )
    except:
        return False


def replace_relative_link(match, readme_location, root_folder):
    link_path = match.group(2).strip()

    if is_relative_link(link_path, readme_location):
        path, suffix = os.path.splitext(link_path)

        if suffix == ".md":
            link_path = path + ".html"

        return "[{}]({})".format(match.group(1), link_path)
    else:
        return match.group(0)


def replace_prefined_relative_links(
    match, readme_location, root_folder, build_sha, repo_id
):
    link_path = match.group(2).strip()

    if is_relative_link(link_path, readme_location):
        path, suffix = os.path.splitext(link_path)

        if suffix == ".md":
            link_path = path + ".html"
        return "{} {}".format(match.group(1), link_path)
    else:
        return match.group(0)


def update_content_relative_references(root_folder, readme_location, content):
    content = re.sub(
        LINK_DISCOVERY_REGEX,
        lambda match, readme_location=readme_location, root_folder=root_folder: replace_relative_link(
            match, readme_location, root_folder
        ),
        content,
    )

    content = re.sub(
        PREDEFINED_LINK_DISCOVERY_REGEX,
        lambda match, readme_location=readme_location, root_folder=root_folder: replace_relative_link(
            match, readme_location, root_folder
        ),
        content,
    )

    return content


def write_text(content, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


candidates_for_move = []

populate_css()
populate_index_content()

# we need to do a single traversal before doing any work
# this is to build the index of files for the ToC
for dirpath, dnames, fnames in os.walk(source_dir):
    for f in fnames:
        current_file = os.path.join(dirpath, f)
        if not os.path.isdir(current_file):
            candidates_for_move.append(current_file)

for current_file in candidates_for_move:
    relpath_inside_source = os.path.relpath(current_file, source_dir)
    target_path = os.path.join(
        target_dir, os.path.splitext(relpath_inside_source)[0] + ".html"
    )

    context = TemplateContext(current_file, candidates_for_move)
    content = context.get_populated_template()
    write_text(content, target_path)
