'use client'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

const ROOM_TIER_COLORS: Record<string, string> = {
  bronze: '#cd7f32', silver: '#c0c0c0', gold: '#ffd700',
  platinum: '#00bcd4', ruby: '#ff1744', emerald: '#00e676', lithium: '#a594ff',
}
const GAME_EMOJIS: Record<string, string> = {
  robux: '💎', bloxfruit: '🍎', mm2: '🔪', sab: '🗡️', gag: '🃏', other: '🎲',
}

function StatCard({ label, value, sub, color }: { label: string; value: string | number; sub?: string; color?: string }) {
  return (
    <div className="glass-card p-5 hover:border-gm-purple/40 transition-all">
      <div className="text-xs text-white/40 mb-2 font-medium uppercase tracking-wide">{label}</div>
      <div className="text-2xl font-display font-black" style={{ color: color || '#fff' }}>
        {typeof value === 'number' ? value.toLocaleString() : value}
      </div>
      {sub && <div className="text-xs text-white/30 mt-1">{sub}</div>}
    </div>
  )
}

function fmt(n: number) {
  if (n >= 1_000_000_000) return `${(n / 1_000_000_000).toFixed(2)}B`
  if (n >= 1_000_000)     return `${(n / 1_000_000).toFixed(2)}M`
  if (n >= 1_000)         return `${(n / 1_000).toFixed(1)}K`
  return n.toLocaleString()
}

export default function Dashboard() {
  const router = useRouter()
  const [data, setData]       = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [tab, setTab]         = useState<'overview' | 'stats' | 'room'>('overview')

  useEffect(() => {
    fetch('/api/me')
      .then(r => {
        if (r.status === 401) { router.push('/login'); return null }
        return r.json()
      })
      .then(d => { if (d) { setData(d); setLoading(false) } })
      .catch(() => router.push('/login'))
  }, [router])

  const logout = async () => {
    await fetch('/api/auth/logout', { method: 'POST' })
    router.push('/')
  }

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gm-void">
        <div className="text-center">
          <div className="w-12 h-12 rounded-full border-2 border-gm-purple border-t-transparent animate-spin mx-auto mb-4" />
          <p className="text-white/40 font-display text-sm">Loading your data...</p>
        </div>
      </main>
    )
  }

  if (!data) return null

  const room = data.room
  const roomColor = room ? (ROOM_TIER_COLORS[room.tier_key] || '#6c5ce7') : null

  return (
    <main className="min-h-screen bg-gm-void text-white">
      <div className="absolute inset-0 bg-grid-pattern opacity-10 pointer-events-none" />

      {/* Navbar */}
      <nav className="relative z-10 border-b border-gm-border/40 bg-gm-deep/80 backdrop-blur-xl">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <a href="/" className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-gm-purple flex items-center justify-center font-black text-sm"
                   style={{ boxShadow: '0 0 15px rgba(108,92,231,0.5)' }}>G</div>
              <span className="font-display font-bold text-gm-violet hidden sm:block">GambleMatch</span>
            </a>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-white/40 text-sm hidden sm:block">@{data.username}</span>
            <button onClick={logout}
                    className="text-sm px-4 py-2 rounded-lg border border-gm-border hover:border-red-500/50
                               text-white/50 hover:text-red-400 transition-all">
              Sign Out
            </button>
          </div>
        </div>
      </nav>

      <div className="relative z-10 max-w-6xl mx-auto px-6 py-10">

        {/* Welcome */}
        <div className="mb-10 flex items-start justify-between flex-wrap gap-4">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <div className="w-12 h-12 rounded-2xl bg-gm-purple/30 border border-gm-purple/40
                              flex items-center justify-center font-black text-xl">
                {data.username?.[0]?.toUpperCase() || '?'}
              </div>
              <div>
                <h1 className="font-display font-black text-2xl text-white">
                  {data.username}
                </h1>
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-gm-violet">{data.rank}</span>
                  <span className="text-white/20">·</span>
                  <span className="text-white/40">#{data.winRank || '?'} ranked</span>
                  {data.stats.streak > 0 && (
                    <>
                      <span className="text-white/20">·</span>
                      <span className="text-gm-amber">🔥 {data.stats.streak} streak</span>
                    </>
                  )}
                </div>
              </div>
            </div>
          </div>
          <a href="https://discord.gg/smxxKFPHZw" target="_blank" rel="noopener noreferrer"
             className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gm-purple/20 border border-gm-purple/40
                        text-gm-violet text-sm font-semibold hover:bg-gm-purple/30 transition-all">
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057c.002.022.015.043.03.056a19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028 14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03z"/>
            </svg>
            Open Discord
          </a>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-8 p-1 rounded-xl bg-gm-surface/40 border border-gm-border/40 w-fit">
          {[['overview','📊 Overview'], ['stats','⚔️ Stats'], ['room','🏠 Room']].map(([t, label]) => (
            <button key={t} onClick={() => setTab(t as any)}
                    className={`px-5 py-2 rounded-lg text-sm font-semibold transition-all ${
                      tab === t ? 'bg-gm-purple text-white' : 'text-white/40 hover:text-white/70'
                    }`}
                    style={tab === t ? { boxShadow: '0 0 15px rgba(108,92,231,0.4)' } : {}}>
              {label}
            </button>
          ))}
        </div>

        {/* ── OVERVIEW TAB ── */}
        {tab === 'overview' && (
          <div className="space-y-6">
            {/* Wealth */}
            <div>
              <h2 className="text-white/40 text-xs font-display font-bold tracking-widest uppercase mb-3">Wealth</h2>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                <StatCard label="💎 Wallet" value={fmt(data.wallet)} sub={`${data.wallet.toLocaleString()} pts`} color="#a594ff" />
                <StatCard label="🏦 Bank"   value={fmt(data.bank)}   sub={`${data.bank.toLocaleString()} pts`}   color="#00e5ff" />
                <StatCard label="📊 Total"  value={fmt(data.total)}  sub={`Rank #${data.ptsRank || '?'} rich list`} color="#ffd700" />
              </div>
            </div>

            {/* Activity */}
            <div>
              <h2 className="text-white/40 text-xs font-display font-bold tracking-widest uppercase mb-3">Activity</h2>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <StatCard label="🔥 Daily Streak" value={data.streak}          sub={`Best: ${data.bestStreak}`}   color="#ff9100" />
                <StatCard label="💬 Messages"      value={data.msgCount.toLocaleString()} sub="lifetime total"   color="#a594ff" />
                <StatCard label="🔗 Invites"       value={data.invites}         sub="members invited"             color="#00e676" />
                <StatCard label="⭐ Rep"            value={data.rep}             sub="reputation points"           color="#ffd700" />
              </div>
            </div>

            {/* Recent matches */}
            <div>
              <h2 className="text-white/40 text-xs font-display font-bold tracking-widest uppercase mb-3">Recent Matches</h2>
              {data.recentMatches.length === 0 ? (
                <div className="glass-card p-6 text-center text-white/30 text-sm">
                  No matches played yet. Head to the server and use <code className="text-gm-violet">/findg</code>!
                </div>
              ) : (
                <div className="space-y-2">
                  {data.recentMatches.map((m: any, i: number) => {
                    const won = String(m.winner_id) === String(data.userId)
                    return (
                      <div key={i} className="flex items-center gap-3 px-4 py-3 rounded-xl
                                              border border-gm-border/40 bg-gm-card/40 hover:bg-gm-surface/40 transition-all">
                        <span className="text-xl flex-shrink-0">{GAME_EMOJIS[m.game] || '🎲'}</span>
                        <div className="flex-1 min-w-0">
                          <div className="text-sm font-semibold" style={{ color: won ? '#00e676' : '#ff4444' }}>
                            {won ? '🏆 Victory' : '💀 Defeat'}
                          </div>
                          <div className="text-xs text-white/40">{m.game?.toUpperCase()} · Bo{m.best_of} · {m.rounds} rounds</div>
                        </div>
                        <div className="text-xs font-mono text-white/25">{m.match_id}</div>
                      </div>
                    )
                  })}
                </div>
              )}
            </div>
          </div>
        )}

        {/* ── STATS TAB ── */}
        {tab === 'stats' && (
          <div className="space-y-6">
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              <StatCard label="Wins"         value={data.stats.wins}         color="#00e676" />
              <StatCard label="Losses"       value={data.stats.losses}       color="#ff4444" />
              <StatCard label="Games Played" value={data.stats.games_played} color="#a594ff" />
              <StatCard label="Win Rate"     value={`${data.winRate}%`}
                        color={parseFloat(data.winRate) >= 60 ? '#00e676' : parseFloat(data.winRate) >= 45 ? '#ffd700' : '#ff4444'} />
              <StatCard label="Rounds Won"   value={data.stats.rounds_won}   color="#00e5ff" />
              <StatCard label="Rounds Lost"  value={data.stats.rounds_lost}  color="#ff9100" />
              <StatCard label="Win Streak"   value={data.stats.streak}       sub={`Best: ${data.stats.best_streak}`} color="#ff9100" />
              <StatCard label="Rank"         value={data.rank}               color="#a594ff" />
              <StatCard label="Leaderboard"  value={`#${data.winRank || '?'}`} sub="by wins"  color="#ffd700" />
            </div>

            {/* Win rate bar */}
            {data.stats.games_played > 0 && (
              <div className="glass-card p-5">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-sm text-white/60 font-medium">Win / Loss ratio</span>
                  <span className="text-sm font-bold text-white">{data.winRate}%</span>
                </div>
                <div className="h-3 bg-gm-void rounded-full overflow-hidden">
                  <div className="h-full rounded-full transition-all duration-700"
                       style={{
                         width: `${data.winRate === 'N/A' ? 0 : data.winRate}%`,
                         background: parseFloat(data.winRate) >= 60 ? '#00e676' : parseFloat(data.winRate) >= 45 ? '#ffd700' : '#ff4444',
                         boxShadow: '0 0 8px currentColor',
                       }} />
                </div>
                <div className="flex justify-between text-xs text-white/25 mt-1.5">
                  <span>{data.stats.wins}W</span>
                  <span>{data.stats.losses}L</span>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ── ROOM TAB ── */}
        {tab === 'room' && (
          <div>
            {!room ? (
              <div className="glass-card p-8 text-center">
                <div className="text-5xl mb-4">🏠</div>
                <h3 className="font-display font-bold text-xl text-white mb-2">No Room Yet</h3>
                <p className="text-white/40 text-sm mb-6">
                  Register a room in the Discord server to unlock luck multipliers and exclusive perks.
                </p>
                <a href="https://discord.gg/smxxKFPHZw" target="_blank" rel="noopener noreferrer"
                   className="inline-flex items-center gap-2 px-6 py-3 rounded-xl font-bold text-sm"
                   style={{ background: 'linear-gradient(135deg, #6c5ce7, #5865F2)', boxShadow: '0 0 20px rgba(108,92,231,0.4)' }}>
                  Open Discord → Register Room
                </a>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="glass-card p-6"
                     style={{ borderColor: `${roomColor}40` }}>
                  <div className="flex items-center gap-4 mb-6">
                    <div className="w-14 h-14 rounded-2xl flex items-center justify-center text-3xl"
                         style={{ background: `${roomColor}20`, border: `1px solid ${roomColor}40` }}>
                      {room.tier_key === 'lithium' ? '⚡' : room.tier_key === 'emerald' ? '💚' :
                       room.tier_key === 'ruby' ? '💎' : room.tier_key === 'platinum' ? '💠' :
                       room.tier_key === 'gold' ? '🥇' : room.tier_key === 'silver' ? '🥈' : '🥉'}
                    </div>
                    <div>
                      <h3 className="font-display font-bold text-xl" style={{ color: roomColor || '#fff' }}>
                        {room.tier_key?.charAt(0).toUpperCase() + room.tier_key?.slice(1)} Room
                      </h3>
                      <p className="text-white/40 text-sm">{room.guests?.length || 0} guest(s) invited</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                    <StatCard label="🍀 Luck Mult"   value={`${room.tier_luck}×`}   color={roomColor || '#fff'} />
                    <StatCard label="⚡ Total Luck"  value={`${room.total_luck}×`}  color={roomColor || '#fff'} />
                    <StatCard label="👥 Guest Slots" value={room.guests?.length || 0} sub="currently invited" color="#a594ff" />
                  </div>

                  <div className="mt-4 px-4 py-3 rounded-xl bg-gm-void/60 border border-gm-border/30 text-xs text-white/40">
                    Created: {room.created_at ? new Date(room.created_at).toLocaleDateString() : 'unknown'}
                    {' · '}
                    Balance at creation: {room.balance_at_creation?.toLocaleString() || 0} pts
                  </div>
                </div>

                <div className="glass-card p-5">
                  <h4 className="font-display font-bold text-sm text-white/60 mb-3">LUCK BREAKDOWN</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-white/50">Room base ({room.tier_key})</span>
                      <span className="font-bold text-white">{room.tier_luck}×</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-white/50">Invite bonus ({data.invites} invites)</span>
                      <span className="font-bold text-gm-emerald">+{(room.total_luck - room.tier_luck).toFixed(2)}×</span>
                    </div>
                    <div className="h-px bg-gm-border/40 my-2" />
                    <div className="flex justify-between text-sm font-bold">
                      <span className="text-white">Total luck</span>
                      <span style={{ color: roomColor || '#fff' }}>{room.total_luck}×</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  )
}
