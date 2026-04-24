import Link from "next/link";
import { Zap, ArrowRight, Sword, Star, Users, ShoppingBag, ChevronRight } from "lucide-react";

const FEATURES = [
  {
    icon: <Sword size={20} />,
    title: "Virtual Item Battles",
    desc: "Wager Blox Fruits, MM2 knives, Pet Sim pets and more in head-to-head duels.",
  },
  {
    icon: <Star size={20} />,
    title: "Tiered Room System",
    desc: "7 tiers from Bronze to Lithium. Higher tier = higher luck multiplier on all games.",
  },
  {
    icon: <Users size={20} />,
    title: "Invite & Earn",
    desc: "Invite friends to earn permanent luck bonuses and 5,000 gems per invite.",
  },
  {
    icon: <ShoppingBag size={20} />,
    title: "Gem Marketplace",
    desc: "Spend earned gems on rare items, robux bundles, and luck boosts.",
  },
];

const STATS = [
  { value: "7", label: "Room Tiers" },
  { value: "6+", label: "Game Modes" },
  { value: "50B", label: "Max Gems" },
  { value: "24/7", label: "Active" },
];

export default function Home() {
  return (
    <main className="home">
      {/* ── Hero ─────────────────────────────────────────── */}
      <section className="hero">
        <div className="hero-badge">
          <span className="badge-dot" />
          Live · Roblox Virtual Items
        </div>

        <h1 className="hero-title">
          <span className="title-line">Gamble.</span>
          <span className="title-line title-outline">Win.</span>
          <span className="title-line title-glow">Dominate.</span>
        </h1>

        <p className="hero-sub">
          The #1 virtual item gambling server for Roblox. Bet your rarest
          items, climb rooms, earn gems, and flex your wealth.
        </p>

        <div className="hero-actions">
          <a
            href="https://discord.gg/bUc6Vu4z8P"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-primary"
          >
            <Zap size={17} />
            Get Started
          </a>
          <Link href="/explore" className="btn-secondary">
            Learn More
            <ArrowRight size={16} />
          </Link>
        </div>

        {/* Stats strip */}
        <div className="stats-strip">
          {STATS.map((s) => (
            <div key={s.label} className="stat-item">
              <span className="stat-value">{s.value}</span>
              <span className="stat-label">{s.label}</span>
            </div>
          ))}
        </div>
      </section>

      {/* ── Features ─────────────────────────────────────── */}
      <section className="features">
        <h2 className="section-title">Why GambleMatch?</h2>
        <div className="features-grid">
          {FEATURES.map((f, i) => (
            <div key={f.title} className="feature-card" style={{ animationDelay: `${i * 80}ms` }}>
              <div className="feature-icon">{f.icon}</div>
              <h3 className="feature-title">{f.title}</h3>
              <p className="feature-desc">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── CTA ──────────────────────────────────────────── */}
      <section className="cta-section">
        <div className="cta-card">
          <h2 className="cta-title">Ready to play?</h2>
          <p className="cta-sub">Join the server and start gambling in seconds.</p>
          <a
            href="https://discord.gg/bUc6Vu4z8P"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-primary"
          >
            <Zap size={16} />
            Join Discord
            <ChevronRight size={16} />
          </a>
        </div>
      </section>
    </main>
  );
}
