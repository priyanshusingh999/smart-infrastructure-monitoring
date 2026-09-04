// ==========================================
// DASHBOARD DEMO DATA
// ==========================================

// Abhi backend nahi hai,
// isliye temporary data use kar rahe hain.

const dashboardData = {

    overallProgress: 68,

    totalActivities: 128,

    delayedActivities: 12,

    documents: 24

};


// ==========================================
// LOAD DASHBOARD
// ==========================================

function loadDashboard() {

    const progressValue = document.getElementById("progressValue");
    if (!progressValue) {
        return;
    }

    // Overall progress
    progressValue.textContent =
        dashboardData.overallProgress + "%";


    // Total activities
    document.getElementById("activityValue").textContent =
        dashboardData.totalActivities;


    // Delayed activities
    document.getElementById("delayValue").textContent =
        dashboardData.delayedActivities;


    // Documents
    document.getElementById("documentValue").textContent =
        dashboardData.documents;


    // Progress bar ki width
    document.getElementById("progressBar").style.width =
        dashboardData.overallProgress + "%";


    // Progress description
    document.getElementById("progressText").textContent =
        dashboardData.overallProgress +
        "% of the project has been completed.";

}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", loadDashboard);
} else {
    loadDashboard();
}