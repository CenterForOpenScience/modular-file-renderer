    var editors = 'jk'
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/textmate");
    editor.getSession().setMode("ace/mode/text");

      $(document).ready(function() {
            $('#save').click(function() {
            var content = editor.getValue();
             $.ajax({
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(content),
            dataType: 'json',
            url: '/save/'+ document.URL.split("edit/").pop(),
            success: function (e) {
                console.log('e');
    }
});