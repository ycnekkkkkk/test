/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  // Optimize for Railway deployment - reduce memory usage
  swcMinify: true,
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },
  // Reduce memory usage during build
  experimental: {
    optimizeCss: false, // Disable CSS optimization to save memory
  },
  // Disable source maps in production to save memory
  productionBrowserSourceMaps: false,
}

module.exports = nextConfig

