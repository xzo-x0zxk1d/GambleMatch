'use client'
import { useState } from 'react'

type Cmd = { name: string; desc: string; args?: string; restricted?: string }
type Category = { label: string; icon: string; color: string; cmds: Cmd[] }

const CATEGORIES: Category[] = [
  {
    label:'Matchmaking', icon:'⚔️', color:'#a594ff',
    cmds:[
      { name:'/findg',     desc:'Find a gambling match against another player', args:'offer game [cross_trade]', restricted:'#findg channel' },
      { name:'/leaveq',    desc:'Leave the matchmaking queue' },
      { name:'/queue',     desc:'View who is currently in the queue' },
      { name:'/challenge', desc:'Directly challenge a specific player via DM', args:'@user offer game' },
    ]
  },
  {
    label:'Casino', icon:'🎰', color:'#ffd700',
    cmds:[
      { name:'/gamble',    desc:'Wager points against another player (1v1)', args:'@user amount', restricted:'casino or room' },
      { name:'/bomb',      desc:'Bomb Field — reveal cells, avoid 3 bombs. Cash out anytime.', args:'wager', restricted:'casino or room' },
      { name:'/mines',     desc:'Mine Field — collect gems, avoid mines. Lower risk.', args:'wager', restricted:'casino or room' },
      { name:'/slots',     desc:'Spin the slot machine. 6 symbols, jackpot at 10×.', args:'wager', restricted:'casino or room' },
      { name:'/flip',      desc:'Solo coin flip vs the house. Win = 2×.', args:'wager', restricted:'casino or room' },
      { name:'/blackjack', desc:'Play Blackjack vs the dealer. Stand on 17+.', args:'wager', restricted:'casino or room' },
    ]
  },
  {
    label:'Economy', icon:'💰', color:'#00e676',
    cmds:[
      { name:'/balance',     desc:'Check your wallet and bank balance' },
      { name:'/daily',       desc:'Claim daily reward. Streak = higher reward (up to 5,000 pts/day)' },
      { name:'/deposit',     desc:'Move points to bank (safe from casino losses)', args:'amount' },
      { name:'/withdraw',    desc:'Move points from bank back to wallet', args:'amount' },
      { name:'/bankbalance', desc:'Full account overview: wallet + bank + total' },
      { name:'/give',        desc:'Send points to another player', args:'@user amount' },
    ]
  },
  {
    label:'Rooms', icon:'🏠', color:'#00e5ff',
    cmds:[
      { name:'/myroom',     desc:'View your room tier, luck multiplier, and guest list' },
      { name:'/rooms',      desc:'List all active rooms publicly' },
      { name:'/upgraderoom',desc:'Upgrade your room based on your current balance' },
      { name:'/deleteroom', desc:'Delete your room channel' },
      { name:'/myluck',     desc:'Show your total luck multiplier (room + invite bonus)' },
    ]
  },
  {
    label:'Shop', icon:'🛒', color:'#ff9100',
    cmds:[
      { name:'/shop',   desc:'Browse the GambleGems shop' },
      { name:'/buy',    desc:'Purchase an item (creates private ticket channel)', args:'item_id' },
      { name:'/redeem', desc:'Redeem a code for points, room rank, or a role', args:'code' },
    ]
  },
  {
    label:'Stats', icon:'📊', color:'#a594ff',
    cmds:[
      { name:'/stats',       desc:'View gambling stats for yourself or another player', args:'[@user]' },
      { name:'/leaderboard', desc:'Top 10 players by wins' },
      { name:'/richlist',    desc:'Top 10 players by points balance' },
      { name:'/history',     desc:'Last 10 completed match results' },
      { name:'/rep',         desc:'Give +1 reputation to a trusted player', args:'@user' },
    ]
  },
  {
    label:'Supplier Only', icon:'🏪', color:'#ff1744',
    cmds:[
      { name:'/additem',    desc:'Add an item to the shop', restricted:'Supplier role' },
      { name:'/edititem',   desc:'Edit a shop item', args:'item_id', restricted:'Supplier role' },
      { name:'/removeitem', desc:'Remove an item from the shop', args:'item_id', restricted:'Supplier role' },
      { name:'/setstock',   desc:'Update item stock level', args:'item_id stock', restricted:'Supplier role' },
      { name:'/addpoints',  desc:'Grant points to a user', args:'@user amount', restricted:'Supplier role' },
      { name:'/purchases',  desc:'View recent purchase log', restricted:'Supplier role' },
      { name:'/addcode',    desc:'Create a redeem code', args:'type value code max_uses', restricted:'Code Maker role' },
      { name:'/listcodes',  desc:'List all active codes', restricted:'Code Maker role' },
      { name:'/deletecode', desc:'Delete a code', args:'code', restricted:'Code Maker role' },
    ]
  },
]

export default function Commands() {
  const [active, setActive] = useState(0)
  const cat = CATEGORIES[active]

  return (
    <section id="commands" className="relative py-24 px-6">
      <div className="absolute inset-0 bg-grid-pattern opacity-10" />
      <div className="relative max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 text-gm-violet text-sm font-medium mb-4
                          px-4 py-1.5 rounded-full border border-gm-purple/30 bg-gm-surface/40">
            📋 Command Reference
          </div>
          <h2 className="font-display font-black gradient-text mb-4"
              style={{ fontSize:'clamp(2rem, 5vw, 3.5rem)' }}>
            All Commands
          </h2>
        </div>

        <div className="flex gap-6 flex-col lg:flex-row">
          {/* Category sidebar */}
          <div className="flex lg:flex-col gap-2 overflow-x-auto lg:overflow-visible pb-2 lg:pb-0 lg:w-48 flex-shrink-0">
            {CATEGORIES.map((c, i) => (
              <button
                key={i}
                onClick={() => setActive(i)}
                className={`flex items-center gap-2 px-4 py-3 rounded-xl text-sm font-semibold
                            whitespace-nowrap transition-all duration-200 text-left
                            ${active === i
                              ? 'bg-gm-surface border-l-2 text-white'
                              : 'text-white/40 hover:text-white/70 hover:bg-gm-surface/40'}`}
                style={active === i ? { borderLeftColor:c.color } : {}}
              >
                <span>{c.icon}</span>
                <span>{c.label}</span>
              </button>
            ))}
          </div>

          {/* Command list */}
          <div className="flex-1 glass-card p-5">
            <div className="flex items-center gap-3 mb-5">
              <span className="text-2xl">{cat.icon}</span>
              <h3 className="font-display font-bold text-lg" style={{ color:cat.color }}>
                {cat.label}
              </h3>
              <span className="text-xs text-white/30 ml-auto">{cat.cmds.length} commands</span>
            </div>

            <div className="space-y-3">
              {cat.cmds.map((cmd, i) => (
                <div key={i}
                     className="flex flex-col sm:flex-row sm:items-start gap-2 sm:gap-4
                                px-4 py-3 rounded-lg bg-gm-void/60 border border-gm-border/30
                                hover:border-gm-border transition-colors">
                  <div className="flex-shrink-0">
                    <code className="text-sm font-mono font-bold"
                          style={{ color:cat.color }}>
                      {cmd.name}
                    </code>
                    {cmd.args && (
                      <span className="text-xs text-white/30 font-mono ml-1">{cmd.args}</span>
                    )}
                  </div>
                  <div className="flex-1">
                    <p className="text-sm text-white/60">{cmd.desc}</p>
                    {cmd.restricted && (
                      <span className="inline-flex items-center gap-1 text-xs text-gm-amber mt-1">
                        <span>🔒</span> {cmd.restricted}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
