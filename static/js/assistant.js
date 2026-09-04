// ==========================================
// AI ASSISTANT
// ==========================================


// Chat input
const chatInput =
    document.getElementById("chatInput");


// Send button
const sendButton =
    document.getElementById("sendBtn");


// Chat messages area
const chatMessages =
    document.getElementById("chatMessages");

if (!chatInput || !sendButton || !chatMessages) {
    // The assistant controls are only present on the assistant page.
} else {


// ==========================================
// SEND BUTTON
// ==========================================

sendButton.addEventListener("click", function () {

    sendMessage();

});


// ==========================================
// ENTER KEY
// ==========================================

chatInput.addEventListener("keydown", function (event) {

    if (event.key === "Enter") {

        sendMessage();

    }

});


// ==========================================
// SEND MESSAGE
// ==========================================

function sendMessage() {

    const message =
        chatInput.value.trim();


    // Empty message ignore karo
    if (!message) {

        return;

    }


    // User message
    const userMessage =
        document.createElement("div");


    userMessage.className =
        "user-message";


    userMessage.innerHTML = `

        <strong>You</strong>

        <p>${message}</p>

    `;


    chatMessages.appendChild(userMessage);


    // Input clear
    chatInput.value = "";


    // Demo AI response
    setTimeout(function () {

        const botMessage =
            document.createElement("div");


        botMessage.className =
            "bot-message";


        botMessage.innerHTML = `

            <strong>🤖 ProjectAI</strong>

            <p>
                This response will come from
                the backend AI service.
            </p>

        `;


        chatMessages.appendChild(botMessage);


        // Chat ko bottom par le jao
        chatMessages.scrollTop =
            chatMessages.scrollHeight;

    }, 700);

}

}