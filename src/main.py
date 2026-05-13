import os
import shutil
import sys
from pathlib import Path

from inline_markdown import markdown_to_html_node


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    destination = "./docs"

    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

    copy("./static", destination)

    generate_pages_recursive("./content", "./template.html", destination, basepath)


def copy(source, destination):
    list_dir = os.listdir(source)

    if not os.path.exists(destination):
        os.mkdir(destination)

    for item in list_dir:
        src_item = os.path.join(source, item)
        dest_item = os.path.join(destination, item)
        # print("copying/creating:", src_item, "->", dest_item)

        if os.path.isfile(src_item):
            shutil.copy(src_item, dest_item)
        else:
            os.mkdir(dest_item)
            copy(src_item, dest_item)


def extract_title(markdown):
    if markdown[0] == "#":
        markdown = markdown[1:]
        markdown = markdown.strip()
    else:
        raise Exception("no header")
    return markdown


"""def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    open_from = open(from_path)
    path = open_from.read()
    html_string = markdown_to_html_node(path)
    html_string = html_string.to_html()
    open_template = open(template_path)
    template = open_template.read()
    title_of_page = extract_title(path)

    template = template.replace("{{ Title }}", title_of_page)
    template = template.replace("{{ Content }}", html_string)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    open_dest = open(dest_path, mode="w")
    open_dest.write(template)
"""


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    open_dir = os.listdir(dir_path_content)

    for arch in open_dir:
        if os.path.isfile(os.path.join(dir_path_content, arch)):
            if arch.endswith(".md"):
                open_md = open(os.path.join(dir_path_content, arch))
                contents = open_md.read()
                html_contents = markdown_to_html_node(contents)
                html_contents = html_contents.to_html()
                open_template = open(template_path)
                template = open_template.read()
                title_of_page = extract_title(contents)

                template = template.replace("{{ Title }}", title_of_page)
                template = template.replace("{{ Content }}", html_contents)
                template = template.replace('href="/', f'href="{basepath}')
                template = template.replace('src="/', f'src="{basepath}')

                dest_path = Path(os.path.join(dest_dir_path, arch)).with_suffix(".html")

                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                open_dest = open(dest_path, mode="w")
                open_dest.write(template)
            else:
                pass
        else:
            generate_pages_recursive(
                os.path.join(dir_path_content, arch),
                template_path,
                os.path.join(dest_dir_path, arch),
                basepath,
            )


if __name__ == "__main__":
    main()
