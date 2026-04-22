import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'GambleMatch | Elite Gambling Matchmaking',
  description: 'The most advanced gambling matchmaking bot on Discord. Bet items, Robux & cash. Ranked matches, live casino, room system, and more.',
  keywords: ['gamble', 'discord', 'roblox', 'robux', 'matchmaking', 'gambling bot'],
  openGraph: {
    title: 'GambleMatch – Best Gambling Bot for Discord',
    description: 'Advanced matchmaking, casino games, ranked system, live leaderboards.',
    url: 'https://gamblematch.vercel.app',
    siteName: 'GambleMatch',
    type: 'website',
    images: [{ url: 'https://i.imgur.com/7X8k3zD.png', width: 1200, height: 630 }],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'GambleMatch – Best Gambling Bot',
    description: 'Advanced gambling matchmaking on Discord.',
    images: ['https://i.imgur.com/7X8k3zD.png'],
  },
  themeColor: '#6c5ce7',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="noise-overlay" />
        <div className="scan-line" />
        {children}
      </body>
    </html>
  )
}
