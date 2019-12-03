var BRONCODE_URL = "http://broncode.cs.wmich.edu"

function create_lesson() {
    lesson_name = $('#lesson-name').val();
    textarea_markdown = $('#textarea-markdown').val();
    course_id = $('#course-id').val();
    lesson_number = $('#new-lesson-number').val();
    code = cEditor.getValue();
    selected_language = $('#select-language').val();
    textarea_compiler_flags = $('#compiler-flags').val();
    lesson_id = "";

    if (!validate_input()) {
        return false;
    }

    $.ajax({
        url : BRONCODE_URL + '/api/lessons/', // the endpoint
        type : 'POST', // http method

        data : {
            title : lesson_name,
            course : course_id,
            number : lesson_number,
            markdown : textarea_markdown,
            compiler_flags: textarea_compiler_flags,
            example_code: code,
            language: selected_language

        }, // data sent with the post request
        dataType: 'json',
        // handle a successful response
        success : function(json) {
            lesson_id = json.id;
            create_test_cases(lesson_id);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

    return true;
};


function post_test_case(idx, jquery_row) {
    test_id = jquery_row.attr("id").split("-")[2];
    input = jquery_row.find("[id|='command-line']");
    output = jquery_row.find("[id|='expected']");
    hint = jquery_row.find("[id|='hint']");

    return $.ajax({
        url : BRONCODE_URL + '/api/solutionsets/', // the endpoint
        type : 'POST', // http method
        data : {
            "stdin": input,
            "stdout": output,
            "hint": hint,
            "lesson": $('#lesson-id').val(),
            "number": test_id
        },
        dataType: 'json',
        // handle a non-successful response
        success : function(json) {
            //
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function update_test_case(idx, jquery_row) {
    test_id = jquery_row.attr("id").split("-")[2];
    input = jquery_row.find("[id|='command-line']");
    output = jquery_row.find("[id|='expected']");
    hint = jquery_row.find("[id|='hint']");
    
    return $.ajax({
        url :  BRONCODE_URL + "/api/solutionsets/" + test_id + "/",
        type : "PUT",
        data : {
            "stdin": input,
            "stdout": output,
            "hint": hint,
            "lesson": $('#lesson-id').val(),
            "number": test_id
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function delete_test_case(idx, jquery_row) {
    return $.ajax({
        test_id = jquery_row.attr("id").split("-")[2];
        url :  BRONCODE_URL + "/api/solutionsets/" + test_id,
        type : "DELETE",
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function handle_test_cases(lesson_id) {
    var testcases = $(".testinputrow");

    if (testcases.length != 0) {
        asyncs = [];

        $.each(testcases, function(idx, row) {
            jquery_row = $("#"+row.id);
            if (jquery_row.find("[id|='is-new']").val() === "true") {
                if (jquery_row.find("[id|='was-deleted']").val() === "false") {
                    action = post_test_case(idx,jquery_row);
                } else {
                    // since its not in the database yet, just delete it
                    jquery_row.empty();
                }
            } else { // is old test case --> already in database
                if (jquery_row.find("[id|='was-deleted']").val() === "false") {
                    action = update_test_case(idx,jquery_row);
                } else {
                    action = delete_test_case(idx,jquery_row);
                    jquery_row.empty();
                }
            }
            asyncs.push(action);
        });

        // wait for all requests to be done
        // https://stackoverflow.com/questions/5627284/pass-in-an-array-of-deferreds-to-when
        $.when.apply($, asyncs).then(function() {
            finish_create();
        });
    } else {
        // no test cases to add, just finish up
        finish_create();
    }
}

function finish_create() {
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


$(document).ready(function(){
    // for some reason, using jquery syntax causes the event to fire twice.
    document.getElementById("btn-create-lesson").onclick = function(event) {
        event.preventDefault();
        create_lesson();
    };

    document.getElementById("btn-hidden-test-add").onclick = function(event) {
        event.preventDefault();
        add_new_testcase();
    };

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
        // Markdown styling fixes -----------------------------------------
    
        // Make tables responsive to size of screen
        $("table").wrap("<div style=\"overflow-x: auto;\"></div>");

        // Style markdown list a bit better
        $("#preview-markdown ul").wrap("<div class=\"markdown-list\" style=\"padding-left: 2em;\"></div>");
        $(".markdown-list > ul > li").css("list-style-type","circle");
        // END Markdown styling fixes --------------------------------------
    });



    // Floating Action Button
    $('.fixed-action-btn').floatingActionButton();

    // Set compiler flag options
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
