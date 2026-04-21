import { NextResponse } from 'next/server'
import { getIronSession } from 'iron-session'
import { sessionOptions } from '@/lib/session'
import { cookies } from 'next/headers'
import fs from 'fs'
import path from 'path'

function readJson(name: string) {
  try {
    const dataPath = process.env.DATA_PATH || path.join(process.cwd(), '..', 'data')
    const filePath = path.join(dataPath, `${name}.json`)
    if (!fs.existsSync(filePath)) return null
    return JSON.parse(fs.readFileSync(filePath, 'utf-8'))
  } catch {
    return null
  }
}

export async function GET() {
  const session = await getIronSession(cookies(), sessionOptions)

  if (!session.user?.loggedIn) {
    return NextResponse.json({ error: 'Not logged in' }, { status: 401 })
  }

  const uid = session.user.userId

  // Read all bot data files
  const statsRaw      = readJson('stats')      || {}
  const pointsRaw     = readJson('points')     || {}
  const bankRaw       = readJson('bank')        || {}
  const repRaw        = readJson('reputation') || {}
  const streakRaw     = readJson('daily_streak') || {}
  const inviteRaw     = readJson('invite_counts') || {}
  const historyRaw    = readJson('history')    || []
  const roomsRaw      = readJson('rooms')      || { rooms: {} }
  const msgRaw        = readJson('msg_counts') || {}
  const dailyRaw      = readJson('daily')      || {}

  const userStats  = statsRaw[uid]  || { wins:0, losses:0, games_played:0, rounds_won:0, rounds_lost:0, streak:0, best_streak:0 }
  const wallet     = pointsRaw[uid] || 0
  const bankBal    = bankRaw[uid]   || 0
  const rep        = repRaw[uid]    || 0
  const streak     = streakRaw[uid] || { last: '', streak: 0 }
  const invites    = inviteRaw[uid] || 0
  const msgCount   = msgRaw[uid]    || 0
  const lastDaily  = dailyRaw[uid]  || ''

  // Find this user's room
  const allRooms = roomsRaw.rooms || roomsRaw || {}
  const myRoom   = Object.values(allRooms).find((r: any) => r.owner_id === parseInt(uid) || r.owner_id === uid) as any || null

  // Leaderboard rank by wins
  const allStats   = Object.entries(statsRaw)
  const sortedWins = allStats.sort(([, a]: any, [, b]: any) => b.wins - a.wins)
  const winRank    = sortedWins.findIndex(([k]) => k === uid) + 1

  const sortedPts  = Object.entries(pointsRaw).sort(([, a]: any, [, b]: any) => b - a)
  const ptsRank    = sortedPts.findIndex(([k]) => k === uid) + 1

  // Last 5 matches
  const myMatches = (historyRaw as any[])
    .filter(m => m.winner_id === parseInt(uid) || m.loser_id === parseInt(uid) ||
                 m.winner_id === uid           || m.loser_id === uid)
    .slice(-5).reverse()

  const winRate = userStats.games_played > 0
    ? ((userStats.wins / userStats.games_played) * 100).toFixed(1)
    : 'N/A'

  const RANK_TIERS = [
    [0,   '🪨 Unranked'], [5,   '🥉 Bronze'],  [15,  '🥈 Silver'],
    [30,  '🥇 Gold'],     [50,  '💠 Platinum'], [75,  '💎 Diamond'], [100, '👑 Legendary'],
  ]
  const rank = RANK_TIERS.reduce((acc, [t, n]) => userStats.wins >= (t as number) ? n : acc, '🪨 Unranked')

  return NextResponse.json({
    userId:     uid,
    username:   session.user.username,
    wallet,
    bank:       bankBal,
    total:      wallet + bankBal,
    rep,
    invites,
    msgCount,
    lastDaily,
    rank,
    winRate,
    winRank:    winRank || null,
    ptsRank:    ptsRank || null,
    streak:     streak.streak,
    bestStreak: userStats.best_streak,
    stats:      userStats,
    room:       myRoom,
    recentMatches: myMatches,
  })
}
