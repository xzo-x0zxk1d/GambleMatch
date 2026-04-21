// src/lib/data.ts
// Replace with real API calls to your bot's data JSON files or an endpoint

export type RankTier = 'Unranked' | 'Bronze' | 'Silver' | 'Gold' | 'Platinum' | 'Diamond' | 'Legendary'
export type RoomTier = 'bronze' | 'silver' | 'gold' | 'platinum' | 'ruby' | 'emerald' | 'lithium'

export interface Player {
  id: string
  name: string
  avatar: string
  wins: number
  losses: number
  winRate: number
  streak: number
  points: number
  rep: number
  rank: RankTier
  room?: RoomTier
}

export interface Match {
  id: string
  p1: string
  p2: string
  game: string
  result: string
  winner: string
  timestamp: string
  bestOf: number
}

export interface LiveStat {
  label: string
  value: string
  delta?: string
  color: string
}

// ── Mock leaderboard data ──────────────────────────────────────────
export const mockLeaderboard: Player[] = [
  { id:'1', name:'xzo',        avatar:'👑', wins:142, losses:31,  winRate:82.1, streak:12, points:2_400_000, rep:88,  rank:'Legendary', room:'lithium'  },
  { id:'2', name:'Blaze_77',   avatar:'🔥', wins:98,  losses:44,  winRate:69.0, streak:5,  points:980_000,   rep:61,  rank:'Diamond',   room:'ruby'     },
  { id:'3', name:'GrindMode',  avatar:'⚡', wins:87,  losses:53,  winRate:62.1, streak:3,  points:740_000,   rep:45,  rank:'Diamond',   room:'emerald'  },
  { id:'4', name:'SlingshotK', avatar:'💎', wins:74,  losses:40,  winRate:64.9, streak:7,  points:510_000,   rep:39,  rank:'Platinum',  room:'ruby'     },
  { id:'5', name:'VoidRunner',  avatar:'🌀', wins:61,  losses:60,  winRate:50.4, streak:1,  points:388_000,   rep:28,  rank:'Gold',      room:'platinum' },
  { id:'6', name:'CryptoAce',  avatar:'🃏', wins:55,  losses:38,  winRate:59.1, streak:4,  points:290_000,   rep:22,  rank:'Gold',      room:'gold'     },
  { id:'7', name:'NoScope99',  avatar:'🎯', wins:44,  losses:55,  winRate:44.4, streak:0,  points:185_000,   rep:14,  rank:'Silver',    room:'silver'   },
  { id:'8', name:'Phantom_X',  avatar:'👻', wins:38,  losses:29,  winRate:56.7, streak:2,  points:120_000,   rep:19,  rank:'Silver',    room:'silver'   },
  { id:'9', name:'Clutch',     avatar:'🎲', wins:28,  losses:33,  winRate:45.9, streak:0,  points:64_000,    rep:8,   rank:'Bronze',    room:'bronze'   },
  { id:'10',name:'NewPlayer',  avatar:'🪨', wins:5,   losses:12,  winRate:29.4, streak:0,  points:12_000,    rep:2,   rank:'Unranked'   },
]

// ── Mock recent matches feed ───────────────────────────────────────
export const mockMatches: Match[] = [
  { id:'M1', p1:'xzo',        p2:'Blaze_77',   game:'Robux',     result:'3–1', winner:'xzo',        timestamp:'2m ago',  bestOf:5 },
  { id:'M2', p1:'GrindMode',  p2:'SlingshotK', game:'Blox Fruit',result:'2–1', winner:'GrindMode',  timestamp:'5m ago',  bestOf:3 },
  { id:'M3', p1:'VoidRunner',  p2:'CryptoAce',  game:'MM2',       result:'4–2', winner:'VoidRunner',  timestamp:'9m ago',  bestOf:7 },
  { id:'M4', p1:'NoScope99',  p2:'Phantom_X',  game:'SAB',       result:'2–0', winner:'Phantom_X',  timestamp:'12m ago', bestOf:3 },
  { id:'M5', p1:'Clutch',     p2:'NewPlayer',  game:'GAG',       result:'3–2', winner:'Clutch',     timestamp:'18m ago', bestOf:5 },
  { id:'M6', p1:'Blaze_77',   p2:'GrindMode',  game:'Robux',     result:'3–0', winner:'Blaze_77',   timestamp:'24m ago', bestOf:5 },
]

// ── Live stats bar ─────────────────────────────────────────────────
export const liveStats: LiveStat[] = [
  { label:'Matches Today',  value:'248',       delta:'+12',  color:'#a594ff' },
  { label:'Points Wagered', value:'4.2M',      delta:'+180K',color:'#ffd700' },
  { label:'Active Players', value:'63',        delta:'+7',   color:'#00e676' },
  { label:'Live Matches',   value:'11',                      color:'#00e5ff' },
  { label:'Shop Items',     value:'24',                      color:'#ff9100' },
  { label:'Total Players',  value:'1,294',                   color:'#a594ff' },
]

export const ROOM_TIER_META: Record<RoomTier, { label:string; color:string; luck:number }> = {
  bronze:   { label:'Bronze',   color:'#cd7f32', luck:0.5  },
  silver:   { label:'Silver',   color:'#c0c0c0', luck:1.5  },
  gold:     { label:'Gold',     color:'#ffd700', luck:2.5  },
  platinum: { label:'Platinum', color:'#00bcd4', luck:5.0  },
  ruby:     { label:'Ruby',     color:'#ff1744', luck:7.5  },
  emerald:  { label:'Emerald',  color:'#00e676', luck:10.0 },
  lithium:  { label:'Lithium',  color:'#a594ff', luck:15.0 },
}

export const GAME_EMOJIS: Record<string, string> = {
  'Robux':     '💎',
  'Blox Fruit':'🍎',
  'MM2':       '🔪',
  'SAB':       '🗡️',
  'GAG':       '🃏',
  'Other':     '🎲',
}

export const FEATURES = [
  { icon:'⚔️',  title:'Live Matchmaking',   desc:'Find opponents instantly across SAB, Blox Fruits, MM2, GAG, Robux & more. Best-of-3/5/7 randomly drawn.' },
  { icon:'🎰',  title:'Casino Games',        desc:'Bomb Field, Mines, Slots, Blackjack, Coin Flip — all powered by GambleGems you earn daily.' },
  { icon:'🏠',  title:'Room System',         desc:'7 tiers from Bronze to Lithium. Own a room, invite friends, and stack luck multipliers up to 15×.' },
  { icon:'🔗',  title:'Invite Rewards',      desc:'Every invite earns 5,000 pts and boosts your luck. 50 invite roles track your grind.' },
  { icon:'🏦',  title:'Bank System',         desc:'Deposit funds to protect them from casino losses. Withdraw anytime.' },
  { icon:'🎫',  title:'Redeem Codes',        desc:'Unlock currencies, room upgrades, and exclusive roles with secret codes.' },
  { icon:'📦',  title:'Exclusive Shop',      desc:'Spend GambleGems on real items. Purchases create private ticket channels for suppliers.' },
  { icon:'💬',  title:'Message Rewards',     desc:'Every 500 messages = 2,000 pts. Stay active, keep earning.' },
]

export const RANK_TIERS = [
  { label:'Unranked', threshold:0,   color:'#8a8a8a', icon:'🪨' },
  { label:'Bronze',   threshold:5,   color:'#cd7f32', icon:'🥉' },
  { label:'Silver',   threshold:15,  color:'#c0c0c0', icon:'🥈' },
  { label:'Gold',     threshold:30,  color:'#ffd700', icon:'🥇' },
  { label:'Platinum', threshold:50,  color:'#00bcd4', icon:'💠' },
  { label:'Diamond',  threshold:75,  color:'#1e88e5', icon:'💎' },
  { label:'Legendary',threshold:100, color:'#ff6f00', icon:'👑' },
]
