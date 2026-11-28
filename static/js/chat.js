// ======================================
// SHIVVER AI — FRONTEND CHAT INTEGRATION
// ======================================


// 1. Get HTML elements

const userInput = document.getElementById("user-message");
const sendButton = document.getElementById("send-button");
const chatMessages = document.getElementById("chat-messages");


// 2. Get Django CSRF token from browser cookie

function getCSRFToken() {

    const cookie = document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="));

    return cookie ? decodeURIComponent(cookie.split("=")[1]) : null;
}


// 3. Display messages in chat window

function displayMessage(message, sender) {

    const messageContainer = document.createElement("div");
    const messageText = document.createElement("p");

    messageText.textContent = message;

    if (sender === "user") {
        messageContainer.classList.add("user-message");
    } else {
        messageContainer.classList.add("assistant-message");
    }

    messageContainer.appendChild(messageText);
    chatMessages.appendChild(messageContainer);

    // Scroll to latest message

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


// 4. Communicate with Django API

async function getAssistantResponse(message) {

    try {

        const response = await fetch("/api/chat/", {

            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },

            credentials: "same-origin",

            body: JSON.stringify({
                message: message
            })

        });


        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to process your message.");
        }

        return data.response;

    }

    catch (error) {

        console.error("SHIVVER API Error:", error);

        throw error;

    }
}


// 5. Send user message

async function sendMessage() {

    const message = userInput.value.trim();

    // Prevent empty messages and duplicate submissions

    if (message === "" || sendButton.disabled) {
        return;
    }

    // Display user message

    displayMessage(message, "user");

    // Clear input

    userInput.value = "";

    // Prevent multiple requests while processing

    sendButton.disabled = true;
    userInput.disabled = true;

    try {

        // Request actual response from Django

        const assistantResponse = await getAssistantResponse(message);

        // Display actual chatbot response

        displayMessage(assistantResponse, "assistant");

    }

    catch (error) {

        displayMessage(
            error.message || "Something went wrong. Please try again.",
            "assistant"
        );

    }

    finally {

        // Enable input again

        sendButton.disabled = false;
        userInput.disabled = false;

        userInput.focus();

    }

}


// 6. Send button event

sendButton.addEventListener("click", sendMessage);


// 7. Enter key event

userInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {

        event.preventDefault();

        sendMessage();

    }

});