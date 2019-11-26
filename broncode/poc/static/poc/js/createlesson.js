var BRONCODE_URL = "http://broncode.cs.wmich.edu:8080"

function create_lesson() {
    lesson_name = $('#lesson-name').val();
    textarea_markdown = $('#textarea-markdown').val();
    course_id = $('#course-id').val();
    lesson_number = $('#new-lesson-number').val();
    code = cEditor.getValue();
    selected_language = $('#select-language').val();
    textarea_compiler_flags = $('#compiler-flags').val();
    lesson_id = "";

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
            console.log(json);
            lesson_id = json.id;
            create_test_cases(lesson_id);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

function create_test_cases(lesson_id) {
    var testcases = $(".testinputrow");

    if (testcases.length != 0) {
        asyncs = [];
        $.each(testcases, function(idx, row) {
            var data = extract_test_data_from_row(row);
            waitfor = $.ajax({
                url : BRONCODE_URL + '/api/solutionsets/', // the endpoint
                type : 'POST', // http method
        
                data : {
                    number: idx + 1,
                    lesson: lesson_id,
                    stdin: data.command_line,
                    stdout: data.expected,
                    hint: data.hint
                }, // data sent with the post request
                dataType: 'json',
                // handle a non-successful response
                success : function(json) {
                    //
                },
                error : function(xhr,errmsg,err) {
                    console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
                }
            });
            asyncs.push(waitfor);
        });
        // wait for all requests to be done
        // https://stackoverflow.com/questions/5627284/pass-in-an-array-of-deferreds-to-when
        $.when.apply($, asyncs).then(function() {
            finish();
        });
    } else {
        // no test cases to add, just finish up
        finish();
    }
}

function finish() {
    window.location.replace(BRONCODE_URL + '/course/' + $('#course-id').val());
}

function extract_test_data_from_row(row) {
    var id = row.id.split("_")[2];
    var data = {};

    data.command_line = $("#command_line_" + id).val();
    data.expected = $("#expected_" + id).val();
    data.hint = $("#hint_" + id).val();

    return data;
}

var next_test_input_id = 0;
function add_new_testcase() {
    var handle = document.getElementById("tests-wrapper");

    var div = document.createElement("div");
    div.classList.add("row", "testinputrow");
    div.id = "test_row_" + next_test_input_id;

    var command_line = create_input_div(4, "command_line_" + next_test_input_id, "Command Line Arguments (Optional)");
    var expected = create_input_div(3, "expected_" + next_test_input_id, "Expected Output");
    var hint = create_input_div(4, "hint_" + next_test_input_id, "Hint Upon Failure (Optional)");
    
    var deletebuttoncol = document.createElement("div");
    deletebuttoncol.classList.add("col", "s1", "testinputdeletecol");
    var deletebutton = document.createElement("div");
    deletebutton.classList.add("btn", "testinputdeletebtn");
    var deletebuttontext = document.createElement("span");
    deletebuttontext.innerHTML = "remove";
    
    deletebutton.appendChild(deletebuttontext);
    deletebuttoncol.appendChild(deletebutton);
    
    div.appendChild(command_line);
    div.appendChild(expected);
    div.appendChild(hint);
    div.appendChild(deletebuttoncol);
    
    deletebutton.onclick = function() {
        this.parentElement.parentElement.remove();
    };
    
    next_test_input_id++;
    handle.appendChild(div);
}

function create_input_div(size, id, label) {
    var div = document.createElement("div");
    div.classList.add("col", "s" + size, "input-field");

    var input = document.createElement("input");
    input.type = "text";
    input.placeholder = "";
    input.id = id;

    var labelElem = document.createElement("label");
    labelElem.innerHTML = label;

    div.appendChild(input);
    div.appendChild(labelElem);
    
    return div;
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
