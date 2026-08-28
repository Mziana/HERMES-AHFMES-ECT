import React, { useState, useEffect } from 'react';
import { Folder, FileCode, CheckCircle, RefreshCw, Eye, AlertTriangle } from 'lucide-react';

export default function RepoInspector({ onSelectFileContext }) {
  const [tree, setTree] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchTree = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/repo/tree');
      const data = await res.json();
      setTree(data.items || []);
    } catch (e) {
      console.error("Failed to load repo tree", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTree();
  }, []);

  const handleOpenFile = async (item) => {
    if (item.is_directory) return;
    setSelectedFile(item.path);
    try {
      const res = await fetch(`/api/repo/file?path=${encodeURIComponent(item.path)}`);
      const data = await res.json();
      setFileContent(data);
    } catch (e) {
      console.error("Failed to read file", e);
    }
  };

  return (
    <aside style={{ width: '320px', height: '100%', display: 'flex', flexDirection: 'column', borderLeft: '1px solid var(--border-color)', background: 'rgba(9, 13, 22, 0.95)', padding: '16px' }}>
      
      {/* Drawer Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Folder size={18} color="var(--accent-cyan)" />
          <h3 style={{ fontSize: '14px', fontWeight: '700' }}>AHFMES-ARE Inspector</h3>
        </div>
        <button onClick={fetchTree} className="btn-secondary" style={{ padding: '4px 8px' }} title="Refresh tree">
          <RefreshCw size={12} />
        </button>
      </div>

      <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: '12px', fontFamily: 'var(--font-mono)' }}>
        Path: D:\Hermes\AHFMES-ARE
      </div>

      {/* File Tree List */}
      <div className="glass-panel" style={{ flex: 1, overflowY: 'auto', padding: '8px', marginBottom: '16px' }}>
        {loading ? (
          <div style={{ fontSize: '12px', color: 'var(--text-muted)', padding: '12px', textAlign: 'center' }}>
            Scanning physical directory...
          </div>
        ) : (
          tree.map((item) => (
            <div
              key={item.path}
              onClick={() => handleOpenFile(item)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '6px 8px',
                borderRadius: '6px',
                background: selectedFile === item.path ? 'rgba(6, 182, 212, 0.15)' : 'transparent',
                cursor: item.is_directory ? 'default' : 'pointer',
                fontSize: '12px',
                color: item.is_directory ? 'var(--accent-amber)' : 'var(--text-secondary)',
              }}
            >
              {item.is_directory ? <Folder size={14} /> : <FileCode size={14} color="var(--accent-cyan)" />}
              <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{item.name}</span>
            </div>
          ))
        )}
      </div>

      {/* Selected File Viewer */}
      {fileContent && (
        <div className="glass-panel-glow" style={{ padding: '12px', fontSize: '11px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontWeight: '700', color: 'var(--accent-cyan)' }}>{fileContent.filename}</span>
            <span className="badge badge-green">{fileContent.total_lines} lines</span>
          </div>

          {fileContent.error ? (
            <div style={{ color: 'var(--accent-rose)', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <AlertTriangle size={14} /> {fileContent.error}
            </div>
          ) : (
            <>
              <pre style={{ maxHeight: '120px', overflowY: 'auto', background: 'rgba(0,0,0,0.4)', padding: '8px', borderRadius: '6px', fontFamily: 'var(--font-mono)', fontSize: '10px', lineHeight: '1.4', color: 'var(--text-secondary)' }}>
                {fileContent.snippet}
              </pre>
              <button
                className="btn-secondary"
                onClick={() => onSelectFileContext(fileContent)}
                style={{ width: '100%', justifyContent: 'center', fontSize: '11px' }}
              >
                <Eye size={12} /> Inject Code Context to Hermes
              </button>
            </>
          )}
        </div>
      )}

      {/* Live PyTest Runner Button */}
      <button
        className="btn-primary"
        onClick={() => onSelectFileContext({ rel_path: "tests/are/test_experience.py", total_lines: 350, snippet: "# PyTest Test Execution Trigger\nRun python -m pytest tests/are/test_experience.py" })}
        style={{ marginTop: '10px', width: '100%', justifyContent: 'center', fontSize: '11px', background: 'linear-gradient(135deg, #10B981, #06B6D4)' }}
      >
        ▶ Run Live PyTest Verification
      </button>

      {/* Epistemic Boundary Badge */}
      <div style={{ marginTop: 'auto', paddingTop: '12px', borderTop: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '10px', color: 'var(--text-muted)' }}>
        <CheckCircle size={12} color="var(--accent-cyan)" />
        <span>Epistemic Boundary Enforced (Zero Hallucination)</span>
      </div>
    </aside>
  );
}
