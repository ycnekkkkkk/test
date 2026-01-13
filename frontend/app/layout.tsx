import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'IELTS Test',
  description: 'AI-powered IELTS assessment test',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="vi">
      <body className={inter.className}>
        <nav className="bg-white shadow-sm mb-4">
          <div className="container mx-auto px-4 py-3">
            <div className="flex justify-between items-center">
              <h1 className="text-xl font-bold text-blue-600">IELTS Test</h1>
            </div>
          </div>
        </nav>
        <main className="container mx-auto px-4 py-8">
          {children}
        </main>
        <footer className="bg-gray-100 mt-12 py-6">
          <div className="container mx-auto px-4 text-center text-gray-600">
            <p>&copy; 2024 IELTS Test. All rights reserved.</p>
          </div>
        </footer>
      </body>
    </html>
  )
}

