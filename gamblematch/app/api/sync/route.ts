import { NextRequest, NextResponse } from "next/server";
import store, { type ShopItem, type RichPlayer } from "@/app/lib/store";

// POST /api/sync  — called by the Discord bot every 60 seconds
export async function POST(req: NextRequest) {
  const secret = req.headers.get("x-sync-secret");
  if (!secret || secret !== process.env.SYNC_SECRET) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  let body: { shop?: ShopItem[]; richlist?: RichPlayer[] };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON" }, { status: 400 });
  }

  if (Array.isArray(body.shop))     store.shop     = body.shop;
  if (Array.isArray(body.richlist)) store.richlist = body.richlist;
  store.lastSync = new Date().toISOString();

  return NextResponse.json({
    ok: true,
    synced: store.lastSync,
    shopCount: store.shop.length,
    richlistCount: store.richlist.length,
  });
}

// GET /api/sync  — health check / status
export async function GET() {
  return NextResponse.json({
    lastSync: store.lastSync,
    shopCount: store.shop.length,
    richlistCount: store.richlist.length,
  });
}
