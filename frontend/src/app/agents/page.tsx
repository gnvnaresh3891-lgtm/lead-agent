'use client';

import { useState, useEffect } from 'react';
import { Target, Github, Linkedin, Twitter, MessageSquare, Play, Square, Activity } from 'lucide-react';
import styles from './page.module.css';

interface AgentStatus {
  reddit: boolean;
  github: boolean;
  linkedin: boolean;
  x: boolean;
}

export default function AgentsPage() {
  const [status, setStatus] = useState<AgentStatus>({
    reddit: false,
    github: false,
    linkedin: false,
    x: false
  });

  const [loading, setLoading] = useState(true);
  const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    fetchStatus();
  }, []);

  const fetchStatus = async () => {
    try {
      // Use fallback defaults if backend is unreachable during build
      const res = await fetch(`${BACKEND_URL}/api/v1/agents/`).catch(() => null);
      if (res && res.ok) {
        const data = await res.json();
        setStatus(data);
      }
    } catch (e) {
      console.error("Failed to fetch agent status", e);
    } finally {
      setLoading(false);
    }
  };

  const toggleAgent = async (agentName: keyof AgentStatus) => {
    const isRunning = status[agentName];
    const action = isRunning ? 'stop' : 'start';
    
    // Optimistic update
    setStatus(prev => ({ ...prev, [agentName]: !isRunning }));

    try {
      await fetch(`${BACKEND_URL}/api/v1/agents/${agentName}/${action}`, {
        method: 'POST'
      });
    } catch (e) {
      console.error(`Failed to ${action} ${agentName}`, e);
      // Revert on failure
      setStatus(prev => ({ ...prev, [agentName]: isRunning }));
    }
  };

  const agents = [
    {
      id: 'reddit',
      name: 'Reddit Lead Agent',
      type: 'Pain-Point Interceptor',
      icon: <MessageSquare size={24} color="#ff4500" />,
      config: [
        { label: 'Subreddits', value: 'r/SaaS, r/sales' },
        { label: 'Keywords', value: '"alternative to", "need tool"' },
        { label: 'Ingest Rate', value: '~14 signals/hr' }
      ]
    },
    {
      id: 'github',
      name: 'GitHub Dev Agent',
      type: 'Technical Intent Monitor',
      icon: <Github size={24} color="#ffffff" />,
      config: [
        { label: 'Target Repos', value: 'competitor-a/core' },
        { label: 'Event Types', value: 'Star, Issues' },
        { label: 'Ingest Rate', value: '~4 signals/hr' }
      ]
    },
    {
      id: 'linkedin',
      name: 'LinkedIn Stealth Agent',
      type: 'Executive Movement',
      icon: <Linkedin size={24} color="#0077b5" />,
      config: [
        { label: 'Target Accounts', value: 'Top 500 ICP list' },
        { label: 'Triggers', value: 'Job Change, Promo' },
        { label: 'Ingest Rate', value: '~2 signals/hr' }
      ]
    },
    {
      id: 'x',
      name: 'X (Twitter) Sentinel',
      type: 'Competitor Complaints',
      icon: <Twitter size={24} color="#1da1f2" />,
      config: [
        { label: 'Keywords', value: '"@competitor is down"' },
        { label: 'Min Follower Req.', value: '500+' },
        { label: 'Ingest Rate', value: '~8 signals/hr' }
      ]
    }
  ];

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Agent Control Center</h1>
          <p className={styles.subtitle}>Manage your specialized AI lead generation scrapers</p>
        </div>
      </div>

      <div className={styles.agentsGrid}>
        {agents.map((agent) => {
          const isRunning = status[agent.id as keyof AgentStatus];
          return (
            <div key={agent.id} className={styles.agentCard}>
              <div className={styles.agentHeader}>
                <div className={styles.agentInfo}>
                  <div className={styles.agentIcon}>{agent.icon}</div>
                  <div>
                    <div className={styles.agentName}>{agent.name}</div>
                    <div className={styles.agentType}>{agent.type}</div>
                  </div>
                </div>
                <div className={`${styles.agentStatus} ${isRunning ? styles.active : styles.inactive}`}>
                  <div className={styles.statusIndicator}></div>
                  {isRunning ? 'Listening' : 'Sleeping'}
                </div>
              </div>

              <div className={styles.agentConfig}>
                {agent.config.map((conf, idx) => (
                  <div key={idx} className={styles.configRow}>
                    <div className={styles.configLabel}>{conf.label}</div>
                    <div className={styles.configValue}>{conf.value}</div>
                  </div>
                ))}
              </div>

              <button 
                className={`${styles.actionButton} ${isRunning ? styles.buttonStop : styles.buttonStart}`}
                onClick={() => toggleAgent(agent.id as keyof AgentStatus)}
                disabled={loading}
              >
                {isRunning ? (
                  <><Square size={14} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'middle' }}/> Stop Agent</>
                ) : (
                  <><Play size={14} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'middle' }}/> Launch Agent</>
                )}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}
