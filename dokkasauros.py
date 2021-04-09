import click
import os
import json

@click.command()
@click.argument('path')
def cli(path):
    """This command traverses the dokka directory and
    look for .md files to map the hierarchy of files
    """
    directory_map = directory_tree_to_map(path)
    sidebar = sidebar_map(directory_map)
    json_dump = json.dumps(sidebar, indent=2, sort_keys=False)

    with open("sidebars.js", "w") as sidebar_file:
        sidebar_file.write("module.exports = ")
        sidebar_file.write(json_dump)

def sidebar_map(content_map):
    docs_list = list()
    docs_list.append(content_map)
    return {"docs": docs_list}

def folders_and_items(path):
    directory_files = os.listdir(path)
    directory_paths = list(map(lambda x: os.path.join(path, x), directory_files))
    folders_path = list(filter(lambda x: os.path.isdir(x), directory_paths))
    items_path = [item for item in directory_paths if item not in folders_path]

    folders = list(map(os.path.basename, folders_path))
    items = list(map(os.path.basename, items_path))

    return folders_path, items_path

def get_docussauros_id(file_path):
    return file_path[2:-3]

def directory_tree_to_map(path):
    directory_map = {}
    directory_map['label'] = os.path.basename(path)
    directory_map['type'] = "category"

    folders_path, items_path = folders_and_items(path)

    cleaned_items = list(filter(is_markdown, items_path))
    items = list(map(get_docussauros_id, cleaned_items))

    for folder_path in folders_path:
        items.append(directory_tree_to_map(folder_path))

    for item in items:
        if "index" in item:
            items.remove(item)
            items.insert(0, item)

    directory_map['items'] = items

    return directory_map

def is_markdown(file_path):
    return file_path.endswith(".md")

def is_index_file(file_path):
    return file_path.endswith("index.md")
