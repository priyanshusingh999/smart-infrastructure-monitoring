// ==========================================
// DOCUMENT UPLOAD
// ==========================================


// Selected file ko store karne ke liye variable
let selectedFile = null;


// File input
const fileInput =
    document.getElementById("fileInput");


// Choose file button
const chooseFile =
    document.getElementById("chooseFile");


// Scan button
const scanButton =
    document.getElementById("scanBtn");


// Upload area
const dropArea =
    document.getElementById("dropArea");

if (!fileInput || !chooseFile || !scanButton || !dropArea) {
    // Upload controls are only present on the documents page.
} else {


// ==========================================
// CHOOSE FILE BUTTON
// ==========================================

chooseFile.addEventListener("click", function () {

    // Hidden file input open hoga
    fileInput.click();

});


// ==========================================
// FILE SELECTED
// ==========================================

fileInput.addEventListener("change", function () {

    const file = fileInput.files[0];

    if (file) {

        handleFile(file);

    }

});


// ==========================================
// HANDLE FILE
// ==========================================

function handleFile(file) {

    selectedFile = file;


    // File information show karo
    document
        .getElementById("fileInfo")
        .classList.remove("hidden");


    // File name
    document.getElementById("fileName").textContent =
        file.name;


    // File size
    document.getElementById("fileSize").textContent =
        (file.size / 1024).toFixed(2) + " KB";

}


// ==========================================
// DRAG OVER
// ==========================================

dropArea.addEventListener("dragover", function (event) {

    event.preventDefault();

    dropArea.classList.add("drag");

});


// ==========================================
// DRAG LEAVE
// ==========================================

dropArea.addEventListener("dragleave", function () {

    dropArea.classList.remove("drag");

});


// ==========================================
// DROP FILE
// ==========================================

dropArea.addEventListener("drop", function (event) {

    event.preventDefault();

    dropArea.classList.remove("drag");


    const file = event.dataTransfer.files[0];


    if (file) {

        handleFile(file);

    }

});


// ==========================================
// SCAN DOCUMENT
// ==========================================

scanButton.addEventListener("click", function () {

    // File select nahi hai
    if (!selectedFile) {

        alert("Please select a document first.");

        return;

    }


    // Processing section show karo
    document
        .getElementById("processing")
        .classList.remove("hidden");


    // Scan button temporarily disable
    scanButton.disabled = true;


    // Demo ke liye 2 seconds wait
    setTimeout(function () {

        // Processing hide
        document
            .getElementById("processing")
            .classList.add("hidden");


        // Result show
        document
            .getElementById("result")
            .classList.remove("hidden");


        // Button enable
        scanButton.disabled = false;


    }, 2000);

});

}