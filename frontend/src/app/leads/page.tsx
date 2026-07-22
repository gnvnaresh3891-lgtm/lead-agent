'use client';

import { useState } from 'react';
import { 
  Users, Zap, Sparkles, Send, X, CheckCircle2, 
  ShieldCheck, ArrowRight, Layers, Bot, Mail, Phone, Cpu
} from 'lucide-react';
import styles from './page.module.css';

const MOCK_COLUMNS = [
  { id: 'new', label: 'New', color: '#6b7280', count: 12 },
  { id: 'enriched', label: 'Enriched', color: 'var(--accent-blue)', count: 18 },
  { id: 'sequenced', label: 'Sequenced', color: 'var(--accent-purple)', count: 24 },
  { id: 'replied', label: 'Replied', color: 'var(--accent-amber)', count: 8 },
  { id: 'qualified', label: 'Qualified', color: 'var(--accent-green)', count: 6 },
  { id: 'booked', label: 'Booked', color: '#10b981', count: 4 },
];

const MOCK_LEADS = [
  {
    id: 'lead-1',
    name: 'Sarah Chen',
    company: 'DataStack AI',
    title: 'VP of Revenue Operations',
    score: 95,
    status: 'enriched',
    email: 'sarah.chen@datastack.ai',
    phone: '+1 (415) 892-4102',
    techStack: ['Salesforce', 'HubSpot', 'Outreach', 'Snowflake'],
    signals: ['Champion Job Change', 'RB2B Pricing Visit'],
    enrichmentChain: ['Clearbit (98%)', 'Apollo (92%)', 'Hunter (100%)'],
    lastActivity: '14m ago',
    variantA: {
      subject: 'quick thought on DataStack\'s RevOps setup',
      body: 'Hi Sarah, congrats on taking over the VP RevOps seat at DataStack. Knowing how effective intent-driven outbound was during your tenure at Acme, I wanted to share how our autonomous signal agent helps scaling RevOps teams generate 3x more pipeline per rep without the deliverability overhead. Worth a quick 2-minute look?'
    },
    variantB: {
      subject: 'DataStack AI + signal-driven outbound',
      body: 'Hi Sarah, saw your recent move to DataStack AI. Most RevOps leaders entering new roles audit their tech stack to prune unused seat licenses. We replace static sequences with real-time intent triggers (funding, tech changes, job updates). Open to comparing benchmarks?'
    }
  },
  {
    id: 'lead-2',
    name: 'Marcus Rodriguez',
    company: 'TechFlow Systems',
    title: 'Chief Revenue Officer',
    score: 92,
    status: 'sequenced',
    email: 'marcus@techflow.io',
    phone: '+1 (650) 412-9011',
    techStack: ['Salesforce', 'Gainsight', 'ChiliPiper'],
    signals: ['Series B $18M Funding', 'Hiring Surge'],
    enrichmentChain: ['Clearbit (95%)', 'Prospeo (94%)'],
    lastActivity: '1h ago',
    variantA: {
      subject: 'scaling TechFlow\'s Series B outbound team',
      body: 'Hi Marcus, congrats on TechFlow\'s $18M Series B. As you double sales headcount, I wanted to show you how our signal agent automates 80% of SDR research work so new reps hit quota in 14 days. Worth a look?'
    },
    variantB: {
      subject: 'TechFlow Series B pipeline velocity',
      body: 'Hi Marcus, Series B growth usually means hiring more SDRs or making existing reps 3x more efficient. SignalSDR reaches out only when active intent signals strike. Let\'s chat?'
    }
  },
  {
    id: 'lead-3',
    name: 'Emily Watson',
    company: 'CloudNova Inc',
    title: 'Head of Growth',
    score: 84,
    status: 'replied',
    email: 'emily@cloudnova.com',
    phone: '+1 (312) 554-1092',
    techStack: ['HubSpot', 'Marketo', 'Pipedrive'],
    signals: ['Competitor Removal', 'Website Visit'],
    enrichmentChain: ['Apollo (90%)', 'Hunter (96%)'],
    lastActivity: '3h ago',
    variantA: {
      subject: 'replacing legacy sequence tools at CloudNova?',
      body: 'Hi Emily, noticed CloudNova recently dropped your legacy sequence platform. We provide an autonomous signal SDR that delivers 18.4% reply rates with zero spam complaints. Open to a brief preview?'
    },
    variantB: {
      subject: 'CloudNova growth stack update',
      body: 'Hi Emily, saw your team evaluating outbound stack alternatives. SignalSDR monitors buying signals and sends personalized emails automatically. Would love to share details.'
    }
  },
  {
    id: 'lead-4',
    name: 'James Wilson',
    company: 'PulseAI Labs',
    title: 'Chief Executive Officer',
    score: 90,
    status: 'qualified',
    email: 'jwilson@pulseai.io',
    phone: '+1 (212) 901-8843',
    techStack: ['Salesforce', 'G2', 'Bombora'],
    signals: ['Pricing Page Visit', 'SEC Filing Mention'],
    enrichmentChain: ['Clearbit (99%)', 'Apollo (96%)'],
    lastActivity: '2h ago',
    variantA: {
      subject: 'PulseAI pricing visit & outbound efficiency',
      body: 'Hi James, noticed 3 leaders from PulseAI spending time on our enterprise pricing breakdown. Happy to put together a tailored pipeline assessment for your team.'
    },
    variantB: {
      subject: 'PulseAI Labs + SignalSDR',
      body: 'Hi James, thanks for checking out our solution. We help executive teams automate signal-driven pipeline creation. Let\'s schedule a brief conversation.'
    }
  }
];

export default function LeadsPage() {
  const [view, setView] = useState<'kanban' | 'table'>('kanban');
  const [selectedLead, setSelectedLead] = useState<any | null>(null);
  const [selectedModel, setSelectedModel] = useState<'gpt4o' | 'claude35'>('claude35');
  const [selectedVariant, setSelectedVariant] = useState<'A' | 'B'>('A');
  const [editableSubject, setEditableSubject] = useState('');
  const [editableBody, setEditableBody] = useState('');
  const [scheduled, setScheduled] = useState(false);

  const handleOpenLead = (lead: any) => {
    setSelectedLead(lead);
    setSelectedVariant('A');
    setEditableSubject(lead.variantA.subject);
    setEditableBody(lead.variantA.body);
    setScheduled(false);
  };

  const handleVariantSwitch = (varKey: 'A' | 'B') => {
    setSelectedVariant(varKey);
    if (selectedLead) {
      if (varKey === 'A') {
        setEditableSubject(selectedLead.variantA.subject);
        setEditableBody(selectedLead.variantA.body);
      } else {
        setEditableSubject(selectedLead.variantB.subject);
        setEditableBody(selectedLead.variantB.body);
      }
    }
  };

  const handleScheduleOutreach = () => {
    setScheduled(true);
    setTimeout(() => {
      setSelectedLead(null);
    }, 1200);
  };

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <div>
          <h1 className={styles.title}>Waterfall Lead Pipeline & AI Studio</h1>
          <p className={styles.subtitle}>Sequential multi-provider enrichment with AI copy variants</p>
        </div>
        <div className={styles.viewToggle}>
          <button 
            className={`${styles.toggleBtn} ${view === 'kanban' ? styles.active : ''}`}
            onClick={() => setView('kanban')}
          >
            Kanban Board
          </button>
          <button 
            className={`${styles.toggleBtn} ${view === 'table' ? styles.active : ''}`}
            onClick={() => setView('table')}
          >
            Data Table
          </button>
        </div>
      </header>

      {/* Waterfall Banner */}
      <div className={styles.waterfallBanner}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Layers size={20} color="var(--accent-blue)" />
          <span style={{ fontWeight: 700, fontSize: '14px' }}>Active Waterfall Enrichment Chain:</span>
        </div>
        <div className={styles.providerChain}>
          <span className={styles.providerChip}><CheckCircle2 size={12} color="var(--accent-green)" /> Clearbit (98% match)</span>
          <span>&rarr;</span>
          <span className={styles.providerChip}><CheckCircle2 size={12} color="var(--accent-green)" /> Apollo.io (94% match)</span>
          <span>&rarr;</span>
          <span className={styles.providerChip}><CheckCircle2 size={12} color="var(--accent-green)" /> Prospeo (91% match)</span>
          <span>&rarr;</span>
          <span className={styles.providerChip}><CheckCircle2 size={12} color="var(--accent-green)" /> Hunter Verification</span>
        </div>
      </div>

      {/* Kanban Board */}
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
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <div>
                        <div className={styles.leadName}>{lead.name}</div>
                        <div className={styles.leadCompany}>{lead.company}</div>
                      </div>
                      <div className={`${styles.scoreBadge} ${lead.score >= 80 ? styles.scoreHigh : styles.scoreMed}`}>
                        {lead.score}
                      </div>
                    </div>
                    <div className={styles.leadTitle}>{lead.title}</div>

                    <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginTop: '4px' }}>
                      {lead.techStack.slice(0, 2).map(t => (
                        <span key={t} style={{ fontSize: '10px', padding: '2px 6px', borderRadius: '6px', background: 'var(--bg-primary)', color: 'var(--text-muted)' }}>
                          {t}
                        </span>
                      ))}
                    </div>

                    <div className={styles.cardBottom}>
                      <div style={{ fontSize: '11px', color: 'var(--accent-green)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <Mail size={12} /> Verified
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
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Name</th>
                <th>Company</th>
                <th>Title</th>
                <th>Verified Email</th>
                <th>Intent Score</th>
                <th>Tech Stack</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {MOCK_LEADS.map(lead => (
                <tr key={lead.id} onClick={() => handleOpenLead(lead)} style={{ cursor: 'pointer' }}>
                  <td style={{ fontWeight: 700 }}>{lead.name}</td>
                  <td>{lead.company}</td>
                  <td style={{ color: 'var(--text-secondary)' }}>{lead.title}</td>
                  <td style={{ color: 'var(--accent-green)', fontWeight: 600 }}>{lead.email}</td>
                  <td>
                    <span className={`${styles.scoreBadge} ${lead.score >= 80 ? styles.scoreHigh : styles.scoreMed}`}>
                      {lead.score}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '4px' }}>
                      {lead.techStack.map(t => (
                        <span key={t} style={{ fontSize: '11px', padding: '2px 6px', borderRadius: '4px', background: 'var(--bg-surface-active)' }}>
                          {t}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td>
                    <button className={styles.toggleBtn} style={{ background: 'var(--accent-blue-glow)', color: 'var(--accent-blue)' }}>
                      <Sparkles size={14} /> AI Studio
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Slide-Over AI Copywriting Studio Drawer */}
      {selectedLead && (
        <div className={styles.drawer}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <div style={{ fontSize: '12px', color: 'var(--accent-blue)', fontWeight: 700, textTransform: 'uppercase' }}>
                AI Copywriting Studio & Inspector
              </div>
              <h2 style={{ fontSize: '22px', fontWeight: 800 }}>{selectedLead.name}</h2>
              <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
                {selectedLead.title} at <strong>{selectedLead.company}</strong>
              </div>
            </div>
            <button 
              onClick={() => setSelectedLead(null)}
              style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
            >
              <X size={24} />
            </button>
          </div>

          {/* Firmographic Card */}
          <div style={{ background: 'var(--bg-primary)', padding: '16px', borderRadius: '14px', border: '1px solid var(--border-subtle)', display: 'grid', gridTemplate-Columns: 'repeat(2, 1fr)', gap: '12px', fontSize: '13px' }}>
            <div><span style={{ color: 'var(--text-muted)' }}>Email:</span> <strong style={{ color: 'var(--accent-green)' }}>{selectedLead.email}</strong></div>
            <div><span style={{ color: 'var(--text-muted)' }}>Phone:</span> <strong>{selectedLead.phone}</strong></div>
            <div><span style={{ color: 'var(--text-muted)' }}>Intent Score:</span> <strong style={{ color: 'var(--accent-green)' }}>{selectedLead.score} / 100</strong></div>
            <div><span style={{ color: 'var(--text-muted)' }}>Enrichment:</span> <strong>Waterfall Verified</strong></div>
          </div>

          {/* Model Selector */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'var(--glass-bg)', padding: '12px 16px', borderRadius: '12px', border: '1px solid var(--glass-border)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px', fontWeight: 600 }}>
              <Cpu size={18} color="var(--accent-purple)" /> Select AI Model Engine:
            </div>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button 
                onClick={() => setSelectedModel('claude35')}
                style={{
                  padding: '6px 12px', borderRadius: '8px', fontSize: '12px', fontWeight: 600, border: 'none', cursor: 'pointer',
                  background: selectedModel === 'claude35' ? 'var(--accent-purple)' : 'transparent',
                  color: selectedModel === 'claude35' ? 'white' : 'var(--text-muted)'
                }}
              >
                Claude 3.5 Sonnet
              </button>
              <button 
                onClick={() => setSelectedModel('gpt4o')}
                style={{
                  padding: '6px 12px', borderRadius: '8px', fontSize: '12px', fontWeight: 600, border: 'none', cursor: 'pointer',
                  background: selectedModel === 'gpt4o' ? 'var(--accent-blue)' : 'transparent',
                  color: selectedModel === 'gpt4o' ? 'white' : 'var(--text-muted)'
                }}
              >
                GPT-4o (OpenAI)
              </button>
            </div>
          </div>

          {/* A/B Variant Generator */}
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
              <div style={{ fontSize: '14px', fontWeight: 700 }}>A/B Copy Variants:</div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button
                  onClick={() => handleVariantSwitch('A')}
                  style={{
                    padding: '6px 14px', borderRadius: '8px', fontSize: '12px', fontWeight: 700, border: 'none', cursor: 'pointer',
                    background: selectedVariant === 'A' ? 'var(--accent-blue)' : 'var(--bg-primary)',
                    color: selectedVariant === 'A' ? 'white' : 'var(--text-secondary)'
                  }}
                >
                  Variant A (Short Hook)
                </button>
                <button
                  onClick={() => handleVariantSwitch('B')}
                  style={{
                    padding: '6px 14px', borderRadius: '8px', fontSize: '12px', fontWeight: 700, border: 'none', cursor: 'pointer',
                    background: selectedVariant === 'B' ? 'var(--accent-blue)' : 'var(--bg-primary)',
                    color: selectedVariant === 'B' ? 'white' : 'var(--text-secondary)'
                  }}
                >
                  Variant B (Value POV)
                </button>
              </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <div>
                <label style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 600 }}>Subject Line</label>
                <input 
                  type="text" 
                  value={editableSubject} 
                  onChange={(e) => setEditableSubject(e.target.value)}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: '10px', background: 'var(--bg-primary)', border: '1px solid var(--border-subtle)', color: 'var(--text-primary)', marginTop: '4px', fontSize: '14px' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 600 }}>Personalized Email Body</label>
                <textarea 
                  rows={6}
                  value={editableBody} 
                  onChange={(e) => setEditableBody(e.target.value)}
                  style={{ width: '100%', padding: '12px 14px', borderRadius: '10px', background: 'var(--bg-primary)', border: '1px solid var(--border-subtle)', color: 'var(--text-primary)', marginTop: '4px', fontSize: '14px', lineHeight: '1.5' }}
                />
              </div>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '16px', fontSize: '12px', color: 'var(--accent-green)', background: 'var(--accent-green-glow)', padding: '12px 16px', borderRadius: '10px' }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}><CheckCircle2 size={14} /> Flesch Reading Score: 88</span>
            <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}><ShieldCheck size={14} /> GDPR Art. 14 LIA Documented</span>
          </div>

          <button 
            onClick={handleScheduleOutreach}
            disabled={scheduled}
            style={{
              background: scheduled ? 'var(--accent-green)' : 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
              color: 'white',
              border: 'none',
              padding: '16px',
              borderRadius: '14px',
              fontWeight: 700,
              fontSize: '15px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              boxShadow: '0 4px 16px var(--accent-blue-glow)'
            }}
          >
            {scheduled ? (
              <> <CheckCircle2 size={20} /> Outreach Scheduled to Queue! </>
            ) : (
              <> <Send size={20} /> Approve & Dispatch Sequence </>
            )}
          </button>
        </div>
      )}
    </div>
  );
}
