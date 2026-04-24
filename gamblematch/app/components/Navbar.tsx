"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Zap, ArrowLeft } from "lucide-react";

export default function Navbar() {
  const path = usePathname();
  const isHome = path === "/";

  return (
    <nav className="navbar">
      <Link href="/" className="nav-logo">
        <span className="nav-logo-icon">
          <Zap size={18} />
        </span>
        <span className="nav-logo-text">
          Gamble<span className="accent">Match</span>
        </span>
      </Link>

      {!isHome && (
        <Link href="/" className="nav-back">
          <ArrowLeft size={15} />
          Back
        </Link>
      )}
    </nav>
  );
}
