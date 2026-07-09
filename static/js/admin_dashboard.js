document.addEventListener("DOMContentLoaded", function () {

    const dataEl = document.getElementById("dashboard-data");
    if (!dataEl) {
        console.error("Dashboard data not found");
        return;
    }

    const DASHBOARD_DATA = JSON.parse(dataEl.textContent);

    // USERS CHART
    const usersChart = document.getElementById("usersChart");
    if (usersChart) {
        new Chart(usersChart, {
            type: "doughnut",
            data: {
                labels: ["Total Users", "Registered Today"],
                datasets: [{
                    data: [
                        DASHBOARD_DATA.totalUsers,
                        DASHBOARD_DATA.todayUsers
                    ],
                    backgroundColor: ["#00e676", "#00b0ff"]
                }]
            },
            options: {
                plugins: {
                    legend: {
                        labels: { color: "white" }
                    }
                }
            }
        });
    }

    // LOGIN CHART
    const loginChart = document.getElementById("loginChart");
    if (loginChart) {
        new Chart(loginChart, {
            type: "bar",
            data: {
                labels: ["Successful Logins", "Failed Logins"],
                datasets: [{
                    data: [
                        DASHBOARD_DATA.successLogins,
                        DASHBOARD_DATA.failedLogins
                    ],
                    backgroundColor: ["#43cea2", "#ff8a80"]
                }]
            },
            options: {
                scales: {
                    y: { ticks: { color: "white" } },
                    x: { ticks: { color: "white" } }
                }
            }
        });
    }

});
