/**
 * Shared in-memory data store.
 *
 * Next.js re-uses the same Node.js module instance for all route handlers
 * within a single Vercel function invocation, so this singleton persists
 * across requests as long as the function is warm.
 *
 * For true cross-cold-start persistence, swap these arrays for
 * Vercel KV / Upstash Redis reads — the interface stays identical.
 */

export interface ShopItem {
  id: number;
  name: string;
  description: string;
  price: number;
  stock: number;
  emoji?: string;
  game?: string;
  image_url?: string | null;
}

export interface RichPlayer {
  id: string;
  username: string;
  globalName: string;
  avatar: string | null;
  balance: number;
  rank: number;
}

interface Store {
  shop: ShopItem[];
  richlist: RichPlayer[];
  lastSync: string | null;
}

// Module-level singleton — shared across all routes in the same process
const store: Store = {
  shop: [],
  richlist: [],
  lastSync: null,
};

export default store;
