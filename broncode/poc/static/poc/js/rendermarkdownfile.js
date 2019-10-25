function renderMarkdown() {
    let container = $("#instructions")

    showdown.setFlavor('github');
    let converter = new showdown.Converter();

    container.innerHTML = converter.makeHtml(text);
}
