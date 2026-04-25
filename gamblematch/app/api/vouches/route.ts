import { NextResponse } from "next/server";
import { discordFetch, VOUCHES_CHANNEL } from "@/app/lib/discord";
import type { DiscordMessage, DiscordUser } from "@/types/discord";
import type { Vouch } from "@/types/discord";

function parseVouch(msg: DiscordMessage): Vouch | null {
  const content = (msg.content ?? "").trim();
  if (!content.toLowerCase().startsWith("vouch")) return null;

  // Pattern: vouch <@!id> reason  OR  vouch @username reason  OR  vouch username reason
  const mentionMatch = content.match(/vouch\s+<@!?(\d+)>\s*([\s\S]*)/i);
  const textMatch    = content.match(/vouch\s+(\S+)\s*([\s\S]*)/i);

  const from: DiscordUser = msg.author;

  if (mentionMatch) {
    const targetId = mentionMatch[1];
    const reason   = mentionMatch[2]?.trim() || "Great trade!";
    const mentioned = msg.mentions?.find((m) => m.id === targetId);
    return {
      id: msg.id,
      from,
      to: {
        id: targetId,
        username: mentioned?.username ?? `User#${targetId.slice(-4)}`,
        global_name: mentioned?.global_name ?? null,
        avatar: mentioned?.avatar ?? null,
      },
      reason,
      timestamp: msg.timestamp,
    };
  }

  if (textMatch) {
    const raw    = textMatch[1];
    const reason = textMatch[2]?.trim() || "Great trade!";
    // Skip if it looks like a command word
    if (["channel", "here", "everyone"].includes(raw.toLowerCase())) return null;
    return {
      id: msg.id,
      from,
      to: { id: null, username: raw.replace(/^@/, ""), global_name: null, avatar: null },
      reason,
      timestamp: msg.timestamp,
    };
  }

  return null;
}

export async function GET() {
  try {
    const messages = await discordFetch<DiscordMessage[]>(
      `/channels/${VOUCHES_CHANNEL}/messages?limit=50`
    );
    const vouches = messages.map(parseVouch).filter(Boolean) as Vouch[];
    return NextResponse.json(vouches);
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
