'use client';

import { usePathname } from 'next/navigation';
import Sidebar from './Sidebar';
import layoutStyles from '@/app/layout.module.css';

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  
  // Public pages that should NOT show the sidebar layout
  const isPublicPage = pathname === '/' || pathname === '/login';

  if (isPublicPage) {
    return <main>{children}</main>;
  }

  return (
    <div className={layoutStyles.container}>
      <Sidebar />
      <main className={layoutStyles.mainContent}>{children}</main>
    </div>
  );
}
