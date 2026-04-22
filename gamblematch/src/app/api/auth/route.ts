import { NextRequest, NextResponse } from 'next/server'
import { getIronSession } from 'iron-session'
import { sessionOptions, type SessionData } from '@/lib/session'
import { cookies } from 'next/headers'
import fs from 'fs'
import path from 'path'

interface LoginCode {
  userId: string
  username: string
  code: string
  expiresAt: number
}

function getLoginCodes(): Record<string, LoginCode> {
  try {
    const dataPath = process.env.DATA_PATH || path.join(process.cwd(), '..', 'data')
    const filePath = path.join(dataPath, 'login_codes.json')
    if (!fs.existsSync(filePath)) return {}
    return JSON.parse(fs.readFileSync(filePath, 'utf-8'))
  } catch {
    return {}
  }
}

function deleteLoginCode(userId: string) {
  try {
    const dataPath = process.env.DATA_PATH || path.join(process.cwd(), '..', 'data')
    const filePath = path.join(dataPath, 'login_codes.json')
    if (!fs.existsSync(filePath)) return
    const codes = JSON.parse(fs.readFileSync(filePath, 'utf-8')) as Record<string, LoginCode>
    delete codes[userId]
    fs.writeFileSync(filePath, JSON.stringify(codes, null, 2))
  } catch {
    // ignore
  }
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json()
    const { userId, code } = body as { userId: string; code: string }

    if (!userId || !code) {
      return NextResponse.json({ error: 'Missing userId or code' }, { status: 400 })
    }

    const codes = getLoginCodes()
    const entry = codes[userId]

    if (!entry) {
      return NextResponse.json({ error: 'No code found. Use /login in Discord first.' }, { status: 401 })
    }

    if (Date.now() > entry.expiresAt) {
      deleteLoginCode(userId)
      return NextResponse.json({ error: 'Code expired. Use /login in Discord again.' }, { status: 401 })
    }

    if (entry.code !== code.trim().toUpperCase()) {
      return NextResponse.json({ error: 'Invalid code.' }, { status: 401 })
    }

    // Code valid — create session with explicit type
    const session = await getIronSession<{ user?: SessionData }>(cookies(), sessionOptions)
    session.user = {
      userId:   entry.userId,
      username: entry.username,
      loggedIn: true,
    }
    await session.save()

    deleteLoginCode(userId)

    return NextResponse.json({ success: true, username: entry.username })
  } catch (err) {
    console.error('Auth error:', err)
    return NextResponse.json({ error: 'Server error' }, { status: 500 })
  }
}
