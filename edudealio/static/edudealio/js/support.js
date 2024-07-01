
$(document).ready(function() {
    $("#contactForm").submit(function(event) {
        event.preventDefault();

        // Disable the send button
        $("#sendMessageBtn").prop("disabled", true);

        var name = $("#name").val();
        var email = $("#email").val();
        var subject = $("#subject").val();
        var message = $("#message").val();

        // Basic validation
        if (name === '' || email === '' || subject === '' || message === '') {
            $("#formMessage").text("Please fill in all fields.").css("color", "red");
            // Re-enable the send button
            $("#sendMessageBtn").prop("disabled", false);
        } else {
            // AJAX request to handle form submission
            $.ajax({
                type: "POST",
                url: "/support",
                data: {
                    name: name,
                    email: email,
                    subject: subject,
                    message: message,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(response) {
                    $("#formMessage").text("Message sent successfully!").css("color", "green");
                    $("#contactForm")[0].reset();
                },
                error: function(error) {
                    $("#formMessage").text("Error sending message.").css("color", "red");
                },
                complete: function() {
                    // Re-enable the send button after completion (success or error)
                    $("#sendMessageBtn").prop("disabled", false);
                }
            });
        }
    });
});