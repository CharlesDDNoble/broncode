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

// delete lesson with id=lesson_id
function delete_lesson(lesson_id) {
    console.log("delete_lesson("+lesson_id+")");

    $.ajax({
        url : 'https://broncode.cs.wmich.edu/api/lessons/' + lesson_id, // the endpoint
        type : 'DELETE', // http method

        data : {}, // data sent with the post request
        dataType: 'json',
        // handle a successful response
        success : function(json) {
            M.toast({html: 'Lesson deleted!', classes: 'rounded green lighten-3'});
            $("#lesson_"+lesson_id+"_list").remove();
            $("#lesson_"+lesson_id+"_modal").remove();
            console.log(json);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            M.toast({html: 'There was an error deleting the lesson!', classes: 'rounded red lighten-3'});
            console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};


// Set up modal interactivity 
$(document).ready(function(){
    $('.modal').modal();
});

// set up ajax to use csrf_token
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});