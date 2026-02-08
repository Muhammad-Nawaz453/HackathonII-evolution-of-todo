'use client'

import { useState, useEffect, useRef } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'
const CHAT_ENDPOINT = process.env.NEXT_PUBLIC_CHAT_ENDPOINT || 'http://localhost:8001/api/chat'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface Task {
  id: number
  title: string
  description?: string
  status: string
  priority?: string
  category?: string
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI todo assistant powered by Google Gemini. I can help you manage your tasks through natural conversation. Try saying "Add a task to buy groceries" or "Show me my tasks".',
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [tasks, setTasks] = useState<Task[]>([])
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Check backend status
  useEffect(() => {
    checkBackendStatus()
    fetchTasks()
  }, [])

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const checkBackendStatus = async () => {
    try {
      const response = await axios.get(`${API_URL}/health`, { timeout: 5000 })
      if (response.data.status === 'healthy') {
        setBackendStatus('online')
      } else {
        setBackendStatus('offline')
      }
    } catch (error) {
      setBackendStatus('offline')
    }
  }

  const fetchTasks = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/tasks`)
      setTasks(response.data.tasks || [])
    } catch (error) {
      console.error('Error fetching tasks:', error)
    }
  }

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await axios.post(CHAT_ENDPOINT, {
        message: input
      })

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, assistantMessage])

      // Refresh tasks after chat
      await fetchTasks()
    } catch (error: any) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Sorry, I encountered an error: ${error.response?.data?.detail || error.message}. Please make sure the backend is running.`,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-800">AI Todo Chatbot</h1>
              <p className="text-gray-600 mt-1">Powered by Google Gemini (FREE)</p>
            </div>
            <div className="flex items-center gap-2">
              <div className={`w-3 h-3 rounded-full ${
                backendStatus === 'online' ? 'bg-green-500' :
                backendStatus === 'offline' ? 'bg-red-500' :
                'bg-yellow-500'
              }`}></div>
              <span className="text-sm text-gray-600">
                {backendStatus === 'online' ? 'Backend Online' :
                 backendStatus === 'offline' ? 'Backend Offline' :
                 'Checking...'}
              </span>
            </div>
          </div>
        </div>

        {/* Main Content - Split View */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {/* Chat Panel */}
          <div className="lg:col-span-2 bg-white rounded-lg shadow-lg flex flex-col" style={{ height: '600px' }}>
            {/* Chat Header */}
            <div className="p-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-800">Chat</h2>
              <p className="text-sm text-gray-500">Ask me to manage your tasks</p>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg p-3 ${
                      message.role === 'user'
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{message.content}</p>
                    <p className={`text-xs mt-1 ${
                      message.role === 'user' ? 'text-blue-100' : 'text-gray-500'
                    }`}>
                      {typeof window !== 'undefined' && message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-lg p-3">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 border-t border-gray-200">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Type your message... (e.g., 'Add a task to buy groceries')"
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800"
                  disabled={isLoading || backendStatus === 'offline'}
                />
                <button
                  onClick={sendMessage}
                  disabled={isLoading || !input.trim() || backendStatus === 'offline'}
                  className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                  {isLoading ? 'Sending...' : 'Send'}
                </button>
              </div>
            </div>
          </div>

          {/* Tasks Panel */}
          <div className="bg-white rounded-lg shadow-lg flex flex-col" style={{ height: '600px' }}>
            {/* Tasks Header */}
            <div className="p-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold text-gray-800">Tasks</h2>
                <span className="text-sm text-gray-500">{tasks.length} total</span>
              </div>
            </div>

            {/* Tasks List */}
            <div className="flex-1 overflow-y-auto p-4">
              {tasks.length === 0 ? (
                <div className="text-center text-gray-500 mt-8">
                  <p>No tasks yet</p>
                  <p className="text-sm mt-2">Try asking the AI to create one!</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {tasks.map((task) => (
                    <div
                      key={task.id}
                      className="p-3 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="font-medium text-gray-800">{task.title}</h3>
                          {task.description && (
                            <p className="text-sm text-gray-600 mt-1">{task.description}</p>
                          )}
                          <div className="flex gap-2 mt-2">
                            {task.priority && (
                              <span className={`text-xs px-2 py-1 rounded ${
                                task.priority === 'high' ? 'bg-red-100 text-red-700' :
                                task.priority === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                                'bg-green-100 text-green-700'
                              }`}>
                                {task.priority}
                              </span>
                            )}
                            {task.category && (
                              <span className="text-xs px-2 py-1 rounded bg-blue-100 text-blue-700">
                                {task.category}
                              </span>
                            )}
                            <span className={`text-xs px-2 py-1 rounded ${
                              task.status === 'complete' ? 'bg-green-100 text-green-700' :
                              'bg-gray-100 text-gray-700'
                            }`}>
                              {task.status}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Refresh Button */}
            <div className="p-4 border-t border-gray-200">
              <button
                onClick={fetchTasks}
                className="w-full px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
              >
                Refresh Tasks
              </button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-4 text-center text-sm text-gray-600">
          <p>Phase 3: AI-Powered Todo Chatbot | Powered by Google Gemini (FREE) | Cost: $0/month</p>
        </div>
      </div>
    </div>
  )
}
