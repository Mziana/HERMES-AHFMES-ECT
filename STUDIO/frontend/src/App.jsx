import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import RepoInspector from './components/RepoInspector';

export default function App() {
  const [sessions, setSessions] = useState([]);
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [activeMode, setActiveMode] = useState('ceo');
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingText, setStreamingText] = useState('');
  const [subagentsEvidence, setSubagentsEvidence] = useState([]);

  // Fetch list of sessions from SQLite backend
  const fetchSessions = async () => {
    try {
      const res = await fetch('/api/sessions');
      const data = await res.json();
      setSessions(data);
      if (data.length > 0 && !currentSessionId) {
        setCurrentSessionId(data[0].id);
      } else if (data.length === 0) {
        handleCreateSession();
      }
    } catch (e) {
      console.error("Failed to fetch sessions", e);
    }
  };

  // Fetch messages for active session
  const fetchMessages = async (sessionId) => {
    if (!sessionId) return;
    try {
      const res = await fetch(`/api/sessions/${sessionId}/messages`);
      const data = await res.json();
      setMessages(data);
    } catch (e) {
      console.error("Failed to fetch messages", e);
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  useEffect(() => {
    if (currentSessionId) {
      fetchMessages(currentSessionId);
    }
  }, [currentSessionId]);

  const handleCreateSession = async () => {
    try {
      const res = await fetch('/api/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: 'New Conversation', mode: activeMode, model: 'hermes-v0.2' })
      });
      const newSession = await res.json();
      setSessions(prev => [newSession, ...prev]);
      setCurrentSessionId(newSession.id);
      setMessages([]);
    } catch (e) {
      console.error("Failed to create session", e);
    }
  };

  const handleDeleteSession = async (sessionId) => {
    try {
      await fetch(`/api/sessions/${sessionId}`, { method: 'DELETE' });
      setSessions(prev => prev.filter(s => s.id !== sessionId));
      if (currentSessionId === sessionId) {
        const remaining = sessions.filter(s => s.id !== sessionId);
        setCurrentSessionId(remaining.length > 0 ? remaining[0].id : null);
      }
    } catch (e) {
      console.error("Failed to delete session", e);
    }
  };

  const handleSendMessage = async (text) => {
    if (!currentSessionId) return;

    // Optimistically update UI
    const tempUserMsg = { id: Date.now().toString(), role: 'user', content: text };
    setMessages(prev => [...prev, tempUserMsg]);

    setIsStreaming(true);
    setStreamingText('');
    setSubagentsEvidence([]);

    try {
      const res = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: currentSessionId,
          message: text,
          mode: activeMode,
          model: 'hermes-v0.2'
        })
      });

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let accumulatedText = '';
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        const events = buffer.split('\n\n');
        buffer = events.pop(); // keep last potentially incomplete fragment in buffer

        for (const evtBlock of events) {
          const trimmed = evtBlock.trim();
          if (trimmed.startsWith('data: ')) {
            try {
              const data = JSON.parse(trimmed.substring(6));
              if (data.type === 'token') {
                accumulatedText += data.content;
                setStreamingText(accumulatedText);
              } else if (data.type === 'subagent') {
                setSubagentsEvidence(prev => [...prev, data]);
              } else if (data.type === 'done') {
                fetchMessages(currentSessionId);
                fetchSessions();
              }
            } catch (e) {
              // Ignore invalid lines
            }
          }
        }
      }
    } catch (e) {
      console.error("Streaming error", e);
    } finally {
      setIsStreaming(false);
      setStreamingText('');
      setSubagentsEvidence([]);
    }
  };

  const handleInjectCodeContext = (fileObj) => {
    const prompt = `Inspect this physical code file: ${fileObj.rel_path} (${fileObj.total_lines} lines):\n\`\`\`python\n${fileObj.snippet}\n\`\`\`\nProvide architectural critique and evidence assessment.`;
    handleSendMessage(prompt);
  };

  return (
    <div style={{ display: 'flex', width: '100vw', height: '100vh', overflow: 'hidden' }}>
      <Sidebar
        sessions={sessions}
        currentSessionId={currentSessionId}
        onSelectSession={setCurrentSessionId}
        onCreateSession={handleCreateSession}
        onDeleteSession={handleDeleteSession}
        activeMode={activeMode}
        onChangeMode={setActiveMode}
      />
      <ChatArea
        messages={messages}
        isStreaming={isStreaming}
        streamingText={streamingText}
        subagentsEvidence={subagentsEvidence}
        onSendMessage={handleSendMessage}
        activeMode={activeMode}
      />
      <RepoInspector onSelectFileContext={handleInjectCodeContext} />
    </div>
  );
}
