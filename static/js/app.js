// ==========================================
// PROJECTAI FRONTEND
// ==========================================


// Backend ka future URL
// Abhi use nahi ho raha.

const API_BASE_URL =
    "http://localhost:8000/api";


// ==========================================
// WEBSITE START
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "ProjectAI Frontend Started"
        );


        // Dashboard load
        if (typeof loadDashboard === "function") loadDashboard();


        // Schedule load
        if (typeof loadSchedule === "function") loadSchedule();


        // Risks load
        if (typeof loadRisks === "function") loadRisks();


        // Progress load
        if (typeof loadProgress === "function") loadProgress();


        // Assistant load
        if (typeof loadAssistant === "function") loadAssistant();


        // Documents load
        if (typeof loadDocuments === "function") loadDocuments();


        // Navigation load
        if (typeof loadNavigation === "function") loadNavigation();


        // Upload load
        if (typeof loadUpload === "function") loadUpload();

        

    }
);