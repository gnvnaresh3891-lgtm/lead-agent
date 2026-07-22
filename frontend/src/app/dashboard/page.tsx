import Link from 'next/link';
import { Users, Zap, MessageSquare, Calendar } from 'lucide-react';
import styles from './page.module.css';

export default function Dashboard() {
  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}>Dashboard</h1>
        <p className={styles.subtitle}>Overview of your AI SDR performance</p>
      </header>

      <section className={styles.metricsGrid}>
        <div className={styles.card}>
          <div className={styles.cardTop}>
            <div className={styles.iconWrapper} style={{ background: 'var(--accent-blue-glow)', color: 'var(--accent-blue)' }}>
              <Users size={20} />
            </div>
            <div className={`${styles.trend} ${styles.positive}`}>+12%</div>
          </div>
          <div>
            <div className={styles.value}>2,847</div>
            <div className={styles.label}>Active Leads</div>
          </div>
          <div className={styles.glow} style={{ background: 'var(--accent-blue)', boxShadow: '0 0 10px var(--accent-blue)' }} />
        </div>
        
        <div className={styles.card}>
          <div className={styles.cardTop}>
            <div className={styles.iconWrapper} style={{ background: 'var(--accent-purple-glow)', color: 'var(--accent-purple)' }}>
              <Zap size={20} />
            </div>
            <div className={styles.trend}>this week</div>
          </div>
          <div>
            <div className={styles.value}>1,284</div>
            <div className={styles.label}>Signals Detected</div>
          </div>
          <div className={styles.glow} style={{ background: 'var(--accent-purple)', boxShadow: '0 0 10px var(--accent-purple)' }} />
        </div>

        <div className={styles.card}>
          <div className={styles.cardTop}>
            <div className={styles.iconWrapper} style={{ background: 'var(--accent-green-glow)', color: 'var(--accent-green)' }}>
              <MessageSquare size={20} />
            </div>
            <div className={`${styles.trend} ${styles.positive}`}>+3.2%</div>
          </div>
          <div>
            <div className={styles.value}>18.4%</div>
            <div className={styles.label}>Reply Rate</div>
          </div>
          <div className={styles.glow} style={{ background: 'var(--accent-green)', boxShadow: '0 0 10px var(--accent-green)' }} />
        </div>

        <div className={styles.card}>
          <div className={styles.cardTop}>
            <div className={styles.iconWrapper} style={{ background: 'var(--accent-amber-glow)', color: 'var(--accent-amber)' }}>
              <Calendar size={20} />
            </div>
            <div className={styles.trend}>this month</div>
          </div>
          <div>
            <div className={styles.value}>47</div>
            <div className={styles.label}>Meetings Booked</div>
          </div>
          <div className={styles.glow} style={{ background: 'var(--accent-amber)', boxShadow: '0 0 10px var(--accent-amber)' }} />
        </div>
      </section>

      <div className={styles.twoCol}>
        <section className={styles.section}>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>Recent Signals</h2>
            <Link href="/signals" className={styles.link}>View All &rarr;</Link>
          </div>
          
          <div className={styles.signalList}>
            {[
              { emoji: '🚀', type: 'Funding', company: 'TechFlow', desc: 'Raised $15M Series B led by Sequoia', time: '2h ago', score: 92 },
              { emoji: '👤', type: 'Job Change', company: 'DataStack', desc: 'Sarah Chen appointed as new VP Sales', time: '5h ago', score: 85 },
              { emoji: '📊', type: 'Hiring Surge', company: 'CloudNova', desc: 'Opened 15 new roles in engineering', time: '1d ago', score: 78 },
              { emoji: '🔧', type: 'Tech Change', company: 'Vertex Solutions', desc: 'Added Salesforce to their tech stack', time: '1d ago', score: 64 },
              { emoji: '👑', type: 'Leadership', company: 'PulseAI', desc: 'New CEO announced in press release', time: '2d ago', score: 88 },
            ].map((sig, i) => (
              <div key={i} className={styles.signalCard}>
                <div className={styles.signalType}>
                  <span className={styles.signalEmoji}>{sig.emoji}</span>
                  <span className={styles.signalLabel}>{sig.type}</span>
                </div>
                <div className={styles.signalContent}>
                  <div className={styles.company}>{sig.company}</div>
                  <div className={styles.desc}>{sig.desc}</div>
                </div>
                <div className={styles.signalMeta}>
                  <span className={styles.time}>{sig.time}</span>
                  <div className={`${styles.scoreBadge} ${sig.score >= 80 ? styles.scoreHigh : styles.scoreMed}`}>
                    {sig.score}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className={styles.section}>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>Lead Pipeline</h2>
          </div>
          
          <div className={styles.pipelineStack}>
            {[
              { label: 'New', count: 423, color: '#6b7280', pct: 15 },
              { label: 'Enriched', count: 312, color: 'var(--accent-blue)', pct: 11 },
              { label: 'Sequenced', count: 891, color: 'var(--accent-purple)', pct: 31 },
              { label: 'Replied', count: 287, color: 'var(--accent-amber)', pct: 10 },
              { label: 'Qualified', count: 156, color: 'var(--accent-green)', pct: 5 },
              { label: 'Booked', count: 47, color: '#10b981', pct: 2 },
            ].map((stage, i) => (
              <div key={i} className={styles.pipelineStage}>
                <div className={styles.stageHeader}>
                  <span style={{ color: stage.color }}>{stage.label}</span>
                  <span>{stage.count}</span>
                </div>
                <div className={styles.barTrack}>
                  <div 
                    className={styles.barFill} 
                    style={{ width: `${stage.pct}%`, background: stage.color }}
                  />
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>

      <section className={styles.section}>
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>Recent Campaigns</h2>
          <Link href="/campaigns" className={styles.link}>View All &rarr;</Link>
        </div>
        
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Campaign</th>
              <th>Status</th>
              <th>Sent</th>
              <th>Opened</th>
              <th>Replied</th>
              <th>Booked</th>
              <th>Reply Rate</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Q3 Enterprise Outreach</td>
              <td>
                <span className={`${styles.statusPill} ${styles.statusActive}`}>
                  <span className={styles.pulseDot}></span> Active
                </span>
              </td>
              <td>1,248</td>
              <td>48%</td>
              <td>124</td>
              <td>12</td>
              <td style={{ color: 'var(--accent-green)' }}>9.9%</td>
            </tr>
            <tr>
              <td>SaaS Leaders Nurture</td>
              <td>
                <span className={`${styles.statusPill} ${styles.statusActive}`}>
                  <span className={styles.pulseDot}></span> Active
                </span>
              </td>
              <td>892</td>
              <td>52%</td>
              <td>86</td>
              <td>8</td>
              <td style={{ color: 'var(--accent-green)' }}>9.6%</td>
            </tr>
            <tr>
              <td>Inbound Demo Requests</td>
              <td>
                <span className={styles.statusPill} style={{ background: 'var(--accent-blue-glow)', color: 'var(--accent-blue)' }}>
                  Completed
                </span>
              </td>
              <td>412</td>
              <td>68%</td>
              <td>112</td>
              <td>45</td>
              <td style={{ color: 'var(--accent-green)' }}>27.1%</td>
            </tr>
            <tr>
              <td>Competitor Switch Campaign</td>
              <td>
                <span className={styles.statusPill} style={{ background: 'var(--accent-amber-glow)', color: 'var(--accent-amber)' }}>
                  Paused
                </span>
              </td>
              <td>234</td>
              <td>32%</td>
              <td>18</td>
              <td>1</td>
              <td style={{ color: 'var(--accent-amber)' }}>7.6%</td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  );
}
