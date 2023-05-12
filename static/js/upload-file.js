// Auto-submission
document.getElementById("upload-form").onchange = function () {
    // submitting the form
    document.getElementById("upload-form").submit();
};

// File box & upload
const fileBox = document.querySelector('.file-box');
const fileUpload = document.querySelector('#file-upload');

// Drag over event handler
fileBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileBox.classList.add('highlight');
});

// Drag leave event handler
fileBox.addEventListener('dragleave', () => {
    fileBox.classList.remove('highlight');
});

// Drop event handler
fileBox.addEventListener('drop', (e) => {
    e.preventDefault();
    fileBox.classList.remove('highlight');
    const files = e.dataTransfer.files;
    fileUpload.files = files;
    document.getElementById("upload-form").submit(); // auto-submit the form on drop
});

// Submit event handler
const uploadForm = document.querySelector('#upload-form');
uploadForm.addEventListener('submit', (e) => {
    if (fileUpload.files.length === 0) {
        e.preventDefault();
        alert('Please select a file to upload.');
    }
});