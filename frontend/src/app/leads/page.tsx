'use client';

import { useState } from 'react';
import { Zap } from 'lucide-react';
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
  { id: 1, name: 'Alex Johnson', company: 'TechFlow', title: 'VP of Engineering', score: 85, status: 'replied', signals: ['#10b981', '#3b82f6'], lastActivity: '2h ago' },
  { id: 2, name: 'Sarah Chen', company: 'DataStack', title: 'Director of Sales', score: 92, status: 'qualified', signals: ['#f59e0b', '#8b5cf6', '#10b981'], lastActivity: '5h ago' },
  { id: 3, name: 'Michael Smith', company: 'CloudNova', title: 'CTO', score: 78, status: 'sequenced', signals: ['#3b82f6'], lastActivity: '1d ago' },
  { id: 4, name: 'Emily Davis', company: 'Vertex Solutions', title: 'VP Operations', score: 64, status: 'new', signals: [], lastActivity: '3d ago' },
  { id: 5, name: 'James Wilson', company: 'PulseAI', title: 'CEO', score: 88, status: 'booked', signals: ['#8b5cf6', '#10b981'], lastActivity: '2d ago' },
  // Adding a few more to populate
  { id: 6, name: 'David Lee', company: 'Acme Corp', title: 'Head of Growth', score: 71, status: 'enriched', signals: ['#f59e0b'], lastActivity: '1d ago' },
  { id: 7, name: 'Laura Martinez', company: 'InnovateX', title: 'CMO', score: 95, status: 'booked', signals: ['#10b981', '#3b82f6', '#8b5cf6'], lastActivity: '4h ago' },
  { id: 8, name: 'Robert Taylor', company: 'Global Systems', title: 'VP Sales', score: 81, status: 'qualified', signals: ['#3b82f6', '#f59e0b'], lastActivity: '6h ago' },
  { id: 9, name: 'Lisa Anderson', company: 'NextGen', title: 'Director of Marketing', score: 55, status: 'new', signals: [], lastActivity: '4d ago' },
  { id: 10, name: 'William Thomas', company: 'TechSolutions', title: 'CTO', score: 89, status: 'replied', signals: ['#8b5cf6', '#3b82f6'], lastActivity: '1d ago' }
];

export default function LeadsPage() {
  const [view, setView] = useState<'kanban' | 'table'>('kanban');

  const getScoreClass = (score: number) => {
    if (score >= 80) return styles.scoreHigh;
    if (score >= 60) return styles.scoreMed;
    return styles.scoreLow;
  };

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <div>
          <h1 className={styles.title}>Leads</h1>
          <p className={styles.subtitle}>Manage and track your active prospects</p>
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
                  <div key={lead.id} className={styles.leadCard}>
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
                  <th>Signals</th>
                  <th>Last Activity</th>
                </tr>
              </thead>
              <tbody>
                {MOCK_LEADS.map(lead => {
                  const statusCol = MOCK_COLUMNS.find(c => c.id === lead.status);
                  return (
                    <tr key={lead.id}>
                      <td style={{ fontWeight: 600 }}>{lead.name}</td>
                      <td>{lead.company}</td>
                      <td style={{ color: 'var(--text-muted)' }}>{lead.title}</td>
                      <td>
                        <span className={`${styles.scoreBadge} ${getScoreClass(lead.score)}`}>
                          {lead.score}
                        </span>
                      </td>
                      <td>
                        <span 
                          className={styles.statusPill}
                          style={{ 
                            background: `rgba(${statusCol?.color === '#6b7280' || statusCol?.color === '#10b981' ? '107, 114, 128' : '255, 255, 255'}, 0.1)`, 
                            color: statusCol?.color || 'var(--text-primary)',
                            border: `1px solid ${statusCol?.color}`
                          }}
                        >
                          {statusCol?.label}
                        </span>
                      </td>
                      <td>
                        {lead.signals.length > 0 ? (
                          <div className={styles.signalCount}>
                            <Zap size={14} className={styles.signalIcon} />
                            <span>{lead.signals.length}</span>
                          </div>
                        ) : (
                          <span style={{ color: 'var(--text-muted)' }}>-</span>
                        )}
                      </td>
                      <td style={{ color: 'var(--text-muted)' }}>{lead.lastActivity}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
