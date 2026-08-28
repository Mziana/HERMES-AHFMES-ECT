import React from 'react';
import { Plus, MessageSquare, Trash2, Cpu, Shield, Database, Sparkles, Crown } from 'lucide-react';

export default function Sidebar({ sessions, currentSessionId, onSelectSession, onCreateSession, onDeleteSession, activeMode, onChangeMode }) {
  return (
    <aside style={{ width: '280px', height: '100%', display: 'flex', flexDirection: 'column', borderRight: '1px solid var(--border-color)', background: 'rgba(9, 13, 22, 0.95)', padding: '16px' }}>
      
      {/* Brand Header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
        <div style={{ width: '36px', height: '36px', borderRadius: '10px', background: 'linear-gradient(135deg, #06B6D4, #8B5CF6)', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 15px rgba(6, 182, 212, 0.4)' }}>
          <Sparkles size={20} color="#FFF" />
        </div>
        <div>
          <h2 style={{ fontSize: '16px', fontWeight: '700', letterSpacing: '0.5px' }}>HERMES STUDIO</h2>
          <span className="badge badge-cyan" style={{ fontSize: '9px' }}>v0.2 QLoRA Tandem</span>
        </div>
      </div>

      {/* New Chat Button */}
      <button className="btn-primary" onClick={onCreateSession} style={{ width: '100%', justifyContent: 'center', marginBottom: '20px' }}>
        <Plus size={18} /> New Conversation
      </button>

      {/* Mode Presets */}
      <div style={{ marginBottom: '20px' }}>
        <label style={{ fontSize: '11px', fontWeight: '600', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.5px', display: 'block', marginBottom: '8px' }}>
          Cognitive Mode
        </label>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
          {[
            { id: 'ceo', label: 'Chief Executive Orchestrator', icon: Crown, desc: 'Master Director & Subagent Command' },
            { id: 'architect', label: 'Engineering Architect', icon: Cpu, desc: 'Systems, bounds & trade-offs' },
            { id: 'researcher', label: 'Research Analyst', icon: Database, desc: 'Trading methods & 2026 papers' },
            { id: 'auditor', label: 'Adversarial Auditor', icon: Shield, desc: 'Critique & verification gates' },
          ].map((m) => {
            const Icon = m.icon;
            const isActive = activeMode === m.id;
            return (
              <button
                key={m.id}
                onClick={() => onChangeMode(m.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  padding: '8px 10px',
                  borderRadius: '8px',
                  border: isActive ? '1px solid var(--accent-cyan)' : '1px solid transparent',
                  background: isActive ? 'rgba(6, 182, 212, 0.15)' : 'rgba(255, 255, 255, 0.03)',
                  color: isActive ? 'var(--accent-cyan)' : 'var(--text-secondary)',
                  cursor: 'pointer',
                  textAlign: 'left',
                  transition: 'all 0.2s ease',
                }}
              >
                <Icon size={16} />
                <div>
                  <div style={{ fontSize: '12px', fontWeight: '600' }}>{m.label}</div>
                  <div style={{ fontSize: '10px', color: 'var(--text-muted)' }}>{m.desc}</div>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Sessions History List */}
      <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '6px' }}>
        <label style={{ fontSize: '11px', fontWeight: '600', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.5px', display: 'block', marginBottom: '4px' }}>
          History (Drive D:\ SQLite)
        </label>

        {sessions.length === 0 ? (
          <div style={{ fontSize: '12px', color: 'var(--text-muted)', textAlign: 'center', padding: '20px 0' }}>
            No sessions saved yet.
          </div>
        ) : (
          sessions.map((s) => {
            const isSelected = s.id === currentSessionId;
            return (
              <div
                key={s.id}
                onClick={() => onSelectSession(s.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '10px 12px',
                  borderRadius: '8px',
                  background: isSelected ? 'rgba(255, 255, 255, 0.08)' : 'transparent',
                  border: isSelected ? '1px solid var(--border-color)' : '1px solid transparent',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', overflow: 'hidden' }}>
                  <MessageSquare size={14} color={isSelected ? 'var(--accent-cyan)' : 'var(--text-muted)'} />
                  <span style={{ fontSize: '13px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', color: isSelected ? 'var(--text-primary)' : 'var(--text-secondary)' }}>
                    {s.title}
                  </span>
                </div>
                <button
                  onClick={(e) => { e.stopPropagation(); onDeleteSession(s.id); }}
                  style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', opacity: 0.6 }}
                  title="Delete session"
                >
                  <Trash2 size={13} />
                </button>
              </div>
            );
          })
        )}
      </div>

      {/* Local Storage Indicator */}
      <div style={{ marginTop: 'auto', paddingTop: '12px', borderTop: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Database size={14} color="var(--accent-green)" />
        <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
          DB: <strong style={{ color: 'var(--accent-green)' }}>D:\Hermes\storage</strong>
        </span>
      </div>
    </aside>
  );
}
