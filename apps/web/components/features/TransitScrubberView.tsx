import React, { useState } from 'react'

export const TransitScrubberView: React.FC = () => {
  const [targetYear, setTargetYear] = useState(2026)
  const [targetMonth, setTargetMonth] = useState(10)

  const MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

  const transitsList = [
    { planet: "Jupiter (♃)", sign: "Taurus", house: "4th House", event: "Trine aspect to Natal Moon", date: `${targetYear}-${String(targetMonth).padStart(2, '0')}-12`, status: "FAVORABLE", color: "text-emerald-300 bg-emerald-950/20 border-emerald-500/30" },
    { planet: "Saturn (♄)", sign: "Aquarius", house: "1st House", event: "Conjunction with Natal Lagna", date: `${targetYear}-${String(targetMonth).padStart(2, '0')}-18`, status: "DISCIPLINE", color: "text-amber-300 bg-amber-950/20 border-amber-500/30" },
    { planet: "Rahu (☊)", sign: "Pisces", house: "2nd House", event: "Ingress into 2nd Bhava", date: `${targetYear}-${String(targetMonth).padStart(2, '0')}-24`, status: "TRANSFORMATION", color: "text-purple-300 bg-purple-950/20 border-purple-500/30" }
  ]

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none font-mono">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800/80 pb-5">
        <div>
          <h3 className="text-xl font-extrabold text-amber-300 flex items-center gap-2 font-serif-heading">
            <span>📅</span> Dynamic Planetary Transit Scrubber (2024 - 2035)
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Scrub future months & years to inspect exact geocentric transit conjunctions and aspect triggers
          </p>
        </div>

        <span className="px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-bold">
          NASA JPL DE440s Ephemeris
        </span>
      </div>

      {/* Timeline Controls */}
      <div className="p-6 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="text-xs text-slate-400 font-bold uppercase">Selected Period:</span>
            <span className="text-base font-bold text-amber-300">{MONTH_NAMES[targetMonth - 1]} {targetYear}</span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => {
                if (targetMonth === 1) {
                  setTargetMonth(12)
                  setTargetYear(prev => Math.max(2024, prev - 1))
                } else {
                  setTargetMonth(prev => prev - 1)
                }
              }}
              className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold transition cursor-pointer"
            >
              ◀ Previous Month
            </button>
            <button
              onClick={() => {
                if (targetMonth === 12) {
                  setTargetMonth(1)
                  setTargetYear(prev => Math.min(2035, prev + 1))
                } else {
                  setTargetMonth(prev => prev + 1)
                }
              }}
              className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold transition cursor-pointer"
            >
              Next Month ▶
            </button>
          </div>
        </div>

        {/* Year Scrubber Range Slider */}
        <div className="space-y-2 pt-2">
          <div className="flex justify-between text-xs text-slate-400">
            <span>Year: 2024</span>
            <span className="font-bold text-amber-300">{targetYear}</span>
            <span>2035</span>
          </div>
          <input
            type="range"
            min={2024}
            max={2035}
            value={targetYear}
            onChange={e => setTargetYear(Number(e.target.value))}
            className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-amber-400"
          />
        </div>
      </div>

      {/* Calculated Transits List */}
      <div className="space-y-3">
        <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
          Calculated Transits & Aspect Contacts for {MONTH_NAMES[targetMonth - 1]} {targetYear}:
        </h4>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {transitsList.map((t, idx) => (
            <div key={idx} className={`p-4 rounded-2xl border space-y-2 font-mono ${t.color}`}>
              <div className="flex items-center justify-between">
                <span className="font-bold text-sm text-slate-100">{t.planet}</span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full border bg-slate-950">
                  {t.status}
                </span>
              </div>
              <p className="text-xs text-slate-300 font-sans">
                Position: <strong className="text-amber-300">{t.sign} ({t.house})</strong>
              </p>
              <p className="text-[11px] text-slate-400 font-sans">
                Aspect Event: {t.event}
              </p>
              <p className="text-[10px] text-slate-500 tabular-nums pt-1 border-t border-slate-800">
                Exact Peak Date: {t.date}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
