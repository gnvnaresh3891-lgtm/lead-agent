import styles from './page.module.css';

export default function CampaignsPage() {
  const campaigns = [
    { id: 1, name: 'Q3 Enterprise Outreach', desc: 'Targeting VP level at companies over 1000 employees', leads: 1248, sent: 1102, replies: 124, booked: 12, rate: 11.2, updated: '2h ago' },
    { id: 2, name: 'SaaS Leaders Nurture', desc: 'Nurture sequence for previous closed-lost opportunities', leads: 892, sent: 892, replies: 86, booked: 8, rate: 9.6, updated: '5h ago' },
    { id: 3, name: 'Competitor Switch Campaign', desc: 'Targeting users of legacy competitor tools', leads: 412, sent: 234, replies: 18, booked: 1, rate: 7.6, updated: '1d ago' },
    { id: 4, name: 'Funding Announcement Reachout', desc: 'Automated outreach to companies who raised Series A/B', leads: 156, sent: 156, replies: 32, booked: 5, rate: 20.5, updated: '3h ago' },
  ];

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <div>
          <h1 className={styles.title}>Campaigns</h1>
          <p className={styles.subtitle}>Manage your automated outreach sequences</p>
        </div>
        <button className={styles.btnPrimary}>+ New Campaign</button>
      </header>

      <div className={styles.grid}>
        {campaigns.map(camp => (
          <div key={camp.id} className={styles.card}>
            <div className={styles.cardTop}>
              <div>
                <div className={styles.campaignName}>{camp.name}</div>
                <div className={styles.campaignDesc}>{camp.desc}</div>
              </div>
              <div className={styles.statusPill}>Active</div>
            </div>

            <div className={styles.metrics}>
              <div className={styles.metric}>
                <span className={styles.metricValue}>{camp.leads}</span>
                <span className={styles.metricLabel}>Leads</span>
              </div>
              <div className={styles.metric}>
                <span className={styles.metricValue}>{camp.sent}</span>
                <span className={styles.metricLabel}>Sent</span>
              </div>
              <div className={styles.metric}>
                <span className={styles.metricValue}>{camp.replies}</span>
                <span className={styles.metricLabel}>Replies</span>
              </div>
              <div className={styles.metric}>
                <span className={styles.metricValue}>{camp.booked}</span>
                <span className={styles.metricLabel}>Booked</span>
              </div>
            </div>

            <div>
              <div className={styles.progressLabel}>
                <span>Reply Rate</span>
                <span style={{ color: 'var(--accent-blue)', fontWeight: 600 }}>{camp.rate}%</span>
              </div>
              <div className={styles.progressBar}>
                <div className={styles.progressFill} style={{ width: `${camp.rate * 4}%` }}></div>
              </div>
            </div>

            <div className={styles.cardActions}>
              <span className={styles.time}>Updated {camp.updated}</span>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button className={styles.btnSecondary}>Pause</button>
                <button className={styles.btnSecondary} style={{ background: 'rgba(255,255,255,0.1)' }}>View Details</button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
