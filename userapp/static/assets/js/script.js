// Script to handle navbar transparency on scroll
window.onscroll = function () {
    var nav = document.querySelector('.navbar');
    if (window.pageYOffset > 50) {
        nav.style.background = "#0056b3";
        nav.style.boxShadow = "0 2px 10px rgba(0,0,0,0.1)";
    } else {
        nav.style.background = "transparent";
        nav.style.boxShadow = "none";
    }
};


// Animation
document.addEventListener("DOMContentLoaded", function () {

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            } else {
                // This resets the animation when the user scrolls away
                entry.target.classList.remove('active');
            }
        });
    }, {
        threshold: 0.1 // Triggers when 10% of the element is visible
    });

    // Target all elements with the .reveal class
    const hiddenElements = document.querySelectorAll('.reveal');

    // Loop through and observe each element
    hiddenElements.forEach((el) => {
        observer.observe(el);
    });

});
document.addEventListener("DOMContentLoaded", function () {

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            } else {
                // Removes active class so it re-animates next time you scroll back
                entry.target.classList.remove('active');
            }
        });
    }, {
        threshold: 0.1
    });

    // Select both .reveal and .rock-item elements
    const animateElements = document.querySelectorAll('.reveal, .rock-item');

    animateElements.forEach((el) => {
        observer.observe(el);
    });

});