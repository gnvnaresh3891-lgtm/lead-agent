'use client';

import { useState } from 'react';
import { Zap, Send, Plus, CheckCircle2 } from 'lucide-react';
import styles from './page.module.css';

export default function SignalsPage() {
  const [signalList, setSignalList] = useState([
    {
      id: 1, type: 'Funding', emoji: '🚀', score: 95,
      company: 'TechFlow', title: 'Raised $15M Series B',
      desc: 'TechFlow recently closed a $15M Series B funding round led by Sequoia Capital. They indicated plans to rapidly scale their sales and marketing teams over the next 6 months.',
      time: '2 hours ago',
      tags: ['Target Account', 'High Intent', 'Sales Leadership'],
      color: 'var(--accent-purple-glow)'
    },
    {
      id: 2, type: 'Job Change', emoji: '👤', score: 88,
      company: 'DataStack', title: 'New VP of Sales: Sarah Chen',
      desc: 'Sarah Chen recently updated her LinkedIn profile, moving from Director of Sales at Acme to VP of Sales at DataStack. First 90 days are critical for new tooling decisions.',
      time: '5 hours ago',
      tags: ['Decision Maker', 'Champion'],
      color: 'var(--accent-blue-glow)'
    },
    {
      id: 3, type: 'Hiring Surge', emoji: '📊', score: 76,
      company: 'CloudNova', title: '15 New Open Roles in Engineering',
      desc: 'CloudNova has posted 15 new engineering roles in the last week, representing a 20% increase in department headcount. Strong indicator for developer tooling needs.',
      time: '1 day ago',
      tags: ['Growth Indicator'],
      color: 'var(--accent-green-glow)'
    },
    {
      id: 4, type: 'Tech Change', emoji: '🔧', score: 65,
      company: 'Vertex Solutions', title: 'Added Salesforce to Tech Stack',
      desc: 'Detected new DNS records and job postings indicating a shift to Salesforce CRM. Opportunity to pitch complementary ecosystem tools.',
      time: '1 day ago',
      tags: ['Tech Stack', 'Ecosystem'],
      color: 'var(--accent-amber-glow)'
    }
  ]);

  const [simulating, setSimulating] = useState(false);
  const [lastFired, setLastFired] = useState<string | null>(null);

  const handleSimulateWebhook = async () => {
    setSimulating(true);
    const mockWebhooks = [
      { type: 'Job Change', emoji: '👑', company: 'PulseAI', title: 'New CRO Appointed: Marcus Rodriguez', desc: 'RB2B de-anonymization webhook detected high intent visit to pricing page.', score: 92, tags: ['C-Suite', 'RB2B Webhook'] },
      { type: 'Funding', emoji: '🚀', company: 'ScaleGrid', title: 'Raised $22M Series C', desc: 'Crunchbase RSS feed detected Series C capital raise.', score: 94, tags: ['Series C', 'Capital Surge'] },
    ];
    const newSig = mockWebhooks[Math.floor(Math.random() * mockWebhooks.length)];

    try {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || 'https://leadagent-backend.onrender.com/api';
      await fetch(`${apiBase}/signals/webhook`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          source: 'rb2b_webhook',
          signal_type: 'website_visit',
          company_name: newSig.company,
          company_domain: `${newSig.company.toLowerCase()}.com`,
          title: 'VP Sales',
          signal_details: { page: '/pricing', duration_seconds: 180 }
        })
      });
    } catch (e) {
      console.warn('Webhook simulated locally:', e);
    }

    setSignalList(prev => [
      {
        id: Date.now(),
        type: newSig.type,
        emoji: newSig.emoji,
        company: newSig.company,
        title: newSig.title,
        desc: newSig.desc,
        score: newSig.score,
        time: 'Just now',
        tags: newSig.tags,
        color: 'var(--accent-green-glow)'
      },
      ...prev
    ]);

    setLastFired(newSig.company);
    setSimulating(false);
  };

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <div>
          <h1 className={styles.title}>Signals</h1>
          <p className={styles.subtitle}>Actionable intent intelligence on your target accounts</p>
        </div>
        <button 
          onClick={handleSimulateWebhook}
          disabled={simulating}
          className={styles.btnPrimary}
          style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
        >
          <Zap size={16} /> {simulating ? 'Firing Webhook...' : '+ Simulate Live Webhook Signal'}
        </button>
      </header>

      {lastFired && (
        <div style={{ background: 'var(--accent-green-glow)', border: '1px solid var(--accent-green)', color: 'var(--accent-green)', padding: '12px 16px', borderRadius: '12px', fontSize: '13px', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px' }}>
          <CheckCircle2 size={16} /> Real-Time Webhook Signal Received & Ingested for <strong>{lastFired}</strong>! Score: 90+
        </div>
      )}

      <div className={styles.filterBar}>
        <div className={styles.filterPill}>Signal Type &#9662;</div>
        <div className={styles.filterPill}>Score: 80+ &#9662;</div>
        <div className={styles.filterPill}>Last 7 Days &#9662;</div>
        <input type="text" placeholder="Search companies, signals..." className={styles.search} />
      </div>

      <div className={styles.signalList}>
        {signalList.map(sig => (
          <div key={sig.id} className={styles.signalCard}>
            <div className={styles.cardTop}>
              <div className={styles.iconCol}>
                <div className={styles.iconCircle} style={{ background: sig.color }}>
                  {sig.emoji}
                </div>
                <div className={`${styles.scoreBadge} ${sig.score >= 80 ? styles.scoreHigh : styles.scoreMed}`}>
                  {sig.score}
                </div>
              </div>
              
              <div className={styles.contentCol}>
                <div className={styles.companyRow}>
                  <div className={styles.companyName}>{sig.company}</div>
                  <div className={styles.time}>{sig.time}</div>
                </div>
                <div className={styles.signalTitle}>{sig.title}</div>
                <div className={styles.signalDesc}>{sig.desc}</div>
              </div>

              <div className={styles.actionCol}>
                <button className={styles.btnPrimary}>Generate Email</button>
                <button className={styles.linkBtn}>View Lead Info</button>
              </div>
            </div>
            
            <div className={styles.tagsRow}>
              {sig.tags.map(tag => (
                <span key={tag} className={styles.tag}>{tag}</span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
