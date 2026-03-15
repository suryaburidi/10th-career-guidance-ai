function sendMessage() {

    let input = document.getElementById("message");
    let msg = input.value.trim();

    if (msg === "") return;

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: msg })
    })
    .then(response => response.json())
    .then(data => {

        if (data.error) {
            alert("Error: " + data.error);
            return;
        }

        // ---------------- CHAT WINDOW ----------------
        let chatBox = document.getElementById("chat-box");

        chatBox.innerHTML += `
            <p><b>You:</b> ${msg}</p>
            <p><b>Bot:</b> ${data.reply}</p>
        `;

        // Auto scroll to bottom
        chatBox.scrollTop = chatBox.scrollHeight;

        input.value = "";

        // ---------------- SIDEBAR HISTORY ----------------
        let historyBox = document.getElementById("history");
        historyBox.innerHTML = "";

        if (data.history && data.history.length > 0) {

            data.history.forEach(item => {
                historyBox.innerHTML += `
                    <div style="margin-bottom:10px;">
                        <small>${item.timestamp}</small><br>
                        <b>${item.role}:</b> ${item.message}
                    </div>
                    <hr>
                `;
            });

        } else {
            historyBox.innerHTML = "<p>No history yet</p>";
        }

    })
    .catch(error => {
        console.error("Fetch Error:", error);
        alert("Backend not responding properly");
    });
}


// Optional: Allow Enter key to send message
document.getElementById("message").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});