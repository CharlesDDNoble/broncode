var test_id = 1;
$(document).ready(function() {
    // if there are already tests, then the next id is the last test id + 1
    if ($("[id|=test-row]").length > 0) {
        var last_id = $("[id|=test-row]:last").attr("id");
        test_id = parseInt(last_id.split("-")[2]) + 1;
    }
});


function remove_testcase_row(row) {
    row.slideUp("", function() {
        // row.empty();
        // defer deleting until submission
        row.find("[id|='was-deleted']").attr("value","true")
        row.hide();
    });
}

function add_testcase_row() {
    var row = $(`
        <div class="row testinputrow valign-wrapper" id="test-row-${test_id}">
            <div class="col s3 input-field">
                <input value="" type="text" id="command-line-${test_id}">
                <label for="command-line-${test_id}">Input (Optional)</label>
            </div>
            <div class="col s3 input-field">
                <input value="" type="text" id="expected-${test_id}" class="testcase-input-output"> 
                <label for="expected-${test_id}">Expected Output</label>
            </div>
            <div class="col s3 input-field">
                <input value="" type="text" id="hint-${test_id}">
                <label for="hint-${test_id}">Hint (Optional)</label>
            </div>
            <div class="col s3 center-align testinputdeletecol">
                <div class="btn red accent-4 testinputdeletebtn">
                <span>remove</span>
                </div>
            </div>
            <input type="hidden" id="number-${test_id}" value="${test_id}">
            <input type="hidden" id="is-new" value="true">
            <input type="hidden" id="was-deleted-${test_id}" value="false">
        </div>
    `);
    row.insertBefore("#add-test-wrapper").hide();
    row.slideDown();
    row.find("div .testinputdeletebtn").click(function() {
        remove_testcase_row(row);
    });
    test_id++;
}

function validate_input() {
    if ($('#lesson-name').val() == "") {
        M.toast({html: 'Lesson name cannot be blank.'})
        return false;
    }
    if ($('#textarea-markdown').val() == "") {
        M.toast({html: 'Markdown content cannot be blank.'})
        return false;
    }
    if ($('#select-language').val() == null) {
        M.toast({html: 'Please choose a language.'})
        return false;
    }
    if (cEditor.getValue() == "") {
        M.toast({html: 'Please provide some example code.'})
        return false;
    }
    expecteds = document.getElementsByClassName("testcase-input-output");
    for (var i in expecteds) {
        if (expecteds[i].value == "") {
            M.toast({html: 'Test cases require at least an expected output.'})
            return false;
        }
    }

    return true;
}


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

// determine api actions for all test cases
function handle_test_cases(lesson_id) {
    var testcases = $(".testinputrow");

    if (testcases.length != 0) {
        asyncs = [];

        $.each(testcases, function(idx, row) {
            jquery_row = $("#"+row.id);
            // if this test case is new --> is not in database yet
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

