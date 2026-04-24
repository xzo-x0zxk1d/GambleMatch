# GambleMatch Website

Modern Next.js 14 website for the GambleMatch Discord server — Roblox virtual item gambling.

## Stack

- **Next.js 14** (App Router, TypeScript)
- **Lucide React** — icons
- **Framer Motion** — animations (available, used optionally)
- All Discord data fetched server-side via API routes (token never exposed to browser)

## Project Structure

```
gamblematch/
├── app/
│   ├── api/
│   │   ├── vouches/route.ts     ← Parses vouch messages
│   │   ├── media/route.ts       ← Fetches images from media channel
│   │   ├── rooms/route.ts       ← Lists rooms from category
│   │   ├── richlist/route.ts    ← Guild members leaderboard
│   │   └── shop/route.ts        ← Shop items (edit to add real data)
│   ├── components/
│   │   ├── ui/
│   │   │   ├── Avatar.tsx
│   │   │   ├── Spinner.tsx
│   │   │   ├── ErrorBox.tsx
│   │   │   └── EmptyState.tsx
│   │   ├── panels/
│   │   │   ├── VouchesPanel.tsx
│   │   │   ├── MediaPanel.tsx
│   │   │   ├── RoomsPanel.tsx
│   │   │   ├── RichListPanel.tsx
│   │   │   └── ShopPanel.tsx
│   │   ├── Background.tsx
│   │   ├── Modal.tsx
│   │   └── Navbar.tsx
│   ├── explore/page.tsx         ← /explore route
│   ├── lib/
│   │   ├── discord.ts           ← Server-side Discord fetcher
│   │   └── utils.ts             ← Shared helpers
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx                 ← Home / landing
├── types/
│   └── discord.ts               ← Shared TypeScript types
├── .env.example                 ← Copy to .env.local
├── .env.local                   ← ⚠️ NEVER commit this
├── .gitignore
├── next.config.js
├── package.json
└── tsconfig.json
```

## Local Setup

```bash
# 1. Install dependencies
npm install

# 2. Set environment variables
cp .env.example .env.local
# Edit .env.local with your real values

# 3. Run dev server
npm run dev
# → http://localhost:3000
```

## Deploy to Vercel

1. Push to GitHub (`.env.local` is gitignored — safe)
2. Import repo in [vercel.com](https://vercel.com)
3. Add environment variables in Vercel dashboard:
   - `DISCORD_BOT_TOKEN`
   - `DISCORD_GUILD_ID`
   - `DISCORD_VOUCHES_CHANNEL`
   - `DISCORD_MEDIA_CHANNEL`
   - `DISCORD_ROOMS_CATEGORY`
4. Deploy — Vercel auto-detects Next.js

## Environment Variables

| Variable | Value |
|---|---|
| `DISCORD_BOT_TOKEN` | Your bot token |
| `DISCORD_GUILD_ID` | `1492847247124070520` |
| `DISCORD_VOUCHES_CHANNEL` | `1492978086969344010` |
| `DISCORD_MEDIA_CHANNEL` | `1492865536957223083` |
| `DISCORD_ROOMS_CATEGORY` | `1494678509266665503` |

## Syncing Real Shop Data

The shop (`app/api/shop/route.ts`) uses a hardcoded default list.  
To sync with live bot data, add a `POST /api/shop` endpoint that:
1. Accepts a signed request from the bot after `/additem` or `/removeitem`
2. Saves to a database (Supabase, PlanetScale, Upstash, etc.)
3. The `GET` handler reads from that database instead

## Rich List

The `/api/richlist` route returns guild members with placeholder balances.  
To show real balances, read from the bot's `data/points.json` (e.g. via a shared database or a bot endpoint).
