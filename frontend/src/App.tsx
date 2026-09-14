import { useRef, useState } from 'react'
import type { FormEvent, KeyboardEvent } from 'react'
import './App.css'

type Message = {
  role: 'user' | 'assistant'
  content: string
}

const suggestions = [
  'What is the weather in Mumbai?',
  'What is on my calendar today?',
  'Search the latest AI news',
]

function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const sendMessage = async (content: string) => {
    const message = content.trim()
    if (!message || isLoading) return

    setMessages((current) => [...current, { role: 'user', content: message }])
    setInput('')
    setIsLoading(true)

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      })
      const data: { response?: string } = await response.json()
      setMessages((current) => [
        ...current,
        { role: 'assistant', content: data.response ?? 'I could not generate a response.' },
      ])
    } catch {
      setMessages((current) => [
        ...current,
        { role: 'assistant', content: 'I could not reach the assistant. Check that the API server is running.' },
      ])
    } finally {
      setIsLoading(false)
      inputRef.current?.focus()
    }
  }

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    void sendMessage(input)
  }

  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      void sendMessage(input)
    }
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand"><div className="brand-mark">+</div><div><strong>Personal Assistant</strong><span>Everyday command center</span></div></div>
        <p className="label">I can help with</p>
        <div className="capabilities">
          <div><strong>Email</strong><span>Find, read, draft, and send</span></div>
          <div><strong>Calendar</strong><span>Plan events and check time</span></div>
          <div><strong>Weather</strong><span>Conditions and forecasts</span></div>
          <div><strong>Web search</strong><span>Research current information</span></div>
        </div>
        <p className="sidebar-footer"><span className="online-dot" /> Assistant online<br /><small>Powered by your local API</small></p>
      </aside>

      <section className="chat-panel">
        <header className="topbar"><div><span className="eyebrow">Workspace</span><h1>Ask anything.</h1></div><button className="clear-button" onClick={() => setMessages([])} type="button">Clear conversation</button></header>
        <section className="conversation" aria-live="polite">
          {messages.length === 0 ? <div className="welcome"><span className="welcome-kicker">Good to have you here</span><h2>What can I take off your plate?</h2><p>Ask about your inbox, schedule, the weather, or anything you need to research. I will route the request to the right specialist.</p><div className="suggestions">{suggestions.map((suggestion) => <button key={suggestion} onClick={() => void sendMessage(suggestion)} type="button">{suggestion}</button>)}</div></div> : <div className="messages">{messages.map((message, index) => <div className={`message ${message.role}`} key={`${message.role}-${index}`}><div className="avatar">{message.role === 'user' ? 'You' : '+'}</div><div className="bubble">{message.content}</div></div>)}{isLoading && <div className="message assistant"><div className="avatar">+</div><div className="bubble typing"><i /><i /><i /></div></div>}</div>}
        </section>
        <div className="composer-wrap"><form className="composer" onSubmit={handleSubmit}><textarea ref={inputRef} value={input} onChange={(event) => setInput(event.target.value)} onKeyDown={handleKeyDown} placeholder="Ask your personal assistant..." rows={1} /><button className="send-button" disabled={isLoading} title="Send message" type="submit">{isLoading ? '...' : '^'}</button></form><div className="hint">Press Enter to send - Shift + Enter for a new line</div></div>
      </section>
    </main>
  )
}

export default App
