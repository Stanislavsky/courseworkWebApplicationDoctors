"use strict";
const elem = document.querySelector(".btn");
elem.addEventListener("click", function(e)
{
    e.preventDefault();
    window.location.href = 'index.html';
});

