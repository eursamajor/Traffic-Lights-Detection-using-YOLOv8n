document.getElementById('browse-link').addEventListener('click', function (e) {
    e.preventDefault();
    document.getElementById('file-input').click();
});

document.getElementById('file-input').addEventListener('change', handleFiles);

document.getElementById('drop-area').addEventListener('dragover', (event) => {
    event.preventDefault();
    document.getElementById('drop-area').classList.add('drag-over');
});

document.getElementById('drop-area').addEventListener('dragleave', (event) => {
    document.getElementById('drop-area').classList.remove('drag-over');
});

document.getElementById('drop-area').addEventListener('drop', (event) => {
    event.preventDefault();
    document.getElementById('drop-area').classList.remove('drag-over');
    handleFiles(event.dataTransfer);
});

document.getElementById('clear-btn').addEventListener('click', function (e) {
    e.preventDefault();
    document.getElementById('file-input').value = '';
    document.getElementById('preview-video').src = '';
    document.getElementById('preview-video').style.display = 'none';
    document.getElementById('result-video').src = '';
});

document.getElementById('scan-btn').addEventListener('click', function (e) {
    e.preventDefault();
    const previewVideoSrc = document.getElementById('preview-video').src;

    if (!previewVideoSrc) {
        alert("No video selected. Please upload or drag a video file.");
        return;
    }

    const form = document.querySelector('form');
    form.submit();
});

function handleFiles(files) {
    if (files instanceof DataTransfer) {
        files = files.files;
    } else {
        files = files.target.files;
    }

    if (files.length > 0) {
        const file = files[0];
        const reader = new FileReader();
        reader.onload = function (event) {
            const videoPreview = document.getElementById('preview-video');
            const imgPreview = document.getElementById('preview-img');

            // Set video source and display it
            videoPreview.style.display = 'block';
            videoPreview.src = event.target.result;

            // Hide image preview
            imgPreview.style.display = 'none';
        };
        reader.readAsDataURL(file);
    }
}
