"use strict";

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('downloadBtn').addEventListener('click', function() {
        const paragraphs = document.querySelectorAll('p');
        let textContent = '';
        paragraphs.forEach(p => {
            textContent += p.innerText + '\n';
        });

        const blob = new Blob([textContent], { type: 'text/plain' });
        const anchor = document.createElement('a');
        anchor.href = URL.createObjectURL(blob);
        anchor.download = 'questionnaire.txt';
        anchor.click();
    });
    
});




document.addEventListener("DOMContentLoaded", function() {
    var button = document.getElementById('toggleDoctorButton');
    var doctorList = document.getElementById('doctorList');

    button.addEventListener('click', function() {
        if (doctorList.style.display === 'none' || doctorList.style.display === '') {
            doctorList.style.display = 'block';
        } else {
            doctorList.style.display = 'none';
        }
    });
});

