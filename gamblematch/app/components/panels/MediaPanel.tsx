"use client";

import { useEffect, useState } from "react";
import { ImageIcon, X, ZoomIn } from "lucide-react";
import Spinner from "@/app/components/ui/Spinner";
import ErrorBox from "@/app/components/ui/ErrorBox";
import EmptyState from "@/app/components/ui/EmptyState";
import { avatarUrl } from "@/app/lib/utils";
import type { MediaItem } from "@/types/discord";

function Lightbox({ item, onClose }: { item: MediaItem; onClose: () => void }) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div className="lightbox" onClick={onClose} role="dialog" aria-modal>
      <button className="lightbox-close" onClick={onClose} aria-label="Close">
        <X size={18} />
      </button>
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={item.url}
        alt="Media"
        className="lightbox-img"
        onClick={(e) => e.stopPropagation()}
      />
      <div className="lightbox-meta" onClick={(e) => e.stopPropagation()}>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={avatarUrl(item.author.id, item.author.avatar, 48)}
          alt={item.author.username}
          width={24}
          height={24}
          className="lb-avatar"
        />
        <span>{item.author.global_name ?? item.author.username}</span>
      </div>
    </div>
  );
}

export default function MediaPanel() {
  const [items, setItems]       = useState<MediaItem[] | null>(null);
  const [error, setError]       = useState<string | null>(null);
  const [active, setActive]     = useState<MediaItem | null>(null);

  useEffect(() => {
    fetch("/api/media")
      .then((r) => r.json())
      .then((d) => {
        if (d.error) throw new Error(d.error);
        setItems(d);
      })
      .catch((e: Error) => setError(e.message));
  }, []);

  if (error)  return <ErrorBox message={error} />;
  if (!items) return <Spinner label="Loading gallery…" />;
  if (items.length === 0)
    return <EmptyState Icon={ImageIcon} title="No images yet" subtitle="Share something in #media!" />;

  return (
    <>
      <div className="media-grid">
        {items.map((item) => (
          <div
            key={item.id}
            className="media-cell"
            onClick={() => setActive(item)}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => e.key === "Enter" && setActive(item)}
          >
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={item.proxy_url} alt="Media" className="media-thumb" loading="lazy" />
            <div className="media-overlay">
              <ZoomIn size={20} />
            </div>
            <div className="media-info">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={avatarUrl(item.author.id, item.author.avatar, 48)}
                alt=""
                width={20}
                height={20}
                className="media-author-avatar"
                onError={(e) => { (e.target as HTMLImageElement).style.display = "none"; }}
              />
              <span className="media-author-name">
                {item.author.global_name ?? item.author.username}
              </span>
            </div>
          </div>
        ))}
      </div>

      {active && <Lightbox item={active} onClose={() => setActive(null)} />}
    </>
  );
}
