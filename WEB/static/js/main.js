// Killo 2.75 DAT Web Client

const messagesDiv = document.getElementById('messages');
const queryInput = document.getElementById('queryInput');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const statsBtn = document.getElementById('statsBtn');
const historyBtn = document.getElementById('historyBtn');

// Send message on Enter key
queryInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Send button click
sendBtn.addEventListener('click', sendMessage);

// Clear history
clearBtn.addEventListener('click', async () => {
    if (confirm('Clear conversation history?')) {
        await fetch('/api/clear', { method: 'POST' });
        messagesDiv.innerHTML = '';
    }
});

// Show stats
statsBtn.addEventListener('click', async () => {
    const res = await fetch('/api/stats');
    const stats = await res.json();
    alert(`📊 Killo Stats\n\nCached Topics: ${stats.cached_topics}\nUser Agents: ${stats.user_agents}\nConversation Length: ${stats.conversation_length}`);
});

// Show history
historyBtn.addEventListener('click', async () => {
    const res = await fetch('/api/history');
    const data = await res.json();
    const history = data.history;
    if (history.length === 0) {
        alert('No conversation history');
    } else {
        let text = '📜 Conversation History\n\n';
        history.forEach((msg, idx) => {
            if (msg.type === 'user') {
                text += `You: ${msg.message}\n`;
            } else {
                text += `Killo: ${msg.response.answer.substring(0, 100)}...\n`;
            }
        });
        alert(text);
    }
});

async function sendMessage() {
    const message = queryInput.value.trim();
    if (!message) return;

    // Clear input
    queryInput.value = '';

    // Add user message
    addMessage(message, 'user', 'You');

    // Show loading
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message bot';
    loadingDiv.innerHTML = '<div class="message-content"><div class="loading"><span></span><span></span><span></span></div></div>';
    messagesDiv.appendChild(loadingDiv);
    scrollToBottom();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        
        // Remove loading
        loadingDiv.remove();

        // Add bot response
        addMessage(data.answer, 'bot', `🧠 ${data.source}`);
    } catch (error) {
        loadingDiv.remove();
        addMessage('❌ Error: ' + error.message, 'bot', 'Error');
    }

    scrollToBottom();
}

function addMessage(content, type, source) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(contentDiv);
    
    if (type === 'bot') {
        const sourceDiv = document.createElement('div');
        sourceDiv.className = 'message-source';
        sourceDiv.textContent = source;
        messageDiv.appendChild(sourceDiv);
    }
    
    messagesDiv.appendChild(messageDiv);
}

function scrollToBottom() {
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Welcome message
window.addEventListener('load', () => {
    addMessage('Hi! I\'m Killo 2.75 DAT 🧠\n\nAsk me anything:\n• Math: "2+3", "what is sqrt(16)"\n• Time: "what time is it"\n• Knowledge: "what is quantum computing"\n• Greetings: "hello", "who are you"', 'bot', 'Welcome');
    queryInput.focus();
});
