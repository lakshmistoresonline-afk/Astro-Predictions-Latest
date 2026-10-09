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
    <html lang="en" className="bg-[#070D1B] text-[#E8EDF7] antialiased">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;0,900;1,600&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
      </head>
      <body className="min-h-screen bg-[#070D1B] text-[#E8EDF7] selection:bg-[#F5B942] selection:text-[#070D1B] font-sans">
        {children}
      </body>
    </html>
  )
}
