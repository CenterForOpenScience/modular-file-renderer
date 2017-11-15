
# Office 365 Renderer


This renderer uses Office Online to render .docx files for us. If the Office Online URL ever changes, it will also need to be changed here in settings.

Currently there is no OSF side component for these changes. Once there is, this specific note can be removed. In the meantime in order to test this renderer, you need to go to your local OSF copy of this file: https://github.com/CenterForOpenScience/osf.io/blob/develop/addons/base/views.py#L728-L736
and add 'public_file' : 1, to the dict. This will send all files as public files.

Testing this renderer locally is hard. Since Office Online needs access to the files it will not work with private files or ones hosted locally. To see what the docx files will render like, replace the render function with something that looks like this:

```
    def render(self):
        static_url = 'https://files.osf.io/v1/resources/<fake_project_id>/providers/osfstorage/<fake_file_id>'
        url = settings.OFFICE_BASE_URL + download_url.url
        return self.TEMPLATE.render(base=self.assets_url, url=url)

```

The file at `static_url` must be publicly available. 
