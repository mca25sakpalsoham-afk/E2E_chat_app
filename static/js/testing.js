// ==============================
// Admin Security Testing Panel
// ==============================

document.addEventListener("DOMContentLoaded", () => {
    const runBtn = document.getElementById("runBtn");
    const tamperBtn = document.getElementById("tamperBtn");

    if (runBtn) {
        runBtn.addEventListener("click", runEncryptionTest);
    }

    if (tamperBtn) {
        tamperBtn.addEventListener("click", runTamperTest);
    }

    loadHistory();
});


// ==============================
// Encryption Integrity Test
// ==============================
function runEncryptionTest() {
    const btn = document.getElementById("runBtn");
    const status = document.getElementById("enc-status");
    const details = document.getElementById("enc-details");
    const time = document.getElementById("enc-time");

    btn.textContent = "⏳ Running...";
    btn.disabled = true;

    fetch("/admin/testing/encryption")
        .then(res => res.json())
        .then(data => {
            status.textContent = data.status;
            details.textContent = data.details;
            time.textContent = data.time + " ms";

            status.className = data.status === "PASS"
                ? "status-pass"
                : "status-fail";
        })
        .catch(err => {
            alert("Encryption test failed");
            console.error(err);
        })
        .finally(() => {
            btn.textContent = "▶ Run Test";
            btn.disabled = false;
            loadHistory();
        });
}


// ==============================
// Tampering Attack Test
// ==============================
function runTamperTest() {
    const status = document.getElementById("tamper-status");
    const details = document.getElementById("tamper-details");
    const time = document.getElementById("tamper-time");

    status.textContent = "Running...";
    status.className = "";

    fetch("/admin/testing/tamper")
        .then(res => res.json())
        .then(data => {
            status.textContent = data.status;
            details.textContent = data.details;
            time.textContent = data.time + " ms";

            status.className = data.status === "PASS"
                ? "status-pass"
                : "status-fail";
        })
        .catch(err => {
            alert("Tampering test failed");
            console.error(err);
        })
        .finally(loadHistory);
}


/* Key Test */
function runKeyTest() {
    fetch("/admin/testing/key-strength")
        .then(res => res.json())
        .then(data => {
            document.getElementById("key-status").textContent = data.status;
            document.getElementById("key-size").textContent = data.key_length + " bits";
            document.getElementById("key-strength").textContent = data.strength;
        });
}


// ==============================
// Load Test History
// ==============================
function loadHistory() {
    fetch("/admin/testing/history")
        .then(res => res.json())
        .then(data => {
            const ul = document.getElementById("historyList");
            if (!ul) return;

            ul.innerHTML = "";

            data.reverse().forEach(test => {
                const li = document.createElement("li");
                li.innerHTML = `
                    ${test.time} — 
                    <b>${test.type}</b> : 
                    <span class="${test.status === "PASS" ? "status-pass" : "status-fail"}">
                        ${test.status}
                    </span>
                    (${test.ms} ms)
                `;
                ul.appendChild(li);
            });
        })
        .catch(err => console.error("History load failed", err));
}

