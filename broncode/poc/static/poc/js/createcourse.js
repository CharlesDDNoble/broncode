// Submit post on submit
var d_user_id = -1 // django_user_id
var d_lesson_id = -1 // django_lesson_id

function loadDynamicData(user, lesson, code) {
    d_user_id = user;
    d_lesson_id = lesson;
}

$('#form-create-course').on('submit', function(event){
    event.preventDefault();
    $('#output-box').text("Running your code...");
    create_post();
});

// AJAX for posting
function create_post() {
    $.ajax({
        url : "http://broncode.cs.wmich.edu:1209/api/submissions/", // the endpoint
        type : "POST", // http method
        data : { 
            user : d_user_id,
            lesson : d_lesson_id,
            code : $('#codemirror').val(), 
            compiler_flags : $('#compiler-flags').val()
        }, // data sent with the post request
        dataType: "json",
        // handle a successful response
        success : function(json) {
	    //json.log = json.log.replace(/\n/g,"<br />")	
            console.log(json);
           $('#output-box').text(json['log']);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#output-box').text("errmsg");

            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

function resetExampleCode() {
    $.ajax({
        url : "http://broncode.cs.wmich.edu:1209/api/lessons/" + d_lesson_id,
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