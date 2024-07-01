$("#submit").prop('disabled', true);

function inputcheck() {
    if ($("#username").val() && $("#password").val()) {
        return "send";
    }
}
$("#login-box").on('mousedown, mouseup, hover, mouseover', function(){
    check = inputcheck()
    if (check === "send"){
        $("#submit").prop('disabled', false);
    }
    else {
        $("#submit").prop('disabled', true);
    };
});