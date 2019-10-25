function renderMarkdown() {
    console.log("Rendering markdown...")
    let container = $("#instructions")

    showdown.setFlavor('github');
    let converter = new showdown.Converter();

    container.html(converter.makeHtml(container.html()));
}
