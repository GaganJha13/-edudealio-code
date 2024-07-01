$("#submit").prop('disabled', true);

function inputcheck() {
    if ($("#check-terms").prop("checked") && $("#username").val() && $("#email").val() && $("#password1").val() && $("#password2").val()) {
        return "send";
    }
}
$("#registration-box").on('mousedown, mouseup, hover, mouseover', function(){
    check = inputcheck()
    if (check === "send"){
        $("#submit").prop('disabled', false);
    }
    else {
        $("#submit").prop('disabled', true);
    };
});