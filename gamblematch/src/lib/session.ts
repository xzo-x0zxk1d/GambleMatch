import type { SessionOptions } from 'iron-session'

export interface SessionData {
  userId: string
  username: string
  loggedIn: boolean
}

export const sessionOptions: SessionOptions = {
  password: process.env.SESSION_SECRET || 'gamblematch-super-secret-key-change-in-production-32chars',
  cookieName: 'gm_session',
  cookieOptions: {
    secure: process.env.NODE_ENV === 'production',
    maxAge: 60 * 60 * 24 * 7,
  },
}
