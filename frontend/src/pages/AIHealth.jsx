import React, { useEffect, useState } from "react";
import "./AIHealth.css";
import { chatAPI } from "../services/api";

const AIHealth = () => {
  const [messages, setMessages] = useState([]);
  const [messageText, setMessageText] = useState("");

  // ✅ Load chat history
  useEffect(() => {
    const loadHistory = async () => {
      try {
        const response = await chatAPI.getHistory();

        const formattedMessages = [];

        (response.data || []).forEach((chat, index) => {
          formattedMessages.push({
            id: index * 2,
            role: "user",
            message: chat.user_message,
          });

          formattedMessages.push({
            id: index * 2 + 1,
            role: "assistant",
            message: chat.ai_response,
          });
        });

        setMessages(formattedMessages);

      } catch (err) {
        console.error("Could not load chat history", err);
      }
    };

    loadHistory();
  }, []);

  // ✅ Send message
  const handleSend = async () => {
    if (!messageText.trim()) return;

    const userMsg = {
      id: Date.now(),
      role: "user",
      message: messageText.trim(),
    };

    // show user message instantly
    setMessages((prev) => [...prev, userMsg]);

    const currentText = messageText;
    setMessageText("");

    try {
      const response = await chatAPI.sendMessage({
        message: currentText,
      });

      const aiMsg = {
        id: Date.now() + 1,
        role: "assistant",
        message: response.data.response,
      };

      setMessages((prev) => [...prev, aiMsg]);

    } catch (err) {
      console.error(err);

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 2,
          role: "assistant",
          message: "Something went wrong",
        },
      ]);
    }
  };

  return (
    <div className="page-container chat-container-wrapper">
      
      {/* Header */}
      <div className="page-header chat-header">
        <div className="header-icon chat-icon">
          <i className="ph ph-chat-circle"></i>
        </div>
        <div>
          <h1>AI Health Companion</h1>
          <p>Private, empathetic, and knowledgeable</p>
        </div>
      </div>

      {/* Chat UI */}
      <div className="chat-interface">
        <div className="chat-history">
          {messages.length === 0 ? (
            <div className="message-row ai-message-row">
              <div className="message-avatar">
                <i className="ph ph-sparkle"></i>
              </div>
              <div className="message-bubble ai-bubble">
                Hello! I'm your HerCare AI health companion. How are you feeling today?
              </div>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`message-row ${
                  message.role === "user"
                    ? "user-message-row"
                    : "ai-message-row"
                }`}
              >
                <div className="message-avatar">
                  <i
                    className={
                      message.role === "user"
                        ? "ph ph-user"
                        : "ph ph-sparkle"
                    }
                  ></i>
                </div>

                <div
                  className={`message-bubble ${
                    message.role === "user"
                      ? "user-bubble"
                      : "ai-bubble"
                  }`}
                >
                  {message.message}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Input */}
        <div className="chat-input-area">
          <div className="input-wrapper">
            <input
              type="text"
              placeholder="Ask about your health, symptoms, or cycle..."
              className="chat-input"
              value={messageText}
              onChange={(e) => setMessageText(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
            />
            <button className="send-btn" onClick={handleSend}>
              <i className="ph ph-paper-plane-right"></i>
            </button>
          </div>

          <p className="disclaimer">
            AI can make mistakes. Always verify medical information with a doctor.
          </p>
        </div>
      </div>
    </div>
  );
};

export default AIHealth;