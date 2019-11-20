$('#btn-create-lesson').on('click', function(event){
    event.preventDefault();
    create_lesson();
});

// AJAX for posting
function create_lesson() {
    console.log('create_lesson()');
    lesson_name = $('#lesson-name').val();
    textarea_markdown = $('#textarea-markdown').val();
    course_id = $('#course-id').val();
    lesson_number = $('#new-lesson-number').val();
    code = cEditor.getValue();
    selected_language = $("#select-language").val();

    $.ajax({
        url : 'http://broncode.cs.wmich.edu/api/lessons/', // the endpoint
        type : 'POST', // http method

        data : {
            title : lesson_name,
            course : course_id,
            number : lesson_number,
            markdown : textarea_markdown,
            example_code: code,
            language: selected_language

        }, // data sent with the post request
        dataType: 'json',
        // handle a successful response
        success : function(json) {
            window.location.replace('http://broncode.cs.wmich.edu/course/' + json.course);

            console.log(json);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

function delete_lesson(lesson_number) {
    console.log("delete_lesson("+lesson_number+")");

    $.ajax({
        url : 'http://broncode.cs.wmich.edu/api/lessons/' + lesson_number, // the endpoint
        type : 'DELETE', // http method

        data : {}, // data sent with the post request
        dataType: 'json',
        // handle a successful response
        success : function(json) {
            $("#list_"+lesson_number).remove();
            $("#delete_modal_"+lesson_number).remove();
            console.log(json);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

// AJAX for posting
function delete_course(course_id) {
    console.log(course_id);
    $.ajax({
        url : 'http://broncode.cs.wmich.edu/api/courses/' + course_id, // the endpoint
        type : 'DELETE', // http method
        dataType: 'json',

        // handle a successful response
        success : function(json) {
            $('#card-create-course').prev().hide('slow', function(){$('#card-create-course').prev().remove()});
            console.log(json);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

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
