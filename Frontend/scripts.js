document.getElementById('submit-button').addEventListener('click', function() {
    let textBox = document.getElementById('text-box');
    let imageUpload = document.getElementById('image-upload');

    if ((textBox.value !== '' && imageUpload.files.length === 0) || (textBox.value === '' && imageUpload.files.length > 0)) {
        let section = document.createElement('div');
        section.classList.add('section');

        if (textBox.value !== '') {
            let textArea = document.createElement('p');
            textArea.textContent = textBox.value;
            section.appendChild(textArea);
        }

        if (imageUpload.files.length > 0) {
            let image = document.createElement('img');
            image.src = URL.createObjectURL(imageUpload.files[0]);
            section.appendChild(image);
        }

        document.body.appendChild(section);

        textBox.value = '';
        imageUpload.value = '';
    } else {
        // Display an error message or take appropriate action
        alert("Choose only one option (text or image).");
    }
});