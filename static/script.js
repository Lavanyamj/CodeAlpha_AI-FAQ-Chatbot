const chatBox = document.getElementById("chatBox");
const questionInput = document.getElementById("questionInput");
const sendButton = document.getElementById("sendButton");
const clearButton = document.getElementById("clearButton");

function addMessage(message, type) {
    const messageDiv = document.createElement("div");

    messageDiv.classList.add(
        "message",
        type === "user" ? "user-message" : "bot-message"
    );

    const avatar = document.createElement("div");
    avatar.classList.add("avatar");
    avatar.textContent = type === "user" ? "👤" : "🤖";

    const content = document.createElement("div");
    content.classList.add("message-content");

    const sender = document.createElement("span");
    sender.classList.add("sender");
    sender.textContent = type === "user" ? "YOU" : "BOT";

    const bubble = document.createElement("div");
    bubble.classList.add("bubble");
    bubble.textContent = message;

    content.appendChild(sender);
    content.appendChild(bubble);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);

    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}


async function sendQuestion() {

    const question = questionInput.value.trim();

    if (!question) {
        return;
    }

    addMessage(question, "user");

    questionInput.value = "";

    sendButton.disabled = true;
    sendButton.textContent = "Sending...";

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        addMessage(data.answer, "bot");

    } catch (error) {

        addMessage(
            "Sorry, I couldn't connect to the chatbot server.",
            "bot"
        );

        console.error(error);

    } finally {

        sendButton.disabled = false;
        sendButton.textContent = "Send";
    }
}


sendButton.addEventListener("click", sendQuestion);


questionInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        sendQuestion();
    }

});


clearButton.addEventListener("click", function() {

    chatBox.innerHTML = "";

    addMessage(
        "Hello! 👋 I'm your AI FAQ assistant. Ask me anything about Artificial Intelligence.",
        "bot"
    );

});