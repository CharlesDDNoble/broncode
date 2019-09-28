// see https://dev.to/shoupn/javascript-fetch-api-and-using-asyncawait-47mp
async function getFileContents(file) {
    let response = await fetch(file);
    let contents = await response.text();
    return contents;
}

function renderMarkdownFile(path) {
    console.log("Rendering " + path);

    // grabs the html element containing the <script> tag invoking this function
    let container = document.currentScript.parentElement;

    // grab file contents...
    getFileContents(path)
    .then(function(text) {
        showdown.setFlavor('github');
        let converter = new showdown.Converter();

        // put in container we grabbed earlier
        container.innerHTML = converter.makeHtml(text); 
    },
    function(text) {
        console.error("Something went wrong in fetching the contents of " + path);
    });
}