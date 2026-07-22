import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Sidebar from '@/components/layout/Sidebar';
import layoutStyles from './layout.module.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'SignalSDR — AI-Powered Sales Intelligence',
  description: 'AI SDR Performance Dashboard',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className={layoutStyles.container}>
          <Sidebar />
          <main className={layoutStyles.mainContent}>{children}</main>
        </div>
      </body>
    </html>
  );
}
