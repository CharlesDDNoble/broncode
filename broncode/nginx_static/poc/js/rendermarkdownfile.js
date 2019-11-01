// turns markdown into html
function renderMarkdown() {
    // console.log("Rendering markdown...")
    let container = $("#instructions")

    showdown.setFlavor('github');
    let converter = new showdown.Converter();

    container.html(converter.makeHtml(container.html()));

    // fix &lt; and &gt; in code blocks
    let codes = container.find("code");
    codes.each(function () {
        $(this).text(function(index, text) {
            return unescapeHTML(text);
        });
    });
}

//from https://stackoverflow.com/a/5302113
function unescapeHTML(escapedHTML) {
    return escapedHTML.replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');
}
