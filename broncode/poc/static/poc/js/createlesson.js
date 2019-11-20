
// Set up modal interactivity 
$(document).ready(function(){
    $('.modal').modal();
});

function delete_lesson(lesson_id) {
    console.log("delete_lesson("+lesson_id+")");

    $.ajax({
        url : 'http://broncode.cs.wmich.edu/api/lessons/' + lesson_id, // the endpoint
        type : 'DELETE', // http method

        data : {}, // data sent with the post request
        dataType: 'json',
        // handle a successful response
        success : function(json) {
            $("#lesson_"+lesson_id+"_list").remove();
            $("#lesson_"+lesson_id+"_modal").remove();
            console.log(json);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};