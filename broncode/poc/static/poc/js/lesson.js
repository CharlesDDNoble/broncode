var d_user_id = -1 // django_user_id
var d_lesson_id = -1 // django_lesson_id
var BRONCODE_URL = "http://broncode.cs.wmich.edu"

function loadDynamicData(user, lesson, code) {
    d_user_id = user;
    d_lesson_id = lesson;
}

// AJAX for posting
function submitCodeForTesting() {
    $.ajax({
        url : BRONCODE_URL + "/api/submissions/",
        type : "POST", 
        data : { 
            user : d_user_id,
            lesson : d_lesson_id,
            code : $('#codemirror').val(), 
            compiler_flags : $('#compiler-flags').val(),
            user_tested : false
        },
        dataType: "json",
        // handle a successful response
        success : function(json) {
            console.log(json);
           $('#output-box').text(json['log']);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#output-box').text("errmsg");

            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function runTest() {
    // need to manually save the new code and stdin into their respective textareas
    // normally, this is done automatically upon form submit
    // but this button doesn't submit the form

    // editor is a globla variable defined in component-flags.html
    // cEditor is a global variable definied in component-codemirror.html
    editor.save();
    cEditor.save();
    $('#output-box').text("Running your code...");
    $.ajax({
        url : BRONCODE_URL + "/api/submissions/",
        type : "POST", 
        data : { 
            user : d_user_id,
            lesson : d_lesson_id,
            code : $('#codemirror').val(), 
            compiler_flags : $('#compiler-flags').val(),
            stdin : $('#stdin').val(),
            user_tested : true,
        },
        dataType: "json",
        // handle a successful response
        success : function(json) {
            console.log(json);
           $('#output-box').text(json['log']);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#output-box').text("errmsg");

            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function resetExampleCode() {
    $.ajax({
        url : BRONCODE_URL + "/api/lessons/" + d_lesson_id,
        type : "GET",
        success : function(json) {	
            // cEditor is the codemirror object
            cEditor.setValue(json.example_code)
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}


function add_try_buttons() {
    // try button html
    try_btn = "<div class=\"try-btn\" style=\"padding = .1 em;\"><a href=\"#!\" class=\"left waves-effect waves-light btn-small\">Try!</a></div>";
    
    // add buttons to code blocks... filter out katex  
    $('pre > code').not(".katex").append(try_btn);

    // set up button to send contents of code block to code mirror editor
    $('.try-btn').on('click', function() {
            code = $(this).parent().text();
            cEditor.setValue(code)
        }
    );
    $('.try-btn').hide();

    // set buttons to appear on hover
    $('pre').hover(
        function() {
            btn = $(this).find(".try-btn")
            btn.slideDown(200);
            btn.delay(1000)
        },
        function() {
            btn = $(this).find(".try-btn")
            btn.clearQueue();
            btn.delay(500);
            btn.slideUp(200);
        }
    );
}


$(document).ready(function (){
    $('#major-form').on('submit', function(event){
        event.preventDefault();
        $('#output-box').text("Testing your code...");
        submitCodeForTesting();
    });

    add_try_buttons()
});

$(function() {
    //adapted from code written by Github user @mjhea0 at https://github.com/realpython/django-form-fun

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
