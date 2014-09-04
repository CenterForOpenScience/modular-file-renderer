#!/usr/bin/env python
import os
import pip
import sys
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.join(HERE, "..")


def pip_install(path, filename):
    """Use pip to install from a requirements file
    :param path: location of file
    :param filename: name of requirements file
    """
    file_location = (os.path.join(path, filename))

    if os.path.isfile(file_location):
        pip.main(['install', "-r", file_location])


def plugin_requirements(render, export, plugins):
    """Install the requirements of the core plugins

    :param render: install only render requirements
    :param export: install only export requirements
    :param plugins: list of plugins to install requirements of
    """

    if plugins == ["all"]:
        path_list = [os.path.join(root_path, directory)
                     for directory in os.listdir(root_path)]
    elif not plugins:
        sys.exit("Missing required argument: plugins")
    else:
        path_list = [os.path.join(root_path, plugin) for plugin in plugins]

    for path in path_list:
        if os.path.isdir(path):
            if not export:
                pip_install(path, "render-requirements.txt")
            if not render:
                pip_install(path, "export-requirements.txt")
        else:
            print("No directory {path}, skipping.".format(path=path))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("-e", "--export", help="Install only export requirements",
                        action="store_true")
    parser.add_argument("-r", "--render", help="Install only render requirements",
                        action="store_true")
    parser.add_argument("plugins", nargs="*", help="List of plugins to install reqs")

    args = parser.parse_args()
    if args.command == 'install':
        plugin_requirements(args.render, args.export, args.plugins)

if __name__ == "__main__":

    main()
