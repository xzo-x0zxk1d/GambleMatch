import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/app/components/Navbar";
import Background from "@/app/components/Background";

export const metadata: Metadata = {
  title: "GambleMatch — Roblox Virtual Item Gambling",
  description:
    "The #1 virtual item gambling server for Roblox. Bet Blox Fruits, MM2 knives, Pet Sim pets and more. Earn gems, climb rooms, and dominate the leaderboard.",
  openGraph: {
    title: "GambleMatch",
    description: "Roblox virtual item gambling. Rooms, gems, shop & more.",
    type: "website",
  },
  icons: { icon: "/favicon.ico" },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Background />
        <div className="layout">
          <Navbar />
          {children}
        </div>
      </body>
    </html>
  );
}
