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
    <html lang="en" className="bg-[#070A14] text-slate-100 antialiased">
      <body className="min-h-screen bg-[#070A14] text-slate-100 selection:bg-amber-400 selection:text-slate-950 font-sans">
        {children}
      </body>
    </html>
  )
}
