'use client';

import { useState } from 'react';
import { X, Plus } from 'lucide-react';
import styles from './page.module.css';

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState<'icp' | 'integrations' | 'domains'>('icp');

  const INTEGRATIONS = [
    { name: 'HubSpot', desc: 'CRM & marketing automation', connected: true, color: '#ff7a59' },
    { name: 'Salesforce', desc: 'Enterprise CRM platform', connected: false, color: '#00a1e0' },
    { name: 'Slack', desc: 'Team notifications & alerts', connected: true, color: '#4a154b' },
    { name: 'Google Calendar', desc: 'Meeting scheduling', connected: true, color: '#4285f4' },
    { name: 'LinkedIn Sales Nav', desc: 'Social selling platform', connected: false, color: '#0a66c2' },
    { name: 'Zapier', desc: 'Workflow automation', connected: false, color: '#ff4f00' }
  ];

  const DOMAINS = [
    { name: 'getsignalsdr.com', status: 'Active', spf: true, dkim: true, dmarc: true, sent: 28, limit: 40, warmup: 100 },
    { name: 'signalsdr.io', status: 'Warming', spf: true, dkim: true, dmarc: false, sent: 8, limit: 15, warmup: 62 },
    { name: 'trysignalsdr.com', status: 'Paused', spf: true, dkim: false, dmarc: false, sent: 0, limit: 0, warmup: 34 }
  ];

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}>Settings</h1>
        <p className={styles.subtitle}>Manage your AI SDR configuration</p>
      </header>

      <div className={styles.tabsContainer}>
        <button 
          className={`${styles.tab} ${activeTab === 'icp' ? styles.active : ''}`}
          onClick={() => setActiveTab('icp')}
        >
          ICP Configuration
        </button>
        <button 
          className={`${styles.tab} ${activeTab === 'integrations' ? styles.active : ''}`}
          onClick={() => setActiveTab('integrations')}
        >
          Integrations
        </button>
        <button 
          className={`${styles.tab} ${activeTab === 'domains' ? styles.active : ''}`}
          onClick={() => setActiveTab('domains')}
        >
          Sending Domains
        </button>
      </div>

      {activeTab === 'icp' && (
        <div>
          <div className={styles.section}>
            <div className={styles.sectionHeader}>
              <div className={styles.sectionTitle}>Target Industries</div>
              <div className={styles.sectionSubtitle}>Which verticals to target</div>
            </div>
            <div className={styles.chipsContainer}>
              {['B2B SaaS', 'Fintech', 'Cloud Infrastructure', 'MarTech', 'DevTools'].map((ind) => (
                <div key={ind} className={styles.chip}>
                  {ind}
                  <button className={styles.chipClose}><X size={14} /></button>
                </div>
              ))}
              <button className={styles.addBtn}>+ Add Industry</button>
            </div>
          </div>

          <div className={styles.section}>
            <div className={styles.sectionHeader}>
              <div className={styles.sectionTitle}>Company Size</div>
              <div className={styles.sectionSubtitle}>Employee count range</div>
            </div>
            <div className={styles.rangeBarDisplay}>50 - 500 employees</div>
            <div className={styles.rangeBarContainer}>
              <div className={styles.rangeBarFill} style={{ left: '20%', width: '40%' }}></div>
            </div>
          </div>

          <div className={styles.section}>
            <div className={styles.sectionHeader}>
              <div className={styles.sectionTitle}>Revenue Range</div>
              <div className={styles.sectionSubtitle}>Estimated annual revenue (ARR)</div>
            </div>
            <div className={styles.rangeBarDisplay}>$5M - $100M ARR</div>
            <div className={styles.rangeBarContainer}>
              <div className={styles.rangeBarFill} style={{ left: '15%', width: '55%' }}></div>
            </div>
          </div>

          <div className={styles.section}>
            <div className={styles.sectionHeader}>
              <div className={styles.sectionTitle}>Target Technologies</div>
              <div className={styles.sectionSubtitle}>Companies using these platforms</div>
            </div>
            <div className={styles.chipsContainer}>
              {['Salesforce', 'HubSpot', 'Outreach', 'Apollo', 'Slack'].map((tech) => (
                <div key={tech} className={styles.chip}>
                  {tech}
                  <button className={styles.chipClose}><X size={14} /></button>
                </div>
              ))}
              <button className={styles.addBtn}>+ Add Technology</button>
            </div>
          </div>

          <div className={styles.section}>
            <div className={styles.sectionHeader}>
              <div className={styles.sectionTitle}>Target Regions</div>
              <div className={styles.sectionSubtitle}>Geographic focus</div>
            </div>
            <div className={styles.chipsContainer}>
              {['United States', 'United Kingdom', 'Canada', 'Germany', 'Australia'].map((region) => (
                <div key={region} className={styles.chip}>
                  {region}
                  <button className={styles.chipClose}><X size={14} /></button>
                </div>
              ))}
              <button className={styles.addBtn}>+ Add Region</button>
            </div>
          </div>

          <div className={styles.section}>
            <div className={styles.sectionHeader}>
              <div className={styles.sectionTitle}>Excluded Domains</div>
              <div className={styles.sectionSubtitle}>Do not contact these companies</div>
            </div>
            <div className={styles.textDisplay}>competitor1.com, competitor2.com, bigcorp.com</div>
          </div>

          <button className={styles.saveBtn}>Save Configuration</button>
        </div>
      )}

      {activeTab === 'integrations' && (
        <div className={styles.grid}>
          {INTEGRATIONS.map((integ) => (
            <div key={integ.name} className={styles.card}>
              <div className={styles.cardHeader}>
                <div className={styles.logoCircle} style={{ backgroundColor: integ.color }}>
                  {integ.name.charAt(0)}
                </div>
                <div>
                  <div className={styles.cardTitle}>{integ.name}</div>
                  <div className={styles.cardDesc}>{integ.desc}</div>
                </div>
              </div>
              <div className={styles.cardFooter}>
                <div className={`${styles.badge} ${integ.connected ? styles.badgeConnected : styles.badgeNotConnected}`}>
                  {integ.connected ? 'Connected' : 'Not Connected'}
                </div>
                <button className={`${styles.actionBtn} ${integ.connected ? styles.btnDisconnect : styles.btnConnect}`}>
                  {integ.connected ? 'Disconnect' : 'Connect'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'domains' && (
        <div className={styles.section} style={{ padding: 0 }}>
          <div className={styles.tableHeader} style={{ padding: '24px 24px 0' }}>
            <h2 className={styles.sectionTitle} style={{ marginBottom: 0 }}>Connected Domains</h2>
            <button className={`${styles.actionBtn} ${styles.btnConnect}`}>
              <Plus size={16} style={{ display: 'inline', marginRight: '4px', verticalAlign: 'text-bottom' }} /> 
              Add Domain
            </button>
          </div>
          <div style={{ overflowX: 'auto', padding: '0 24px 24px' }}>
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>Domain</th>
                  <th>Status</th>
                  <th>SPF</th>
                  <th>DKIM</th>
                  <th>DMARC</th>
                  <th>Sent Today</th>
                  <th>Daily Limit</th>
                  <th>Warmup</th>
                </tr>
              </thead>
              <tbody>
                {DOMAINS.map((domain) => (
                  <tr key={domain.name}>
                    <td style={{ fontWeight: 500 }}>{domain.name}</td>
                    <td>
                      <span className={`${styles.badge} ${domain.status === 'Active' ? styles.statusActive : domain.status === 'Warming' ? styles.statusWarming : styles.statusPaused}`}>
                        {domain.status === 'Active' ? '✅' : domain.status === 'Warming' ? '🟡' : '⏸️'} {domain.status}
                      </span>
                    </td>
                    <td className={styles.authIcon}>{domain.spf ? '✅' : '❌'}</td>
                    <td className={styles.authIcon}>{domain.dkim ? '✅' : '❌'}</td>
                    <td className={styles.authIcon}>{domain.dmarc ? '✅' : '❌'}</td>
                    <td>{domain.sent} / {domain.limit}</td>
                    <td>{domain.limit}</td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <div className={styles.warmupBarContainer}>
                          <div className={styles.warmupBarFill} style={{ width: `${domain.warmup}%` }}></div>
                        </div>
                        <span style={{ fontSize: '13px', color: 'var(--text-muted)' }}>{domain.warmup}%</span>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
