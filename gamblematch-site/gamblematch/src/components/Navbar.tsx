'use client'
import { useState, useEffect } from 'react'

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40)
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        scrolled
          ? 'bg-[rgba(7,7,26,0.95)] backdrop-blur-xl border-b border-gm-border'
          : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-8 h-8 rounded-lg bg-gm-purple flex items-center justify-center text-sm font-black"
                 style={{ boxShadow:'0 0 15px rgba(108,92,231,0.6)' }}>
              G
            </div>
            <div className="absolute -top-1 -right-1 w-3 h-3 rounded-full bg-gm-emerald animate-pulse"
                 style={{ boxShadow:'0 0 8px #00e676' }} />
          </div>
          <span className="font-display text-lg font-bold tracking-wider gradient-text">
            GambleMatch
          </span>
        </div>

        {/* Desktop nav */}
        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-white/70">
          {[['#features','Features'],['#leaderboard','Leaderboard'],['#rooms','Rooms'],['#commands','Commands']].map(([href,label]) => (
            <a key={href} href={href}
               className="hover:text-gm-violet transition-colors duration-200 relative group">
              {label}
              <span className="absolute -bottom-1 left-0 w-0 h-px bg-gm-violet transition-all duration-300 group-hover:w-full" />
            </a>
          ))}
        </div>

        {/* CTA */}
        <div className="hidden md:flex items-center gap-3">
          <a
            href="https://discord.gg/smxxKFPHZw"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-5 py-2.5 rounded-full text-sm font-semibold transition-all duration-300 hover:scale-105"
            style={{
              background: 'linear-gradient(135deg, #6c5ce7, #5865F2)',
              boxShadow: '0 0 20px rgba(108,92,231,0.5)',
            }}
          >
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057c.002.022.015.043.03.056a19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028 14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03z"/>
            </svg>
            Join Server
          </a>
        </div>

        {/* Mobile hamburger */}
        <button className="md:hidden text-white/80 hover:text-white"
                onClick={() => setMenuOpen(!menuOpen)}>
          <div className="space-y-1.5">
            <span className={`block h-0.5 w-6 bg-current transition-all ${menuOpen ? 'rotate-45 translate-y-2' : ''}`} />
            <span className={`block h-0.5 w-6 bg-current transition-all ${menuOpen ? 'opacity-0' : ''}`} />
            <span className={`block h-0.5 w-6 bg-current transition-all ${menuOpen ? '-rotate-45 -translate-y-2' : ''}`} />
          </div>
        </button>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <div className="md:hidden border-t border-gm-border bg-[rgba(7,7,26,0.98)] px-6 py-4 space-y-4">
          {[['#features','Features'],['#leaderboard','Leaderboard'],['#rooms','Rooms'],['#commands','Commands']].map(([href,label]) => (
            <a key={href} href={href} className="block text-white/70 hover:text-white py-2"
               onClick={() => setMenuOpen(false)}>
              {label}
            </a>
          ))}
          <a href="https://discord.gg/smxxKFPHZw" target="_blank" rel="noopener noreferrer"
             className="block text-center py-3 rounded-full bg-gm-purple text-white font-semibold mt-2"
             onClick={() => setMenuOpen(false)}>
            Join Discord Server
          </a>
        </div>
      )}
    </nav>
  )
}
