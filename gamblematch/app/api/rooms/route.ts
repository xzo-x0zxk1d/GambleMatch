import { NextResponse } from "next/server";
import { discordFetch, GUILD_ID, ROOMS_CATEGORY } from "@/app/lib/discord";
import type { DiscordChannel } from "@/types/discord";
import type { Room, RoomTier } from "@/types/discord";
import { TIER_ORDER } from "@/app/lib/utils";

const KNOWN_TIERS: RoomTier[] = [
  "lithium","emerald","ruby","platinum","gold","silver","bronze",
  "vvvip","vvip","vip",
];

function extractTier(channelName: string): RoomTier {
  const lower = channelName.toLowerCase();
  for (const t of KNOWN_TIERS) {
    if (lower.startsWith(t) || lower.includes(`-${t}`) || lower.includes(`${t}-`)) {
      return t;
    }
  }
  return "bronze";
}

export async function GET() {
  try {
    const channels = await discordFetch<DiscordChannel[]>(
      `/guilds/${GUILD_ID}/channels`
    );

    const roomChannels = channels.filter(
      (c) => c.type === 0 && String(c.parent_id) === ROOMS_CATEGORY
    );

    const rooms: Room[] = roomChannels.map((ch) => {
      const tier = extractTier(ch.name ?? "");

      // Parse topic: "Tier Label · Owner: DisplayName · Luck: 2.5×"
      const topic    = ch.topic ?? "";
      const luckMatch = topic.match(/Luck:\s*([\d.]+)/i) || topic.match(/([\d.]+)[×x]/);
      const ownerMatch = topic.match(/Owner:\s*([^·|]+)/i);

      // Fallback owner from channel name: "gold-ownername" → "ownername"
      const nameParts = (ch.name ?? "").split("-");
      const fallbackOwner = nameParts
        .slice(1)
        .map((s) => s.charAt(0).toUpperCase() + s.slice(1))
        .join(" ")
        .trim() || "Unknown";

      return {
        id: ch.id,
        channelName: ch.name ?? "",
        tier,
        ownerName: ownerMatch ? ownerMatch[1].trim() : fallbackOwner,
        luck: luckMatch ? `${luckMatch[1]}×` : null,
        guests: 0,
      };
    });

    // Sort: highest tier first
    rooms.sort(
      (a, b) => (TIER_ORDER[b.tier] ?? 0) - (TIER_ORDER[a.tier] ?? 0)
    );

    return NextResponse.json(rooms);
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
