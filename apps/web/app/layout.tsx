import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Astrovision - Know Your Stars • Shape Your Tomorrow',
  description: 'Deterministic, explainable astrology computation and prediction platform.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="bg-[#050816]">
      <body className="text-ivory min-h-screen relative overflow-x-hidden">
        {/* Full-Screen Immersive Celestial Horizon Background */}
        <div
          style={{
            position: 'fixed',
            inset: 0,
            zIndex: -1,
            pointerEvents: 'none',
            background: 'linear-gradient(to bottom, #17163A 0%, #0B1026 50%, #050816 100%)'
          }}
        >
          {/* Glowing Planets across Horizon */}
          <div className="absolute top-12 inset-x-0 flex justify-around items-center opacity-80 px-16">
            <div className="w-12 h-12 rounded-full bg-blue-400/80 shadow-[0_0_30px_rgba(96,165,250,0.9)]"></div>
            <div className="w-16 h-16 rounded-full bg-amber-500/90 shadow-[0_0_40px_rgba(245,158,11,0.9)]"></div>
            <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-amber-600 to-amber-300 shadow-[0_0_60px_rgba(245,158,11,1)] ring-2 ring-champagne/60"></div>
            <div className="w-14 h-14 rounded-full bg-rose-400/80 shadow-[0_0_35px_rgba(251,113,133,0.9)]"></div>
          </div>

          {/* Giant Zodiac Astrolabe Wheel in Sky */}
          <div className="absolute top-10 left-1/2 -translate-x-1/2 w-[700px] h-[700px] rounded-full border-2 border-champagne/30 flex items-center justify-center opacity-30 animate-spin" style={{ animationDuration: '200s' }}>
            <div className="absolute inset-12 rounded-full border border-champagne/20 border-dashed"></div>
            <div className="absolute inset-24 rounded-full border border-champagne/40"></div>
            <span className="text-champagne text-5xl">♓ ♈ ♉ ♊ ♋ ♌ ♍ ♎ ♏ ♐ ♑ ♒</span>
          </div>

          {/* Cosmic Horizon Water Gradient */}
          <div className="absolute bottom-0 inset-x-0 h-64 bg-gradient-to-t from-[#050816] via-[#080D1F]/90 to-transparent"></div>
        </div>

        {children}
      </body>
    </html>
  )
}
