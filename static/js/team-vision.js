// Our Vision 
const visionSection = document.querySelector('#vision-section');
const observer = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) {
        visionSection.classList.add('vision-section--visible');
        observer.unobserve(visionSection);
    }
}, { threshold: 0.2 });
observer.observe(visionSection);

// Scroll Animation
$(window).scroll(function () {
    console.log("Scrolling detected"); // Add this line to check if the script is running
    $('.wrap').addClass('show');
});