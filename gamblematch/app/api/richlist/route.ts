import { NextResponse } from "next/server";
import { discordFetch, GUILD_ID } from "@/app/lib/discord";
import type { DiscordMember } from "@/types/discord";
import type { RichPlayer } from "@/types/discord";

export async function GET() {
  try {
    const members = await discordFetch<DiscordMember[]>(
      `/guilds/${GUILD_ID}/members?limit=1000`
    );

    // Filter out bots, take up to 10
    const human = members
      .filter((m) => !m.user.bot)
      .slice(0, 10);

    // We don't have direct wallet access from Discord API without a database.
    // We surface the member list and assign display-order balance placeholders.
    // In production, replace this with a real DB read (e.g. Supabase / PlanetScale).
    const players: RichPlayer[] = human.map((m, i) => ({
      id: m.user.id,
      username: m.user.username,
      globalName: m.user.global_name ?? m.nick ?? m.user.username,
      avatar: m.user.avatar,
      balance: Math.max(0, 500_000_000 - i * 35_000_000),
      rank: i + 1,
    }));

    return NextResponse.json(players);
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
