class Chat {
    /**
     * @param {string} containerId  ID of the chat-window div
     */
    constructor(containerId) {
      this.container = document.getElementById(containerId);
      this.conversationId = this.container.dataset.conversationId;
      this.messagesEl = this.container.querySelector('.messages');
      this.inputEl = this.container.querySelector('.message-input');
      this.sendBtn = this.container.querySelector('.btn-send');
      this.statusEl = this.container.querySelector('.status');
      this.toggleBtn = this.container.querySelector('.btn-toggle-status');
  
      this.sendBtn.addEventListener('click', () => this.sendMessage());
      this.toggleBtn.addEventListener('click', () => this.toggleStatus());
  
      this.poll();                 // load immediately
      this.polling = setInterval(() => this.poll(), 3000);
    }
  
    /** Fetch latest messages and state, then render */
    async poll() {
      try {
        const res = await fetch(`/conversations/${this.conversationId}/`);
        if (!res.ok) throw new Error('Fetch failed');
        const { messages, state } = await res.json();
        this.renderMessages(messages);
        this.updateStatus(state);
      } catch (err) {
        console.error('Polling error:', err);
      }
    }
  
    /** Render message bubbles */
    renderMessages(msgs) {
      this.messagesEl.innerHTML = '';
      msgs.forEach(m => {
        const div = document.createElement('div');
        div.className = `message ${m.direction.toLowerCase()}`;
        div.innerHTML = `
          <div class="text">${m.content}</div>
          <div class="timestamp">${new Date(m.timestamp).toLocaleTimeString()}</div>
        `;
        this.messagesEl.appendChild(div);
      });
      this.messagesEl.scrollTop = this.messagesEl.scrollHeight;
    }
  
    /** Send a new message via webhook and append optimistically */
    async sendMessage() {
      const text = this.inputEl.value.trim();
      if (!text || this.statusEl.textContent === 'CLOSED') return;
  
      // Optimistic UI
      const tempMsg = { direction: 'SENT', content: text, timestamp: new Date().toISOString() };
      this.renderMessages([...Array.from(this.messagesEl.children).map(c => ({
        direction: c.classList.contains('sent') ? 'SENT' : 'RECEIVED',
        content: c.querySelector('.text').textContent,
        timestamp: new Date().toISOString()
      })), tempMsg]);
      this.inputEl.value = '';
  
      // Real webhook call
      try {
        await fetch('/webhook/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            type: 'NEW_MESSAGE',
            timestamp: new Date().toISOString(),
            data: {
              id: crypto.randomUUID(),
              direction: 'SENT',
              content: text,
              conversation_id: this.conversationId
            }
          })
        });
      } catch (err) {
        console.error('Send error:', err);
      }
    }
  
    /** Toggle between OPEN ⇄ CLOSED */
    async toggleStatus() {
      const newType = this.statusEl.textContent === 'OPEN'
        ? 'CLOSE_CONVERSATION'
        : 'NEW_CONVERSATION';
  
      try {
        await fetch('/webhook/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            type: newType,
            timestamp: new Date().toISOString(),
            data: { id: this.conversationId }
          })
        });
        // After server update, fetch new state
        this.poll();
      } catch (err) {
        console.error('Toggle status error:', err);
      }
    }
  
    /** Update header button & input enable/disable */
    updateStatus(state) {
      this.statusEl.textContent = state;
      if (state === 'OPEN') {
        this.toggleBtn.textContent = 'Fechar';
        this.toggleBtn.classList.remove('closed');
        this.inputEl.disabled = false;
        this.sendBtn.disabled = false;
      } else {
        this.toggleBtn.textContent = 'Encerrado';
        this.toggleBtn.classList.add('bg-dark');
        this.inputEl.disabled = true;
        this.sendBtn.disabled = true;
      }
    }
  }
  
  // On DOM ready, instantiate both
  document.addEventListener('DOMContentLoaded', () => {
    new Chat('chatA');
    new Chat('chatB');
  });
  