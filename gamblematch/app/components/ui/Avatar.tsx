"use client";

import Image from "next/image";
import { useState } from "react";
import { avatarUrl } from "@/app/lib/utils";

interface AvatarProps {
  userId: string;
  avatarHash?: string | null;
  displayName?: string;
  size?: number;
  className?: string;
}

export default function Avatar({
  userId,
  avatarHash,
  displayName = "?",
  size = 44,
  className = "",
}: AvatarProps) {
  const [error, setError] = useState(false);
  const url = avatarUrl(userId, avatarHash, size * 2);
  const letter = displayName.charAt(0).toUpperCase();

  if (error) {
    return (
      <div
        className={`avatar-fallback ${className}`}
        style={{ width: size, height: size, fontSize: size * 0.38 }}
        aria-label={displayName}
      >
        {letter}
      </div>
    );
  }

  return (
    <Image
      src={url}
      alt={displayName}
      width={size}
      height={size}
      className={`avatar-img ${className}`}
      style={{ width: size, height: size }}
      onError={() => setError(true)}
      unoptimized
    />
  );
}
