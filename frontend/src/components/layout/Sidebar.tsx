'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { 
  LayoutDashboard, Zap, Users, Send, 
  BarChart3, Shield, Settings, LogOut
} from 'lucide-react';
import styles from './Sidebar.module.css';

const navItems = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/signals', label: 'Signals', icon: Zap },
  { href: '/leads', label: 'Leads', icon: Users },
  { href: '/campaigns', label: 'Campaigns', icon: Send },
  { href: '/analytics', label: 'Analytics', icon: BarChart3 },
  { href: '/compliance', label: 'Compliance', icon: Shield },
  { href: '/settings', label: 'Settings', icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const [user, setUser] = useState<{ name: string; orgName: string; role: string } | null>(null);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('signalsdr_user');
      if (stored) {
        try {
          setUser(JSON.parse(stored));
        } catch (e) {
          console.error(e);
        }
      } else {
        setUser({ name: 'Alex Morgan', orgName: 'Acme Technologies', role: 'admin' });
      }
    }
  }, []);

  const handleLogout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('signalsdr_user');
    }
    router.push('/login');
  };

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase()
      .substring(0, 2);
  };

  return (
    <aside className={styles.sidebar}>
      <div className={styles.logoContainer}>
        <Zap className={styles.logoIcon} size={28} />
        <div>
          <h1 className={styles.logoText}>SignalSDR</h1>
          <div style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 600 }}>
            {user?.orgName || 'Acme Technologies'}
          </div>
        </div>
      </div>

      <nav className={styles.nav}>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          
          return (
            <Link 
              key={item.href} 
              href={item.href}
              className={`${styles.navItem} ${isActive ? styles.active : ''}`}
            >
              <Icon size={20} className={styles.navIcon} />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className={styles.userCard} style={{ cursor: 'pointer' }} onClick={handleLogout} title="Click to log out">
        <div className={styles.avatar}>
          {user?.name ? getInitials(user.name) : 'AM'}
        </div>
        <div className={styles.userInfo} style={{ flexGrow: 1 }}>
          <div className={styles.userName}>{user?.name || 'Alex Morgan'}</div>
          <div className={styles.userRole}>
            {user?.role ? user.role.toUpperCase() : 'ADMIN'} • Growth Plan
          </div>
        </div>
        <LogOut size={16} color="var(--text-muted)" />
      </div>
    </aside>
  );
}
