/**
 * ChatMessage component for Phase III AI-Powered Todo Chatbot.
 * Reference: @specs/003-ai-chatbot/ui/chatkit.md
 */

"use client";

import { Message } from "@/lib/types";

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} animate-fadeIn`}>
      <div className="flex items-start gap-2 sm:gap-3 max-w-[90%] sm:max-w-[80%] lg:max-w-[70%]">
        {/* Avatar for assistant */}
        {!isUser && (
          <div className="w-8 h-8 sm:w-10 sm:h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center flex-shrink-0 shadow-md">
            <svg className="w-4 h-4 sm:w-5 sm:h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
        )}

        <div
          className={`rounded-2xl px-3 sm:px-4 py-2 sm:py-3 shadow-md ${
            isUser
              ? "bg-gradient-to-br from-blue-600 to-blue-700 text-white"
              : "bg-white text-gray-900 border border-gray-200"
          }`}
        >
          {/* Role label */}
          <div className={`text-[10px] sm:text-xs font-semibold mb-1 ${isUser ? "opacity-90" : "text-blue-600"}`}>
            {isUser ? "You" : "AI Assistant"}
          </div>

          {/* Message content */}
          <div className="text-xs sm:text-sm whitespace-pre-wrap break-words leading-relaxed">
            {message.content}
          </div>

          {/* Timestamp */}
          <div className={`text-[10px] sm:text-xs mt-1.5 sm:mt-2 ${isUser ? "opacity-75" : "text-gray-500"}`}>
            {new Date(message.created_at).toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </div>
        </div>

        {/* Avatar for user */}
        {isUser && (
          <div className="w-8 h-8 sm:w-10 sm:h-10 bg-gradient-to-br from-gray-600 to-gray-700 rounded-full flex items-center justify-center flex-shrink-0 shadow-md">
            <svg className="w-4 h-4 sm:w-5 sm:h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
        )}
      </div>
    </div>
  );
}
