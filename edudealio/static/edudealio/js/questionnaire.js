$(document).ready(function() {
    // Show advertisement bar
    $('.advertisement-bar').slideDown();
  
    // Close button functionality
    $('.close-btn').on('click', function(e) {
      e.preventDefault();
      $('.advertisement-bar').slideUp();
    });
});