import React, { useState } from 'react'
import { FullVimshottariDashaResult } from '../../types/api'

interface DashasTimelineProps {
  dashaSuite?: FullVimshottariDashaResult
}

const DASHA_SEQUENCE = ["Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus"]
const DASHA_YEARS_MAP: Record<string, number> = {
  Sun: 6, Moon: 10, Mars: 7, Rahu: 18, Jupiter: 16, Saturn: 19, Mercury: 17, Ketu: 7, Venus: 20
}

export const DashasTimeline: React.FC<DashasTimelineProps> = ({ dashaSuite }) => {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(0)

  const mahadashas = dashaSuite?.mahadashas || []
  const balance = dashaSuite?.birth_balance
  const nowIso = new Date().toISOString().slice(0, 10)

  // Compute 9 Antardasha sub-periods for a Mahadasha
  const getAntardashas = (mLord: string, mStartIso: string, mDurationYrs: number) => {
    const startDt = new Date(mStartIso)
    const mYears = mDurationYrs || DASHA_YEARS_MAP[mLord] || 10
    const startIndex = DASHA_SEQUENCE.indexOf(mLord)
    const antardashas = []

    let currentStart = new Date(startDt)

    for (let i = 0; i < 9; i++) {
      const aLord = DASHA_SEQUENCE[(startIndex + i) % 9]
      const aYears = DASHA_YEARS_MAP[aLord] || 10
      const durationYrs = (mYears * aYears) / 120.0
      const durationDays = durationYrs * 365.2425

      const endDt = new Date(currentStart.getTime() + durationDays * 24 * 60 * 60 * 1000)

      antardashas.push({
        lord: `${mLord} / ${aLord}`,
        subLord: aLord,
        startIso: currentStart.toISOString().slice(0, 10),
        endIso: endDt.toISOString().slice(0, 10),
        durationYrs: durationYrs.toFixed(2)
      })

      currentStart = endDt
    }

    return antardashas
  }

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h3 className="text-xl font-extrabold text-amber-300 flex items-center gap-2 font-serif-heading">
            <span>⌛</span> Vimshottari Dasha 120-Year Timeline & Antardashas
          </h3>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Exact Planetary Mahadasha Sequence & Expandable Antardasha Boundaries
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
            const isExpanded = expandedIndex === i
            const antardashas = isExpanded ? getAntardashas(md.lord, md.start_utc_iso, md.duration_years) : []

            return (
              <div
                key={i}
                className={`rounded-2xl border transition duration-200 font-mono overflow-hidden ${
                  isActive
                    ? 'bg-slate-950 border-amber-500/50 shadow-lg shadow-amber-500/10'
                    : 'bg-slate-950/50 border-slate-800/80 hover:border-slate-700'
                }`}
              >
                {/* Mahadasha Header Card */}
                <div
                  onClick={() => setExpandedIndex(isExpanded ? null : i)}
                  className="p-4 md:p-5 flex flex-wrap items-center justify-between gap-4 cursor-pointer hover:bg-slate-900/60 transition"
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
                    <span className="text-slate-400 text-xs">{isExpanded ? '▲' : '▼'}</span>
                  </div>
                </div>

                {/* Expandable Antardashas Sub-Periods Table */}
                {isExpanded && (
                  <div className="p-4 bg-slate-900/80 border-t border-slate-800 space-y-3 font-mono text-xs">
                    <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                      <span className="font-bold text-amber-300 uppercase tracking-wider text-[11px]">
                        9 Sub-Antardashas for {md.lord} Mahadasha
                      </span>
                      <span className="text-[10px] text-slate-500">Parashari Proportional Sub-Divisions</span>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                      {antardashas.map((ad, idx) => {
                        const isSubActive = nowIso >= ad.startIso && nowIso <= ad.endIso

                        return (
                          <div
                            key={idx}
                            className={`p-3 rounded-xl border flex flex-col justify-between space-y-1 ${
                              isSubActive
                                ? 'bg-amber-500/20 border-amber-500/60 text-amber-200 shadow-md'
                                : 'bg-slate-950/60 border-slate-800 text-slate-300'
                            }`}
                          >
                            <div className="flex justify-between items-center">
                              <span className="font-bold text-slate-100">{ad.lord}</span>
                              {isSubActive && <span className="text-[9px] bg-emerald-500/30 text-emerald-300 font-bold px-1.5 py-0.5 rounded">ACTIVE</span>}
                            </div>
                            <p className="text-[10px] text-slate-400 tabular-nums">
                              {ad.startIso} to {ad.endIso}
                            </p>
                            <span className="text-[10px] text-amber-300/80 font-semibold">{ad.durationYrs} Yrs</span>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
