"use client";

import { useEffect, useState } from "react";
import { Trophy, Gem } from "lucide-react";
import Avatar from "@/app/components/ui/Avatar";
import Spinner from "@/app/components/ui/Spinner";
import ErrorBox from "@/app/components/ui/ErrorBox";
import EmptyState from "@/app/components/ui/EmptyState";
import { formatBalance } from "@/app/lib/utils";
import type { RichPlayer } from "@/types/discord";

const MEDAL_COLORS = ["#FFD700", "#C0C0C0", "#CD7F32"];

export default function RichListPanel() {
  const [players, setPlayers] = useState<RichPlayer[] | null>(null);
  const [error, setError]     = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/richlist")
      .then((r) => r.json())
      .then((d) => {
        if (d.error) throw new Error(d.error);
        setPlayers(d);
      })
      .catch((e: Error) => setError(e.message));
  }, []);

  if (error)   return <ErrorBox message={error} />;
  if (!players) return <Spinner label="Loading rich list…" />;
  if (players.length === 0)
    return <EmptyState Icon={Trophy} title="No players yet" />;

  return (
    <div className="rich-list">
      {players.map((p, i) => {
        const medalColor = MEDAL_COLORS[i] ?? null;
        return (
          <div key={p.id} className="rich-item" style={{ animationDelay: `${i * 40}ms` }}>
            {/* Rank */}
            <div
              className={`rich-rank ${i < 3 ? "rich-rank-top" : ""}`}
              style={medalColor ? { background: medalColor, color: "#000" } : undefined}
            >
              {i < 3 ? <Trophy size={14} /> : <span>#{i + 1}</span>}
            </div>

            {/* Avatar */}
            <Avatar userId={p.id} avatarHash={p.avatar} displayName={p.globalName} size={44} />

            {/* Name */}
            <div className="rich-info">
              <p className="rich-name">{p.globalName}</p>
              {p.globalName !== p.username && (
                <p className="rich-handle">@{p.username}</p>
              )}
            </div>

            {/* Balance */}
            <div className="rich-balance">
              <Gem size={14} className="gem-icon" />
              <span>{formatBalance(p.balance)}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
