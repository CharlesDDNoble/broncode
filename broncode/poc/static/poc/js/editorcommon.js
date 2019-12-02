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

var next_test_input_id = 1;
function add_new_testcase() {
    var handle = document.getElementById("tests-wrapper");

    var div = document.createElement("div");
    div.classList.add("row", "testinputrow", "valign-wrapper");
    div.id = "test-row-" + next_test_input_id;

    var command_line = create_input_div(3, "command_line-" + next_test_input_id, "Input (Optional)");
    var expected = create_input_div(3, "expected-" + next_test_input_id, "Expected Output", "testcase-input-output");
    var hint = create_input_div(3, "hint-" + next_test_input_id, "Hint (Optional)");
    
    var deletebuttoncol = document.createElement("div");
    deletebuttoncol.classList.add("col", "s3", "testinputdeletecol", "center-align");
    var deletebutton = document.createElement("div");
    deletebutton.classList.add("btn", "testinputdeletebtn", "red", "accent-4");
    var deletebuttontext = document.createElement("span");
    deletebuttontext.innerHTML = "remove";
    
    var add_test_wrapper = document.getElementById("add-test-wrapper"); 

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
    handle.insertBefore(div,add_test_wrapper);
}

function create_input_div(size, id, label, cls = "") {
    var div = document.createElement("div");
    div.classList.add("col", "s" + size, "input-field");

    var input = document.createElement("input");
    input.type = "text";
    input.placeholder = "";
    input.id = id;

    if (cls != "") {
        input.classList.add(cls);
    }

    var labelElem = document.createElement("label");
    labelElem.innerHTML = label;

    div.appendChild(input);
    div.appendChild(labelElem);
    
    return div;
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
