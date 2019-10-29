// turns markdown into html
function renderMarkdown(html_id) {
    // console.log("Rendering markdown...")

    container = $(html_id)

    showdown.setFlavor('github');
    converter = new showdown.Converter();

    container.each(function() { container.html(converter.makeHtml(container.html())); });

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
