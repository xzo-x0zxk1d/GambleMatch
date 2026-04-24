export interface DiscordUser {
  id: string;
  username: string;
  global_name: string | null;
  avatar: string | null;
  discriminator?: string;
  bot?: boolean;
}

export interface DiscordMember {
  user: DiscordUser;
  nick: string | null;
  avatar: string | null;
  joined_at: string;
  roles: string[];
}

export interface DiscordAttachment {
  id: string;
  url: string;
  proxy_url: string;
  filename: string;
  content_type?: string;
  width?: number;
  height?: number;
  size: number;
}

export interface DiscordEmbed {
  type?: string;
  title?: string;
  description?: string;
  image?: { url: string; proxy_url?: string; width?: number; height?: number };
  thumbnail?: { url: string; proxy_url?: string };
  fields?: { name: string; value: string; inline?: boolean }[];
  footer?: { text: string };
}

export interface DiscordMessage {
  id: string;
  content: string;
  author: DiscordUser;
  timestamp: string;
  attachments: DiscordAttachment[];
  embeds: DiscordEmbed[];
  mentions: DiscordUser[];
}

export interface DiscordChannel {
  id: string;
  name: string;
  type: number;
  parent_id: string | null;
  topic?: string | null;
  position?: number;
}

// ─── App Types ───────────────────────────────────────────────────

export interface Vouch {
  id: string;
  from: DiscordUser;
  to: { id: string | null; username: string; global_name: string | null; avatar: string | null };
  reason: string;
  timestamp: string;
}

export interface MediaItem {
  id: string;
  url: string;
  proxy_url: string;
  author: DiscordUser;
  timestamp: string;
  width?: number;
  height?: number;
}

export type RoomTier =
  | "bronze" | "silver" | "gold" | "platinum"
  | "ruby" | "emerald" | "lithium"
  | "vip" | "vvip" | "vvvip";

export interface Room {
  id: string;
  channelName: string;
  tier: RoomTier;
  ownerName: string;
  luck: string | null;
  guests?: number;
}

export interface RichPlayer {
  id: string;
  username: string;
  globalName: string;
  avatar: string | null;
  balance: number;
  rank: number;
}

export interface ShopItem {
  id: number;
  name: string;
  description: string;
  price: number;
  stock: number;
  emoji?: string;
  game?: string;
}
