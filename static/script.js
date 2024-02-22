let c = 3;

function onPlusButtonClick(inside_div) {
    let new_module_key_input = document.createElement("input");
    let new_module_value_input = document.createElement("input");

    new_module_key_input.id = c;
    new_module_value_input.id = c + 1;

    new_module_key_input.name = "module_key";
    new_module_value_input.name = "module_value";

    new_module_key_input.type = "text";
    new_module_value_input.type = "text";

    new_module_key_input.placeholder = "Item title";
    new_module_value_input.placeholder = "Item content";

    let new_plus_button = document.createElement("button");

    new_plus_button.type = "button";
    new_plus_button.classList.add("round");

    let new_span = document.createElement("span");

    new_span.innerText = '+';

    new_plus_button.appendChild(new_span);

    new_plus_button.addEventListener("click", function() {
        this.classList.add("hidden");
        onPlusButtonClick(inside_div);
    }, false);

    let new_div = document.createElement("div");

    new_div.appendChild(new_module_key_input);
    new_div.appendChild(new_module_value_input);
    new_div.appendChild(new_plus_button);

    inside_div.appendChild(new_div);
    c += 2;
}

function onSubmit(submit_button) {
    if (document.getElementsByName("title")[0].value === "" ||
        document.getElementsByName("header")[0].value === "" ||
        document.getElementsByName("qr_code_content")[0].value === "")
        return;

    submit_button.children[1].innerText = "Adding..."

    let inside_values = document.getElementsByName("inside_values")[0];

    for (let i = 1; i < c; i += 2) {
        let key = document.getElementById(String(i)).value.trim();
        let value = document.getElementById(String(i + 1)).value.trim();

        if (key.length === 0 || value.length === 0)
            continue;

        inside_values.value += `${key}:${value},`;
    }
}

// After DOM has been loaded.
document.addEventListener("DOMContentLoaded", function() {
    let inside_div = document.getElementsByClassName("inside")[0];
    let plus_button = document.getElementsByClassName("round")[0];

    plus_button.addEventListener("click", function() {
        this.classList.add("hidden");
        onPlusButtonClick(inside_div);
    }, false);

    let submit_button = document.getElementsByName("submit")[0];

    submit_button.addEventListener("click", function() {
        onSubmit(this);
    }, false)
});