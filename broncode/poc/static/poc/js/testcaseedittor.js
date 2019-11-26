function extract_test_data_from_row(row) {
    var id = row.id.split("_")[2];
    var data = {};

    data.id = id;
    data.command_line = $("#command_line_" + id).val();
    data.expected = $("#expected_" + id).val();
    data.hint = $("#hint_" + id).val();

    if ($("#number_" + id).length) { // check if element exists
        data.number = $("#number_" + id).val();
    } else {
        data.number = undefined;
    }

    return data;
}

var next_test_input_id = -1;
function add_new_testcase() {
    var handle = document.getElementById("tests-wrapper");

    var div = document.createElement("div");
    div.classList.add("row", "testinputrow");
    div.id = "test_row_" + next_test_input_id;

    var command_line = create_input_div(4, "command_line_" + next_test_input_id, "Command Line Arguments (Optional)");
    var expected = create_input_div(3, "expected_" + next_test_input_id, "Expected Output");
    var hint = create_input_div(4, "hint_" + next_test_input_id, "Hint Upon Failure (Optional)");
    
    var deletebuttoncol = document.createElement("div");
    deletebuttoncol.classList.add("col", "s1", "testinputdeletecol");
    var deletebutton = document.createElement("div");
    deletebutton.classList.add("btn", "testinputdeletebtn");
    var deletebuttontext = document.createElement("span");
    deletebuttontext.innerHTML = "remove";
    
    deletebutton.appendChild(deletebuttontext);
    deletebuttoncol.appendChild(deletebutton);
    
    div.appendChild(command_line);
    div.appendChild(expected);
    div.appendChild(hint);
    div.appendChild(deletebuttoncol);
    
    deletebutton.onclick = function() {
        this.parentElement.parentElement.remove();
    };
    
    next_test_input_id--;
    handle.appendChild(div);
}

function create_input_div(size, id, label) {
    var div = document.createElement("div");
    div.classList.add("col", "s" + size, "input-field");

    var input = document.createElement("input");
    input.type = "text";
    input.placeholder = "";
    input.id = id;

    var labelElem = document.createElement("label");
    labelElem.innerHTML = label;

    div.appendChild(input);
    div.appendChild(labelElem);
    
    return div;
}
