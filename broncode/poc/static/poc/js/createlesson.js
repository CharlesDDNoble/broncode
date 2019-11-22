function validate_rmarkdown(input) {
    valid_regex = /(output:)(.|\n){0,}(html_document:)(.|\n){0,}((theme: null)|(css: null)){1}(.|\n){0,}((theme: null)|(css: null)){1}/;
    send_btn = $("#btn-create-lesson")
    if (valid_regex.test(input)) {
    } else {
        M.toast({html: 'Invalid template for RMarkdown!', classes: 'rounded red lighten-3'});
        M.toast({html: 'RMarkdown template must include:\noutput:\n\thtml_document:\n\t\tcss: null\n\t\ttheme: null', classes: 'rounded red lighten-3'});
    }
}

$(document).ready(function(){
    $('.sidenav').sidenav();
    // $('#login').attr('class', 'waves-effect waves-light btn-small brown');
    // $('#navbar-username').css("color", "rgb(132,108,99)");

    // Render the tabs
    $('.tabs').tabs({
        swipeable: true
    });

    // Render select
    $('select').formSelect();

    // Render markdown realtime
    function renderTextarea(textarea_id) {
        $("#preview-markdown").html($(textarea_id).val());
        renderMarkdownClass("#preview-markdown");
    }

    $("#textarea-markdown").on('change keyup paste', function() {
        renderTextarea("#textarea-markdown");
        renderKatex();
    });

    // Floating Action Button
    $('.fixed-action-btn').floatingActionButton();

    // Set comiler flag options
    editor.setSize('100%', '5vh');
    
    // Set codemirror size (Variable declared in `component-codemirror.html`)
    cEditor.setSize('100%', '70vh');

    // Grabbing input file
    // Reference: https://stackoverflow.com/questions/31746837/reading-uploaded-text-file-contents-in-html
    $('#input-file').change(getFile);

    function getFile(event) {
        const input = event.target;
        if ('files' in input && input.files.length > 0) {
            placeFileContent($('#textarea-markdown'), input.files[0]);
        }
    }

    function placeFileContent(target, file) {
        readFileContent(file).then(content => {
            console.log(content);
            $(target).val(content);
            var textarea = target;
            renderTextarea(textarea);
            M.textareaAutoResize($(target));
        }).catch(error => console.log(error))
    }

    function readFileContent(file) {
        const reader = new FileReader()
        return new Promise((resolve, reject) => {
            reader.onload = event => resolve(event.target.result);
            reader.onerror = error => reject(error);
            reader.readAsText(file);
        })
    }

});