/**
 * Footer component.
 * Reference: @specs/002-fullstack-web-app/ui/components.md
 */

import React from "react";
import Link from "next/link";

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white border-t border-gray-700 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          {/* Brand Section */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <span className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-blue-500 bg-clip-text text-transparent">
                Todo App
              </span>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              Manage your tasks effortlessly with our AI-powered todo application. Simple, secure, and powerful.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-white">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/dashboard" className="text-gray-400 hover:text-blue-400 transition-colors flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                  My Tasks
                </Link>
              </li>
              <li>
                <Link href="/chat" className="text-gray-400 hover:text-blue-400 transition-colors flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                  AI Chatbot
                </Link>
              </li>
              <li>
                <Link href="/login" className="text-gray-400 hover:text-blue-400 transition-colors flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                  Login
                </Link>
              </li>
              <li>
                <Link href="/signup" className="text-gray-400 hover:text-blue-400 transition-colors flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                  Sign Up
                </Link>
              </li>
            </ul>
          </div>

          {/* Tech Stack */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-white">Built With</h3>
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-gray-800 rounded-lg flex items-center justify-center">
                  <span className="text-blue-400 font-bold text-xs">N</span>
                </div>
                <span className="text-gray-400 text-sm">Next.js 16</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-gray-800 rounded-lg flex items-center justify-center">
                  <span className="text-green-400 font-bold text-xs">F</span>
                </div>
                <span className="text-gray-400 text-sm">FastAPI</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-gray-800 rounded-lg flex items-center justify-center">
                  <span className="text-purple-400 font-bold text-xs">AI</span>
                </div>
                <span className="text-gray-400 text-sm">OpenRouter AI</span>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-gray-700">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-gray-400 text-sm">
              © {currentYear} Todo App. Phase III - AI-Powered Chatbot
            </p>
            <div className="flex items-center gap-6">
              <span className="text-gray-500 text-xs flex items-center gap-2">
                <svg className="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                All Systems Operational
              </span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
