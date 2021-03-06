// Submit post on submit
var d_user_id = -1 // django_user_id
var d_lesson_id = -1 // django_lesson_id
var BRONCODE_URL = "https://broncode.cs.wmich.edu"

function loadDynamicData(user, lesson, code) {
    d_user_id = user;
    d_lesson_id = lesson;
}

// AJAX for posting
function create_course() {
    var course_name = $("#course-name").val();

    // validate input on course form    
    if ($("#course-name").val() === "") {
        M.toast({html: 'Course name must not be blank!', classes: 'rounded red lighten-3'});
        return;
    }

    // var course_lang = $("#course-language").val();
    console.log(course_name);

    $.ajax({
        url : BRONCODE_URL + "/api/courses/", // the endpoint
        type : "POST", // http method
        data : {
            title : course_name
            // title : course_lang
        }, // data sent with the post request
        dataType: "json",
        // handle a successful response
        success : function(json) {
            // Since the card will not exist unless the page is refreshed, add it
            $(`
                <div id="course_`+json.id+`_card" class="col s12 m6 l4">
                    <div class="card small blue-grey darken-4">
                        <div class="card-content white-text">
                            <span class="card-title">` + json.title + `</span>
                            <p></p>
                        </div>
                        <div class="card-action">
                            <a class="waves-effect waves-light btn-flat" href="` + json.id + `/">Lessons</a>
                            <!-- Modal Trigger -->
                            <button data-toggle="modal" data-target="course_`+json.id+`_modal" class="waves-effect waves-light modal-trigger right btn-flat red-text">Delete</button>
                        </div>
                    </div>
                </div>
                `
            ).insertBefore("#card-create-course").hide().show("slow");
            $(`
                <!-- Modal For Lesson Deletion -->
                <div id="course_`+json.id+`_modal" class="modal">
                    <div class="modal-content">
                        <h4>Delete Lesson</h4>
                        <p>Are you sure you want to delete this course?</p>
                        </div><div class="modal-footer">
                        <a href="#!" class="modal-close waves-effect waves-green btn-flat">Cancel</a>
                        <a href="#!" onclick="delete_course(`+json.id+`)" class="modal-close waves-effect waves-green btn-flat">Delete</a>
                    </div>
                </div>
            `).insertAfter("#course_"+json.id+"_card").hide()
            $('.modal').modal();
            console.log(json);
            // window.location.replace("http://broncode.cs.wmich.edu/course/"+json.id);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

// delete course with id=course_id
function delete_course(course_id) {
    console.log("delete_course("+course_id+")");

    $.ajax({
        url : BRONCODE_URL + '/api/courses/' + course_id, // the endpoint
        type : 'DELETE', // http method

        data : {}, // data sent with the post request
        dataType: 'json',
        // handle a successful response
        success : function(json) {
            $("#course_"+course_id+"_modal").remove();
            $("#course_"+course_id+"_card").hide("slow", 
                function() {
                    $("#course_"+course_id+"_card").remove()
                    M.toast({html: 'Course deleted!', classes: 'rounded green lighten-3'});
                }
            );
            console.log(json);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            M.toast({html: 'There was an error deleting the course!', classes: 'rounded red lighten-3'});
            console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

$(document).ready(function(){
    // submit on button press
    $('#btn-create-course').on('click', function(event){
        event.preventDefault();
        create_course();
    });

    // submit on 'enter'
    $("#course-name").keypress(function(event){
        if (event.which === 13) {
            event.preventDefault();
            create_course();
        }
    });
});

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
