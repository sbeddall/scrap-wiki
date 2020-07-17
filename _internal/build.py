import os
import markdown2
import re
try:
    from pathlib import Path
except:
    from pathlib2 import Path

RELATIVE_LINK_REPLACEMENT_SYNTAX = (
    "https://github.com/{repo_id}/tree/{build_sha}/{target_resource_path}"
)

LINK_DISCOVERY_REGEX = r"\[([^\]]*)\]\(([^)]+)\)"
PREDEFINED_LINK_DISCOVERY_REGEX = r"(\[[^\]]+]\:)\s*([^\s]+)"

IMAGE_FILE_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.gif', '.tiff']
RELATIVE_LINK_REPLACEMENT_SYNTAX_FOR_IMAGE = (
    "https://github.com/{repo_id}/raw/{build_sha}/{target_resource_path}"
)

root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", ".."))
source_dir = os.path.join(root_dir, "source")
target_dir = os.path.join(root_dir, "target")
template_html = os.path.join(root_dir, "_internal", "template.html")

print("Source Directory: ".format(source_dir))
print("Target Directory: ".format(target_dir))

def get_template():
  with open(template_html, "r", encoding="utf-8") as f:
    return f.read()

def is_relative_link(link_value, readme_location):
    link_without_location = link_value
    if link_without_location.find('#') > 0:
        link_without_location = link_without_location[0:link_without_location.find('#')]

    try:
        return os.path.exists(
            os.path.abspath(os.path.join(os.path.dirname(readme_location), link_without_location))
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

def replace_prefined_relative_links(match, readme_location, root_folder, build_sha, repo_id):
    link_path = match.group(2).strip()

    if is_relative_link(link_path, readme_location):
        path, suffix = os.path.splitext(link_path)

        if suffix == ".md":
          link_path = path + ".html"
        return "{} {}".format(match.group(1), link_path)
    else:
        return match.group(0)

def update_content_relative_references(
    root_folder, readme_location, content
):
    content = re.sub(
        LINK_DISCOVERY_REGEX,
        lambda match, readme_location=readme_location, root_folder=root_folder: replace_relative_link(
            match, readme_location, root_folder,
        ),
        content,
    )

    content = re.sub(
        PREDEFINED_LINK_DISCOVERY_REGEX,
        lambda match, readme_location=readme_location, root_folder=root_folder: replace_relative_link(
            match, readme_location, root_folder,
        ),
        content,
    )

    return content

def writeText(content, filename):
  os.makedirs(os.path.dirname(filename), exist_ok=True)
  with open(filename, "w", encoding="utf-8") as f:
    f.write(content)

def construct_toc(file_list):
  pass

candidates_for_move = []

# we need to do a single traversal before doing any work
# this is to build the index of files for the ToC
for dirpath, dnames, fnames in os.walk(source_dir):
    for f in fnames:
      current_file = os.path.join(dirpath,f)
      if not os.path.isdir(current_file):
        candidates_for_move.append(current_file)

for current_file in candidates_for_move:
  current_file_title = os.path.splitext(os.path.basename(current_file))[0]
  relpath_inside_source = os.path.relpath(current_file, source_dir)
  print(relpath_inside_source)
  target_path = os.path.join(target_dir, os.path.splitext(relpath_inside_source)[0] + ".html")
  print(target_path)

  with open(current_file, 'r', encoding="utf-8") as f:
    current_file_content = f.read()

  updated_content = update_content_relative_references(os.path.join(root_dir, "source"), current_file, current_file_content)
  converted_html = markdown2.markdown(updated_content)
  final_content = get_template().replace("{{nav_content}}", "").replace("{{content}}", converted_html).replace("{{title}}",current_file_title)

  writeText(final_content, target_path)
