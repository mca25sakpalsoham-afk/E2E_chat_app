const socket = io();
    // Join private room
socket.emit("join", {
    username: CURRENT_USER,
});
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("messageInput");
    const sendBtn = document.getElementById("sendBtn");
    const messagesDiv = document.getElementById("messages");

    sendBtn.addEventListener("click", sendMessage);
    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") sendMessage();
    });

    function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        socket.emit("send_message", {
            sender: CURRENT_USER,
            receiver: CHAT_USER,
            message: text
        });

        input.value = "";
    }

    socket.on("new_message", (data) => {
        if (
            data.sender !== CURRENT_USER &&
            data.sender !== CHAT_USER
        ) return;

        const msgDiv = document.createElement("div");
        msgDiv.className =
            "message " +
            (data.sender === CURRENT_USER ? "self" : "other");

        msgDiv.innerHTML = `
            <div class="message-text">${data.message}</div>
            <div class="message-time">${data.time}</div>
        `;

        messagesDiv.appendChild(msgDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });
});