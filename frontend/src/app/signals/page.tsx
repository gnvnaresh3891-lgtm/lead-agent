'use client';

import { useState } from 'react';
import { 
  Zap, Filter, Search, Code, CheckCircle2, 
  Sparkles, X, ArrowUpRight, ShieldCheck, Play 
} from 'lucide-react';
import styles from './page.module.css';

const ENHANCED_SIGNALS = [
  {
    id: 'sig-101',
    type: 'Job Change',
    emoji: '👤',
    score: 95,
    company: 'DataStack AI',
    source: 'LinkedIn API',
    title: 'Sarah Chen Appointed as VP Revenue Operations',
    desc: 'Sarah Chen updated her LinkedIn profile from Director of RevOps at Acme to VP of Revenue Operations at DataStack AI. First 90 days represent prime window for sales stack evaluation.',
    detected: '14 mins ago',
    tags: ['Champion Job Change', 'C-Suite Target', 'High Intent'],
    color: 'var(--accent-purple-glow)',
    payload: {
      event: 'job_change_detected',
      prospect: { name: 'Sarah Chen', title: 'VP Revenue Operations', prev_company: 'Acme Corp' },
      company: { name: 'DataStack AI', domain: 'datastack.ai', size: 280, arr: '$25M' },
      confidence_score: 0.98,
      decay_factor: 1.0,
    }
  },
  {
    id: 'sig-102',
    type: 'Funding Round',
    emoji: '🚀',
    score: 92,
    company: 'TechFlow Systems',
    source: 'Crunchbase RSS',
    title: 'Closed $18M Series B led by Sequoia Capital',
    desc: 'TechFlow Systems announced an $18M Series B expansion round to scale GTM operations and double engineering headcount over the next two quarters.',
    detected: '1 hour ago',
    tags: ['Series B', 'GTM Expansion', 'Capital Influx'],
    color: 'var(--accent-blue-glow)',
    payload: {
      event: 'funding_round_closed',
      amount_usd: 18000000,
      round: 'Series B',
      lead_investor: 'Sequoia Capital',
      company: { name: 'TechFlow Systems', domain: 'techflow.io', headcount: 140 },
      confidence_score: 0.96,
      decay_factor: 0.98,
    }
  },
  {
    id: 'sig-103',
    type: 'Website Pricing Visit',
    emoji: '👑',
    score: 90,
    company: 'PulseAI Labs',
    source: 'RB2B De-anonymizer',
    title: '3 Executive Stakeholders Visited Pricing & Security Pages',
    desc: 'De-anonymized 3 visitors from PulseAI Labs (CRO, Director of Security, VP Sales Ops) spending 4.5 minutes on the Enterprise Pricing breakdown page.',
    detected: '2 hours ago',
    tags: ['Multi-Stakeholder', 'Pricing Page', 'High Intent'],
    color: 'var(--accent-green-glow)',
    payload: {
      event: 'de_anonymized_visit',
      domain: 'pulseai.io',
      visitors: [
        { role: 'CRO', duration: 240 },
        { role: 'VP Sales Ops', duration: 180 }
      ],
      pages: ['/pricing', '/enterprise-security'],
      confidence_score: 0.94,
    }
  },
  {
    id: 'sig-104',
    type: 'Competitor Switch',
    emoji: '🔧',
    score: 84,
    company: 'CloudNova Inc',
    source: 'BuiltWith Tracker',
    title: 'Removed Competitor Outreach Tool from Tech Stack',
    desc: 'Detected removal of legacy email sequence scripts from main web domain. Indicates active evaluation of alternative sales automation providers.',
    detected: '4 hours ago',
    tags: ['Tech Stack Drop', 'Competitor Replacement'],
    color: 'var(--accent-amber-glow)',
    payload: {
      event: 'tech_stack_removed',
      dropped_tool: 'LegacyOutreachV1',
      domain: 'cloudnova.com',
      confidence_score: 0.91,
    }
  },
  {
    id: 'sig-105',
    type: 'Hiring Surge',
    emoji: '📊',
    score: 78,
    company: 'Vertex Solutions',
    source: 'Indeed & LinkedIn Scraper',
    title: 'Opened 18 New Roles in Sales & RevOps',
    desc: 'Vertex Solutions posted 18 new positions in revenue operations and account management within the last 72 hours, indicating rapid GTM scaling.',
    detected: '1 day ago',
    tags: ['Hiring Surge', 'Headcount Growth'],
    color: 'var(--accent-blue-glow)',
    payload: {
      event: 'hiring_surge_detected',
      department: 'Sales & RevOps',
      open_roles_count: 18,
      headcount_growth_pct: 28,
      confidence_score: 0.88,
    }
  }
];

export default function SignalsPage() {
  const [filter, setFilter] = useState<'all' | 'hot' | 'warm'>('all');
  const [search, setSearch] = useState('');
  const [signals, setSignals] = useState(ENHANCED_SIGNALS);
  const [selectedSignal, setSelectedSignal] = useState<any | null>(null);
  const [simulating, setSimulating] = useState(false);
  const [notification, setNotification] = useState<string | null>(null);

  const filteredSignals = signals.filter(sig => {
    if (filter === 'hot' && sig.score < 80) return false;
    if (filter === 'warm' && (sig.score >= 80 || sig.score < 60)) return false;
    if (search) {
      const q = search.toLowerCase();
      return (
        sig.company.toLowerCase().includes(q) ||
        sig.title.toLowerCase().includes(q) ||
        sig.type.toLowerCase().includes(q)
      );
    }
    return true;
  });

  const handleSimulateWebhook = () => {
    setSimulating(true);
    setTimeout(() => {
      const newSignal = {
        id: `sig-${Date.now()}`,
        type: 'De-anonymized Visit',
        emoji: '⚡',
        score: 96,
        company: 'ScaleGrid Systems',
        source: 'Koala Webhook',
        title: 'VP of RevOps & CRO Visited Demo Page',
        desc: 'Real-time webhook trigger: 2 decision makers from ScaleGrid Systems spent 3.8 mins reviewing product feature comparisons.',
        detected: 'Just now',
        tags: ['Live Webhook', 'High Intent', 'Pricing Visit'],
        color: 'var(--accent-green-glow)',
        payload: {
          event: 'webhook_live_ingest',
          company: 'ScaleGrid Systems',
          domain: 'scalegrid.io',
          intent_rating: 'VERY_HIGH',
          timestamp: new Date().toISOString()
        }
      };
      setSignals(prev => [newSignal, ...prev]);
      setSimulating(false);
      setNotification(`Received live webhook signal for ScaleGrid Systems (Score: 96)`);
      setTimeout(() => setNotification(null), 4000);
    }, 600);
  };

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <div>
          <h1 className={styles.title}>Signal Intelligence Center</h1>
          <p className={styles.subtitle}>Continuous real-time intent monitoring across 10+ signals</p>
        </div>
        <div className={styles.actionGroup}>
          <button 
            onClick={handleSimulateWebhook}
            disabled={simulating}
            className={styles.primaryBtn}
          >
            <Zap size={16} /> {simulating ? 'Ingesting...' : '+ Fire Webhook Simulator'}
          </button>
        </div>
      </header>

      {notification && (
        <div style={{
          background: 'var(--accent-green-glow)',
          border: '1px solid var(--accent-green)',
          color: 'var(--accent-green)',
          padding: '14px 20px',
          borderRadius: '14px',
          fontSize: '13px',
          fontWeight: 600,
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          <CheckCircle2 size={18} /> {notification}
        </div>
      )}

      {/* Filter Bar */}
      <div className={styles.filterBar}>
        <div 
          className={`${styles.filterPill} ${filter === 'all' ? styles.active : ''}`}
          onClick={() => setFilter('all')}
        >
          All Signals ({signals.length})
        </div>
        <div 
          className={`${styles.filterPill} ${filter === 'hot' ? styles.active : ''}`}
          onClick={() => setFilter('hot')}
        >
          🔥 Hot Intent (Score 80+)
        </div>
        <div 
          className={`${styles.filterPill} ${filter === 'warm' ? styles.active : ''}`}
          onClick={() => setFilter('warm')}
        >
          ⚡ Warm Intent (60-79)
        </div>
        <div style={{ flexGrow: 1 }} />
        <input 
          type="text" 
          placeholder="Filter by company, signal type..." 
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className={styles.search}
        />
      </div>

      {/* Signal Cards Feed */}
      <div className={styles.signalList}>
        {filteredSignals.map((sig) => (
          <div 
            key={sig.id} 
            className={styles.signalCard}
            onClick={() => setSelectedSignal(sig)}
          >
            <div className={styles.cardMain}>
              <div className={styles.signalHeader}>
                <div className={styles.iconBox} style={{ background: sig.color }}>
                  {sig.emoji}
                </div>
                <div>
                  <div className={styles.companyName}>
                    {sig.company}
                    <span className={styles.sourceBadge}>{sig.source}</span>
                  </div>
                  <div className={styles.signalTitle}>{sig.title}</div>
                  <div className={styles.signalDesc}>{sig.desc}</div>
                </div>
              </div>

              <div className={`${styles.scoreRing} ${sig.score >= 80 ? styles.scoreHigh : styles.scoreMed}`}>
                {sig.score}
              </div>
            </div>

            <div className={styles.cardFooter}>
              <div className={styles.tags}>
                {sig.tags.map(t => (
                  <span key={t} className={styles.tag}>{t}</span>
                ))}
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', fontSize: '13px', color: 'var(--text-muted)' }}>
                <span>{sig.detected}</span>
                <span style={{ color: 'var(--accent-blue)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '4px' }}>
                  Inspect Payload <ArrowUpRight size={14} />
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Raw Signal Inspection Drawer */}
      {selectedSignal && (
        <div className={styles.drawer}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Code size={20} color="var(--accent-blue)" />
              <h3 style={{ fontSize: '18px', fontWeight: 700 }}>Signal Payload Inspector</h3>
            </div>
            <button 
              onClick={() => setSelectedSignal(null)}
              style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
            >
              <X size={20} />
            </button>
          </div>

          <div style={{ background: 'var(--bg-primary)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '14px', fontWeight: 700, marginBottom: '4px' }}>
              {selectedSignal.company} — {selectedSignal.type}
            </div>
            <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              Source: {selectedSignal.source} | Detected: {selectedSignal.detected}
            </div>
          </div>

          <div>
            <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '8px' }}>
              Raw Ingested JSON Payload
            </div>
            <pre className={styles.jsonBox}>
              {JSON.stringify(selectedSignal.payload, null, 2)}
            </pre>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-secondary)' }}>
              Automated SDR Action Triggers
            </div>
            <button 
              className={styles.primaryBtn}
              onClick={() => {
                alert(`Triggered automated outreach campaign for ${selectedSignal.company}!`);
                setSelectedSignal(null);
              }}
              style={{ justifyContent: 'center' }}
            >
              <Play size={16} /> Execute Outreach Sequence Now
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
