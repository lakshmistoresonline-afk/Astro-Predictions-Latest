import React from 'react'
import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="min-h-screen bg-[#070A14] text-slate-100 flex flex-col items-center justify-center p-6 text-center space-y-4 font-mono">
      <span className="text-4xl text-amber-400">✦</span>
      <h2 className="text-2xl font-black text-amber-300">404 - Page Not Found</h2>
      <p className="text-sm text-slate-400 max-w-md font-sans">
        The cosmic page or profile route you are looking for does not exist.
      </p>
      <Link
        href="/"
        className="px-5 py-2.5 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 border border-amber-500/40 text-amber-300 text-xs font-bold transition"
      >
        Return to Astrovision Dashboard →
      </Link>
    </div>
  )
}
