// turns markdown into html
function renderMarkdown(html_id) {
    // console.log("Rendering markdown...")
    let container = $(html_id)

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

// turns markdown into html
function renderMarkdownClass(html_class) {
    // console.log("Rendering markdown...")
    classes = $(html_class)

    showdown.setFlavor('github');
    let converter = new showdown.Converter();

    classes.each(function() {
        $(this).html(converter.makeHtml($(this).html()));
    });

    // fix &lt; and &gt; in code blocks
    let codes = classes.find("code");
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
