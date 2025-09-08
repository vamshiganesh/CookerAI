document.addEventListener('DOMContentLoaded', () => {
    // API endpoints for your Flask backend
    const CHAT_API_URL = 'http://localhost:5000/chat';
    const RESET_API_URL = 'http://localhost:5000/reset';

    // DOM element references
    const chatContainer = document.getElementById('chatContainer');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const resetButton = document.getElementById('resetButton');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const statusElement = document.getElementById('status');

    // --- Event Listeners ---

    // Handle sending message on button click
    sendButton.addEventListener('click', sendMessage);

    // Handle sending message on 'Enter' key press
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Handle conversation reset
    resetButton.addEventListener('click', resetConversation);

    // --- Core Functions ---

    async function sendMessage() {
        const userMessage = messageInput.value.trim();
        if (!userMessage) return;

        appendMessage(userMessage, 'user');
        messageInput.value = '';
        setLoadingState(true);

        try {
            const response = await fetch(CHAT_API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `API Error: ${response.status}`);
            }

            const data = await response.json();
            appendMessage(data.bot_response, 'bot');

        } catch (error) {
            console.error('Error sending message:', error);
            appendMessage(`Sorry, I had trouble connecting. Please check if the backend is running. Error: ${error.message}`, 'bot');
        } finally {
            setLoadingState(false);
        }
    }

    async function resetConversation() {
        setLoadingState(true);
        try {
            const response = await fetch(RESET_API_URL, { method: 'POST' });
            if (!response.ok) throw new Error('Failed to reset conversation.');

            const data = await response.json();
            // Clear the chat window and add the initial bot message back
            chatContainer.innerHTML = `
                <div class="message bot-message">
                    <div class="message-avatar"><i class="fas fa-robot"></i></div>
                    <div class="message-content">
                        <p>Hello! I'm your cooking assistant. I can help you with:</p>
                        <ul>
                            <li>🍳 Recipe ideas and detailed cooking instructions</li>
                            <li>🥗 Ingredient substitutions and modifications</li>
                            <li>⏱️ Cooking techniques and tips</li>
                            <li>🍽️ Meal planning suggestions</li>
                        </ul>
                        <p>What would you like to cook today?</p>
                    </div>
                </div>`;
            console.log(data.message); // "Conversation reset."

        } catch (error) {
            console.error('Error resetting conversation:', error);
            appendMessage('Could not reset the conversation. Please try again.', 'bot');
        } finally {
            setLoadingState(false);
        }
    }

    // This function is called by the onclick attributes in the HTML
    window.sendQuickMessage = (message) => {
        messageInput.value = message;
        sendMessage();
    };
    // --- UI Helper Functions ---

    function appendMessage(message, sender) {
        const messageWrapper = document.createElement('div');
        messageWrapper.className = `message ${sender}-message`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'bot' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';

        const content = document.createElement('div');
        content.className = 'message-content';

        // A simple way to render newlines from the bot

        if (sender === 'bot') {
        // Convert Markdown to HTML for bot responses
        var converter = new showdown.Converter();
        content.innerHTML = converter.makeHtml(message);
        } else {
        // For user messages, just display plain text safely
        content.textContent = message;
        }

        messageWrapper.appendChild(avatar);
        messageWrapper.appendChild(content);
        chatContainer.appendChild(messageWrapper);

        // Scroll to the latest message
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function setLoadingState(isLoading) {
        messageInput.disabled = isLoading;
        sendButton.disabled = isLoading;
        resetButton.disabled = isLoading;

        if (isLoading) {
            loadingOverlay.style.display = 'flex';
            statusElement.textContent = 'Thinking...';
        } else {
            loadingOverlay.style.display = 'none';
            statusElement.textContent = 'Ready to help with recipes!';
            messageInput.focus();
        }
    }
});