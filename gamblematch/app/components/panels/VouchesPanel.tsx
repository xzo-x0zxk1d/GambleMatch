"use client";

import { useEffect, useState } from "react";
import { CheckCircle2, ArrowRight, Clock } from "lucide-react";
import Avatar from "@/app/components/ui/Avatar";
import Spinner from "@/app/components/ui/Spinner";
import ErrorBox from "@/app/components/ui/ErrorBox";
import EmptyState from "@/app/components/ui/EmptyState";
import { timeAgo, avatarUrl } from "@/app/lib/utils";
import type { Vouch } from "@/types/discord";

function VouchCard({ vouch }: { vouch: Vouch }) {
  const [hovered, setHovered] = useState(false);

  const fromName = vouch.from.global_name ?? vouch.from.username;
  const toName   = vouch.to.global_name   ?? vouch.to.username;

  return (
    <div className="vouch-card">
      <Avatar
        userId={vouch.from.id}
        avatarHash={vouch.from.avatar}
        displayName={fromName}
        size={42}
      />

      <div className="vouch-body">
        <div className="vouch-header">
          <span className="vouch-from">{fromName}</span>
          <ArrowRight size={13} className="vouch-arrow-icon" />
          <span className="vouch-verb">vouched</span>

          <div
            className="vouch-to-wrap"
            onMouseEnter={() => setHovered(true)}
            onMouseLeave={() => setHovered(false)}
          >
            <span className="vouch-to">@{toName}</span>

            {hovered && vouch.to.id && (
              <div className="vouch-tooltip">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={avatarUrl(vouch.to.id, vouch.to.avatar, 80)}
                  alt={toName}
                  width={38}
                  height={38}
                  className="tooltip-avatar"
                  onError={(e) => { (e.target as HTMLImageElement).style.display = "none"; }}
                />
                <div>
                  <p className="tooltip-name">{vouch.to.global_name ?? vouch.to.username}</p>
                  <p className="tooltip-handle">@{vouch.to.username}</p>
                </div>
              </div>
            )}
          </div>

          <span className="vouch-badge">
            <CheckCircle2 size={10} />
            Verified
          </span>
        </div>

        <p className="vouch-reason">&ldquo;{vouch.reason}&rdquo;</p>

        <div className="vouch-foot">
          <Clock size={11} />
          <span>{timeAgo(vouch.timestamp)}</span>
        </div>
      </div>
    </div>
  );
}

export default function VouchesPanel() {
  const [data, setData]   = useState<Vouch[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/vouches")
      .then((r) => r.json())
      .then((d) => {
        if (d.error) throw new Error(d.error);
        setData(d);
      })
      .catch((e: Error) => setError(e.message));
  }, []);

  if (error) return <ErrorBox message={error} />;
  if (!data)  return <Spinner label="Loading vouches…" />;
  if (data.length === 0)
    return <EmptyState Icon={CheckCircle2} title="No vouches yet" subtitle="Be the first to vouch!" />;

  return (
    <div className="vouch-list">
      {data.map((v) => <VouchCard key={v.id} vouch={v} />)}
    </div>
  );
}
