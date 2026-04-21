'use client'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const router = useRouter()
  const [userId, setUserId]   = useState('')
  const [code, setCode]       = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState('')
  const [step, setStep]       = useState<'id' | 'code'>('id')

  // Format code input as XXXXX (uppercase, letters+digits)
  const handleCodeChange = (val: string) => {
    setCode(val.replace(/[^A-Za-z0-9]/g, '').toUpperCase().slice(0, 6))
  }

  const handleSubmit = async () => {
    setError(''); setLoading(true)
    try {
      const res = await fetch('/api/auth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: userId.trim(), code: code.trim() }),
      })
      const data = await res.json()
      if (!res.ok) { setError(data.error || 'Login failed'); setLoading(false); return }
      router.push('/dashboard')
    } catch {
      setError('Connection error. Try again.'); setLoading(false)
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center px-4"
          style={{ background: 'radial-gradient(ellipse at 50% 0%, rgba(108,92,231,0.15) 0%, transparent 60%), #02020a' }}>

      {/* BG grid */}
      <div className="absolute inset-0 bg-grid-pattern opacity-10 pointer-events-none" />

      <div className="relative w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gm-purple mb-4"
               style={{ boxShadow: '0 0 40px rgba(108,92,231,0.6)' }}>
            <span className="font-display font-black text-2xl">G</span>
          </div>
          <h1 className="font-display font-black text-3xl gradient-text mb-1">GambleMatch</h1>
          <p className="text-white/40 text-sm">Sign in to your account</p>
        </div>

        {/* Card */}
        <div className="glass-card p-8">
          <div className="mb-6">
            <h2 className="font-display font-bold text-xl text-white mb-1">Login with Discord</h2>
            <p className="text-white/50 text-sm leading-relaxed">
              Run <code className="bg-gm-surface px-2 py-0.5 rounded text-gm-violet font-mono">/login</code> in
              the Discord server. The bot will DM you a 6-digit code.
            </p>
          </div>

          {/* How it works steps */}
          <div className="flex gap-3 mb-8 p-4 rounded-xl bg-gm-surface/50 border border-gm-border/40">
            {[
              { n:'1', label:'Open Discord' },
              { n:'2', label:'Run /login' },
              { n:'3', label:'Check your DMs' },
            ].map(s => (
              <div key={s.n} className="flex-1 text-center">
                <div className="w-7 h-7 rounded-full bg-gm-purple/40 border border-gm-purple/60
                                flex items-center justify-center text-gm-violet font-bold text-xs mx-auto mb-1.5">
                  {s.n}
                </div>
                <div className="text-white/50 text-xs">{s.label}</div>
              </div>
            ))}
          </div>

          <div className="space-y-4">
            {/* Discord User ID */}
            <div>
              <label className="block text-sm text-white/60 mb-2 font-medium">Your Discord User ID</label>
              <input
                type="text"
                value={userId}
                onChange={e => setUserId(e.target.value.replace(/\D/g, ''))}
                placeholder="e.g. 123456789012345678"
                className="w-full px-4 py-3 rounded-xl bg-gm-void border border-gm-border focus:border-gm-purple
                           text-white placeholder-white/20 font-mono text-sm outline-none transition-colors"
                style={{ caretColor: '#a594ff' }}
              />
              <p className="text-white/25 text-xs mt-1.5">
                Discord → Settings → Advanced → Developer Mode → right-click your name → Copy ID
              </p>
            </div>

            {/* Code */}
            <div>
              <label className="block text-sm text-white/60 mb-2 font-medium">Login Code (from DM)</label>
              <input
                type="text"
                value={code}
                onChange={e => handleCodeChange(e.target.value)}
                placeholder="ABC123"
                maxLength={6}
                className="w-full px-4 py-3 rounded-xl bg-gm-void border border-gm-border focus:border-gm-purple
                           text-white placeholder-white/20 font-mono text-xl text-center tracking-[0.4em]
                           outline-none transition-colors uppercase"
                style={{ caretColor: '#a594ff', letterSpacing: code ? '0.4em' : undefined }}
                onKeyDown={e => e.key === 'Enter' && handleSubmit()}
              />
              <p className="text-white/25 text-xs mt-1.5 text-center">Code expires in 5 minutes</p>
            </div>

            {/* Error */}
            {error && (
              <div className="flex items-center gap-2 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
                <span>⚠️</span> {error}
              </div>
            )}

            {/* Submit */}
            <button
              onClick={handleSubmit}
              disabled={loading || !userId || code.length < 6}
              className="w-full py-3.5 rounded-xl font-bold text-base transition-all duration-200
                         disabled:opacity-40 disabled:cursor-not-allowed hover:scale-[1.02] active:scale-[0.98]"
              style={{
                background: 'linear-gradient(135deg, #6c5ce7, #5865F2)',
                boxShadow: loading || !userId || code.length < 6 ? 'none' : '0 0 25px rgba(108,92,231,0.5)',
              }}
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                  </svg>
                  Verifying...
                </span>
              ) : 'Sign In →'}
            </button>

            <a href="/" className="block text-center text-white/30 text-sm hover:text-white/60 transition-colors mt-2">
              ← Back to home
            </a>
          </div>
        </div>

        <p className="text-center text-white/15 text-xs mt-6">
          Session lasts 7 days · No password stored · Code is single-use
        </p>
      </div>
    </main>
  )
}
