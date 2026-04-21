import Navbar from '@/components/Navbar'
import Hero from '@/components/Hero'
import LiveTicker from '@/components/LiveTicker'
import Features from '@/components/Features'
import Leaderboard from '@/components/Leaderboard'
import Rooms from '@/components/Rooms'
import Commands from '@/components/Commands'
import Footer from '@/components/Footer'

export default function Home() {
  return (
    <main className="min-h-screen bg-gm-void relative">
      {/* Ambient background orbs */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden z-0">
        <div className="absolute top-[-200px] left-[-200px] w-[700px] h-[700px] rounded-full opacity-30"
             style={{ background:'radial-gradient(circle, rgba(108,92,231,0.15) 0%, transparent 70%)', filter:'blur(60px)' }} />
        <div className="absolute top-[40%] right-[-150px] w-[500px] h-[500px] rounded-full opacity-20"
             style={{ background:'radial-gradient(circle, rgba(0,229,255,0.1) 0%, transparent 70%)', filter:'blur(60px)' }} />
        <div className="absolute bottom-[-100px] left-[30%] w-[600px] h-[400px] rounded-full opacity-20"
             style={{ background:'radial-gradient(circle, rgba(108,92,231,0.1) 0%, transparent 70%)', filter:'blur(60px)' }} />
      </div>

      <div className="relative z-10">
        <Navbar />
        <Hero />
        <LiveTicker />
        <Features />
        <Leaderboard />
        <Rooms />
        <Commands />

        {/* Final CTA */}
        <section className="py-24 px-6 relative overflow-hidden">
          <div className="absolute inset-0 bg-grid-pattern opacity-10" />
          <div className="relative max-w-3xl mx-auto text-center">
            <h2 className="font-display font-black gradient-text mb-6"
                style={{ fontSize:'clamp(2rem, 5vw, 3.5rem)' }}>
              Ready to Gamble?
            </h2>
            <p className="text-white/50 text-lg mb-10 max-w-xl mx-auto">
              Join thousands of players already grinding, matching, and winning on GambleMatch.
            </p>
            <a
              href="https://discord.gg/smxxKFPHZw"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-3 px-10 py-5 rounded-2xl font-bold text-xl
                         transition-all duration-300 hover:scale-105 hover:-translate-y-1"
              style={{
                background: 'linear-gradient(135deg, #6c5ce7 0%, #5865F2 100%)',
                boxShadow: '0 0 40px rgba(108,92,231,0.6), 0 20px 40px rgba(0,0,0,0.3)',
              }}
            >
              <svg className="w-7 h-7" viewBox="0 0 24 24" fill="currentColor">
                <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057c.002.022.015.043.03.056a19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028 14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03z"/>
              </svg>
              Join the Server — It&apos;s Free
              <span className="text-white/60">→</span>
            </a>
          </div>
        </section>

        <Footer />
      </div>
    </main>
  )
}
