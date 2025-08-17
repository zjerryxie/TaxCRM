/**
 * TaxCRM AI Chat Interface
 * Handles real-time tax advice conversations
 */

class TaxChatInterface {
  constructor(options = {}) {
    // Configuration
    this.endpoint = options.endpoint || '/taxcrm/ai_chatbot/chat';
    this.maxLength = options.maxLength || 500;
    this.csrfToken = options.csrfToken || '';
    this.theme = options.theme || 'taxcrm';

    // DOM Elements
    this.chatContainer = document.querySelector(options.container || '.chat-container');
    this.inputField = document.querySelector(options.inputField || '#chat-input');
    this.sendButton = document.querySelector(options.sendButton || '#send-button');
    this.loadingIndicator = document.querySelector(options.loadingIndicator || '.loading-indicator');

    // State
    this.conversationId = null;
    this.isProcessing = false;

    // Initialize
    this._setupEventListeners();
    this._applyTheme();
    this._focusInput();
  }

  _setupEventListeners() {
    // Send message on button click
    this.sendButton.addEventListener('click', () => this._sendMessage());

    // Send message on Enter key
    this.inputField.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this._sendMessage();
      }
    });

    // Input validation
    this.inputField.addEventListener('input', () => {
      this._validateInput();
    });
  }

  _applyTheme() {
    // Add theme-specific CSS classes
    this.chatContainer.classList.add(`theme-${this.theme}`);
    
    // TaxCRM-specific styling
    const style = document.createElement('style');
    style.textContent = `
      .theme-taxcrm .chat-message.ai {
        border-left: 4px solid #4a6da7; /* IRS blue */
      }
      .theme-taxcrm .disclaimer {
        color: #d9534f; /* Bootstrap danger red */
        font-size: 0.9em;
      }
    `;
    document.head.appendChild(style);
  }

  async _sendMessage() {
    if (this.isProcessing) return;
    
    const message = this.inputField.value.trim();
    if (!message) return;

    // Clear input and disable during processing
    this.inputField.value = '';
    this.isProcessing = true;
    this._showLoading(true);

    try {
      // Add user message to chat
      this._addMessage('user', message);

      // Get AI response
      const response = await this._fetchAIResponse(message);

      // Add AI response with formatting
      this._addAIResponse(response);

    } catch (error) {
      this._showError("Failed to get tax advice. Please try again.");
      console.error("Chat error:", error);
    } finally {
      this._showLoading(false);
      this.isProcessing = false;
      this._focusInput();
    }
  }

  async _fetchAIResponse(message) {
    const response = await fetch(this.endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-Token': this.csrfToken
      },
      body: JSON.stringify({
        question: message,
        conversation_id: this.conversationId
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    // Store conversation ID if returned
    if (data.conversation_id) {
      this.conversationId = data.conversation_id;
    }

    return data;
  }

  _addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${role}`;
    
    // Format AI responses differently
    if (role === 'ai') {
      messageDiv.innerHTML = `
        <div class="message-header">
          <span class="sender">Tax Advisor</span>
          <span class="time">${new Date().toLocaleTimeString()}</span>
        </div>
        <div class="message-content">${content.answer}</div>
        ${this._formatSources(content.sources)}
        ${this._formatDisclaimers(content.disclaimers)}
      `;
    } else {
      messageDiv.innerHTML = `
        <div class="message-header">
          <span class="sender">You</span>
          <span class="time">${new Date().toLocaleTimeString()}</span>
        </div>
        <div class="message-content">${content}</div>
      `;
    }

    this.chatContainer.appendChild(messageDiv);
    this._scrollToBottom();
  }

  _addAIResponse(response) {
    if (response.status === 'success') {
      this._addMessage('ai', response.data);
      
      // Highlight tax terms
      this._highlightTaxTerms();
    } else {
      this._showError(response.error || "Unknown error occurred");
    }
  }

  _formatSources(sources) {
    if (!sources || sources.length === 0) return '';
    
    const sourceItems = sources.map(src => 
      `<li><a href="https://www.irs.gov/${src.toLowerCase().replace(' ', '-')}" target="_blank">${src}</a></li>`
    ).join('');
    
    return `
      <div class="sources">
        <strong>IRS References:</strong>
        <ul>${sourceItems}</ul>
      </div>
    `;
  }

  _formatDisclaimers(disclaimers) {
    if (!disclaimers || disclaimers.length === 0) return '';
    
    const disclaimerItems = disclaimers.map(d => 
      `<li class="disclaimer">⚠️ ${d}</li>`
    ).join('');
    
    return `<ul class="disclaimers">${disclaimerItems}</ul>`;
  }

  _highlightTaxTerms() {
    // Highlight tax-specific terminology
    const terms = ['deduction', 'credit', 'W-2', '1099', 'AGI', 'IRS'];
    const contentDivs = document.querySelectorAll('.message-content');
    
    terms.forEach(term => {
      const regex = new RegExp(`\\b${term}\\b`, 'gi');
      contentDivs.forEach(div => {
        div.innerHTML = div.innerHTML.replace(
          regex, 
          `<span class="tax-term">${term}</span>`
        );
      });
    });
  }

  _validateInput() {
    const remaining = this.maxLength - this.inputField.value.length;
    const counter = document.querySelector('.char-counter') || 
                   this._createCharCounter();
    
    counter.textContent = `${remaining} characters remaining`;
    
    if (remaining < 0) {
      counter.classList.add('invalid');
      this.sendButton.disabled = true;
    } else {
      counter.classList.remove('invalid');
      this.sendButton.disabled = false;
    }
  }

  _createCharCounter() {
    const counter = document.createElement('div');
    counter.className = 'char-counter';
    this.inputField.parentNode.appendChild(counter);
    return counter;
  }

  _showLoading(show) {
    if (this.loadingIndicator) {
      this.loadingIndicator.style.display = show ? 'block' : 'none';
    }
    
    this.sendButton.disabled = show;
  }

  _showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'chat-error';
    errorDiv.textContent = message;
    this.chatContainer.appendChild(errorDiv);
    this._scrollToBottom();
  }

  _scrollToBottom() {
    this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
  }

  _focusInput() {
    this.inputField.focus();
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  // Get CSRF token from meta tag (web2py standard)
  const csrfToken = document.querySelector('meta[name="csrf_token"]')?.content || '';
  
  window.taxChat = new TaxChatInterface({
    endpoint: '/taxcrm/ai_chatbot/chat',
    csrfToken: csrfToken,
    container: '.chat-container',
    inputField: '#chat-input',
    sendButton: '#send-button',
    loadingIndicator: '.loading-indicator',
    theme: 'taxcrm'
  });
});
