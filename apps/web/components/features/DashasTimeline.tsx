import React from 'react'
import { FullVimshottariDashaResult } from '../../types/api'

interface DashasTimelineProps {
  dashaSuite?: FullVimshottariDashaResult
}

export const DashasTimeline: React.FC<DashasTimelineProps> = ({ dashaSuite }) => {
  const mahadashas = dashaSuite?.mahadashas || []
  const balance = dashaSuite?.birth_balance

  const nowIso = new Date().toISOString().slice(0, 10)

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h3 className="text-xl font-extrabold text-amber-300 flex items-center gap-2">
            <span>⌛</span> Vimshottari Dasha 120-Year Timeline
          </h3>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Exact Planetary Mahadasha Sequence & UTC Boundary Dates
          </p>
        </div>
        <span className="px-3 py-1 bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-mono rounded-full">
          120-Year Parashari Cycle
        </span>
      </div>

      {balance && (
        <div className="p-5 bg-slate-950/60 rounded-2xl border border-slate-800/80 text-xs font-mono text-slate-300 space-y-2">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <span className="text-slate-500 uppercase tracking-wider block text-[10px]">Birth Balance Lord</span>
              <span className="font-bold text-amber-300 text-sm">{balance.mahadasha_lord}</span>
            </div>
            <div>
              <span className="text-slate-500 uppercase tracking-wider block text-[10px]">Remaining Years</span>
              <span className="font-bold text-slate-100 text-sm tabular-nums">{balance.remaining_years} Years ({balance.remaining_days} Days)</span>
            </div>
            <div>
              <span className="text-slate-500 uppercase tracking-wider block text-[10px]">First Mahadasha End</span>
              <span className="font-bold text-cyan-300 text-sm tabular-nums">{balance.first_mahadasha_end_utc_iso?.slice(0, 10)}</span>
            </div>
          </div>
        </div>
      )}

      {mahadashas.length === 0 ? (
        <div className="p-8 text-center bg-slate-950/40 rounded-2xl border border-slate-800 text-xs font-mono text-slate-400">
          Dasha timeline evidence unavailable.
        </div>
      ) : (
        <div className="space-y-3">
          {mahadashas.map((md, i) => {
            const startDate = md.start_utc_iso?.slice(0, 10) || ''
            const endDate = md.end_utc_iso?.slice(0, 10) || ''
            const isActive = nowIso >= startDate && nowIso <= endDate

            return (
              <div
                key={i}
                className={`p-4 md:p-5 rounded-2xl border transition duration-200 flex flex-wrap items-center justify-between gap-4 font-mono ${
                  isActive
                    ? 'bg-amber-500/10 border-amber-500/50 text-white shadow-lg shadow-amber-500/10'
                    : 'bg-slate-950/50 border-slate-800/80 hover:border-slate-700 text-slate-300'
                }`}
              >
                <div className="flex items-center gap-4">
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center font-bold text-sm shrink-0 ${
                    isActive ? 'bg-amber-400 text-slate-950' : 'bg-slate-800 text-amber-300'
                  }`}>
                    {md.lord.slice(0, 2).toUpperCase()}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <p className="font-black text-sm md:text-base text-slate-100">{md.lord} Mahadasha</p>
                      {isActive && (
                        <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-[10px] font-bold animate-pulse">
                          ACTIVE NOW
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-slate-400 tabular-nums mt-0.5">
                      {startDate} — {endDate}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <span className={`px-3 py-1 font-bold rounded-xl text-xs tabular-nums ${
                    isActive ? 'bg-amber-400/20 text-amber-300 border border-amber-400/40' : 'bg-slate-800/80 text-slate-300 border border-slate-700/60'
                  }`}>
                    {md.duration_years} Years
                  </span>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
