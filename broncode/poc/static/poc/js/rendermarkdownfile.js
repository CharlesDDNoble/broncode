function renderMarkdown() {
    console.log("Rendering markdown...")
    let container = $("#instructions")

    showdown.setFlavor('github');
    let converter = new showdown.Converter();

    container.innerHTML = converter.makeHtml(container.innerHTML);
}
