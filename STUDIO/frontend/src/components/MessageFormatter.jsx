import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Terminal, Shield, CheckCircle2, AlertTriangle, Loader2 } from 'lucide-react';

export default function MessageFormatter({ content, role }) {
  const [expandedBlocks, setExpandedBlocks] = useState({});
  const [execStatus, setExecStatus] = useState(null);
  const [isExecuting, setIsExecuting] = useState(false);

  const toggleBlock = (index) => {
    setExpandedBlocks(prev => ({ ...prev, [index]: !prev[index] }));
  };

  const handleApproveExecute = async (token, relPath, proposedCode) => {
    if (!token) {
      setExecStatus({ success: false, message: "Error: No valid approval token provided." });
      return;
    }
    setIsExecuting(true);
    setExecStatus(null);
    try {
      const res = await fetch("http://localhost:8000/api/action/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ approval_token: token, rel_path: relPath, content: proposedCode }),
      });
      const data = await res.json();
      if (res.ok) {
        setExecStatus({ success: true, message: data.message, pytest: data.pytest_result });
      } else {
        setExecStatus({ success: false, message: data.detail || "Execution failed: Unauthorized or Token Expiry" });
      }
    } catch (err) {
      setExecStatus({ success: false, message: err.message });
    } finally {
      setIsExecuting(false);
    }
  };

  // Parse Action Execution proposal token & path if present in content
  const hasTokenMatch = content.match(/tok_[a-f0-9]+/i);
  const extractedToken = hasTokenMatch ? hasTokenMatch[0] : null;
  const hasPathMatch = content.match(/Target Terikat \(Capability Bound\):\s*`([^`]+)`/i) || content.match(/target:\s*`([^`]+)`/i);
  const extractedPath = hasPathMatch ? hasPathMatch[1] : "are/experience.py";

  // Parse code block if present
  const codeBlockMatch = content.match(/```(?:python|diff|markdown|text)?\n([\s\S]*?)\n```/);
  const proposedCode = codeBlockMatch ? codeBlockMatch[1] : "# experience module proposed edit";

  const isCommandOrCodeBlock = content.includes("Ran command:") || content.includes("$code") || content.includes("```");

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', width: '100%' }}>
      
      {/* Main Content Body */}
      {isCommandOrCodeBlock ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', width: '100%' }}>
          {content.split(/(Ran command: [\s\S]*?`|```[\s\S]*?```)/g).map((part, idx) => {
            if (!part.trim()) return null;

            const isCode = part.startsWith("Ran command:") || part.startsWith("```") || part.includes("$code =");

            if (isCode) {
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
                      <span>Code / Execution Block ({lines.length} lines)</span>
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
                    {isExpanded ? part : previewText + (lines.length > 4 ? '\n... (Click Expand to view full snippet)' : '')}
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
        </div>
      ) : (
        <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>{content}</div>
      )}

      {/* Render Capability Approval Gate Button if an Approval Token is present */}
      {extractedToken && (
        <div
          style={{
            marginTop: '12px',
            padding: '14px',
            borderRadius: '10px',
            background: 'rgba(245, 158, 11, 0.1)',
            border: '1px solid var(--accent-amber)',
            display: 'flex',
            flexDirection: 'column',
            gap: '10px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px', fontWeight: '700', color: 'var(--accent-amber)' }}>
            <Shield size={16} /> Capability Approval Gate (One-Time Execution Token)
          </div>
          <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
            Token: <code style={{ color: 'white', background: 'rgba(0,0,0,0.4)', padding: '2px 6px', borderRadius: '4px' }}>{extractedToken}</code> | Target: <code style={{ color: 'var(--accent-cyan)' }}>{extractedPath}</code>
          </div>

          <button
            onClick={() => handleApproveExecute(extractedToken, extractedPath, proposedCode)}
            disabled={isExecuting || (execStatus && execStatus.success)}
            className="btn-primary"
            style={{
              alignSelf: 'flex-start',
              background: execStatus?.success ? 'var(--accent-green)' : 'linear-gradient(135deg, #f59e0b, #d97706)',
              borderColor: 'transparent',
              fontSize: '12px',
              fontWeight: '700',
              gap: '6px',
            }}
          >
            {isExecuting ? (
              <>
                <Loader2 size={14} className="spin" /> Authorizing & Executing Action...
              </>
            ) : execStatus?.success ? (
              <>
                <CheckCircle2 size={14} /> Action Authorized & Consumed
              </>
            ) : (
              <>
                <Shield size={14} /> Approve & Execute Authorized Code Edit
              </>
            )}
          </button>
        </div>
      )}

      {/* Execution Approval Status Banner */}
      {execStatus && (
        <div
          style={{
            padding: '10px 14px',
            borderRadius: '8px',
            background: execStatus.success ? 'rgba(16, 185, 129, 0.15)' : 'rgba(244, 63, 94, 0.15)',
            border: execStatus.success ? '1px solid var(--accent-green)' : '1px solid var(--accent-rose)',
            fontSize: '12px',
            color: execStatus.success ? 'var(--accent-green)' : 'var(--accent-rose)',
            display: 'flex',
            flexDirection: 'column',
            gap: '4px',
            marginTop: '8px',
          }}
        >
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
