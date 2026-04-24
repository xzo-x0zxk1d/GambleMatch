"use client";

import { useEffect, useState } from "react";
import { Home, Star, Users } from "lucide-react";
import Spinner from "@/app/components/ui/Spinner";
import ErrorBox from "@/app/components/ui/ErrorBox";
import EmptyState from "@/app/components/ui/EmptyState";
import { TIER_META } from "@/app/lib/utils";
import type { Room } from "@/types/discord";

const TIER_ICONS: Record<string, string> = {
  bronze:   "🥉", silver: "🥈", gold:    "🥇",
  platinum: "💠", ruby:   "💎", emerald: "💚",
  lithium:  "⚡", vip:    "👑", vvip:    "👑",  vvvip: "🌟",
};

export default function RoomsPanel() {
  const [rooms, setRooms]   = useState<Room[] | null>(null);
  const [error, setError]   = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/rooms")
      .then((r) => r.json())
      .then((d) => {
        if (d.error) throw new Error(d.error);
        setRooms(d);
      })
      .catch((e: Error) => setError(e.message));
  }, []);

  if (error)  return <ErrorBox message={error} />;
  if (!rooms) return <Spinner label="Loading rooms…" />;
  if (rooms.length === 0)
    return <EmptyState Icon={Home} title="No active rooms" subtitle="Register a room in Discord!" />;

  return (
    <div className="rooms-list">
      {rooms.map((room) => {
        const meta  = TIER_META[room.tier] ?? TIER_META.bronze;
        const icon  = TIER_ICONS[room.tier] ?? "🏠";

        return (
          <div
            key={room.id}
            className="room-card"
            style={{ "--tier-color": meta.color, "--tier-glow": meta.glow } as React.CSSProperties}
          >
            <div className="room-tier-badge" style={{ color: meta.color, borderColor: meta.color }}>
              <span className="room-tier-icon">{icon}</span>
              <span>{meta.label}</span>
            </div>

            <div className="room-info">
              <p className="room-channel">#{room.channelName}</p>
              <div className="room-meta">
                <span className="room-meta-item">
                  <Users size={12} />
                  {room.ownerName}
                </span>
                {room.luck && (
                  <span className="room-luck">
                    <Star size={11} />
                    {room.luck} luck
                  </span>
                )}
              </div>
            </div>

            <div className="room-glow-dot" style={{ background: meta.color, boxShadow: `0 0 10px ${meta.glow}` }} />
          </div>
        );
      })}
    </div>
  );
}
