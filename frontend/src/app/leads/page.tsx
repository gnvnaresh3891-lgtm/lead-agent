'use client';

import { useState } from 'react';
import { Zap, Sparkles, Send, X, CheckCircle2, ShieldCheck, Sliders } from 'lucide-react';
import { generateAIEmail } from '@/lib/api';
import styles from './page.module.css';

const MOCK_COLUMNS = [
  { id: 'new', label: 'New', color: '#6b7280', count: 8 },
  { id: 'enriched', label: 'Enriched', color: 'var(--accent-blue)', count: 6 },
  { id: 'sequenced', label: 'Sequenced', color: 'var(--accent-purple)', count: 12 },
  { id: 'replied', label: 'Replied', color: 'var(--accent-amber)', count: 5 },
  { id: 'qualified', label: 'Qualified', color: 'var(--accent-green)', count: 4 },
  { id: 'booked', label: 'Booked', color: '#10b981', count: 3 },
];

const MOCK_LEADS = [
  { id: '1', name: 'Alex Johnson', company: 'TechFlow', company_name: 'TechFlow', title: 'VP of Engineering', score: 85, status: 'replied', signals: ['#10b981', '#3b82f6'], lastActivity: '2h ago' },
  { id: '2', name: 'Sarah Chen', company: 'DataStack', company_name: 'DataStack', title: 'Director of Sales', score: 92, status: 'qualified', signals: ['#f59e0b', '#8b5cf6', '#10b981'], lastActivity: '5h ago' },
  { id: '3', name: 'Michael Smith', company: 'CloudNova', company_name: 'CloudNova', title: 'CTO', score: 78, status: 'sequenced', signals: ['#3b82f6'], lastActivity: '1d ago' },
  { id: '4', name: 'Emily Davis', company: 'Vertex Solutions', company_name: 'Vertex Solutions', title: 'VP Operations', score: 64, status: 'new', signals: [], lastActivity: '3d ago' },
  { id: '5', name: 'James Wilson', company: 'PulseAI', company_name: 'PulseAI', title: 'CEO', score: 88, status: 'booked', signals: ['#8b5cf6', '#10b981'], lastActivity: '2d ago' },
  { id: '6', name: 'David Lee', company: 'Acme Corp', company_name: 'Acme Corp', title: 'Head of Growth', score: 71, status: 'enriched', signals: ['#f59e0b'], lastActivity: '1d ago' },
  { id: '7', name: 'Laura Martinez', company: 'InnovateX', company_name: 'InnovateX', title: 'CMO', score: 95, status: 'booked', signals: ['#10b981', '#3b82f6', '#8b5cf6'], lastActivity: '4h ago' },
  { id: '8', name: 'Robert Taylor', company: 'Global Systems', company_name: 'Global Systems', title: 'VP Sales', score: 81, status: 'qualified', signals: ['#3b82f6', '#f59e0b'], lastActivity: '6h ago' },
];

export default function LeadsPage() {
  const [view, setView] = useState<'kanban' | 'table'>('kanban');
  const [selectedLead, setSelectedLead] = useState<any | null>(null);
  const [tone, setTone] = useState('challenger');
  const [aiSubject, setAiSubject] = useState('');
  const [aiBody, setAiBody] = useState('');
  const [generating, setGenerating] = useState(false);
  const [approved, setApproved] = useState(false);

  const getScoreClass = (score: number) => {
    if (score >= 80) return styles.scoreHigh;
    if (score >= 60) return styles.scoreMed;
    return styles.scoreLow;
  };

  const handleOpenLead = async (lead: any) => {
    setSelectedLead(lead);
    setApproved(false);
    setGenerating(true);
    const result = await generateAIEmail(lead.id, lead);
    setAiSubject(result.subject || `Quick thought on ${lead.company}`);
    setAiBody(result.body || `Hi ${lead.name.split(' ')[0]}, noticed your intent signals. Would love to connect.`);
    setGenerating(false);
  };

  const handleGenerateClick = async () => {
    if (!selectedLead) return;
    setGenerating(true);
    const result = await generateAIEmail(selectedLead.id, { ...selectedLead, tone });
    setAiSubject(result.subject);
    setAiBody(result.body);
    setGenerating(false);
  };

  const handleApprove = () => {
    setApproved(true);
    setTimeout(() => {
      setSelectedLead(null);
    }, 1200);
  };

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <div>
          <h1 className={styles.title}>Leads</h1>
          <p className={styles.subtitle}>Manage and track your active prospects with AI Copilot</p>
        </div>
        <div className={styles.viewToggle}>
          <button 
            className={`${styles.toggleBtn} ${view === 'kanban' ? styles.active : ''}`}
            onClick={() => setView('kanban')}
          >
            Kanban
          </button>
          <button 
            className={`${styles.toggleBtn} ${view === 'table' ? styles.active : ''}`}
            onClick={() => setView('table')}
          >
            Table
          </button>
        </div>
      </header>

      {view === 'kanban' ? (
        <div className={styles.kanbanBoard}>
          {MOCK_COLUMNS.map(column => (
            <div key={column.id} className={styles.kanbanColumn}>
              <div className={styles.columnHeader}>
                <div className={styles.columnDot} style={{ background: column.color }} />
                <div className={styles.columnTitle}>{column.label}</div>
                <div className={styles.columnCount}>{column.count}</div>
              </div>
              <div className={styles.columnCards}>
                {MOCK_LEADS.filter(lead => lead.status === column.id).map(lead => (
                  <div key={lead.id} className={styles.leadCard} onClick={() => handleOpenLead(lead)}>
                    <div className={styles.cardTop}>
                      <div>
                        <div className={styles.leadName}>{lead.name}</div>
                        <div className={styles.leadCompany}>{lead.company}</div>
                      </div>
                      <div className={`${styles.scoreBadge} ${getScoreClass(lead.score)}`}>
                        {lead.score}
                      </div>
                    </div>
                    <div className={styles.leadTitle}>{lead.title}</div>
                    <div className={styles.cardBottom}>
                      <div className={styles.signalIndicators}>
                        {lead.signals.map((color, i) => (
                          <div key={i} className={styles.signalDot} style={{ background: color }} />
                        ))}
                      </div>
                      <div className={styles.time}>{lead.lastActivity}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className={styles.tableContainer}>
          <div className={styles.tableWrapper}>
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Company</th>
                  <th>Title</th>
                  <th>Score</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {MOCK_LEADS.map(lead => (
                  <tr key={lead.id} onClick={() => handleOpenLead(lead)} style={{ cursor: 'pointer' }}>
                    <td style={{ fontWeight: 600 }}>{lead.name}</td>
                    <td>{lead.company}</td>
                    <td style={{ color: 'var(--text-muted)' }}>{lead.title}</td>
                    <td>
                      <span className={`${styles.scoreBadge} ${getScoreClass(lead.score)}`}>
                        {lead.score}
                      </span>
                    </td>
                    <td>
                      <span className={styles.statusPill}>{lead.status}</span>
                    </td>
                    <td>
                      <button className={styles.toggleBtn} style={{ background: 'var(--accent-blue-glow)', color: 'var(--accent-blue)' }}>
                        <Sparkles size={14} /> AI Copilot
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* AI Copilot & Email Personalization Modal */}
      {selectedLead && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.7)',
          backdropFilter: 'blur(8px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          padding: '20px'
        }}>
          <div style={{
            background: 'var(--bg-surface)',
            border: '1px solid var(--glass-border)',
            borderRadius: '24px',
            padding: '32px',
            maxWidth: '640px',
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            gap: '20px',
            boxShadow: '0 20px 50px rgba(0,0,0,0.5)',
            position: 'relative'
          }}>
            <button 
              onClick={() => setSelectedLead(null)}
              style={{ position: 'absolute', top: '20px', right: '20px', background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
            >
              <X size={20} />
            </button>

            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{ background: 'var(--accent-purple-glow)', padding: '10px', borderRadius: '12px', color: 'var(--accent-purple)' }}>
                <Sparkles size={24} />
              </div>
              <div>
                <h2 style={{ fontSize: '20px', fontWeight: 700 }}>AI Copilot — Personalize Outreach</h2>
                <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
                  Target: <strong>{selectedLead.name}</strong> ({selectedLead.title} at {selectedLead.company})
                </div>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '8px', alignItems: 'center', background: 'var(--bg-primary)', padding: '12px', borderRadius: '12px' }}>
              <span style={{ fontSize: '13px', color: 'var(--text-muted)', fontWeight: 600 }}>Tone Profile:</span>
              {['challenger', 'executive', 'casual'].map((t) => (
                <button
                  key={t}
                  onClick={() => setTone(t)}
                  style={{
                    padding: '6px 12px',
                    borderRadius: '8px',
                    fontSize: '12px',
                    fontWeight: 600,
                    cursor: 'pointer',
                    background: tone === t ? 'var(--accent-blue)' : 'transparent',
                    color: tone === t ? 'white' : 'var(--text-secondary)',
                    border: 'none'
                  }}
                >
                  {t.toUpperCase()}
                </button>
              ))}
              <button 
                onClick={handleGenerateClick} 
                disabled={generating}
                style={{ marginLeft: 'auto', background: 'var(--accent-purple-glow)', border: '1px solid var(--accent-purple)', color: 'var(--accent-purple)', padding: '6px 12px', borderRadius: '8px', fontSize: '12px', fontWeight: 600, cursor: 'pointer' }}
              >
                {generating ? 'Regenerating...' : 'Regenerate'}
              </button>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <div>
                <label style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 600 }}>Subject Line</label>
                <input 
                  type="text" 
                  value={aiSubject} 
                  onChange={(e) => setAiSubject(e.target.value)}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', background: 'var(--bg-primary)', border: '1px solid var(--border-subtle)', color: 'var(--text-primary)', marginTop: '4px' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 600 }}>Email Body (Personalized)</label>
                <textarea 
                  rows={6}
                  value={aiBody} 
                  onChange={(e) => setAiBody(e.target.value)}
                  style={{ width: '100%', padding: '12px 14px', borderRadius: '8px', background: 'var(--bg-primary)', border: '1px solid var(--border-subtle)', color: 'var(--text-primary)', marginTop: '4px', fontSize: '14px', lineHeight: '1.5' }}
                />
              </div>
            </div>

            <div style={{ display: 'flex', gap: '16px', fontSize: '12px', color: 'var(--accent-green)', background: 'var(--accent-green-glow)', padding: '10px 14px', borderRadius: '10px' }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}><CheckCircle2 size={14} /> Flesch Readability: 88</span>
              <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}><ShieldCheck size={14} /> GDPR & CAN-SPAM Compliant</span>
            </div>

            <button 
              onClick={handleApprove}
              disabled={approved}
              style={{
                background: approved ? 'var(--accent-green)' : 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                color: 'white',
                border: 'none',
                padding: '14px',
                borderRadius: '12px',
                fontWeight: 600,
                fontSize: '15px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px'
              }}
            >
              {approved ? (
                <> <CheckCircle2 size={18} /> Outreach Approved & Scheduled! </>
              ) : (
                <> <Send size={18} /> Approve & Schedule Outreach </>
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
