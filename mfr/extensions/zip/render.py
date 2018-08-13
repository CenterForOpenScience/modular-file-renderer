import os
from typing import List, Union
from zipfile import ZipFile, ZipInfo

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
        return True

    def render(self):

        zip_file = ZipFile(self.file_path, 'r')

        # ``ZipFile.filelist`` contains both files and folders.  Using ``obj`` for better clarity.
        sorted_obj_list = self.sanitize_obj_list(zip_file.filelist, sort=True)
        obj_tree = self.sorted_obj_list_to_tree(sorted_obj_list)

        return self.TEMPLATE.render(data=obj_tree, base=self.assets_url)

    def sorted_obj_list_to_tree(self, sorted_obj_list: list) -> List[dict]:
        """Build the object tree from a sorted object list.  Each node is a dictionary.  Leaf nodes
        represent files and empty folders.  Non-leaf nodes represent non-emtpy folders.  Return a
        list of dictionary that contains only one element: the root node.  The tree can be accessed
        and searched via the ``children`` key, of which the value is a list of child nodes.

        :param sorted_obj_list: the sorted object list
        :rtype: ``List[dict]``
        :return: a list that contains only one element: the root node.
        """
        # Build the root node of the tree
        tree_root = {
            'text': self.metadata.name + self.metadata.ext,
            'icon': self.assets_url + '/img/file-ext-zip.png',
            'children': []
        }
        # Iterate through each path and build the tree
        for obj in sorted_obj_list:
            path_from_root = obj.filename
            print(path_from_root)
            path_segments = [segment for segment in path_from_root.split('/') if segment]
            # Find the parent node of the current object, always start from the root node
            parent = tree_root
            for index, segment in enumerate(path_segments):
                # last segment is the current object, parents must have been found, end loop
                if index == len(path_segments) - 1:
                    break
                # for a sorted list, every segment on the path must have a tree node
                sibling_list = parent.get('children', [])
                parent = self.find_node_among_siblings(segment, sibling_list)
                # TODO: do we need this assert?
                assert parent
            # Create a new node, update details and add it to the sibling list
            sibling_list = parent.get('children', [])
            is_folder = path_from_root[-1] == '/'
            new_node = {
                'text': path_segments[-1],
                'children': [],
            }
            self.update_node_with_attributes(new_node, obj, is_folder=is_folder)
            sibling_list.append(new_node)
        return [tree_root, ]

    # TODO: should we remove this function?
    def unsorted_obj_list_to_tree(self, obj_list: list) -> List[dict]:
        """Build the object tree from an object list.  Each node is a dictionary, where leaf nodes
        represent empty folders and files and non-leaf nodes represent non-emtpy folders. Return a
        list that contains only one element: the root node.

        :param obj_list: the object list
        :rtype: ``List[dict]``
        :return: a list that contains only one element: the root node.
        """
        # Build the root node of the tree
        tree_root = {
            'text': self.metadata.name + self.metadata.ext,
            'icon': self.assets_url + '/img/file-ext-zip.png',
            'children': []
        }
        for obj in obj_list:
            # For each object, always start from the root of the tree
            parent = tree_root
            path_from_root = obj.filename
            is_folder = path_from_root[-1] == '/'
            path_segments = [segment for segment in path_from_root.split('/') if segment]
            last_index = len(path_segments) - 1
            # Iterate through the path segments list.  Add the segment to tree if not already there
            # and update the details with the current object if it is the last one along the path.
            for index, segment in enumerate(path_segments):
                # Check if the segment has already been added
                siblings = parent.get('children', [])
                current_node = self.find_node_among_siblings(segment, siblings)
                # Found
                if current_node:
                    if index == last_index:
                        # If it is the last segment, this node must be a folder and represents the
                        # current object.  Update it with the objects' info and break.
                        assert is_folder
                        self.update_node_with_attributes(current_node, obj, is_folder=is_folder)
                        break
                    # Otherwise, jump to the next segment with the current node as the new parent
                    parent = current_node
                    continue
                # Not found
                new_node = {
                    'text': segment,
                    'children': [],
                }
                if index == last_index:
                    # If it is the last segment, the node represents the current object.  Update the
                    # it with the objects' info, add it to the siblings and break.
                    self.update_node_with_attributes(new_node, obj, is_folder=is_folder)
                    siblings.append(new_node)
                    break
                # Otherwise, append the new node to tree, jump to the next segment with the current
                # node as the new parent
                siblings.append(new_node)
                parent = new_node
                continue
        return [tree_root, ]

    def update_node_with_attributes(self, node: dict, obj: ZipInfo, is_folder: bool=True) -> None:
        """Update details (date, size, icon, etc.) of the node with the given object.

        :param node: the node to update
        :param obj: the object that the node represents
        :param is_folder: the folder flag
        """
        date = '%d-%02d-%02d %02d:%02d:%02d' % obj.date_time[:6]
        size = sizeof_fmt(int(obj.file_size)) if obj.file_size else ''
        if is_folder:
            icon_path = self.assets_url + '/img/folder.png'
        else:
            ext = (os.path.splitext(obj.filename)[1].lstrip('.')).lower()
            if self.icon_exists(ext):
                icon_path = '{}/img/file-ext-{}.png'.format(self.assets_url, ext)
            else:
                icon_path = '{}/img/file-ext-generic.png'.format(self.assets_url)
        node.update({
            'icon': icon_path,
            'data': {
                'date': date,
                'size': size,
            },
        })

    @staticmethod
    def icon_exists(ext: str) -> bool:
        """Check if an icon exists for the given file type.  The extension string is converted to
        lower case.

        :param ext: the file extension string
        :rtype: ``bool``
        :return: ``True`` if found, ``False`` otherwise
        """
        return os.path.isfile(os.path.join(
            os.path.dirname(__file__),
            'static',
            'img',
            'file-ext-{}.png'.format(ext.lower())
        ))

    @staticmethod
    def sanitize_obj_list(obj_list: list, sort: bool=False) -> list:
        """Remove macOS system and temporary files with an option flag to sort the list.  Current
        implementation only removes '__MACOSX/' and '.DS_Store'.

        TODO: If necessary, extend the sanitizer to exclude more file types.

        :param obj_list: a list of full paths for each file or folder in the zip
        :param sort: the flag for returning a sorted list
        :rtype: ``list``
        :return: a sanitized list
        """
        sanitized_obj_list = []
        for obj in obj_list:
            obj_path = obj.filename
            # Ignore macOS '__MACOSX' folder for zip file
            if obj_path.startswith('__MACOSX/'):
                continue
            # Ignore macOS '.DS_STORE' file
            if obj_path == '.DS_Store' or obj_path.endswith('/.DS_Store'):
                continue
            sanitized_obj_list.append(obj)
        if sort:
            return sorted(sanitized_obj_list, key=lambda obj: obj.filename)
        return sanitized_obj_list

    @staticmethod
    def find_node_among_siblings(segment: str, siblings: list) -> Union[dict, None]:
        """Find the folder or file node represented by the path segment.

        :param segment: the path segment
        :param siblings: the list containing all sibling nodes
        :rtype: ``Union[dict, None]``
        :return: the node dictionary if found or ``None`` otherwise
        """
        for sibling in siblings:
            if sibling.get('text', '') == segment:
                return sibling
        return None
