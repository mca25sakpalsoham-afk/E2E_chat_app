const socket = io();
let typingTimeout;

function sendMessage() {
    const input = document.getElementById("messageInput");
    if (input.value.trim() !== "") {
        socket.send(input.value);
        socket.emit("stop_typing");
        input.value = "";
    }
}

const inputField = document.getElementById("messageInput");

inputField.addEventListener("input", () => {
    socket.emit("typing", currentUser);

    clearTimeout(typingTimeout);
    typingTimeout = setTimeout(() => {
        socket.emit("stop_typing");
    }, 1000);
});

socket.on("message", function(data) {
    const messages = document.getElementById("messages");
    const div = document.createElement("div");

    div.className =
        data.sender === currentUser ? "message self" : "message other";

    div.innerHTML = `
        <div>${data.sender}: ${data.message}</div>
        <div class="message-time">${data.time}</div>
    `;

    // Remove empty state on first message
const emptyChat = document.getElementById("emptyChat");
if (emptyChat) {
    emptyChat.remove();
}

    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
});



socket.on("typing", function(username) {
    if (username !== currentUser) {
        document.getElementById("typing").innerHTML = `
            <span>${username} is typing</span>
            <span class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </span>
        `;
    }
});


socket.on("stop_typing", function() {
    document.getElementById("typing").innerText = "";
});
