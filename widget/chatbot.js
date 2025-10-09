/**
 * RX4M Chatbot Widget
 * Embeddable chat widget for RX4 Miracles and Louisiana Dental Plan
 */

(function() {
    'use strict';

    const RX4MChatbot = {
        config: {
            apiUrl: '',
            site: '',
            position: 'bottom-right',
            sessionId: null,
        },

        init: function(options) {
            this.config = { ...this.config, ...options };
            this.config.sessionId = this.generateSessionId();
            this.loadConfig();
            this.createWidget();
            this.attachEventListeners();
        },

        generateSessionId: function() {
            return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        },

        loadConfig: async function() {
            try {
                const response = await fetch(`${this.config.apiUrl}/api/config/${this.config.site}`);
                const config = await response.json();
                this.updateWidgetStyles(config);
            } catch (error) {
                console.error('Failed to load widget config:', error);
            }
        },

        updateWidgetStyles: function(config) {
            const root = document.documentElement;
            root.style.setProperty('--chatbot-primary-color', config.primary_color);

            // Update greeting message if widget is already created
            const greetingEl = document.getElementById('rx4m-chatbot-greeting');
            if (greetingEl) {
                greetingEl.textContent = config.greeting_message;
            }
        },

        createWidget: function() {
            const container = document.getElementById('rx4m-chatbot-container');
            if (!container) {
                console.error('Chatbot container not found');
                return;
            }

            const position = this.config.position;
            const positionClass = `chatbot-${position}`;

            container.innerHTML = `
                <div class="rx4m-chatbot ${positionClass}">
                    <!-- Chat Button -->
                    <button id="rx4m-chat-toggle" class="chat-toggle" aria-label="Open chat">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M20 2H4C2.9 2 2 2.9 2 4V22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2Z" fill="white"/>
                        </svg>
                        <span class="notification-badge" style="display: none;">1</span>
                    </button>

                    <!-- Chat Window -->
                    <div id="rx4m-chat-window" class="chat-window" style="display: none;">
                        <!-- Header -->
                        <div class="chat-header">
                            <h3>Chat Support</h3>
                            <button id="rx4m-chat-close" class="close-button" aria-label="Close chat">×</button>
                        </div>

                        <!-- Messages -->
                        <div id="rx4m-chat-messages" class="chat-messages">
                            <div class="message bot-message">
                                <div class="message-content" id="rx4m-chatbot-greeting">
                                    Hi! How can I help you today?
                                </div>
                            </div>
                        </div>

                        <!-- Input -->
                        <div class="chat-input-container">
                            <input
                                type="text"
                                id="rx4m-chat-input"
                                class="chat-input"
                                placeholder="Type your message..."
                                autocomplete="off"
                            />
                            <button id="rx4m-chat-send" class="send-button" aria-label="Send message">
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M2 10L18 2L10 18L8 11L2 10Z" fill="currentColor"/>
                                </svg>
                            </button>
                        </div>

                        <!-- Powered by -->
                        <div class="chat-footer">
                            <span>Powered by Agent Eva</span>
                        </div>
                    </div>
                </div>
            `;
        },

        attachEventListeners: function() {
            const toggleBtn = document.getElementById('rx4m-chat-toggle');
            const closeBtn = document.getElementById('rx4m-chat-close');
            const sendBtn = document.getElementById('rx4m-chat-send');
            const input = document.getElementById('rx4m-chat-input');

            if (toggleBtn) {
                toggleBtn.addEventListener('click', () => this.toggleChat());
            }

            if (closeBtn) {
                closeBtn.addEventListener('click', () => this.toggleChat());
            }

            if (sendBtn) {
                sendBtn.addEventListener('click', () => this.sendMessage());
            }

            if (input) {
                input.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        this.sendMessage();
                    }
                });
            }
        },

        toggleChat: function() {
            const chatWindow = document.getElementById('rx4m-chat-window');
            const toggleBtn = document.getElementById('rx4m-chat-toggle');
            const badge = toggleBtn.querySelector('.notification-badge');

            if (chatWindow.style.display === 'none') {
                chatWindow.style.display = 'flex';
                toggleBtn.style.display = 'none';
                if (badge) badge.style.display = 'none';
                document.getElementById('rx4m-chat-input').focus();
            } else {
                chatWindow.style.display = 'none';
                toggleBtn.style.display = 'flex';
            }
        },

        sendMessage: async function() {
            const input = document.getElementById('rx4m-chat-input');
            const message = input.value.trim();

            if (!message) return;

            // Add user message to chat
            this.addMessage(message, 'user');
            input.value = '';

            // Show typing indicator
            this.showTypingIndicator();

            try {
                const response = await fetch(`${this.config.apiUrl}/api/chat`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        session_id: this.config.sessionId,
                        site: this.config.site,
                    }),
                });

                const data = await response.json();

                // Remove typing indicator
                this.removeTypingIndicator();

                // Add bot response
                this.addMessage(data.response, 'bot');

            } catch (error) {
                console.error('Error sending message:', error);
                this.removeTypingIndicator();
                this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            }
        },

        addMessage: function(text, sender) {
            const messagesContainer = document.getElementById('rx4m-chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;

            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = text;

            messageDiv.appendChild(contentDiv);
            messagesContainer.appendChild(messageDiv);

            // Scroll to bottom
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        },

        showTypingIndicator: function() {
            const messagesContainer = document.getElementById('rx4m-chat-messages');
            const typingDiv = document.createElement('div');
            typingDiv.id = 'typing-indicator';
            typingDiv.className = 'message bot-message';
            typingDiv.innerHTML = `
                <div class="message-content typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            `;
            messagesContainer.appendChild(typingDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        },

        removeTypingIndicator: function() {
            const typingIndicator = document.getElementById('typing-indicator');
            if (typingIndicator) {
                typingIndicator.remove();
            }
        },
    };

    // Export to global scope
    window.RX4MChatbot = RX4MChatbot;
})();
