$(document).ready(function() {
  // Handle hover events to show/hide the dropdown
  $('.customDropdown').hover(
    function() {
      $(this).find('.myDropdown').show()
      $(this).find('.dropdown-menu').addClass("moving-up");
    },
    function() {
      $(this).find('.myDropdown').hide();
      $(this).find('.dropdown-menu').removeClass("moving-up")
    }
  );
});

// moving text down animation
const down_animation = document.querySelectorAll('.moving-content-down')
const down_observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('moving-down')
        }
            else {
                entry.target.classList.remove('moving-down')
            }
        
        })
    },
    { threshold: 0.5
});
//
for (let i = 0; i < down_animation.length; i++) {
    const elements = down_animation[i];
    down_observer.observe(elements);
}
