function toggleTheme() {
    document.body.classList.toggle("dark");

    const isDark = document.body.classList.contains("dark");
    localStorage.setItem("theme", isDark ? "dark" : "light");

    updateThemeButton();
}

function updateThemeButton() {
    const btn = document.querySelector(".theme-toggle");
    if (!btn) return;

    const icon = btn.querySelector(".icon");
    const label = btn.querySelector(".label");

    const isDark = document.body.classList.contains("dark");

    if (isDark) {
        icon.textContent = "☀";
        label.textContent = "Light";
    } else {
        icon.textContent = "🌙";
        label.textContent = "Dark";
    }
}


document.addEventListener("DOMContentLoaded", () => {
    // Apply saved theme
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark");
    }

    updateThemeButton();

    // ✅ SAFE EVENT BINDING (CSP COMPLIANT)
    const btn = document.querySelector(".theme-toggle");
    if (btn) {
        btn.addEventListener("click", toggleTheme);
    }
});
