import React from 'react'

interface LoadingStateProps {
  stepMessage?: string
}

export const LoadingState: React.FC<LoadingStateProps> = ({ stepMessage }) => {
  return (
    <div className="fixed inset-0 bg-[#070A14]/90 backdrop-blur-xl z-50 flex flex-col items-center justify-center p-6 space-y-8 select-none">
      {/* Outer Pulse Glow */}
      <div className="relative w-28 h-28 flex items-center justify-center">
        <div className="absolute inset-0 rounded-full border-2 border-amber-500/20 border-t-amber-400 animate-spin"></div>
        <div className="absolute inset-2 rounded-full border-2 border-cyan-500/20 border-b-cyan-400 animate-spin" style={{ animationDirection: 'reverse', animationDuration: '3s' }}></div>
        <div className="text-3xl text-amber-300 animate-pulse">✦</div>
      </div>

      {/* Message and Progress Bar */}
      <div className="text-center space-y-4 max-w-lg">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-mono uppercase tracking-widest">
          <span className="w-2 h-2 rounded-full bg-amber-400 animate-ping"></span>
          NASA JPL DE440s Engine
        </div>

        <h3 className="text-2xl font-black text-slate-100 tracking-wide">
          Computing Ephemeris & Canonical Evidence
        </h3>

        {stepMessage && (
          <p className="text-sm font-mono text-slate-400 animate-pulse leading-relaxed bg-slate-900/80 px-4 py-2 rounded-xl border border-slate-800">
            {stepMessage}
          </p>
        )}

        {/* Shimmer Progress Bar */}
        <div className="w-full bg-slate-800/80 rounded-full h-1.5 overflow-hidden border border-slate-700/50">
          <div className="bg-gradient-to-r from-amber-400 via-cyan-400 to-amber-300 h-full w-2/3 animate-pulse rounded-full"></div>
        </div>
      </div>
    </div>
  )
}
