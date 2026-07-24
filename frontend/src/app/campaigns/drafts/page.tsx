'use client';

import { useState } from 'react';
import { Bot, Check, X, Sparkles } from 'lucide-react';
import styles from './page.module.css';

export default function DraftsPage() {
  const [drafts, setDrafts] = useState([
    {
      id: 1,
      signalType: 'topic_intent',
      target: 'growth_hacker_99',
      company: 'Apollo Alternative Seeker',
      subject: 'quick question regarding your post in r/SaaS',
      body: "Hi growth_hacker_99,\n\nI saw your recent post about Looking for an alternative to Apollo.\n\nSince you're looking for solutions, I thought I'd reach out. Our platform natively handles exactly this by automating the workflow.\n\nWould you be open to a quick chat?\n\nBest,\nAlex",
      status: 'pending'
    },
    {
      id: 2,
      signalType: 'job_change',
      target: 'Marcus Rodriguez',
      company: 'DataStack',
      subject: 'congratulations on the new role at DataStack',
      body: "Hey Marcus,\n\nMassive congrats on stepping into the new role at DataStack.\n\nUsually, new leaders evaluate their tech stack in the first 90 days. If you're looking to scale outbound, we just launched a new playbook for teams like DataStack.\n\nWorth a quick look?\n\nCheers,\nAlex",
      status: 'pending'
    }
  ]);

  const handleAction = (id: number, action: 'approve' | 'reject') => {
    setDrafts(prev => prev.filter(d => d.id !== id));
    // In real app, call backend to mark approved/rejected
  };

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>AI Draft Review</h1>
          <p className={styles.subtitle}>Review zero-cost personalization drafts before sending</p>
        </div>
      </div>

      <div>
        {drafts.length === 0 ? (
          <div style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '40px' }}>
            <Bot size={48} style={{ margin: '0 auto 16px', opacity: 0.5 }} />
            <h3>All caught up!</h3>
            <p>No new drafts awaiting approval.</p>
          </div>
        ) : (
          drafts.map(draft => (
            <div key={draft.id} className={styles.draftCard}>
              <div className={styles.draftHeader}>
                <div>
                  <div className={styles.signalBadge}>
                    <Sparkles size={12} style={{ display: 'inline', marginRight: '4px' }}/>
                    Signal: {draft.signalType}
                  </div>
                  <div style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
                    Target: <strong>{draft.target}</strong> @ {draft.company}
                  </div>
                </div>
                <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                  Generated via Spintax Engine ($0 cost)
                </div>
              </div>
              
              <div className={styles.subjectLine}>
                Subject: {draft.subject}
              </div>
              
              <div className={styles.emailBody}>
                {draft.body}
              </div>

              <div className={styles.actionRow}>
                <button 
                  className={styles.btnApprove}
                  onClick={() => handleAction(draft.id, 'approve')}
                >
                  <Check size={16} style={{ display: 'inline', marginRight: '6px' }} />
                  Approve & Send
                </button>
                <button 
                  className={styles.btnReject}
                  onClick={() => handleAction(draft.id, 'reject')}
                >
                  <X size={16} style={{ display: 'inline', marginRight: '6px' }} />
                  Reject
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
