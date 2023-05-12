// Text Box & Area
const textBox = document.querySelector('.text-box');
const textarea = textBox.querySelector('textarea');
label = textBox.querySelector('label');

// Event Listner For Text Box Activation
textarea.addEventListener('focus', () => {
    label.classList.add('active');
});

// Event Listener For Text Box Deactivation
textarea.addEventListener('blur', () => {
    if (!textarea.value) {
        label.classList.remove('active');
    }
});

// Text Box Entry View Expander
const textbox = document.querySelector('#text-box');
const observer2 = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) {
        textbox.classList.add('text-box--visible');
        observer2.unobserve(textbox);
    }
}, { threshold: 0.5 });
observer2.observe(textbox);