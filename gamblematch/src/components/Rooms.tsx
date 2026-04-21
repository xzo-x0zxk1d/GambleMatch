import { ROOM_TIER_META, type RoomTier } from '@/lib/data'

const ROOM_DETAILS: Record<RoomTier, { guests: number; perks: string[] }> = {
  bronze:   { guests:1,  perks:['0.5× luck','1 guest','Basic shop'] },
  silver:   { guests:2,  perks:['1.5× luck','2 guests','Silver shop','Public stats'] },
  gold:     { guests:2,  perks:['2.5× luck','2 guests','Gold shop','Priority queue'] },
  platinum: { guests:2,  perks:['5× luck','2 guests','Platinum shop','Platinum badge'] },
  ruby:     { guests:4,  perks:['7.5× luck','4 guests','Full shop + early drops','Weekly bonus pts'] },
  emerald:  { guests:5,  perks:['10× luck','5 guests','Exclusive drops','Bi-weekly bonus','Restock pings'] },
  lithium:  { guests:10, perks:['15× luck','10 guests','First access all drops','Crown badge','Secret channel'] },
}

export default function Rooms() {
  const tiers = Object.entries(ROOM_TIER_META) as [RoomTier, typeof ROOM_TIER_META[RoomTier]][]

  return (
    <section id="rooms" className="relative py-24 px-6 overflow-hidden">
      <div className="absolute inset-0 bg-grid-pattern opacity-10" />

      <div className="relative max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 text-gm-violet text-sm font-medium mb-4
                          px-4 py-1.5 rounded-full border border-gm-purple/30 bg-gm-surface/40">
            🏠 Private Rooms
          </div>
          <h2 className="font-display font-black gradient-text mb-4"
              style={{ fontSize:'clamp(2rem, 5vw, 3.5rem)' }}>
            Room Tiers
          </h2>
          <p className="text-white/50 max-w-xl mx-auto">
            Your balance determines your tier. Higher tiers unlock more luck, more guests, and exclusive perks.
          </p>
        </div>

        {/* Tier cards */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-7 gap-3">
          {tiers.map(([key, meta]) => {
            const details = ROOM_DETAILS[key]
            const isLithium = key === 'lithium'

            return (
              <div
                key={key}
                className={`group relative rounded-2xl p-4 text-center transition-all duration-300
                            hover:-translate-y-3 cursor-default
                            ${isLithium ? 'lg:col-span-1' : ''}`}
                style={{
                  background: `linear-gradient(135deg, ${meta.color}10, ${meta.color}05)`,
                  border: `1px solid ${meta.color}40`,
                  boxShadow: `0 0 0 ${meta.color}00`,
                }}
                onMouseEnter={e => {
                  ;(e.currentTarget as HTMLElement).style.boxShadow = `0 8px 30px ${meta.color}30`
                  ;(e.currentTarget as HTMLElement).style.borderColor = `${meta.color}80`
                }}
                onMouseLeave={e => {
                  ;(e.currentTarget as HTMLElement).style.boxShadow = ''
                  ;(e.currentTarget as HTMLElement).style.borderColor = `${meta.color}40`
                }}
              >
                {isLithium && (
                  <div className="absolute -top-2 left-1/2 -translate-x-1/2 text-xs px-2 py-0.5 rounded-full font-display font-bold"
                       style={{ background:meta.color, color:'#02020a', fontSize:'0.6rem' }}>
                    MAX
                  </div>
                )}

                <div className="text-2xl mb-2"
                     style={{ filter:`drop-shadow(0 0 8px ${meta.color})` }}>
                  {key === 'bronze' ? '🥉' : key === 'silver' ? '🥈' : key === 'gold' ? '🥇'
                   : key === 'platinum' ? '💠' : key === 'ruby' ? '💎' : key === 'emerald' ? '💚' : '⚡'}
                </div>

                <div className="font-display font-bold text-xs mb-1" style={{ color:meta.color }}>
                  {meta.label}
                </div>

                <div className="text-lg font-black font-display mb-2" style={{ color:meta.color }}>
                  {meta.luck}×
                </div>

                <div className="text-xs text-white/40 mb-3">luck</div>

                <div className="text-xs text-white/50">
                  {details.guests} guest{details.guests > 1 ? 's' : ''}
                </div>

                {/* Perks on hover */}
                <div className="mt-3 space-y-1 hidden lg:block opacity-0 group-hover:opacity-100
                                transition-opacity duration-300 max-h-0 group-hover:max-h-40 overflow-hidden">
                  {details.perks.slice(2).map((p, i) => (
                    <div key={i} className="text-xs text-white/40 leading-tight">{p}</div>
                  ))}
                </div>
              </div>
            )
          })}
        </div>

        {/* Luck formula */}
        <div className="mt-10 glass-card p-6 max-w-2xl mx-auto text-center">
          <h3 className="font-display font-bold text-gm-violet mb-2 text-sm">Total Luck Formula</h3>
          <div className="font-mono text-white/70 text-sm">
            <span className="text-gm-cyan">Total Luck</span>
            {' = '}
            <span className="text-gm-gold">Room Tier Mult</span>
            {' + '}
            <span className="text-gm-emerald">Invite Bonus</span>
            {' (max +1.5×)'}
          </div>
          <p className="text-white/40 text-xs mt-2">
            50+ invites = max bonus. Lithium + max invites = <strong className="text-gm-violet">16.5× luck</strong>
          </p>
        </div>
      </div>
    </section>
  )
}
