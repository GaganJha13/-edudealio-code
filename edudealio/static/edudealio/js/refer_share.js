$(document).ready(function() {
    $('#copyButton').click(function() {
        var referralLink = document.getElementById('referralLink');
        referralLink.select();
        
        try {
            // Attempt to copy the selected text to clipboard using the Clipboard API
            document.execCommand('copy');
            $(this).text('Copied!');
        } catch (err) {
            // Fallback to prompt user to copy the text manually
            prompt('Copy the link below:', referralLink.value);
        }

        setTimeout(function() {
            $('#copyButton').text('Copy');
        }, 1500);
    });
});