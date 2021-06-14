// Shows or hides content and changes button text accordingly
function showHide(contentClass, buttonId) {
    var contents = document.getElementsByClassName(contentClass);
    var button = document.getElementById(buttonId);

    if (button.textContent == "+") { // Show if hidden
        for (var i = 0; i < contents.length; i++) {
            element = contents[i]
            if (element.nodeName == "TR") {
                element.style.display = "table-row";
            }
            else {
                element.style.display = "block";
            }
        }
        button.textContent = "-";
    }
    else { // Hide if showing
        for (var i = 0; i < contents.length; i++) {
            contents[i].style.display = "none";
            for (var j = 0; j < contents[i].children.length; j++) {
                if (contents[i].children[j].classList.contains("button")) {
                    contents[i].children[j].textContent = "+";
                }
            }
        }
        var children = document.getElementsByClassName(contentClass + "Child");
        for (var i = 0; i < children.length; i++) {
            children[i].style.display = "none";
        }
        button.textContent = "+";
    }
};
