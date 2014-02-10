from .. import FileRenderer
import os.path
import pydocx
import logging
import pipes
logging.basicConfig(level=logging.DEBUG)


class DocxRenderer(FileRenderer):

    def _detect(self, file_pointer):
        """Detects whether a given file pointer can be rendered by
        this renderer. Checks both the extension in list and the file encoding
        using the imghdr lib

        :param file_pointer: File pointer
        :return: Can file be rendered? (bool)

        """
        _, ext = os.path.splitext(file_pointer.name)
        return ext == ".docx"

    def _render(self, file_pointer, **kwargs):
        return pydocx.Docx2Html(file_pointer).parsed