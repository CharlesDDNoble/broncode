function extract_test_data_from_row(row) {
    var id = row.id.split("-")[2];
    var data = {};

    data.id = id;
    data.command_line = $("#command-line-" + id).val();
    data.expected = $("#expected-" + id).val();
    data.hint = $("#hint-" + id).val();

    if ($("#number-" + id).length) { // check if element exists
        data.number = $("#number-" + id).val();
    } else {
        data.number = undefined;
    }

    return data;
}

var test_id = 1;
$(document).ready(function() {
    // if there are already tests, then the next id is the last test id + 1
    if ($("[id|=test-row]").length > 0) {
        var last_id = $("[id|=test-row]:last").attr("id");
        test_id = parseInt(last_id.split("-")[2]) + 1;
    }
});


function add_new_testcase() {
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
        </div>
    `);
    row.insertBefore("#add-test-wrapper").hide();
    row.slideDown();
    row.find("div .testinputdeletebtn").click(function(event) {
        row.slideUp("", function(event) {
            row.empty();
        });
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
