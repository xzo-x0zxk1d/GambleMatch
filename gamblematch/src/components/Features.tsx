import { FEATURES } from '@/lib/data'

export default function Features() {
  return (
    <section id="features" className="relative py-24 px-6 overflow-hidden">
      {/* BG accent */}
      <div className="absolute inset-0 bg-grid-pattern opacity-10" />
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-gm-purple/40 to-transparent" />
      <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-gm-purple/40 to-transparent" />

      <div className="relative max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 text-gm-violet text-sm font-medium mb-4
                          px-4 py-1.5 rounded-full border border-gm-purple/30 bg-gm-surface/40">
            ⚡ Everything You Need
          </div>
          <h2 className="font-display font-black gradient-text mb-4"
              style={{ fontSize:'clamp(2rem, 5vw, 3.5rem)' }}>
            Features
          </h2>
          <p className="text-white/50 max-w-xl mx-auto text-lg">
            Built for serious gamblers. Every system designed to be fair, fast, and addictive.
          </p>
        </div>

        {/* Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {FEATURES.map((f, i) => (
            <div
              key={i}
              className="group glass-card p-6 hover:border-gm-purple/60 transition-all duration-300
                         hover:-translate-y-2 cursor-default"
              style={{ animationDelay:`${i * 0.08}s` }}
            >
              <div className="text-4xl mb-4 group-hover:scale-110 transition-transform duration-300 inline-block">
                {f.icon}
              </div>
              <h3 className="font-display font-bold text-white mb-2 text-sm tracking-wide">
                {f.title}
              </h3>
              <p className="text-white/50 text-sm leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
