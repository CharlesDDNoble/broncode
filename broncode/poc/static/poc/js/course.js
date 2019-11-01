// Submit post on submit
var d_user_id = -1 // django_user_id
var d_lesson_id = -1 // django_lesson_id

function loadDynamicData(user, lesson, code) {
    d_user_id = user;
    d_lesson_id = lesson;
}

$('#btn-create-course').on('click', function(event){
    event.preventDefault();
    create_course();
});

// $('#btn-delete-course').on('click', function(event){
//     event.preventDefault();
//     delete_course();
// });

// AJAX for posting
function create_course() {
    var course_name = $("#course-name").val();

    $.ajax({
        url : "http://broncode.cs.wmich.edu:1234/api/courses/", // the endpoint
        type : "POST", // http method
        data : {
            title: course_name
        }, // data sent with the post request
        dataType: "json",
        // handle a successful response
        success : function(json) {
            $(`
                <div class="col s12 m6 l4">
                    <div class="card small blue-grey darken-1">
                        <div class="card-content white-text">
                            <span class="card-title">` + json.title + `</span>
                            <p></p>
                        </div>
                        <div class="card-action">
                            <a href="/course/` + json.id + `">Lessons</a>
                            <!-- Modal Trigger -->
                            <a class="waves-effect waves-light modal-trigger right" href="#modal2">Delete</a>

                            <!-- Modal Structure -->
                            <div id="modal2" class="modal">
                                <div class="modal-content">
                                    <h4>Confirmation</h4>
                                    <h6>Are you sure you want to delete?</h6>
                                </div>
                                <div class="modal-footer">
                                    <a href="#!" id="btn-cancel-course" class="modal-close waves-effect waves-green btn">Cancel</a>
                                    <a href="#!" class="modal-close waves-effect waves-green btn red">Delete</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                `
            ).insertBefore("#card-create-course").hide().show("slow");

            console.log(json);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

// AJAX for posting
function delete_course(course_id) {
    alert(course_id);
    $.ajax({
        url : "http://broncode.cs.wmich.edu:1234/api/courses/" + course_id, // the endpoint
        type : "DELETE", // http method
        dataType: "json",
        // handle a successful response
        success : function(json) {
            $("#card-create-course").prev().remove();
            console.log(json);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
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
