import { CheckCircle, Info, Plus } from 'lucide-react';
import styles from './page.module.css';

export default function CompliancePage() {
  const SUPPRESSION_LIST = [
    { id: 1, email: 'john.doe@example.com', reason: 'Unsubscribe', source: 'Campaign reply', date: '2023-10-25' },
    { id: 2, email: 'admin@testcorp.com', reason: 'Bounce', source: 'System auto-detect', date: '2023-10-24' },
    { id: 3, email: 'sarah.smith@eu-domain.co.uk', reason: 'GDPR Objection', source: 'GDPR request', date: '2023-10-20' },
    { id: 4, email: 'info@bigcorp.com', reason: 'Manual', source: 'Admin manual', date: '2023-10-18' },
    { id: 5, email: 'support@techstart.io', reason: 'Complaint', source: 'System auto-detect', date: '2023-10-15' },
    { id: 6, email: 'marketing@agency.net', reason: 'Unsubscribe', source: 'Campaign reply', date: '2023-10-12' },
    { id: 7, email: 'sales@competitor.com', reason: 'Manual', source: 'Admin manual', date: '2023-10-10' },
    { id: 8, email: 'hello@startup.co', reason: 'Bounce', source: 'System auto-detect', date: '2023-10-05' },
    { id: 9, email: 'ceo@megacorp.com', reason: 'Complaint', source: 'Campaign reply', date: '2023-09-28' },
    { id: 10, email: 'data.protection@eu-corp.de', reason: 'GDPR Objection', source: 'GDPR request', date: '2023-09-20' },
    { id: 11, email: 'billing@service.com', reason: 'Manual', source: 'Admin manual', date: '2023-09-15' },
    { id: 12, email: 'test@test.com', reason: 'Bounce', source: 'System auto-detect', date: '2023-09-01' }
  ];

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}>Compliance Dashboard</h1>
        <p className={styles.subtitle}>Monitor deliverability and regulatory compliance</p>
      </header>

      <section className={styles.healthSection}>
        <div className={styles.gaugeContainer}>
          <div className={styles.gaugeInner}>
            <div className={styles.scoreValue}>96%</div>
          </div>
        </div>
        <div className={styles.scoreLabel}>Compliance Score</div>
      </section>

      <section className={styles.metricsGrid}>
        <div className={styles.metricCard}>
          <div className={styles.cardTop}>
            <div className={styles.metricLabel}>Spam Rate</div>
            <div className={`${styles.statusIcon} ${styles.statusGood}`}>
              <CheckCircle size={14} />
            </div>
          </div>
          <div>
            <div className={styles.metricValue}>0.04%</div>
            <div className={styles.threshold}>Threshold: &lt;0.10%</div>
          </div>
        </div>
        
        <div className={styles.metricCard}>
          <div className={styles.cardTop}>
            <div className={styles.metricLabel}>Bounce Rate</div>
            <div className={`${styles.statusIcon} ${styles.statusGood}`}>
              <CheckCircle size={14} />
            </div>
          </div>
          <div>
            <div className={styles.metricValue}>1.2%</div>
            <div className={styles.threshold}>Threshold: &lt;3%</div>
          </div>
        </div>

        <div className={styles.metricCard}>
          <div className={styles.cardTop}>
            <div className={styles.metricLabel}>Unsubscribe Rate</div>
            <div className={`${styles.statusIcon} ${styles.statusGood}`}>
              <CheckCircle size={14} />
            </div>
          </div>
          <div>
            <div className={styles.metricValue}>0.31%</div>
            <div className={styles.threshold}>Threshold: &lt;0.5%</div>
          </div>
        </div>

        <div className={styles.metricCard}>
          <div className={styles.cardTop}>
            <div className={styles.metricLabel}>Suppressed Contacts</div>
            <div className={`${styles.statusIcon} ${styles.statusNeutral}`}>
              <Info size={14} />
            </div>
          </div>
          <div>
            <div className={styles.metricValue}>127</div>
            <div className={styles.threshold}>No threshold</div>
          </div>
        </div>
      </section>

      <section className={styles.section}>
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>Jurisdiction Breakdown</h2>
        </div>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Jurisdiction</th>
              <th>Regulation</th>
              <th>Contacts</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style={{ fontWeight: 500 }}>United States</td>
              <td className={styles.sourceCell}>CAN-SPAM</td>
              <td>4,821</td>
              <td><span className={`${styles.badge} ${styles.badgeCompliant}`}>✅ Compliant</span></td>
            </tr>
            <tr>
              <td style={{ fontWeight: 500 }}>European Union</td>
              <td className={styles.sourceCell}>GDPR</td>
              <td>1,247</td>
              <td><span className={`${styles.badge} ${styles.badgeCompliant}`}>✅ Compliant</span></td>
            </tr>
            <tr>
              <td style={{ fontWeight: 500 }}>United Kingdom</td>
              <td className={styles.sourceCell}>UK GDPR + PECR</td>
              <td>892</td>
              <td><span className={`${styles.badge} ${styles.badgeCompliant}`}>✅ Compliant</span></td>
            </tr>
            <tr>
              <td style={{ fontWeight: 500 }}>Canada</td>
              <td className={styles.sourceCell}>CASL</td>
              <td>341</td>
              <td><span className={`${styles.badge} ${styles.badgeReview}`}>⚠️ Needs Review</span></td>
            </tr>
            <tr>
              <td style={{ fontWeight: 500 }}>Germany</td>
              <td className={styles.sourceCell}>UWG</td>
              <td>87</td>
              <td><span className={`${styles.badge} ${styles.badgeRestricted}`}>⚠️ Restricted</span></td>
            </tr>
          </tbody>
        </table>
      </section>

      <section className={styles.section}>
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>Suppression List</h2>
          <div style={{ display: 'flex', gap: '16px' }}>
            <input type="text" placeholder="Search emails..." className={styles.searchBar} />
            <button className={styles.button}>
              <Plus size={16} style={{ display: 'inline', marginRight: '4px', verticalAlign: 'text-bottom' }} /> 
              Add to Suppression
            </button>
          </div>
        </div>
        <div style={{ overflowX: 'auto' }}>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Email</th>
                <th>Reason</th>
                <th>Source</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {SUPPRESSION_LIST.map((item) => (
                <tr key={item.id}>
                  <td style={{ fontWeight: 500 }}>{item.email}</td>
                  <td>
                    <span className={styles.reasonBadge} style={{
                      color: item.reason === 'Unsubscribe' ? 'var(--accent-amber)' : 
                             item.reason === 'Bounce' ? 'var(--accent-red)' : 
                             item.reason === 'GDPR Objection' ? 'var(--accent-purple)' : 'inherit',
                      background: item.reason === 'Unsubscribe' ? 'var(--accent-amber-glow)' : 
                                  item.reason === 'Bounce' ? 'rgba(239, 68, 68, 0.15)' : 
                                  item.reason === 'GDPR Objection' ? 'var(--accent-purple-glow)' : 'var(--bg-surface-active)'
                    }}>
                      {item.reason}
                    </span>
                  </td>
                  <td className={styles.sourceCell}>{item.source}</td>
                  <td className={styles.dateCell}>{item.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
