/**
 * Chatbot Microservice Widget
 * Embeddable chat widget for multi-tenant chatbot platform
 */

(function() {
    'use strict';

    const ChatbotWidget = {
        config: {
            apiUrl: '',
            site: '',
            position: 'bottom-right',
            sessionId: null,
        },

        init: function(options) {
            this.config = { ...this.config, ...options };
            this.config.sessionId = this.generateSessionId();
            this.config.hasShownGreeting = false;
            this.loadConfig();
            this.createWidget();
            this.attachEventListeners();
            this.checkFirstVisit();
        },

        // Cookie helper functions
        setCookie: function(name, value, days) {
            const expires = new Date();
            expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
            document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
        },

        getCookie: function(name) {
            const nameEQ = name + "=";
            const ca = document.cookie.split(';');
            for(let i = 0; i < ca.length; i++) {
                let c = ca[i];
                while (c.charAt(0) === ' ') c = c.substring(1, c.length);
                if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
            }
            return null;
        },

        checkFirstVisit: function() {
            const hasVisited = this.getCookie('chatbot_visited');

            if (!hasVisited) {
                // First visit - show bounce animation and tooltip
                this.showFirstVisitHelp();
            }
        },

        showFirstVisitHelp: function() {
            const toggleBtn = document.getElementById('rx4m-chat-toggle');
            if (!toggleBtn) return;

            // Add bounce animation
            toggleBtn.classList.add('first-visit');

            // Create and add tooltip
            const tooltip = document.createElement('div');
            tooltip.className = 'chat-tooltip';
            tooltip.textContent = 'Click here for chat assistance';
            toggleBtn.parentElement.appendChild(tooltip);

            // Store reference for later removal
            this.tooltip = tooltip;
        },

        removeFirstVisitHelp: function() {
            const toggleBtn = document.getElementById('rx4m-chat-toggle');
            if (toggleBtn) {
                toggleBtn.classList.remove('first-visit');
            }

            if (this.tooltip) {
                this.tooltip.remove();
                this.tooltip = null;
            }

            // Set cookie so it doesn't show again (expires in 365 days)
            this.setCookie('chatbot_visited', 'true', 365);
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

            // Store greeting message in config
            this.config.greetingMessage = config.greeting_message;
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
                        <svg width="46" height="46" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <rect x="2.5" y="4.5" width="31" height="22" rx="3" stroke="white" stroke-width="4" fill="none"/>
                            <path d="M7.5 26.5L13 32L23 32L28.5 26.5" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                            <line x1="8.5" y1="12" x2="27.5" y2="12" stroke="white" stroke-width="4" stroke-linecap="round"/>
                        </svg>
                        <span class="notification-badge" style="display: none;">1</span>
                    </button>

                    <!-- Chat Window -->
                    <div id="rx4m-chat-window" class="chat-window" style="display: none;">
                        <!-- Header -->
                        <div class="chat-header">
                            <div class="chat-header-content">
                                <div class="chat-header-icon">
                                    <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <circle cx="20" cy="20" r="20" fill="#1e293b"/>
                                        <rect x="12" y="13" width="16" height="12" rx="2" stroke="white" stroke-width="2" fill="none"/>
                                        <path d="M15 25L17 27L23 27L25 25" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                                        <line x1="16" y1="17" x2="24" y2="17" stroke="white" stroke-width="2" stroke-linecap="round"/>
                                        <circle cx="30" cy="14" r="4" fill="#10b981"/>
                                    </svg>
                                </div>
                                <div class="chat-header-text">
                                    <h3>Text Support</h3>
                                    <span class="chat-header-subtitle">AI assistant</span>
                                </div>
                            </div>
                            <button id="rx4m-chat-close" class="close-button" aria-label="Close chat">×</button>
                        </div>

                        <!-- Messages -->
                        <div id="rx4m-chat-messages" class="chat-messages">
                            <!-- Greeting will be added dynamically -->
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
                            <span>Powered by AgentEva</span>
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
                // Remove first visit help on first click
                this.removeFirstVisitHelp();

                chatWindow.style.display = 'flex';
                toggleBtn.style.display = 'none';
                if (badge) badge.style.display = 'none';

                // Show greeting with typing effect on first open
                if (!this.config.hasShownGreeting) {
                    this.config.hasShownGreeting = true;
                    this.showGreetingWithTyping();
                }

                document.getElementById('rx4m-chat-input').focus();
            } else {
                chatWindow.style.display = 'none';
                toggleBtn.style.display = 'flex';
            }
        },

        showGreetingWithTyping: async function() {
            // Show typing indicator
            this.showTypingIndicator();

            // Wait for 1.5 seconds to simulate typing
            await new Promise(resolve => setTimeout(resolve, 1500));

            // Remove typing indicator
            this.removeTypingIndicator();

            // Get the greeting message (will be updated by loadConfig if available)
            const greetingMessage = this.config.greetingMessage || `Hi! I'm here to help with ${this.config.site === 'rx4miracles' ? 'RX4 Miracles' : 'Louisiana Dental Plan'}. How can I assist you today?`;

            // Add the greeting message
            this.addMessage(greetingMessage, 'bot');
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

            // Add bot icon for bot messages
            if (sender === 'bot') {
                const iconDiv = document.createElement('div');
                iconDiv.className = 'bot-icon';
                iconDiv.innerHTML = `
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="12" cy="12" r="12" fill="#1e293b"/>
                        <rect x="7.5" y="8" width="9" height="7" rx="1.5" stroke="white" stroke-width="1.2" fill="none"/>
                        <path d="M9 15L10 16L14 16L15 15" stroke="white" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                        <line x1="9.5" y1="10.5" x2="14.5" y2="10.5" stroke="white" stroke-width="1.2" stroke-linecap="round"/>
                    </svg>
                `;
                messageDiv.appendChild(iconDiv);
            }

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
                <div class="bot-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="12" cy="12" r="12" fill="#1e293b"/>
                        <rect x="7.5" y="8" width="9" height="7" rx="1.5" stroke="white" stroke-width="1.2" fill="none"/>
                        <path d="M9 15L10 16L14 16L15 15" stroke="white" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                        <line x1="9.5" y1="10.5" x2="14.5" y2="10.5" stroke="white" stroke-width="1.2" stroke-linecap="round"/>
                    </svg>
                </div>
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

    // Export to global scope (keep RX4MChatbot for backward compatibility)
    window.ChatbotWidget = ChatbotWidget;
    window.RX4MChatbot = ChatbotWidget; // Backward compatibility alias
})();
