$(document).ready(function() {
    var checkExist = setInterval(function() {
        var targetNode = document.querySelector('.note-editor');

        if (targetNode) {
            clearInterval(checkExist);

            var observerOptions = {
                childList: true,
                attributes: true,
                subtree: true
            };

            var observer = new MutationObserver(hideSummernoteElement);
            observer.observe(targetNode, observerOptions);
        }
    }, 500); // check every 500 ms
});

function hideSummernoteElement() {
    var selectNode = document.querySelector('.note-group-select-from-files');
    if (selectNode) {
        selectNode.style.display = 'none';
    }
}