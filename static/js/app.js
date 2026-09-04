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
        loadDashboard();


        // Schedule load
        loadSchedule();


        // Risks load
        loadRisks();


        // Progress load
        loadProgress();


        // Assistant load
        loadAssistant();


        // Documents load
        loadDocuments();


        // Navigation load
        loadNavigation();


        // Upload load
        loadUpload();

        

    }
);