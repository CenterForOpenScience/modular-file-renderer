import os
from typing import List
from zipfile import ZipFile

from mako.lookup import TemplateLookup

from mfr.core.utils import sizeof_fmt
from mfr.core.extension import BaseRenderer


class ZipRenderer(BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return False

    def render(self):

        zip_file = ZipFile(self.file_path, 'r')

        file_list = self.sanitize_file_list(zip_file.filelist)
        file_tree = self.file_list_to_tree(file_list)

        return self.TEMPLATE.render(data=file_tree, base=self.assets_url)

    def file_list_to_tree(self, file_list: list) -> List[dict]:
        """Build the file tree and return a "tree".

        TODO: Fix this algorithm
        This algorithm only works when the ``file_list`` are in strict alphabetical order. Here is
        an example file A.zip where list 1 fails while list 2 succeed.

        A.zip
        --- A/
            --- A/aa.png
            --- B/ab.png

        File list 1: [ A/, A/B/, A/A/, A/A/aa.png, A/B/ab.png, ]

        File list 2: [ A/, A/A/, A/A/aa.png, A/B/, A/B/ab.png, ]

        :param file_list: the sanitized file list
        :rtype: ``List[dict]``
        :return: a "tree" in form of a list which contains one dictionary as the root node
        """

        icons_url = self.assets_url + '/img'

        # Build the root of the file tree
        tree_root = [{
            'text': self.metadata.name + self.metadata.ext,
            'icon': icons_url + '/file-ext-zip.png',
            'children': []
        }]

        # Iteratively build the file tree for each file and folder.egments.
        for file in file_list:

            node_path = tree_root[0]

            # Split the full path into segments, add each path segment to the tree if the segment
            # doesn't already exist.  The segments can be either a folder or a file.
            paths = [path for path in file.filename.split('/') if path]
            for path in paths:

                # Add a child to the node
                if not len(node_path['children']) or node_path['children'][-1]['text'] != path:

                    new_node = {'text': path, 'children': []}

                    date = '%d-%02d-%02d %02d:%02d:%02d' % file.date_time[:6]
                    size = sizeof_fmt(int(file.file_size)) if file.file_size else ''
                    new_node['data'] = {'date': date, 'size': size}

                    if file.filename[-1] == '/':
                        new_node['icon'] = icons_url + '/folder.png'
                    else:
                        ext = os.path.splitext(file.filename)[1].lstrip('.')
                        if ext:
                            ext = ext.lower()
                        if self.icon_exists_for_type(ext):
                            new_node['icon'] = '{}/file-ext-{}.png'.format(icons_url, ext)
                        else:
                            new_node['icon'] = '{}/file-ext-generic.png'.format(icons_url)

                    node_path['children'].append(new_node)

                    node_path = new_node
                # Go one level deeper
                else:
                    node_path = node_path['children'][-1]

        return tree_root

    @staticmethod
    def icon_exists_for_type(ext: str) -> bool:
        """Check if an icon exists for the given file type.  The extension string is converted to
        lower case.

        :param ext: the file extension str
        :rtype: ``bool``
        :return: ``True`` if found; ``False`` otherwise
        """

        return os.path.isfile(os.path.join(
            os.path.dirname(__file__),
            'static',
            'img',
            'file-ext-{}.png'.format(ext.lower())
        ))

    @staticmethod
    def sanitize_file_list(file_list: list) -> list:
        """Remove macOS system and temporary files.  Current implementation only removes '__MACOSX/'
        and '.DS_Store'.  If necessary, extend the sanitizer to exclude more file types.

        :param file_list: the list of the path for each file and folder in the zip
        :rtype: ``list``
        :return: a sanitized list
        """

        sanitized_file_list = []

        for file in file_list:

            file_path = file.filename
            # Ignore macOS '__MACOSX' folder for zip file
            if file_path.startswith('__MACOSX/'):
                continue

            # Ignore macOS '.DS_STORE' file
            if file_path == '.DS_Store' or file_path.endswith('/.DS_Store'):
                continue

            sanitized_file_list.append(file)

        return sanitized_file_list
