/**
 * ChatInterface component for Phase III AI-Powered Todo Chatbot.
 * Reference: @specs/003-ai-chatbot/ui/chatkit.md
 */

"use client";

import { useState, useRef, useEffect } from "react";
import { sendMessage } from "@/lib/chat";
import { ChatResponse, Message } from "@/lib/types";
import ChatMessage from "./ChatMessage";

interface ChatInterfaceProps {
  userId: string;
}

export default function ChatInterface({ userId }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim() || loading) {
      return;
    }

    const userMessage = inputValue.trim();
    setInputValue("");
    setError(null);
    setLoading(true);

    // Add user message to UI immediately (optimistic update)
    const tempUserMessage: Message = {
      id: `temp-${Date.now()}`,
      user_id: userId,
      conversation_id: conversationId || "",
      role: "user",
      content: userMessage,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempUserMessage]);

    try {
      // Send message to backend
      const response = await sendMessage(userId, {
        conversation_id: conversationId || undefined,
        message: userMessage,
      });

      // Update conversation ID if this is the first message
      if (!conversationId && "conversation_id" in response) {
        setConversationId(response.conversation_id);
      }

      // Add assistant response to UI
      if ("response" in response) {
        const assistantMessage: Message = {
          id: `assistant-${Date.now()}`,
          user_id: userId,
          conversation_id: response.conversation_id,
          role: "assistant",
          content: response.response,
          created_at: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, assistantMessage]);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send message");
      // Remove optimistic user message on error
      setMessages((prev) => prev.slice(0, -1));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[500px] sm:h-[600px] lg:h-[650px] bg-gradient-to-b from-gray-50 to-white rounded-lg shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-4 sm:px-6 py-3 sm:py-4 border-b border-blue-800">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 sm:w-10 sm:h-10 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center">
            <svg className="w-5 h-5 sm:w-6 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
          <div>
            <h3 className="text-white font-semibold text-sm sm:text-base">AI Assistant</h3>
            <p className="text-blue-100 text-xs">Always here to help</p>
          </div>
        </div>
      </div>

      {/* Messages area */}
      <div ref={messagesContainerRef} className="flex-1 overflow-y-auto p-3 sm:p-4 lg:p-6 space-y-3 sm:space-y-4 bg-gradient-to-b from-blue-50/30 to-transparent scroll-smooth">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-6 sm:mt-8 px-4">
            <div className="w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-blue-100 to-blue-200 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 sm:w-10 sm:h-10 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <p className="text-base sm:text-lg font-semibold text-gray-700 mb-2">Start a conversation</p>
            <p className="text-xs sm:text-sm text-gray-500">
              Try asking me to add a task, show your tasks, or mark something as complete.
            </p>
          </div>
        )}

        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}

        {loading && (
          <div className="flex items-center space-x-3 text-blue-600 bg-gradient-to-r from-blue-50 to-blue-100 rounded-xl px-4 py-3 shadow-md border border-blue-200">
            <div className="animate-spin rounded-full h-5 w-5 border-2 border-blue-600 border-t-transparent"></div>
            <span className="text-sm font-medium">AI is thinking...</span>
          </div>
        )}

        {error && (
          <div className="bg-gradient-to-r from-red-50 to-red-100 border-l-4 border-red-500 rounded-lg p-3 sm:p-4 shadow-md">
            <div className="flex items-start gap-3">
              <svg className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <p className="text-red-800 text-xs sm:text-sm font-medium">{error}</p>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="border-t border-gray-200 bg-white p-3 sm:p-4 shadow-lg">
        <form onSubmit={handleSendMessage} className="flex flex-col sm:flex-row gap-2 sm:gap-3">
          <div className="flex-1 relative">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Type your message... (e.g., 'Add a task to buy groceries')"
              className="w-full px-4 py-3 text-sm sm:text-base border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed transition-all shadow-sm"
              disabled={loading}
              maxLength={2000}
            />
            <div className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-gray-400">
              {inputValue.length}/2000
            </div>
          </div>
          <button
            type="submit"
            disabled={loading || !inputValue.trim()}
            className="w-full sm:w-auto px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white text-sm sm:text-base font-medium rounded-xl hover:from-blue-700 hover:to-blue-800 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed transition-all shadow-md hover:shadow-lg flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                <span>Sending...</span>
              </>
            ) : (
              <>
                <span>Send</span>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </>
            )}
          </button>
        </form>
        <p className="mt-2 text-xs text-gray-500 text-center sm:text-left flex items-center justify-center sm:justify-start gap-2">
          <svg className="w-3 h-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Press Enter to send your message
        </p>
      </div>
    </div>
  );
}
