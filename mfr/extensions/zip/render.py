import os
import zipfile

from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.core.utils import sizeof_fmt


class ZipRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        zip_file = zipfile.ZipFile(self.file_path, 'r')
        files = [file for file in zip_file.filelist if not file.filename.startswith('__MACOSX')]

        data = self.filelist_to_tree(files)

        return self.TEMPLATE.render(data=data, base=self.assets_url)

    def filelist_to_tree(self, files):

        self.icons_url = self.assets_url + '/img'

        tree_data = [{
            'text': self.metadata.name + self.metadata.ext,
            'icon': self.icons_url + '/file_extension_zip.png',
            'children': []
        }]

        for file in files:
            node_path = tree_data[0]
            paths = [path for path in file.filename.split('/') if path]
            for path in paths:
                if not len(node_path['children']) or node_path['children'][-1]['text'] != path:
                    # Add a child
                    new_node = {'text': path, 'children': []}

                    if new_node['text']:  # If not a placeholder/"root" directory.
                        date = '%d-%02d-%02d %02d:%02d:%02d' % file.date_time[:6]
                        size = sizeof_fmt(int(file.file_size)) if file.file_size else ''

                        # create new node
                        new_node['data'] = {'date': date, 'size': size}

                        if file.filename[-1] == '/':
                            new_node['icon'] = self.icons_url + '/folder.png'
                        else:
                            ext = os.path.splitext(file.filename)[1].lstrip('.')
                            if check_icon_ext(ext):
                                new_node['icon'] = \
                                    self.icons_url + '/file_extension_{}.png'.format(ext)
                            else:
                                new_node['icon'] = self.icons_url + '/generic-file.png'

                        node_path['children'].append(new_node)

                    node_path = new_node
                else:
                    # "go deeper" to get children of children.
                    node_path = node_path['children'][-1]

        return tree_data

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True

def check_icon_ext(ext):
    return os.path.isfile(os.path.join(os.path.dirname(__file__), 'static', 'img', 'icons',
                                'file_extension_{}.png'.format(ext)))
