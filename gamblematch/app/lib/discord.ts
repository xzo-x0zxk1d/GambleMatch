const BASE = "https://discord.com/api/v10";

export async function discordFetch<T>(endpoint: string): Promise<T> {
  const token = process.env.DISCORD_BOT_TOKEN;
  if (!token) throw new Error("DISCORD_BOT_TOKEN is not set");

  const res = await fetch(`${BASE}${endpoint}`, {
    headers: {
      Authorization: `Bot ${token}`,
      "Content-Type": "application/json",
    },
    next: { revalidate: 60 }, // cache 60s on Vercel
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Discord API ${res.status}: ${text}`);
  }

  return res.json() as Promise<T>;
}

export const GUILD_ID        = process.env.DISCORD_GUILD_ID        ?? "";
export const VOUCHES_CHANNEL = process.env.DISCORD_VOUCHES_CHANNEL ?? "";
export const MEDIA_CHANNEL   = process.env.DISCORD_MEDIA_CHANNEL   ?? "";
export const ROOMS_CATEGORY  = process.env.DISCORD_ROOMS_CATEGORY  ?? "";
