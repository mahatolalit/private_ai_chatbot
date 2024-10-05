let currentConversationId = null;

// Fetch and display all conversations on page load
document.addEventListener('DOMContentLoaded', () => {
    fetchConversations(); 
});

// Function to fetch conversations from backend
function fetchConversations() {
    fetch('/api/conversations')
        .then(response => response.json())
        .then(data => {
            const conversationList = document.getElementById('conversations');
            conversationList.innerHTML = ''; // Clear existing list
            
            if (data.length > 0) {
                // If there are existing conversations, load the most recent one
                currentConversationId = data[data.length - 1].id;
                loadConversation(currentConversationId);
            } else {
                // If no conversations exist, start a new chat
                startNewChat();
            }

            data.forEach(convo => {
                const conversationItem = document.createElement('div');
                conversationItem.classList.add('conversation');
                conversationItem.textContent = convo.title;
                conversationItem.onclick = () => loadConversation(convo.id);
                conversationList.appendChild(conversationItem);
            });
        })
        .catch(error => {
            console.error('Error fetching conversations:', error);
        });
}

// Function to start a new chat
function startNewChat() {
    fetch('/api/conversations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        currentConversationId = data.id;
        fetchConversations(); // Refresh conversation list
        clearChatBox();
        addSystemMessage(`Started ${data.name}.`);
    })
    .catch(error => {
        console.error('Error creating new conversation:', error);
    });
}

// Function to load a conversation
function loadConversation(id) {
    currentConversationId = id;
    fetch(`/api/conversations/${id}/messages`)
        .then(response => response.json())
        .then(messages => {
            clearChatBox();
            messages.forEach(msg => {
                if (msg.startsWith("You: ")) {
                    addUserMessage(msg.replace("You: ", ""));
                } else if (msg.startsWith("Bot: ")) {
                    addBotMessage(msg.replace("Bot: ", ""));
                }
            });
            addExportOption(id);
        })
        .catch(error => {
            console.error('Error loading conversation:', error);
        });
}

// Function to send a message
function sendMessage() {
    const userInput = document.getElementById("user-input").value.trim();
    const chatBox = document.getElementById("chat-box");

    if (userInput === "" || currentConversationId === null) return;

    // Append user's message to chat box
    addUserMessage(userInput);

    // Clear input field
    document.getElementById("user-input").value = "";

    // Send message to backend
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            message: userInput,
            conversation_id: currentConversationId
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.response) {
            addBotMessage(data.response);
        }
    })
    .catch(error => {
        console.error('Error sending message:', error);
    });
}

// Function to handle "Enter" key press
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Function to add user message to chat box
function addUserMessage(message) {
    const chatBox = document.getElementById('chat-box');
    const msg = document.createElement('div');
    msg.classList.add('message', 'user-message');
    msg.textContent = message;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Function to add bot message to chat box
function addBotMessage(message) {
    const chatBox = document.getElementById('chat-box');
    const msg = document.createElement('div');
    msg.classList.add('message', 'bot-message');
    msg.textContent = message;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Function to add system message
function addSystemMessage(message) {
    const chatBox = document.getElementById('chat-box');
    const msg = document.createElement('div');
    msg.classList.add('message', 'bot-message');
    msg.style.backgroundColor = '#555555';
    msg.textContent = message;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Function to clear chat box
function clearChatBox() {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = '';
}

// Function to export a conversation
function exportConversation(id) {
    fetch(`/api/conversations/${id}/export`)
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Error exporting conversation:', error);
        });
}

// Modify loadConversation to include view/export option
function loadConversation(id) {
    currentConversationId = id;
    fetch(`/api/conversations/${id}/messages`)
        .then(response => response.json())
        .then(messages => {
            clearChatBox();
            messages.forEach(msg => {
                if (msg.startsWith("You: ")) {
                    addUserMessage(msg.replace("You: ", ""));
                } else if (msg.startsWith("Bot: ")) {
                    addBotMessage(msg.replace("Bot: ", ""));
                }
            });
            addExportOption(id);
        })
        .catch(error => {
            console.error('Error loading conversation:', error);
        });
}

// Function to add export button after loading conversation
function addExportOption(id) {
    const chatBox = document.getElementById('chat-box');
    const exportBtn = document.createElement('button');
    exportBtn.textContent = "Export Conversation";
    exportBtn.style.marginTop = "10px";
    exportBtn.style.padding = "10px";
    exportBtn.style.backgroundColor = "#28a745";
    exportBtn.style.color = "#fff";
    exportBtn.style.border = "none";
    exportBtn.style.borderRadius = "5px";
    exportBtn.style.cursor = "pointer";
    exportBtn.onclick = () => exportConversation(id);
    chatBox.appendChild(exportBtn);
    chatBox.scrollTop = chatBox.scrollHeight;
}
