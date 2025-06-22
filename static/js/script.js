document.addEventListener('DOMContentLoaded', function () {
    const startChatBtn = document.getElementById('start-chat');
    const resourcesBtn = document.getElementById('resources');
    const languageSelector = document.getElementById('language');

    // Handle homepage button clicks
    if (startChatBtn) {
        startChatBtn.addEventListener('click', function () {
            const lang = languageSelector?.value || 'en';
            window.location.href = `/chat?lang=${lang}`;
        });
    }

    if (resourcesBtn) {
        resourcesBtn.addEventListener('click', function () {
            const lang = languageSelector?.value || 'en';
            window.location.href = `/resources?lang=${lang}`;
        });
    }

    // Initialize chat interface if on chat page
    if (document.getElementById('chat-input')) {
        setupChatInterface();
    }
});

const chatState = {
    currentState: 'initial',
    reset: function () {
        this.currentState = 'initial';
    }
};

async function setupChatInterface() {
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const language = new URLSearchParams(window.location.search).get('lang') || 'en';

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    async function sendMessage() {
        const message = chatInput.value.trim();
        if (message) {
            addUserMessage(message);
            chatInput.value = '';

            const typingIndicator = document.createElement('div');
            typingIndicator.className = 'message bot-message typing';
            typingIndicator.textContent = 'Santio is typing...';
            chatMessages.appendChild(typingIndicator);
            chatMessages.scrollTop = chatMessages.scrollHeight;

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        message: message,
                        language: language,
                        state: chatState.currentState
                    })
                });

                const data = await response.json();
                chatMessages.removeChild(typingIndicator);

                if (data.new_state) {
                    chatState.currentState = data.new_state;
                }

                addBotMessage(data.translated_response || data.response);
            } catch (error) {
                chatMessages.removeChild(typingIndicator);
                addBotMessage("Sorry, I'm having trouble connecting. Please try again.");
                console.error('Error:', error);
            }
        }
    }

    function addUserMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addBotMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.innerHTML = text.replace(/\n/g, '<br>');
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}
