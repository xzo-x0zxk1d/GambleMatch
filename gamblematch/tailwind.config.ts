import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      fontFamily: {
        display: ['var(--font-display)', 'monospace'],
        body: ['var(--font-body)', 'sans-serif'],
      },
      colors: {
        gm: {
          void:    '#02020a',
          deep:    '#07071a',
          surface: '#0d0d28',
          card:    '#111130',
          border:  '#1e1e4a',
          purple:  '#6c5ce7',
          violet:  '#a594ff',
          cyan:    '#00e5ff',
          gold:    '#ffd700',
          emerald: '#00e676',
          ruby:    '#ff1744',
          amber:   '#ff9100',
        },
      },
      animation: {
        'pulse-slow':   'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float':        'float 6s ease-in-out infinite',
        'float-delay':  'float 6s ease-in-out 2s infinite',
        'glow-pulse':   'glowPulse 3s ease-in-out infinite',
        'scan-line':    'scanLine 8s linear infinite',
        'counter':      'counterUp 0.4s ease-out forwards',
        'slide-in-up':  'slideInUp 0.6s ease-out forwards',
        'fade-in':      'fadeIn 0.5s ease-out forwards',
        'gradient-x':   'gradientX 6s ease infinite',
        'glitch':       'glitch 4s infinite',
        'ticker':       'ticker 30s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%':      { transform: 'translateY(-20px)' },
        },
        glowPulse: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(108,92,231,0.4)' },
          '50%':      { boxShadow: '0 0 60px rgba(108,92,231,0.8), 0 0 100px rgba(108,92,231,0.3)' },
        },
        scanLine: {
          '0%':   { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100vh)' },
        },
        slideInUp: {
          from: { opacity: '0', transform: 'translateY(40px)' },
          to:   { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          from: { opacity: '0' },
          to:   { opacity: '1' },
        },
        gradientX: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%':      { backgroundPosition: '100% 50%' },
        },
        glitch: {
          '0%, 92%, 100%': { textShadow: '0 0 6px #6c5ce7' },
          '93%': { textShadow: '-3px 0 #ff1744, 3px 0 #00e5ff', transform: 'skew(3deg)' },
          '94%': { textShadow: '3px 0 #ff1744, -3px 0 #00e5ff', transform: 'skew(-3deg)' },
          '95%': { textShadow: '0 0 6px #6c5ce7', transform: 'skew(0deg)' },
        },
        counterUp: {
          from: { opacity: '0', transform: 'translateY(10px)' },
          to:   { opacity: '1', transform: 'translateY(0)' },
        },
        ticker: {
          '0%':   { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-50%)' },
        },
      },
      backgroundImage: {
        'grid-pattern': "url(\"data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32' width='32' height='32' fill='none' stroke='%231e1e4a' stroke-opacity='0.5'%3e%3cpath d='M0 .5H31.5V32'/%3e%3c/svg%3e\")",
      },
    },
  },
  plugins: [],
}
export default config
