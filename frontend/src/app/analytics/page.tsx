'use client';

import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import styles from './page.module.css';

const signalData = [
  { name: 'Job Change', rate: 24 },
  { name: 'Leadership', rate: 19 },
  { name: 'Competitor', rate: 17 },
  { name: 'Tech Change', rate: 14 },
  { name: 'Hiring', rate: 12 },
  { name: 'Funding', rate: 11 },
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
      <div>
        <h1 className={styles.title}>Analytics</h1>
        <p className={styles.subtitle}>Detailed insights into your pipeline and performance</p>
      </div>

      <div className={styles.funnelContainer}>
        <h2 className={styles.funnelTitle}>Conversion Funnel</h2>
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

      {mounted && (
        <div className={styles.chartsGrid}>
          <div className={styles.chartCard}>
            <h3 className={styles.chartTitle}>Reply Rate by Signal Type</h3>
            <div className={styles.chartContainer}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={signalData} layout="vertical" margin={{ left: 20 }}>
                  <XAxis type="number" hide />
                  <YAxis dataKey="name" type="category" stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} />
                  <Tooltip 
                    cursor={{ fill: 'var(--bg-surface-hover)' }}
                    contentStyle={{ background: 'var(--glass-bg)', border: '1px solid var(--glass-border)', borderRadius: '8px', color: 'var(--text-primary)' }}
                  />
                  <Bar dataKey="rate" fill="var(--accent-blue)" radius={[0, 4, 4, 0]} barSize={24} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className={styles.chartCard}>
            <h3 className={styles.chartTitle}>Campaign Trends (30 Days)</h3>
            <div className={styles.chartContainer}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={trendData}>
                  <defs>
                    <linearGradient id="colorSent" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="var(--accent-blue)" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="var(--accent-blue)" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorReplies" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="var(--accent-green)" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="var(--accent-green)" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="day" stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} />
                  <Tooltip 
                    contentStyle={{ background: 'var(--glass-bg)', border: '1px solid var(--glass-border)', borderRadius: '8px', color: 'var(--text-primary)' }}
                  />
                  <Area type="monotone" dataKey="sent" stroke="var(--accent-blue)" fillOpacity={1} fill="url(#colorSent)" />
                  <Area type="monotone" dataKey="replies" stroke="var(--accent-green)" fillOpacity={1} fill="url(#colorReplies)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
