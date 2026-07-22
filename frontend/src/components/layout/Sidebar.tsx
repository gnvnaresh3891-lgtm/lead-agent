'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard, Zap, Users, Send, 
  BarChart3, Shield, Settings, Globe
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
  { href: '/', label: 'Landing Page', icon: Globe },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className={styles.sidebar}>
      <div className={styles.logoContainer}>
        <Zap className={styles.logoIcon} size={28} />
        <h1 className={styles.logoText}>SignalSDR</h1>
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

      <div className={styles.userCard}>
        <div className={styles.avatar}>AM</div>
        <div className={styles.userInfo}>
          <div className={styles.userName}>Alex Morgan</div>
          <div className={styles.userRole}>Growth Plan</div>
        </div>
      </div>
    </aside>
  );
}
