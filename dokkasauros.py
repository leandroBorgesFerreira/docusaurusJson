import click
import os
import json

@click.command()
@click.argument('path')
def cli(path):
    """This command traverses the dokka directory and
    look for .md files to map the hierarchy of files
    """
    directory_map = directory_tree_to_map2(path)
    print(json.dumps(directory_map))

def folders_and_items(path):
    directory_files = os.listdir(path)
    directory_paths = list(map(lambda x: os.path.join(path, x), directory_files))
    folders_path = list(filter(lambda x: os.path.isdir(x), directory_paths))
    items_path = [item for item in directory_paths if item not in folders_path]

    folders = list(map(os.path.basename, folders_path))
    items = list(map(os.path.basename, items_path))

    return folders_path, folders, items

def directory_tree_to_map2(path):
    directory_map = {'name': os.path.basename(path)}
    directory_map = {'type': "category"}

    folders_path, folders, items = folders_and_items(path)

    directory_map['items'] = items

    for folder_path in folders_path:
        directory_map[folder_path] = directory_tree_to_map2(folder_path)

    return directory_map
