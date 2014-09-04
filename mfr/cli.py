#!/usr/bin/env python
import os
import pip
import sys
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(HERE, "..")


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
        path_list = [os.path.join(ROOT_PATH, directory)
                     for directory in os.listdir(ROOT_PATH)]
    else:
        path_list = [os.path.join(ROOT_PATH, plugin) for plugin in plugins]

    for path in path_list:
        if os.path.isdir(path):
            if not export:
                pip_install(path, "render-requirements.txt")
            if not render:
                pip_install(path, "export-requirements.txt")
        else:
            print('Plugin with name "{plugin}" not found. Skipping...'.format(
                plugin=os.path.basename(os.path.normpath(path))
            ))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("-e", "--export", help="Install only export requirements",
                        action="store_true")
    parser.add_argument("-r", "--render", help="Install only render requirements",
                        action="store_true")
    parser.add_argument("plugin", nargs="*", help="List of plugins to install reqs")

    args = parser.parse_args()
    if args.command == 'install':
        if not args.plugin:
            print('Must provide at least one plugin name to install')
            sys.exit(1)
        plugin_requirements(args.render, args.export, args.plugin)
    else:
        print('Invalid subcommand: "{command}"'.format(command=args.command))
        sys.exit(1)

if __name__ == "__main__":

    main()
