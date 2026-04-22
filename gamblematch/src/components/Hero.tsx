'use client'
import { useState, useEffect } from 'react'
import { liveStats } from '@/lib/data'

const TYPEWRITER_MSGS = [
  'bet anything, win everything',
  'ranked matches. real stakes.',
  'casino. rooms. codes.',
  'the ultimate gambling hub.',
]

export default function Hero() {
  const [text, setText] = useState('')
  const [msgIdx, setMsgIdx] = useState(0)
  const [deleting, setDeleting] = useState(false)
  const [statsVisible, setStatsVisible] = useState(false)

  useEffect(() => {
    setStatsVisible(true)
  }, [])

  useEffect(() => {
    const msg = TYPEWRITER_MSGS[msgIdx]
    let timeout: ReturnType<typeof setTimeout>

    if (!deleting && text.length < msg.length) {
      timeout = setTimeout(() => setText(msg.slice(0, text.length + 1)), 75)
    } else if (!deleting && text.length === msg.length) {
      timeout = setTimeout(() => setDeleting(true), 2200)
    } else if (deleting && text.length > 0) {
      timeout = setTimeout(() => setText(text.slice(0, -1)), 40)
    } else if (deleting && text.length === 0) {
      setDeleting(false)
      setMsgIdx((prev) => (prev + 1) % TYPEWRITER_MSGS.length)
    }
    return () => clearTimeout(timeout)
  }, [text, deleting, msgIdx])

  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center px-6 pt-24 pb-12 overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 bg-grid-pattern opacity-20" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full"
           style={{ background:'radial-gradient(circle, rgba(108,92,231,0.12) 0%, transparent 70%)' }} />
      <div className="absolute top-20 left-10 w-64 h-64 rounded-full animate-float"
           style={{ background:'radial-gradient(circle, rgba(108,92,231,0.08) 0%, transparent 70%)', filter:'blur(40px)' }} />
      <div className="absolute bottom-32 right-10 w-80 h-80 rounded-full animate-float-delay"
           style={{ background:'radial-gradient(circle, rgba(0,229,255,0.06) 0%, transparent 70%)', filter:'blur(40px)' }} />

      {/* Badge */}
      <div className="flex items-center gap-2 px-4 py-2 rounded-full border border-gm-purple/40 bg-gm-surface/60 backdrop-blur-md mb-8
                      animate-fade-in text-sm font-medium text-gm-violet"
           style={{ animationDelay:'0.1s', opacity:0 }}>
        <span className="live-dot" />
        <span>{liveStats[2].value} players online now</span>
        <span className="text-white/30 mx-1">·</span>
        <span className="text-white/60">{liveStats[3].value} live matches</span>
      </div>

      {/* Title */}
      <h1 className="text-center mb-6 animate-slide-in-up" style={{ animationDelay:'0.2s', opacity:0 }}>
        <span className="block font-display font-black animate-glitch"
              style={{ fontSize:'clamp(3rem, 8vw, 7rem)', lineHeight:1.05 }}>
          <span className="gradient-text">GambleMatch</span>
        </span>
        <span className="block text-white/40 font-display font-medium mt-2"
              style={{ fontSize:'clamp(0.9rem, 2.5vw, 1.4rem)', letterSpacing:'0.15em' }}>
          DISCORD GAMBLING MATCHMAKING
        </span>
      </h1>

      {/* Typewriter */}
      <div className="mb-10 animate-slide-in-up" style={{ animationDelay:'0.35s', opacity:0 }}>
        <div className="px-6 py-3 rounded-full border border-gm-purple/50 bg-gm-surface/50 backdrop-blur-md
                        font-mono text-gm-violet min-w-[280px] text-center"
             style={{ fontSize:'clamp(0.9rem, 2vw, 1.2rem)' }}>
          {text}<span className="animate-pulse text-gm-cyan">_</span>
        </div>
      </div>

      {/* CTAs */}
      <div className="flex flex-col sm:flex-row gap-4 mb-16 animate-slide-in-up"
           style={{ animationDelay:'0.5s', opacity:0 }}>
        <a
          href="https://discord.gg/smxxKFPHZw"
          target="_blank"
          rel="noopener noreferrer"
          className="group flex items-center gap-3 px-8 py-4 rounded-2xl font-bold text-lg transition-all duration-300 hover:scale-105"
          style={{
            background:'linear-gradient(135deg, #6c5ce7 0%, #5865F2 100%)',
            boxShadow:'0 0 30px rgba(108,92,231,0.5), inset 0 1px 0 rgba(255,255,255,0.1)',
          }}
        >
          <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057c.002.022.015.043.03.056a19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028 14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03z"/>
          </svg>
          Join the Server
          <span className="group-hover:translate-x-1 transition-transform">→</span>
        </a>
        <a
          href="#leaderboard"
          className="flex items-center gap-3 px-8 py-4 rounded-2xl font-bold text-lg border border-gm-border
                     hover:border-gm-purple/60 hover:bg-gm-surface/60 transition-all duration-300 text-white/80 hover:text-white"
        >
          🏆 Live Leaderboard
        </a>
      </div>

      {/* Stats strip */}
      <div className={`grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 w-full max-w-5xl
                       transition-all duration-700 ${statsVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'}`}
           style={{ transitionDelay:'0.6s' }}>
        {liveStats.map((s, i) => (
          <div key={i}
               className="glass-card px-4 py-3 text-center hover:border-gm-purple/50 transition-all duration-300 hover:-translate-y-1">
            <div className="text-xl font-display font-bold" style={{ color:s.color }}>
              {s.value}
              {s.delta && (
                <span className="text-xs font-normal text-gm-emerald ml-1">{s.delta}</span>
              )}
            </div>
            <div className="text-xs text-white/40 mt-1">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Scroll hint */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 animate-bounce text-white/30">
        <span className="text-xs tracking-widest font-display">SCROLL</span>
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </div>
    </section>
  )
}
