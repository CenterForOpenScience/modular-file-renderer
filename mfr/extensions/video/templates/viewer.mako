<style>
    body {
        margin: 0;
        padding: 0;
    }
</style>

<video id="video" controls height="100%">
  <source src="${url}">
  Your browser does not support the video tag.
</video>

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>
<script>
    window.pymChild.sendMessage('embed', 'embed-responsive-16by9');
</script>
