function renderKatex() {
    var elements = $(".language-katex");
    for (var i = 0; i < elements.length; i++) {
        var ele = elements[i]
        var text = ele.innerText;
        ele.innerText = "";
        katex.render(text, ele, {
            throwOnError: false
        });
    }
}
