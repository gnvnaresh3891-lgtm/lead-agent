'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Zap, ArrowRight, ShieldCheck, Sparkles, Building, Lock } from 'lucide-react';
import styles from './page.module.css';

export default function LoginPage() {
  const router = useRouter();
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [orgName, setOrgName] = useState('');
  const [role, setRole] = useState('admin');
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    // Save session context
    const userSession = {
      email: email || 'alex@acme.com',
      name: email ? email.split('@')[0] : 'Alex Morgan',
      orgName: orgName || 'Acme Technologies',
      role: role,
      token: 'jwt-demo-token-signalsdr-2026',
    };

    if (typeof window !== 'undefined') {
      localStorage.setItem('signalsdr_user', JSON.stringify(userSession));
    }

    setTimeout(() => {
      setLoading(false);
      router.push('/dashboard');
    }, 600);
  };

  const handleOneClickDemo = () => {
    const demoUser = {
      email: 'alex.morgan@acmetech.com',
      name: 'Alex Morgan',
      orgName: 'Acme Technologies',
      role: 'admin',
      token: 'jwt-demo-token-signalsdr-2026',
    };
    if (typeof window !== 'undefined') {
      localStorage.setItem('signalsdr_user', JSON.stringify(demoUser));
    }
    router.push('/dashboard');
  };

  return (
    <div className={styles.loginPage}>
      <div className={styles.loginCard}>
        <div className={styles.logoBox}>
          <Zap size={28} color="var(--accent-blue)" />
          <span className={styles.logoText}>SignalSDR</span>
        </div>

        <div className={styles.header}>
          <h1 className={styles.title}>
            {isSignUp ? 'Create Workspace Account' : 'Sign in to SignalSDR'}
          </h1>
          <p className={styles.subtitle}>
            {isSignUp
              ? 'Start your 14-day free trial. No credit card required.'
              : 'Access your signal intelligence workspace'}
          </p>
        </div>

        <button onClick={handleOneClickDemo} className={styles.demoBtn}>
          <Sparkles size={16} /> 1-Click Demo Sign In (Alex Morgan - Admin)
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', margin: '4px 0' }}>
          <div style={{ flex: 1, height: '1px', background: 'var(--border-subtle)' }} />
          <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>OR</span>
          <div style={{ flex: 1, height: '1px', background: 'var(--border-subtle)' }} />
        </div>

        <form onSubmit={handleSubmit} className={styles.form}>
          {isSignUp && (
            <>
              <div className={styles.field}>
                <label className={styles.label}>Organization / Company Name</label>
                <input
                  type="text"
                  required
                  placeholder="Acme Corp"
                  value={orgName}
                  onChange={(e) => setOrgName(e.target.value)}
                  className={styles.input}
                />
              </div>

              <div className={styles.field}>
                <label className={styles.label}>Your Role</label>
                <select
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  className={styles.select}
                >
                  <option value="admin">Admin / CRO / Head of RevOps</option>
                  <option value="manager">SDR Manager</option>
                  <option value="rep">SDR Representative</option>
                </select>
              </div>
            </>
          )}

          <div className={styles.field}>
            <label className={styles.label}>Work Email</label>
            <input
              type="email"
              required
              placeholder="alex@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className={styles.input}
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label}>Password</label>
            <input
              type="password"
              required
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className={styles.input}
            />
          </div>

          <button type="submit" disabled={loading} className={styles.submitBtn}>
            {loading
              ? 'Authenticating...'
              : isSignUp
              ? 'Create Account & Launch'
              : 'Sign In'}
          </button>
        </form>

        <div className={styles.footerText}>
          {isSignUp ? 'Already have an account?' : "Don't have an account?"}
          <span
            onClick={() => setIsSignUp(!isSignUp)}
            className={styles.toggleLink}
          >
            {isSignUp ? 'Sign In' : 'Sign Up Free'}
          </span>
        </div>

        <div style={{ textAlign: 'center', fontSize: '12px', color: 'var(--text-muted)' }}>
          <Link href="/" style={{ color: 'var(--text-muted)', textDecoration: 'underline' }}>
            ← Back to Public Site
          </Link>
        </div>
      </div>
    </div>
  );
}
