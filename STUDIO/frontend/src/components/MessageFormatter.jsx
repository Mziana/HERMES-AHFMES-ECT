import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Terminal, Play, CheckCircle2, AlertTriangle } from 'lucide-react';

export default function MessageFormatter({ content, role }) {
  const [expandedBlocks, setExpandedBlocks] = useState({});
  const [execStatus, setExecStatus] = useState(null);
  const [isExecuting, setIsExecuting] = useState(false);

  const toggleBlock = (index) => {
    setExpandedBlocks(prev => ({ ...prev, [index]: !prev[index] }));
  };

  const handleApproveExecute = async (relPath, proposedCode) => {
    setIsExecuting(true);
    setExecStatus(null);
    try {
      const res = await fetch("http://localhost:8000/api/action/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rel_path: relPath, content: proposedCode }),
      });
      const data = await res.json();
      if (res.ok) {
        setExecStatus({ success: true, message: data.message, pytest: data.pytest_result });
      } else {
        setExecStatus({ success: false, message: data.detail || "Execution failed" });
      }
    } catch (err) {
      setExecStatus({ success: false, message: err.message });
    } finally {
      setIsExecuting(false);
    }
  };

  // If text contains "Ran command:" or long multi-line code blocks
  if (content.includes("Ran command:") || content.includes("$code") || content.includes("```")) {
    const parts = content.split(/(Ran command: [\s\S]*?`|```[\s\S]*?```)/g);

    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', width: '100%' }}>
        {parts.map((part, idx) => {
          if (!part.trim()) return null;

          const isCommandBlock = part.startsWith("Ran command:") || part.startsWith("```") || part.includes("$code =");

          if (isCommandBlock) {
            const isExpanded = expandedBlocks[idx];
            const lines = part.split('\n');
            const previewText = lines.slice(0, 4).join('\n');

            return (
              <div
                key={idx}
                style={{
                  background: 'rgba(0, 0, 0, 0.45)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '10px',
                  padding: '10px 14px',
                  fontFamily: 'var(--font-mono)',
                  fontSize: '12px',
                  margin: '6px 0',
                }}
              >
                <div
                  onClick={() => toggleBlock(idx)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    cursor: 'pointer',
                    color: 'var(--accent-cyan)',
                    fontWeight: '600',
                    fontSize: '11px',
                    paddingBottom: isExpanded ? '8px' : '0',
                    borderBottom: isExpanded ? '1px solid rgba(255,255,255,0.08)' : 'none',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <Terminal size={13} />
                    <span>Ran command output ({lines.length} lines)</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    {isExpanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                    <span>{isExpanded ? 'Collapse' : 'Expand'}</span>
                  </div>
                </div>

                <div
                  style={{
                    maxHeight: isExpanded ? '500px' : '120px',
                    overflowY: 'auto',
                    transition: 'all 0.3s ease',
                    marginTop: '6px',
                    whiteSpace: 'pre-wrap',
                    color: 'var(--text-secondary)',
                    lineHeight: '1.4',
                  }}
                >
                  {isExpanded ? part : previewText + (lines.length > 4 ? '\n... (Click Expand to view full command)' : '')}
                </div>
              </div>
            );
          }

          return (
            <div key={idx} style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>
              {part}
            </div>
          );
        })}

        {/* Execution Approval Status Banner */}
        {execStatus && (
          <div style={{
            padding: '10px 14px',
            borderRadius: '8px',
            background: execStatus.success ? 'rgba(16, 185, 129, 0.15)' : 'rgba(244, 63, 94, 0.15)',
            border: execStatus.success ? '1px solid var(--accent-green)' : '1px solid var(--accent-rose)',
            fontSize: '12px',
            color: execStatus.success ? 'var(--accent-green)' : 'var(--accent-rose)',
            display: 'flex',
            flexDirection: 'column',
            gap: '4px'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: '700' }}>
              {execStatus.success ? <CheckCircle2 size={16} /> : <AlertTriangle size={16} />}
              {execStatus.message}
            </div>
            {execStatus.pytest && (
              <pre style={{ fontSize: '10px', background: 'rgba(0,0,0,0.4)', padding: '6px', borderRadius: '4px', whiteSpace: 'pre-wrap', margin: '4px 0 0', color: 'var(--text-secondary)' }}>
                {execStatus.pytest}
              </pre>
            )}
          </div>
        )}
      </div>
    );
  }

  // Normal text message
  return <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>{content}</div>;
}
