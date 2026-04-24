"use client";

import { useState, type ReactNode } from "react";
import {
  CheckCircle2, ImageIcon, Home,
  Trophy, ShoppingBag, ArrowUpRight,
} from "lucide-react";
import Modal from "@/app/components/Modal";
import VouchesPanel  from "@/app/components/panels/VouchesPanel";
import MediaPanel    from "@/app/components/panels/MediaPanel";
import RoomsPanel    from "@/app/components/panels/RoomsPanel";
import RichListPanel from "@/app/components/panels/RichListPanel";
import ShopPanel     from "@/app/components/panels/ShopPanel";

type PanelId = "vouches" | "media" | "rooms" | "rich" | "shop";

interface Card {
  id: PanelId;
  Icon: React.FC<{ size?: number; className?: string }>;
  title: string;
  desc: string;
  color: string;
  glow: string;
}

const CARDS: Card[] = [
  {
    id: "vouches",
    Icon: CheckCircle2,
    title: "Vouches",
    desc: "See who vouched for who and their reasons. Real trades verified by the community.",
    color: "#3fb950",
    glow: "rgba(63,185,80,0.25)",
  },
  {
    id: "media",
    Icon: ImageIcon,
    title: "Media Gallery",
    desc: "Browse images and clips shared by members in the community media channel.",
    color: "#58a6ff",
    glow: "rgba(88,166,255,0.25)",
  },
  {
    id: "rooms",
    Icon: Home,
    title: "Active Rooms",
    desc: "All current gambling rooms ranked by tier — from Bronze all the way to Lithium.",
    color: "#ab47bc",
    glow: "rgba(171,71,188,0.25)",
  },
  {
    id: "rich",
    Icon: Trophy,
    title: "Rich List",
    desc: "The wealthiest players ranked by their total GambleGem balance. Who reigns?",
    color: "#ffd700",
    glow: "rgba(255,215,0,0.25)",
  },
  {
    id: "shop",
    Icon: ShoppingBag,
    title: "Shop",
    desc: "All items available right now in the points shop — prices, stock, and game tags.",
    color: "#00e5ff",
    glow: "rgba(0,229,255,0.25)",
  },
];

const PANEL_MAP: Record<PanelId, ReactNode> = {
  vouches: <VouchesPanel />,
  media:   <MediaPanel />,
  rooms:   <RoomsPanel />,
  rich:    <RichListPanel />,
  shop:    <ShopPanel />,
};

const PANEL_TITLE: Record<PanelId, ReactNode> = {
  vouches: <><CheckCircle2 size={18} /> Vouches</>,
  media:   <><ImageIcon    size={18} /> Media Gallery</>,
  rooms:   <><Home         size={18} /> Active Rooms</>,
  rich:    <><Trophy       size={18} /> Rich List</>,
  shop:    <><ShoppingBag  size={18} /> Shop Items</>,
};

export default function ExplorePage() {
  const [active, setActive] = useState<PanelId | null>(null);

  return (
    <main className="explore">
      <div className="explore-header">
        <h1 className="explore-title">
          Explore <span className="accent">GambleMatch</span>
        </h1>
        <p className="explore-sub">
          Dive into the community — vouches, media, rooms, leaderboards and the shop.
        </p>
      </div>

      <div className="explore-grid">
        {CARDS.map((card, i) => (
          <button
            key={card.id}
            className="explore-card"
            style={{
              "--card-color": card.color,
              "--card-glow": card.glow,
              animationDelay: `${i * 70}ms`,
            } as React.CSSProperties}
            onClick={() => setActive(card.id)}
          >
            <div className="explore-card-icon" style={{ color: card.color }}>
              <card.Icon size={24} />
            </div>
            <div className="explore-card-body">
              <h2 className="explore-card-title">{card.title}</h2>
              <p className="explore-card-desc">{card.desc}</p>
            </div>
            <ArrowUpRight size={16} className="explore-card-arrow" />
            <div className="explore-card-shine" />
          </button>
        ))}
      </div>

      {active && (
        <Modal title={PANEL_TITLE[active]} onClose={() => setActive(null)}>
          {PANEL_MAP[active]}
        </Modal>
      )}
    </main>
  );
}
