'use client';

import { useState } from 'react';
import Link from 'next/link';
import { 
  Zap, ArrowRight, CheckCircle2, Shield, TrendingUp, 
  Users, Sparkles, Building, Layers, Sliders, DollarSign,
  HelpCircle, ChevronRight, LogIn
} from 'lucide-react';
import styles from './page.module.css';

export default function LandingPage() {
  const [sdrCount, setSdrCount] = useState(3);
  const [activeSignalTab, setActiveSignalTab] = useState(0);

  // ROI Calculator Math
  const humanCostPerSdr = 125000; // $125K fully loaded cost
  const totalHumanCost = sdrCount * humanCostPerSdr;
  const aiAgentCost = 399 * 12; // Growth Tier
  const netSavings = totalHumanCost - aiAgentCost;

  const signalDemos = [
    {
      type: '🚀 Funding Announcement',
      company: 'TechFlow (Series B - $15M)',
      detected: '2 hours ago',
      target: 'Sarah Chen, VP Revenue Operations',
      subject: 'quick thought on TechFlow\'s Series B growth',
      body: 'Hi Sarah, congrats on the $15M Series B led by Sequoia — huge milestone. Most RevOps leaders building out post-funding teams evaluate whether to double headcount or automate pipeline velocity. We help scaling teams like TechFlow generate 2-3x more pipeline per rep by timing outreach to active buying signals. Worth a 2-minute look?',
    },
    {
      type: '👤 Champion Job Change',
      company: 'DataStack (New Hire)',
      detected: '4 hours ago',
      target: 'Marcus Rodriguez, CRO',
      subject: 'congrats on the DataStack CRO role, Marcus',
      body: 'Hi Marcus, congrats on stepping into the CRO seat at DataStack. Knowing how successful your team was with intent-driven outbound in your previous role, I wanted to share our latest signal playbooks designed for new sales leaders hitting the ground running in their first 90 days. Would it be useful to review?',
    },
    {
      type: '🔧 Competitor Tech Removal',
      company: 'CloudNova (Dropped Competitor)',
      detected: 'Yesterday',
      target: 'Emily Watson, Head of Growth',
      subject: 'evaluating replacement for your outbound stack?',
      body: 'Hi Emily, noticed CloudNova recently discontinued your legacy sequence tool. Many growth teams switching away from expensive seat-based subscriptions find our autonomous signal agent delivers 3x higher reply rates without the domain deliverability headaches. Open to comparing notes?',
    },
  ];

  return (
    <div className={styles.landing}>
      {/* Top Public Marketing Navigation Header */}
      <header style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '20px 40px',
        borderBottom: '1px solid var(--glass-border)',
        background: 'var(--glass-bg)',
        backdropFilter: 'blur(20px)',
        position: 'sticky',
        top: 0,
        zIndex: 100
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Zap size={28} color="var(--accent-blue)" />
          <span style={{ fontSize: '20px', fontWeight: 800 }}>SignalSDR</span>
        </div>

        <nav style={{ display: 'flex', gap: '24px', fontSize: '14px', fontWeight: 500 }}>
          <a href="#economics" style={{ color: 'var(--text-secondary)' }}>Economics</a>
          <a href="#demo" style={{ color: 'var(--text-secondary)' }}>Live Demo</a>
          <a href="#pricing" style={{ color: 'var(--text-secondary)' }}>Pricing</a>
          <a href="#roi" style={{ color: 'var(--text-secondary)' }}>ROI Calculator</a>
        </nav>

        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <Link 
            href="/login" 
            style={{ 
              color: 'var(--text-primary)', 
              fontSize: '14px', 
              fontWeight: 600, 
              padding: '8px 16px',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <LogIn size={16} /> Sign In
          </Link>

          <Link 
            href="/dashboard" 
            className={styles.primaryBtn}
            style={{ padding: '8px 18px', fontSize: '14px' }}
          >
            Launch App <ArrowRight size={16} />
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroBadge}>
          <Sparkles size={16} />
          <span>Composite Score: 81.9 | Signal-Driven Outbound</span>
        </div>

        <h1 className={styles.heroTitle}>
          Your AI SDR That Reaches Out<br />
          <span className={styles.heroTitleHighlight}>When Timing & Intent Strike.</span>
        </h1>

        <p className={styles.heroSubtitle}>
          Stop blasting generic cold emails to static lists. SignalSDR continuously monitors 10+ buying signals — job changes, funding rounds, tech stack removals — and sends hyper-personalized outreach at the exact right moment.
        </p>

        <div className={styles.heroActions}>
          <Link href="/dashboard" className={styles.primaryBtn}>
            Launch App Dashboard <ArrowRight size={18} />
          </Link>
          <Link href="/login" className={styles.secondaryBtn}>
            Create Free Account
          </Link>
        </div>

        <div className={styles.statsBar}>
          <div className={styles.statItem}>
            <div className={styles.statNum}>18.4%</div>
            <div className={styles.statLabel}>Avg Reply Rate (vs 2.1% benchmark)</div>
          </div>
          <div className={styles.statItem}>
            <div className={styles.statNum}>60%</div>
            <div className={styles.statLabel}>Lower Outbound CAC</div>
          </div>
          <div className={styles.statItem}>
            <div className={styles.statNum}>100%</div>
            <div className={styles.statLabel}>CAN-SPAM & GDPR Compliant</div>
          </div>
        </div>
      </section>

      {/* Outbound Economics Breakdown */}
      <section id="economics">
        <div className={styles.sectionHeader}>
          <div className={styles.sectionBadge}>Outbound Economics</div>
          <h2 className={styles.sectionTitle}>The $4,920 CAC Myth vs. True SDR Cost</h2>
          <p className={styles.sectionSubtitle}>
            Why traditional SDR teams and budget email warmers fail — and how SignalSDR transforms unit economics.
          </p>
        </div>

        <div className={styles.comparisonGrid}>
          <div className={styles.compCard}>
            <div className={styles.compHeader}>
              <div className={styles.compTitle}>Human SDR Team</div>
              <div className={styles.compPrice}>$125,000<span style={{ fontSize: '14px', color: 'var(--text-muted)' }}>/year per rep</span></div>
            </div>
            <ul className={styles.compList}>
              <li className={styles.compItem}><CheckCircle2 size={16} color="var(--accent-red)" /> $75k base + $50k OTE + taxes</li>
              <li className={styles.compItem}><CheckCircle2 size={16} color="var(--accent-red)" /> 3-6 month ramp productivity period</li>
              <li className={styles.compItem}><CheckCircle2 size={16} color="var(--accent-red)" /> 40% annual SDR turnover rate</li>
              <li className={styles.compItem}><CheckCircle2 size={16} color="var(--accent-red)" /> Heavy manual research & admin</li>
            </ul>
          </div>

          <div className={styles.compCard}>
            <div className={styles.compHeader}>
              <div className={styles.compTitle}>Generic Email Senders</div>
              <div className={styles.compPrice}>$37 – $97<span style={{ fontSize: '14px', color: 'var(--text-muted)' }}>/month</span></div>
            </div>
            <ul className={styles.compList}>
              <li className={styles.compItem}><CheckCircle2 size={16} color="var(--accent-amber)" /> Cheap high-volume email blasts</li>
              <li className={styles.compItem}><CheckCircle2 size={16} color="var(--accent-red)" /> Zero signal detection or timing</li>
              <li className={styles.compItem}><CheckCircle2 size={16} color="var(--accent-red)" /> Domain blacklisting & spam filters</li>
              <li className={styles.compItem}><CheckCircle2 size={16} color="var(--accent-red)" /> &lt;2% response rates (burned leads)</li>
            </ul>
          </div>

          <div className={`${styles.compCard} ${styles.compCardHighlight}`}>
            <div className={styles.compHeader}>
              <div className={styles.compTitle} style={{ color: 'var(--accent-blue)' }}>SignalSDR Agent</div>
              <div className={styles.compPrice}>$199 – $399<span style={{ fontSize: '14px', color: 'var(--text-muted)' }}>/month</span></div>
            </div>
            <ul className={styles.compList}>
              <li className={styles.compItem}><CheckCircle2 size={16} color="var(--accent-green)" /> Continuous real-time signal monitoring</li>
              <li className={styles.compItem}><CheckCircle2 size={16} color="var(--accent-green)" /> Multi-model AI contextual copywriting</li>
              <li className={styles.compItem}><CheckCircle2 size={16} color="var(--accent-green)" /> Multi-jurisdiction compliance framework</li>
              <li className={styles.compItem}><CheckCircle2 size={16} color="var(--accent-green)" /> 18.4% average reply rate</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Interactive Signal Demo */}
      <section id="demo">
        <div className={styles.sectionHeader}>
          <div className={styles.sectionBadge}>Interactive Product Demo</div>
          <h2 className={styles.sectionTitle}>How Signals Turn Into Meetings</h2>
          <p className={styles.sectionSubtitle}>
            Select a buying signal below to see how SignalSDR extracts context and composes non-generic outreach.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', marginBottom: '24px' }}>
          {signalDemos.map((demo, idx) => (
            <button
              key={idx}
              onClick={() => setActiveSignalTab(idx)}
              style={{
                padding: '10px 18px',
                borderRadius: '12px',
                background: activeSignalTab === idx ? 'var(--accent-blue-glow)' : 'var(--glass-bg)',
                border: activeSignalTab === idx ? '1px solid var(--accent-blue)' : '1px solid var(--glass-border)',
                color: activeSignalTab === idx ? 'var(--accent-blue)' : 'var(--text-secondary)',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              {demo.type}
            </button>
          ))}
        </div>

        <div className={styles.demoCard}>
          <div className={styles.demoSignal}>
            <div style={{ fontSize: '12px', color: 'var(--accent-blue)', fontWeight: 700, textTransform: 'uppercase' }}>
              Detected Intent Signal
            </div>
            <div style={{ fontSize: '20px', fontWeight: 700 }}>
              {signalDemos[activeSignalTab].type}
            </div>
            <div style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
              Company: <strong>{signalDemos[activeSignalTab].company}</strong>
            </div>
            <div style={{ color: 'var(--text-muted)', fontSize: '13px' }}>
              Detected: {signalDemos[activeSignalTab].detected}
            </div>
            <div style={{ color: 'var(--text-muted)', fontSize: '13px', borderTop: '1px solid var(--border-subtle)', paddingTop: '12px' }}>
              Target Persona: <strong>{signalDemos[activeSignalTab].target}</strong>
            </div>
          </div>

          <div className={styles.demoEmail}>
            <div style={{ fontSize: '12px', color: 'var(--accent-green)', fontWeight: 700, textTransform: 'uppercase', marginBottom: '8px' }}>
              AI Personalization Output (Flesch Score: 88 | Quality: 94%)
            </div>
            <div style={{ fontWeight: 600, marginBottom: '12px', color: 'var(--text-primary)' }}>
              Subject: {signalDemos[activeSignalTab].subject}
            </div>
            <div style={{ color: 'var(--text-secondary)' }}>
              {signalDemos[activeSignalTab].body}
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing">
        <div className={styles.sectionHeader}>
          <div className={styles.sectionBadge}>Transparent Pricing</div>
          <h2 className={styles.sectionTitle}>Built for Mid-Market Growth</h2>
          <p className={styles.sectionSubtitle}>
            No mandatory 10-seat minimums. No $36,000 upfront annual lock-ins. Upgrade or cancel anytime.
          </p>
        </div>

        <div className={styles.pricingGrid}>
          {/* Starter Tier */}
          <div className={styles.priceCard}>
            <div>
              <div className={styles.priceTitle}>Starter</div>
              <div style={{ color: 'var(--text-muted)', fontSize: '13px', marginTop: '4px' }}>For early startups & solo SDRs</div>
            </div>
            <div>
              <span className={styles.priceAmount}>$199</span>
              <span className={styles.pricePeriod}>/month</span>
            </div>
            <ul className={styles.priceFeatures}>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> 500 signal leads / month</li>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> 2 active signal feeds</li>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> 1 sending domain</li>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> Email channel automation</li>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> Built-in compliance engine</li>
            </ul>
            <Link href="/login" className={styles.secondaryBtn} style={{ justifyContent: 'center' }}>
              Sign Up
            </Link>
          </div>

          {/* Growth Tier */}
          <div className={`${styles.priceCard} ${styles.pricePopular}`}>
            <div className={styles.popularBadge}>Most Popular</div>
            <div>
              <div className={styles.priceTitle} style={{ color: 'var(--accent-green)' }}>Growth</div>
              <div style={{ color: 'var(--text-muted)', fontSize: '13px', marginTop: '4px' }}>For scaling RevOps & sales teams</div>
            </div>
            <div>
              <span className={styles.priceAmount}>$399</span>
              <span className={styles.pricePeriod}>/month</span>
            </div>
            <ul className={styles.priceFeatures}>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> 2,000 signal leads / month</li>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> All signal feeds (Job, Funding, Tech)</li>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> 5 sending domains with warmup</li>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> Email + LinkedIn automation</li>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> HubSpot & Salesforce integration</li>
            </ul>
            <Link href="/login" className={styles.primaryBtn} style={{ justifyContent: 'center' }}>
              Start 14-Day Trial
            </Link>
          </div>

          {/* Scale Tier */}
          <div className={styles.priceCard}>
            <div>
              <div className={styles.priceTitle}>Scale</div>
              <div style={{ color: 'var(--text-muted)', fontSize: '13px', marginTop: '4px' }}>For high-volume outbound teams</div>
            </div>
            <div>
              <span className={styles.priceAmount}>$799</span>
              <span className={styles.pricePeriod}>/month</span>
            </div>
            <ul className={styles.priceFeatures}>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> 10,000 signal leads / month</li>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> Custom signal trigger builder</li>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> Unlimited sending domains</li>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> Multi-channel + voice agent</li>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> Priority support & SLA</li>
            </ul>
            <Link href="/login" className={styles.secondaryBtn} style={{ justifyContent: 'center' }}>
              Go Scale
            </Link>
          </div>

          {/* Enterprise Tier */}
          <div className={styles.priceCard}>
            <div>
              <div className={styles.priceTitle}>Enterprise</div>
              <div style={{ color: 'var(--text-muted)', fontSize: '13px', marginTop: '4px' }}>For custom security & IP scale</div>
            </div>
            <div>
              <span className={styles.priceAmount}>Custom</span>
            </div>
            <ul className={styles.priceFeatures}>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> Unlimited signal volume</li>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> Dedicated single-tenant infrastructure</li>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> Fine-tuned proprietary LLMs</li>
              <li><CheckCircle2 size={14} color="var(--accent-green)" /> Dedicated CSM & GTM engineer</li>
            </ul>
            <Link href="/login" className={styles.secondaryBtn} style={{ justifyContent: 'center' }}>
              Contact Sales
            </Link>
          </div>
        </div>
      </section>

      {/* Interactive ROI Calculator */}
      <section id="roi">
        <div className={styles.sectionHeader}>
          <div className={styles.sectionBadge}>Interactive ROI Calculator</div>
          <h2 className={styles.sectionTitle}>Calculate Your Cost Savings</h2>
          <p className={styles.sectionSubtitle}>
            Drag the slider to see your yearly savings compared to hiring full-time SDR headcount.
          </p>
        </div>

        <div className={styles.roiCard}>
          <div className={styles.sliderContainer}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontWeight: 600, fontSize: '16px' }}>Number of SDR Seats:</span>
              <span style={{ fontSize: '28px', fontWeight: 800, color: 'var(--accent-blue)' }}>{sdrCount} Reps</span>
            </div>
            <input 
              type="range" 
              min="1" 
              max="20" 
              value={sdrCount}
              onChange={(e) => setSdrCount(parseInt(e.target.value))}
              className={styles.rangeInput}
            />
            <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
              Assumes $125,000 fully-loaded cost per human SDR vs. SignalSDR Growth Plan ($399/mo).
            </div>
          </div>

          <div className={styles.roiResults}>
            <div>
              <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Traditional Human SDR Cost</div>
              <div style={{ fontSize: '24px', fontWeight: 700, color: 'var(--accent-red)' }}>${totalHumanCost.toLocaleString()}/yr</div>
            </div>
            <div>
              <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>SignalSDR Annual Investment</div>
              <div style={{ fontSize: '24px', fontWeight: 700, color: 'var(--accent-blue)' }}>${aiAgentCost.toLocaleString()}/yr</div>
            </div>
            <div style={{ borderTop: '1px solid var(--border-subtle)', paddingTop: '16px' }}>
              <div style={{ fontSize: '14px', color: 'var(--accent-green)', fontWeight: 600 }}>Net Projected Annual Savings</div>
              <div style={{ fontSize: '36px', fontWeight: 800, color: 'var(--accent-green)' }}>${netSavings.toLocaleString()}</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className={styles.ctaBox}>
        <h2 style={{ fontSize: '36px', fontWeight: 800 }}>Ready to Turn Buying Signals into Pipeline?</h2>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto' }}>
          Join high-growth B2B teams replacing generic outbound spam with signal-driven AI sales development.
        </p>
        <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', marginTop: '12px' }}>
          <Link href="/login" className={styles.primaryBtn} style={{ padding: '16px 36px', fontSize: '18px' }}>
            Start Free Trial <ArrowRight size={20} />
          </Link>
          <Link href="/dashboard" className={styles.secondaryBtn} style={{ padding: '16px 36px', fontSize: '18px' }}>
            Launch App Dashboard
          </Link>
        </div>
      </section>
    </div>
  );
}
