// ==========================================
// SCHEDULE DEMO DATA
// ==========================================

const scheduleData = [

    {
        activity: "Site Excavation",
        planned: "10 Aug 2026",
        actual: "10 Aug 2026",
        status: "Completed"
    },

    {
        activity: "Foundation Work",
        planned: "15 Aug 2026",
        actual: "18 Aug 2026",
        status: "Delayed"
    },

    {
        activity: "RCC Structure",
        planned: "25 Aug 2026",
        actual: "-",
        status: "In Progress"
    },

    {
        activity: "Electrical Installation",
        planned: "05 Sep 2026",
        actual: "-",
        status: "Upcoming"
    }

];


// ==========================================
// LOAD SCHEDULE
// ==========================================

function loadSchedule() {

    const tableBody =
        document.getElementById("scheduleTable");


    if (!tableBody) {

        return;

    }


    tableBody.innerHTML = "";


    scheduleData.forEach(function (activity) {

        const row = document.createElement("tr");


        row.innerHTML = `

            <td>${activity.activity}</td>

            <td>${activity.planned}</td>

            <td>${activity.actual}</td>

            <td>${activity.status}</td>

        `;


        tableBody.appendChild(row);

    });

}