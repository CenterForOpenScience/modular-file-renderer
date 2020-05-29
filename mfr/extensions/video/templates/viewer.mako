<style>
    ## Setting margin and padding to 0 for body fixes the scrollbar flickering issue
    body {
        margin: 0;
        padding: 0;
    }
</style>

<video controls poster="/static/images/vid-thumbnail.png" preload="none" height="100%">
  <source src="${url}">
  Your browser does not support the video tag.
</video>

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>
<script>
    window.pymChild.sendMessage('embed', 'embed-responsive-16by9');
</script>
