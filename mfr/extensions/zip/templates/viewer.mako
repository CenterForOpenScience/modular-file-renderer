<link href="https://fonts.googleapis.com/css?family=Open+Sans:400,600,300,700" rel="stylesheet" type="text/css">
<link rel="stylesheet" href="static/css/bootstrap.min.css">
<link rel="stylesheet" href="static/css/default.css">
<div style="word-wrap: break-word;" class="mfrViewer">
    <h1>
        Zip File:
    </h1>
    <p>
        Download the .zip file to view the contents.
    </p>
    ${message}
    <table class="table table-hover">
        <thead>
            <th>File Name</th>
            <th>Modified</th>
            <th>Size</th>
        </thead>
        <tbody>
            % for file in zipped_filenames:
                <tr>
                    <td>${file['name']}</td>
                    <td>${file['date']}</td>
                    <td>${file['size']}<td>
                </tr>
            % endfor
        </tbody>
    </table>
</div>

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>
