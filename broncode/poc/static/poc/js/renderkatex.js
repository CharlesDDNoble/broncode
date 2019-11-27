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
    // HACK: katex generates two spans: mathml and katex-html. Not sure what katex-html is for, but
    // it displays unformatted expressions. Mark it as hidden vvvv
    // $(".katex-html").prop("hidden",true);
}
