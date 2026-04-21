'use client'
import { useState } from 'react'
import { mockLeaderboard, mockMatches, ROOM_TIER_META, GAME_EMOJIS, type Player } from '@/lib/data'

const RANK_COLORS: Record<string, string> = {
  Legendary: '#ff6f00', Diamond: '#1e88e5', Platinum: '#00bcd4',
  Gold: '#ffd700', Silver: '#c0c0c0', Bronze: '#cd7f32', Unranked: '#8a8a8a',
}

function PlayerRow({ player, rank }: { player: Player; rank: number }) {
  const rankColor = RANK_COLORS[player.rank] || '#8a8a8a'
  const room = player.room ? ROOM_TIER_META[player.room] : null

  return (
    <div className="group flex items-center gap-3 sm:gap-4 px-4 py-3.5 rounded-xl
                    border border-gm-border/50 hover:border-gm-purple/50
                    bg-gm-card/40 hover:bg-gm-surface/60
                    transition-all duration-200 hover:-translate-y-0.5">
      {/* Rank number */}
      <div className="w-8 text-center flex-shrink-0">
        {rank === 1 ? <span className="text-xl">🥇</span>
         : rank === 2 ? <span className="text-xl">🥈</span>
         : rank === 3 ? <span className="text-xl">🥉</span>
         : <span className="text-white/40 font-display font-bold text-sm">#{rank}</span>}
      </div>

      {/* Avatar */}
      <div className="w-9 h-9 rounded-xl flex items-center justify-center text-lg flex-shrink-0"
           style={{ background:`linear-gradient(135deg, ${rankColor}22, ${rankColor}44)`,
                    border:`1px solid ${rankColor}55` }}>
        {player.avatar}
      </div>

      {/* Name + badges */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="font-semibold text-white truncate">{player.name}</span>
          <span className="text-xs px-2 py-0.5 rounded-full border font-display"
                style={{ color:rankColor, borderColor:`${rankColor}60`, fontSize:'0.65rem' }}>
            {player.rank}
          </span>
          {room && (
            <span className="text-xs px-2 py-0.5 rounded-full border font-display hidden sm:inline-flex"
                  style={{ color:room.color, borderColor:`${room.color}60`, fontSize:'0.65rem' }}>
              {room.label} {room.luck}×
            </span>
          )}
        </div>
        <div className="text-xs text-white/40 mt-0.5 flex items-center gap-2">
          <span>{player.wins}W {player.losses}L</span>
          <span className="text-white/20">·</span>
          <span style={{ color: player.winRate >= 60 ? '#00e676' : player.winRate >= 45 ? '#ffd700' : '#ff4444' }}>
            {player.winRate}%
          </span>
          {player.streak > 0 && (
            <>
              <span className="text-white/20">·</span>
              <span className="text-gm-amber">🔥{player.streak}</span>
            </>
          )}
        </div>
      </div>

      {/* Points */}
      <div className="text-right flex-shrink-0 hidden sm:block">
        <div className="text-sm font-bold text-gm-violet font-display">
          {player.points >= 1_000_000
            ? `${(player.points / 1_000_000).toFixed(1)}M`
            : player.points >= 1_000
            ? `${(player.points / 1_000).toFixed(0)}K`
            : player.points.toLocaleString()}
        </div>
        <div className="text-xs text-white/30">pts</div>
      </div>

      {/* Rep */}
      <div className="text-right flex-shrink-0">
        <div className="text-sm font-bold text-gm-gold">⭐ {player.rep}</div>
        <div className="text-xs text-white/30">rep</div>
      </div>
    </div>
  )
}

function MatchFeed() {
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2 mb-4">
        <span className="live-dot" />
        <span className="text-sm text-white/50 font-medium">Live match feed</span>
      </div>
      {mockMatches.map((m) => (
        <div key={m.id}
             className="flex items-center gap-3 px-4 py-3 rounded-xl border border-gm-border/50
                        bg-gm-card/40 hover:bg-gm-surface/50 transition-all duration-200">
          <span className="text-xl flex-shrink-0">{GAME_EMOJIS[m.game] || '🎲'}</span>
          <div className="flex-1 min-w-0">
            <div className="text-sm font-semibold flex items-center gap-1.5 flex-wrap">
              <span className="text-gm-emerald truncate">{m.winner}</span>
              <span className="text-white/30 text-xs">defeated</span>
              <span className="text-white/60 truncate">
                {m.p1 === m.winner ? m.p2 : m.p1}
              </span>
            </div>
            <div className="text-xs text-white/40 mt-0.5">
              {m.game} · Bo{m.bestOf} · {m.result}
            </div>
          </div>
          <div className="text-right flex-shrink-0">
            <div className="text-xs text-white/30">{m.timestamp}</div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default function Leaderboard() {
  const [tab, setTab] = useState<'top' | 'feed'>('top')

  return (
    <section id="leaderboard" className="relative py-24 px-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 text-gm-violet text-sm font-medium mb-4
                          px-4 py-1.5 rounded-full border border-gm-purple/30 bg-gm-surface/40">
            🏆 Live Rankings
          </div>
          <h2 className="font-display font-black gradient-text mb-4"
              style={{ fontSize:'clamp(2rem, 5vw, 3.5rem)' }}>
            Leaderboard
          </h2>
          <p className="text-white/50 max-w-md mx-auto">
            Real-time rankings based on wins, streaks, and reputation. Updated after every match.
          </p>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 p-1 rounded-xl bg-gm-surface/40 border border-gm-border/50 w-fit mx-auto">
          {[['top','🏆 Top Players'], ['feed','⚡ Match Feed']].map(([t, label]) => (
            <button
              key={t}
              onClick={() => setTab(t as 'top' | 'feed')}
              className={`px-5 py-2 rounded-lg text-sm font-semibold transition-all duration-200 ${
                tab === t
                  ? 'bg-gm-purple text-white shadow-lg'
                  : 'text-white/50 hover:text-white/80'
              }`}
              style={tab === t ? { boxShadow:'0 0 15px rgba(108,92,231,0.4)' } : {}}
            >
              {label}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="glass-card p-4 sm:p-6">
          {tab === 'top' ? (
            <div className="space-y-2">
              {mockLeaderboard.map((p, i) => (
                <PlayerRow key={p.id} player={p} rank={i + 1} />
              ))}
            </div>
          ) : (
            <MatchFeed />
          )}
        </div>

        {/* Note */}
        <p className="text-center text-xs text-white/25 mt-4">
          Data refreshes automatically · Connect your bot&apos;s API endpoint to show live data
        </p>
      </div>
    </section>
  )
}
