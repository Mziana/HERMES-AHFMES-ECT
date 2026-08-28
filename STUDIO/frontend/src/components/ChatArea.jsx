import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, ShieldAlert, Sparkles, Activity, FileSearch } from 'lucide-react';
import MessageFormatter from './MessageFormatter';

export default function ChatArea({ messages, isStreaming, streamingText, subagentsEvidence, onSendMessage, activeMode }) {
  const [input, setInput] = useState('');
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingText, subagentsEvidence]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || isStreaming) return;
    onSendMessage(input);
    setInput('');
  };

  return (
    <main style={{ flex: 1, height: '100%', display: 'flex', flexDirection: 'column', background: 'var(--bg-dark)' }}>
      
      {/* Header Bar */}
      <header style={{ padding: '16px 24px', borderBottom: '1px solid var(--border-color)', background: 'rgba(9, 13, 22, 0.8)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: 'var(--accent-green)', boxShadow: '0 0 10px var(--accent-green)' }}></div>
          <h1 style={{ fontSize: '15px', fontWeight: '600' }}>Hermes v0.2 QLoRA (Llama-3.2-3B)</h1>
          <span className="badge badge-cyan">Ollama API (localhost:11434)</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', color: 'var(--text-muted)' }}>
            <Activity size={14} color="var(--accent-cyan)" />
            Mode: <strong style={{ color: 'var(--accent-cyan)', textTransform: 'capitalize' }}>{activeMode}</strong>
          </div>
        </div>
      </header>

      {/* Messages Stream Container */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '24px', display: 'flex', flexDirection: 'column', gap: '18px' }}>
        
        {messages.length === 0 && (
          <div style={{ margin: 'auto', textAlign: 'center', maxWidth: '480px', padding: '40px 20px' }}>
            <div style={{ width: '54px', height: '54px', borderRadius: '16px', background: 'linear-gradient(135deg, rgba(6,182,212,0.2), rgba(139,92,246,0.2))', border: '1px solid var(--border-accent)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 16px' }}>
              <Bot size={28} color="var(--accent-cyan)" />
            </div>
            <h3 style={{ fontSize: '18px', fontWeight: '700', marginBottom: '8px' }}>Hermes Cognitive Tandem</h3>
            <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
              Ask technical questions, inspect AHFMES-ARE architecture, or request evidence-based risk analysis.
            </p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '20px' }}>
              {[
                "Sampai mana progres pengembangan AHFMES-ARE saat ini?",
                "Bagaimana verifikasi dilakukan sebelum menghapus environment?",
                "Review desain database connection pool untuk 50 worker concurrent."
              ].map((suggestion, idx) => (
                <button
                  key={idx}
                  className="btn-secondary"
                  onClick={() => onSendMessage(suggestion)}
                  style={{ textAlign: 'left', fontSize: '12px', justifyContent: 'flex-start' }}
                >
                  <Sparkles size={13} color="var(--accent-cyan)" /> {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((m, i) => (
          <div key={m.id || i} style={{ display: 'flex', gap: '14px', maxWidth: '85%', alignSelf: m.role === 'user' ? 'flex-end' : 'flex-start' }}>
            {m.role === 'assistant' && (
              <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: 'rgba(6, 182, 212, 0.15)', border: '1px solid rgba(6, 182, 212, 0.3)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                <Bot size={18} color="var(--accent-cyan)" />
              </div>
            )}
            
            <div className={m.role === 'user' ? 'glass-panel-glow' : 'glass-panel'} style={{ padding: '14px 18px', fontSize: '14px', lineHeight: '1.6', color: m.role === 'user' ? 'white' : 'var(--text-primary)', maxWidth: '100%', overflowX: 'hidden' }}>
              <MessageFormatter content={m.content} role={m.role} />
            </div>

            {m.role === 'user' && (
              <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: 'rgba(139, 92, 246, 0.15)', border: '1px solid rgba(139, 92, 246, 0.3)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                <User size={18} color="var(--accent-violet)" />
              </div>
            )}
          </div>
        ))}

        {/* Live Subagents Evidence Notification Stream */}
        {subagentsEvidence.length > 0 && (
          <div className="glass-panel" style={{ padding: '12px 16px', borderColor: 'var(--accent-amber)', background: 'rgba(245, 158, 11, 0.08)', alignSelf: 'flex-start', maxWidth: '85%' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', fontWeight: '600', color: 'var(--accent-amber)', marginBottom: '4px' }}>
              <FileSearch size={14} /> Physical Subagent Inspection Triggered
            </div>
            {subagentsEvidence.map((sa, idx) => (
              <div key={idx} style={{ fontSize: '11px', color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)' }}>
                {sa.evidence}
              </div>
            ))}
          </div>
        )}

        {/* Streaming Live Text */}
        {isStreaming && (
          <div style={{ display: 'flex', gap: '14px', maxWidth: '85%', alignSelf: 'flex-start' }}>
            <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: 'rgba(6, 182, 212, 0.15)', border: '1px solid rgba(6, 182, 212, 0.3)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
              <Bot size={18} color="var(--accent-cyan)" />
            </div>
            <div className="glass-panel" style={{ padding: '14px 18px', fontSize: '14px', lineHeight: '1.6', whiteSpace: 'pre-wrap' }}>
              {streamingText || <span style={{ color: 'var(--text-muted)' }}>Hermes is thinking & verifying evidence...</span>}
            </div>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* Input Box */}
      <footer style={{ padding: '16px 24px', borderTop: '1px solid var(--border-color)', background: 'rgba(9, 13, 22, 0.95)' }}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your instruction or inquiry for Hermes..."
            disabled={isStreaming}
            style={{
              flex: 1,
              background: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid var(--border-color)',
              borderRadius: '10px',
              padding: '12px 16px',
              color: 'white',
              fontSize: '14px',
              outline: 'none',
            }}
          />
          <button type="submit" className="btn-primary" disabled={isStreaming || !input.trim()}>
            <Send size={16} /> Send
          </button>
        </form>
      </footer>
    </main>
  );
}
