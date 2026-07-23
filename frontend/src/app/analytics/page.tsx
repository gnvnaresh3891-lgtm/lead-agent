'use client';

import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, AreaChart, Area, CartesianGrid } from 'recharts';
import { ArrowUpRight, ArrowDownRight, Activity, Users, Mail, Target } from 'lucide-react';
import styles from './page.module.css';

const signalData = [
  { name: 'Job Change', rate: 24.5 },
  { name: 'Leadership', rate: 19.2 },
  { name: 'Competitor', rate: 17.8 },
  { name: 'Tech Change', rate: 14.1 },
  { name: 'Hiring', rate: 12.4 },
  { name: 'Funding', rate: 11.0 },
];

const trendData = [
  { day: '1', sent: 120, replies: 12 },
  { day: '5', sent: 180, replies: 15 },
  { day: '10', sent: 220, replies: 28 },
  { day: '15', sent: 200, replies: 25 },
  { day: '20', sent: 250, replies: 35 },
  { day: '25', sent: 300, replies: 42 },
  { day: '30', sent: 280, replies: 45 },
];

export default function AnalyticsPage() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Analytics Hub</h1>
          <p className={styles.subtitle}>Real-time insights into your AI SDR performance pipeline</p>
        </div>
      </div>

      <div className={styles.statsGrid}>
        <div className={styles.statCard}>
          <div className={styles.statLabel}>Total Signals Processed</div>
          <div className={styles.statValue}>1,284</div>
          <div className={`${styles.statTrend} ${styles.trendUp}`}>
            <ArrowUpRight size={16} />
            <span>+12.4% vs last month</span>
          </div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statLabel}>Avg. Lead Quality Score</div>
          <div className={styles.statValue}>84.2</div>
          <div className={`${styles.statTrend} ${styles.trendUp}`}>
            <ArrowUpRight size={16} />
            <span>+3.1% vs last month</span>
          </div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statLabel}>Meetings Booked</div>
          <div className={styles.statValue}>47</div>
          <div className={`${styles.statTrend} ${styles.trendUp}`}>
            <ArrowUpRight size={16} />
            <span>+18.0% vs last month</span>
          </div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statLabel}>Bounce Rate</div>
          <div className={styles.statValue}>1.2%</div>
          <div className={`${styles.statTrend} ${styles.trendDown}`}>
            <ArrowDownRight size={16} />
            <span>-0.4% vs last month</span>
          </div>
        </div>
      </div>

      {mounted && (
        <div className={styles.chartsGrid}>
          <div className={styles.chartCard}>
            <h3 className={styles.chartTitle}>
              <Activity size={20} color="var(--accent-blue)" />
              Campaign Outreach Trends (30 Days)
            </h3>
            <div className={styles.chartContainer}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={trendData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorSent" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="var(--accent-blue)" stopOpacity={0.4}/>
                      <stop offset="95%" stopColor="var(--accent-blue)" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorReplies" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="var(--accent-green)" stopOpacity={0.4}/>
                      <stop offset="95%" stopColor="var(--accent-green)" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border-subtle)" />
                  <XAxis dataKey="day" stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} />
                  <Tooltip 
                    contentStyle={{ background: 'var(--glass-bg)', border: '1px solid var(--glass-border)', borderRadius: '8px', color: 'var(--text-primary)', backdropFilter: 'blur(10px)' }}
                    itemStyle={{ color: 'var(--text-primary)' }}
                  />
                  <Area type="monotone" dataKey="sent" name="Emails Sent" stroke="var(--accent-blue)" strokeWidth={2} fillOpacity={1} fill="url(#colorSent)" />
                  <Area type="monotone" dataKey="replies" name="Replies Received" stroke="var(--accent-green)" strokeWidth={2} fillOpacity={1} fill="url(#colorReplies)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className={styles.chartCard}>
            <h3 className={styles.chartTitle}>
              <Target size={20} color="var(--accent-purple)" />
              Pipeline Velocity
            </h3>
            <div className={styles.chartContainer} style={{ minHeight: 'auto' }}>
              <div className={styles.funnelStack}>
                {[
                  { label: 'Sent', count: '10,847', pct: '100%', width: '100%', color: 'var(--accent-blue)' },
                  { label: 'Delivered', count: '10,234', pct: '94.3%', width: '94%', color: '#60a5fa' },
                  { label: 'Opened', count: '3,892', pct: '38.0%', width: '70%', color: 'var(--accent-purple)' },
                  { label: 'Replied', count: '1,284', pct: '12.5%', width: '40%', color: 'var(--accent-amber)' },
                  { label: 'Qualified', count: '642', pct: '6.3%', width: '25%', color: 'var(--accent-green)' },
                  { label: 'Booked', count: '186', pct: '1.8%', width: '10%', color: '#059669' },
                ].map((stage, i) => (
                  <div key={i} className={styles.funnelRow}>
                    <div className={styles.funnelLabel}>{stage.label}</div>
                    <div className={styles.funnelBarWrapper}>
                      <div 
                        className={styles.funnelBar} 
                        style={{ width: stage.width, background: stage.color }}
                      >
                        {stage.count}
                      </div>
                    </div>
                    <div className={styles.funnelPct}>{stage.pct}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {mounted && (
        <div className={styles.chartsGrid} style={{ gridTemplateColumns: '1fr', marginTop: '-8px' }}>
          <div className={styles.chartCard}>
            <h3 className={styles.chartTitle}>
              <Users size={20} color="var(--accent-amber)" />
              Reply Rate by Signal Type (%)
            </h3>
            <div className={styles.chartContainer} style={{ height: '240px', minHeight: '240px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={signalData} layout="vertical" margin={{ left: 20, right: 20, top: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="var(--border-subtle)" />
                  <XAxis type="number" stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis dataKey="name" type="category" stroke="var(--text-secondary)" fontSize={13} tickLine={false} axisLine={false} />
                  <Tooltip 
                    cursor={{ fill: 'var(--bg-surface-hover)' }}
                    contentStyle={{ background: 'var(--glass-bg)', border: '1px solid var(--glass-border)', borderRadius: '8px', color: 'var(--text-primary)', backdropFilter: 'blur(10px)' }}
                    formatter={(value: number) => [`${value}%`, 'Reply Rate']}
                  />
                  <Bar dataKey="rate" fill="var(--accent-amber)" radius={[0, 4, 4, 0]} barSize={28} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
