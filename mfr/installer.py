#!/usr/bin/env python
import os
import pip
import argparse


def pip_install(path, filename):
    """Use pip to install from a requirements file
    :param path: location of file
    :param filename: name of requirements file
    """
    file_location = (os.path.join(path, filename))

    if os.path.isfile(file_location):
        pip.main(['install', "-r", file_location])


def plugin_requirements(render, export, modules=None):
    """Install the requirements of the core modules

    :param render: install only render requirements
    :param export: install only export requirements
    :param modules: list of modules to install requirements of
    """

    HERE = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.join(HERE, "..")

    path_list = modules or [os.path.join(root_path, directory)
                            for directory in os.listdir(root_path)]

    for path in path_list:
        if os.path.isdir(path):
            if not export:
                pip_install(path, "render-requirements.txt")
            if not render:
                pip_install(path, "export-requirements.txt")


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("-e", "--export", help="Install only export requirements",
                        action="store_true")
    parser.add_argument("-r", "--render", help="Install only render requirements",
                        action="store_true")
    parser.add_argument("packages", nargs="*", help="List of packages to install reqs")

    args = parser.parse_args()

    if args.command == 'install':
        plugin_requirements(args.render, args.export, args.packages)

if __name__ == "__main__":

    main()
