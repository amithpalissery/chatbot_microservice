const userInput = document.getElementById('user-query');
const sendButton = document.getElementById('send-button');
const chatHistory = document.getElementById('chatHistory');

// Function to add a message to the chat container with the correct structure
function addMessage(message, sender) {
    const chatWrapper = document.createElement('div');
    chatWrapper.classList.add('chat');
    chatWrapper.classList.add(sender === 'user' ? 'user-chat' : 'bot-chat');

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message');
    messageDiv.innerHTML = message;
    
    chatWrapper.appendChild(messageDiv);
    chatHistory.appendChild(chatWrapper);
    
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

sendButton.addEventListener('click', async () => {
    const userMessage = userInput.value.trim();

    if (userMessage !== '') {
        // Clear the input field immediately
        userInput.value = '';

        // Add user's message to the chat
        addMessage(userMessage, 'user');

        // Show a loading message
        addMessage('...', 'bot');

        try {
            // Use the fetch API to send the user's question to your Flask server
            const response = await fetch('/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'question': userMessage
                })
            });

            const jsonResponse = await response.json();
            
            // Remove the loading message. The last message is always the typing indicator.
            chatHistory.removeChild(chatHistory.lastChild);
            
            const botMessage = jsonResponse.answer;
            if (botMessage) {
                addMessage(botMessage, 'bot');
            } else {
                addMessage("Sorry, I could not get a response.", "bot");
            }

        } catch (error) {
            console.error('Error fetching data:', error);
            // Remove the loading message and show an error
            chatHistory.removeChild(chatHistory.lastChild);
            addMessage("Sorry, an error occurred while connecting to the server.", "bot");
        }
    }
});

// Optional: Add event listener for "Enter" key press
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        sendButton.click();
    }
});
