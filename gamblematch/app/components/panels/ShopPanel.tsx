"use client";

import { useEffect, useState } from "react";
import { ShoppingBag, Gem, Package, Infinity } from "lucide-react";
import Spinner from "@/app/components/ui/Spinner";
import ErrorBox from "@/app/components/ui/ErrorBox";
import EmptyState from "@/app/components/ui/EmptyState";
import { formatBalance } from "@/app/lib/utils";
import type { ShopItem } from "@/types/discord";

const GAME_COLORS: Record<string, string> = {
  "Blox Fruits": "#f97316",
  "MM2":         "#ef4444",
  "Pet Sim X":   "#a855f7",
  "Robux":       "#3b82f6",
  "SAB":         "#10b981",
  "GAG":         "#ec4899",
  "GambleMatch": "#00e5ff",
};

export default function ShopPanel() {
  const [items, setItems]   = useState<ShopItem[] | null>(null);
  const [error, setError]   = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/shop")
      .then((r) => r.json())
      .then((d) => {
        if (d.error) throw new Error(d.error);
        setItems(d);
      })
      .catch((e: Error) => setError(e.message));
  }, []);

  if (error)  return <ErrorBox message={error} />;
  if (!items) return <Spinner label="Loading shop…" />;
  if (items.length === 0)
    return <EmptyState Icon={ShoppingBag} title="Shop is empty" subtitle="New items coming soon!" />;

  return (
    <div className="shop-grid">
      {items.map((item) => {
        const gameColor = item.game ? (GAME_COLORS[item.game] ?? "#8b949e") : "#8b949e";
        const soldOut   = item.stock === 0;
        const unlimited = item.stock === -1;

        return (
          <div key={item.id} className={`shop-card ${soldOut ? "shop-card-out" : ""}`}>
            {/* Game tag */}
            {item.game && (
              <div className="shop-game-tag" style={{ color: gameColor, borderColor: gameColor }}>
                {item.game}
              </div>
            )}

            {/* Icon area */}
            <div className="shop-icon-area">
              <span className="shop-emoji">{item.emoji ?? "🎮"}</span>
            </div>

            <div className="shop-body">
              <h3 className="shop-name">{item.name}</h3>
              <p className="shop-desc">{item.description}</p>

              <div className="shop-footer">
                <span className="shop-price">
                  <Gem size={13} className="gem-icon" />
                  {formatBalance(item.price)}
                </span>

                {soldOut ? (
                  <span className="shop-stock shop-stock-out">Sold Out</span>
                ) : unlimited ? (
                  <span className="shop-stock shop-stock-inf">
                    <Infinity size={11} /> Unlimited
                  </span>
                ) : (
                  <span className="shop-stock">
                    <Package size={11} />
                    {item.stock} left
                  </span>
                )}
              </div>
            </div>

            {soldOut && <div className="shop-soldout-overlay" />}
          </div>
        );
      })}
    </div>
  );
}
