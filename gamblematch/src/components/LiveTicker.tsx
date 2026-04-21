const TICKER_ITEMS = [
  '🏆 xzo just won 2,400,000 pts in a Lithium room match',
  '🎰 Blaze_77 hit JACKPOT on /slots — 10× multiplier!',
  '🔗 SlingshotK earned 5,000 pts for inviting a new member',
  '💎 GrindMode opened an Emerald Room',
  '🎁 Daily streak milestone: VoidRunner hit 14 days — +15,000 pts bonus!',
  '⚔️ CryptoAce vs NoScope99 — Bo7 match starting now',
  '🛒 New item listed in shop: Dragon Fruit (limited stock)',
  '🔥 xzo is on a 12-win streak',
  '💣 Phantom_X survived 11/12 cells in Bomb Field — cashed out +3,200 pts',
  '⭐ Clutch was vouched — 8 rep total',
]

export default function LiveTicker() {
  const doubled = [...TICKER_ITEMS, ...TICKER_ITEMS]

  return (
    <div className="relative overflow-hidden py-3 border-y border-gm-border/40 bg-gm-surface/30">
      <div className="flex gap-12 animate-ticker whitespace-nowrap" style={{ width:'max-content' }}>
        {doubled.map((item, i) => (
          <span key={i} className="text-sm text-white/50 font-medium flex-shrink-0">
            <span className="text-gm-purple mx-3">◆</span>
            {item}
          </span>
        ))}
      </div>
    </div>
  )
}
