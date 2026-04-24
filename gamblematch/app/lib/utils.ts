export function formatBalance(n: number): string {
  if (n >= 1e9) return (n / 1e9).toFixed(1) + "B";
  if (n >= 1e6) return (n / 1e6).toFixed(1) + "M";
  if (n >= 1e3) return (n / 1e3).toFixed(1) + "K";
  return n.toLocaleString();
}

export function timeAgo(timestamp: string): string {
  const diff = Date.now() - new Date(timestamp).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  if (days < 7) return `${days}d ago`;
  return new Date(timestamp).toLocaleDateString();
}

export function avatarUrl(
  userId: string,
  avatarHash: string | null | undefined,
  size: number = 64
): string {
  if (!avatarHash) {
    // Avoid BigInt — just use last few digits of userId mod 6
    const defaultIndex = Number(userId.slice(-4)) % 6;
    return `https://cdn.discordapp.com/embed/avatars/${defaultIndex}.png`;
  }
  const ext = avatarHash.startsWith("a_") ? "gif" : "png";
  return `https://cdn.discordapp.com/avatars/${userId}/${avatarHash}.${ext}?size=${size}`;
}

export type RoomTier =
  | "bronze" | "silver" | "gold" | "platinum"
  | "ruby" | "emerald" | "lithium"
  | "vip" | "vvip" | "vvvip";

export const TIER_ORDER: Record<string, number> = {
  lithium: 7, vvvip: 7,
  emerald: 6, vvip: 6,
  ruby: 5, vip: 5,
  platinum: 4,
  gold: 3,
  silver: 2,
  bronze: 1,
};

export const TIER_META: Record<string, { label: string; color: string; glow: string }> = {
  bronze:   { label: "Bronze",   color: "#cd7f32", glow: "rgba(205,127,50,0.4)" },
  silver:   { label: "Silver",   color: "#c0c0c0", glow: "rgba(192,192,192,0.4)" },
  gold:     { label: "Gold",     color: "#ffd700", glow: "rgba(255,215,0,0.4)" },
  platinum: { label: "Platinum", color: "#00bcd4", glow: "rgba(0,188,212,0.4)" },
  ruby:     { label: "Ruby",     color: "#ef5350", glow: "rgba(239,83,80,0.4)" },
  emerald:  { label: "Emerald",  color: "#66bb6a", glow: "rgba(102,187,106,0.4)" },
  lithium:  { label: "Lithium",  color: "#ab47bc", glow: "rgba(171,71,188,0.4)" },
  vip:      { label: "VIP",      color: "#ef5350", glow: "rgba(239,83,80,0.4)" },
  vvip:     { label: "VVIP",     color: "#66bb6a", glow: "rgba(102,187,106,0.4)" },
  vvvip:    { label: "VVVIP",    color: "#ab47bc", glow: "rgba(171,71,188,0.4)" },
};
