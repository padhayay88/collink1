/** @type {import('next').NextConfig} */
const nextConfig = {
  // Use a custom build directory to avoid OneDrive/.next placeholder issues
  distDir: '.next-dev',
  reactStrictMode: true,
  swcMinify: true,
  // Reduce cache corruption issues on OneDrive/Windows by disabling
  // Webpack's filesystem cache during development.
  webpack: (config, { dev }) => {
    if (dev) {
      config.cache = false
    }
    return config
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL
          ? `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`
          : 'http://localhost:8000/api/:path*',
      },
    ]
  },
}

module.exports = nextConfig 