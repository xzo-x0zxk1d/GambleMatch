/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'cdn.discordapp.com' },
      { protocol: 'https', hostname: 'i.imgur.com' },
    ],
  },
  // Allow reading the bot's data/ directory from API routes
  experimental: {
    serverComponentsExternalPackages: [],
  },
  webpack: (config, { isServer }) => {
    if (isServer) {
      // Don't bundle fs/path — use Node.js built-ins
      config.externals = [...(config.externals || []), 'fs', 'path']
    }
    return config
  },
}
module.exports = nextConfig
