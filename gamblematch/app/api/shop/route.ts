import { NextResponse } from "next/server";
import type { ShopItem } from "@/types/discord";

// ──────────────────────────────────────────────────────────────────
// In production: read from the bot's JSON file (./data/shop.json)
// or from your database. For now this returns a realistic default
// set that mirrors what the bot would hold.
//
// To sync with the real bot data, add a POST /api/shop route that
// accepts signed updates from the bot whenever /additem is used.
// ──────────────────────────────────────────────────────────────────

const DEFAULT_SHOP: ShopItem[] = [
  {
    id: 1,
    name: "Dragon Fruit",
    description: "Legendary Blox Fruits devil fruit. Grants powerful dragon transformation abilities.",
    price: 50_000_000,
    stock: 3,
    emoji: "🐉",
    game: "Blox Fruits",
  },
  {
    id: 2,
    name: "Godly Knife (MM2)",
    description: "Rare godly tier knife from Murder Mystery 2. Highly sought after.",
    price: 25_000_000,
    stock: 5,
    emoji: "🔪",
    game: "MM2",
  },
  {
    id: 3,
    name: "Huge Cat (Pet Sim X)",
    description: "Exclusive huge pet from Pet Simulator X. Massive demand, limited supply.",
    price: 80_000_000,
    stock: 1,
    emoji: "🐱",
    game: "Pet Sim X",
  },
  {
    id: 4,
    name: "Robux Bundle (10K)",
    description: "10,000 Robux delivered via Gamepass. Verify your username in ticket.",
    price: 100_000_000,
    stock: -1,
    emoji: "💎",
    game: "Robux",
  },
  {
    id: 5,
    name: "Soul Guitar",
    description: "Blox Fruits legendary fighting style. Deals massive AoE damage.",
    price: 35_000_000,
    stock: 2,
    emoji: "🎸",
    game: "Blox Fruits",
  },
  {
    id: 6,
    name: "Corrupt Scythe (SAB)",
    description: "Top-tier blade from Super Animal Battle. Perfect condition.",
    price: 15_000_000,
    stock: 7,
    emoji: "⚔️",
    game: "SAB",
  },
  {
    id: 7,
    name: "Luck Multiplier (7 Days)",
    description: "Boosts your luck multiplier by +0.5× for 7 days on all casino games.",
    price: 200_000_000,
    stock: -1,
    emoji: "🍀",
    game: "GambleMatch",
  },
  {
    id: 8,
    name: "Rainbow Halo (GAG)",
    description: "Ultra-rare halo accessory from Grow a Garden. Rainbow edition.",
    price: 60_000_000,
    stock: 0,
    emoji: "🌈",
    game: "GAG",
  },
];

export async function GET() {
  return NextResponse.json(DEFAULT_SHOP);
}
