var BRONCODE_URL = "http://broncode.cs.wmich.edu"

// AJAX for posting
function edit_lesson() {
    lesson_name = $('#lesson-name').val();
    textarea_markdown = $('#textarea-markdown').val();
    course_id = $('#course-id').val();
    lesson_id = $('#lesson-id').val();
    lesson_number = $('#lesson-number').val();
    code = cEditor.getValue();
    selected_language = $('#select-language').val();
    textarea_compiler_flags = $('#compiler-flags').val();

    if (!validate_input()) {
        return false;
    }

    $.ajax({
        url : BRONCODE_URL + '/api/lessons/' + lesson_id + '/', // the endpoint
        type : 'PUT', // http method

        data : {
            title : lesson_name,
            course : course_id,
            number : lesson_number,
            markdown : textarea_markdown,
            compiler_flags : textarea_compiler_flags,
            example_code : code,
            language : selected_language

        }, // data sent with the post request
        dataType: 'json',
        // handle a successful response
        success : function(json) {
            handle_test_cases(lesson_id);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

    return true;
};

function finish_edit() {
    window.location.replace(BRONCODE_URL + '/course/' + $('#course-id').val());
}

$(function() {
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});

$(document).ready(function() {
    lesson_id = $("#lesson-id").val()

    document.getElementById("btn-hidden-test-add").onclick = function(event) {
        event.preventDefault();
        add_testcase_row();
    };

    $('#btn-edit-lesson').on('click', function(event){
        event.preventDefault();
        edit_lesson();
    });

    // rig current delete buttons to delete
    $(".testinputdeletebtn").click(function(event) {
        row = $(event.target).parents("[id|=test-row]");
        remove_testcase_row(row);
    });


    // Side navbar for mobile
    $('.sidenav').sidenav();

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
        renderKatex();
        // Markdown styling fixes -----------------------------------------
    
        // Make tables responsive to size of screen
        $("table").wrap("<div style=\"overflow-x: auto;\"></div>");

        // Style markdown list a bit better
        $("#preview-markdown ul").wrap("<div class=\"markdown-list\" style=\"padding-left: 2em;\"></div>");
        $(".markdown-list > ul > li").css("list-style-type","circle");
        // END Markdown styling fixes --------------------------------------
    }

    // INITIALIZE DEFAULT TEXTAREA
    /*
     * The reason this has to be done through a get request
     * rather than using the passing in `lesson` object
     * is because the markdown text contains codeblocks.
     * The code blocks start with backticks (`).
     * In javascript the backticks start a block string.
     * So for example 'this is a single line string'.
     * Meaning that I can just use single or double quotes.
     * But `this 
     * is a 
     * multiline
     * string`.
     * So codeblocks break the string since they themselves use
     * backticks.
     */
    $.ajax({
        url :  BRONCODE_URL + "/api/lessons/" + lesson_id,
        type : "GET",
        success : function(json) {  
            // cEditor is the codemirror object
            $('#textarea-markdown').val(json.markdown);
            renderTextarea($('#textarea-markdown'));
            M.textareaAutoResize($('#textarea-markdown'));
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });


    $("#textarea-markdown").on('change keyup paste', function() {
        renderTextarea("#textarea-markdown");
    });

    // Floating Action Button
    $('.fixed-action-btn').floatingActionButton();

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


    // INITIALIZE DEFAULT CODE AREA
    $.ajax({
        url :  BRONCODE_URL + "/api/lessons/" + lesson_id,
        type : "GET",
        success : function(json) {  
            // cEditor is the codemirror object
            // Define in component-codemirror as global variable
            cEditor.getDoc().setValue(json.example_code);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
});