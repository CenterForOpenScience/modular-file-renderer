import os
import json
from .. import FileRenderer
from .utilities import column_population, row_population, check_shape, MAX_COLS, MAX_ROWS, TooBigError

class TabularRenderer(FileRenderer):

        #todo look into custom exceptions

    def render(self, file_pointer, file_path):
        _, file_name = os.path.split(file_pointer.name)
        _, ext = os.path.splitext(file_name)

        try:
            data_frame = self._build_df(file_pointer)
        except TooBigError:
            return """
                <div>There was an error rendering {file_name}</div><br>
                <div>Too many rows or columns</div>
                <div>Max rows x cols: {max_rows} x {max_cols} </div>
                """.format(file_name=file_name,
                           max_rows=MAX_ROWS,
                           max_cols=MAX_COLS,
                           )

        except IndexError:
            return """
            <div>There was an error rendering {file_name}:</div><br>
            <div>Is this file blank?</div>
                """.format(file_name=file_name)
        if data_frame is None:
            return """
        <div>There was an error rendering {file_name}</div><br>
        <div>Is it a valid {ext} file?</div>
        <div>Is it empty?</div>
        """.format(file_name=file_name, ext=ext)

        try:
            check_shape(data_frame)
        except TooBigError:
            return """
                <div>There was an error rendering {file_name}:</div><br>
                <div>Too many rows or columns: </div>
                <div>Max rows x cols = {max_rows} x {max_cols};
                 File rows x cols = {file_rows} x {file_cols}</div>
                """.format(file_name=file_name,
                           max_rows=MAX_ROWS,
                           max_cols=MAX_COLS,
                           file_rows=data_frame.shape[0],
                           file_cols=data_frame.shape[1],
                           )

        # TODO: Catch specific exceptions if possible
        try:
            columns = column_population(data_frame)

            rows = row_population(data_frame)
            html_from_file = \
                open(os.getcwd() +
                     "/renderer/tabular/static/html/tabular.html").read()
            html_with_data = html_from_file % (
                json.dumps(columns), json.dumps(rows)
            )
        except Exception as error:
            return "There was an error rendering {}: {}".format(
                file_name, error
            )
        return html_with_data