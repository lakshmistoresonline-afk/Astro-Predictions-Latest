import React, { useState } from 'react'
import { ShadbalaSuiteResult, AshtakavargaPredictiveEvidence } from '../../types/api'

interface ShadbalaAshtakavargaViewProps {
  shadbalaSuite?: ShadbalaSuiteResult
  ashtakavargaEvidence?: AshtakavargaPredictiveEvidence
}

export const ShadbalaAshtakavargaView: React.FC<ShadbalaAshtakavargaViewProps> = ({
  shadbalaSuite,
  ashtakavargaEvidence
}) => {
  const [activeTab, setActiveTab] = useState<'shadbala' | 'ashtakavarga'>('shadbala')
  const planets = shadbalaSuite?.planets ? Object.values(shadbalaSuite.planets) : []
  const savEvidences = ashtakavargaEvidence?.house_sav_evidences || []

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h3 className="text-xl font-extrabold text-amber-300 flex items-center gap-2">
            <span>⚡</span> Quantitative Strength Engine (Shadbala & SAV)
          </h3>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Six-Bala Planetary Power & Sarvashtakavarga House Bindu Heatmap
          </p>
        </div>

        <div className="flex bg-slate-950 p-1 rounded-xl border border-slate-800 font-mono">
          <button
            onClick={() => setActiveTab('shadbala')}
            className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition ${
              activeTab === 'shadbala' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : 'text-slate-400 hover:text-white'
            }`}
          >
            Shadbala 6-Bala ({planets.length})
          </button>
          <button
            onClick={() => setActiveTab('ashtakavarga')}
            className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition ${
              activeTab === 'ashtakavarga' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : 'text-slate-400 hover:text-white'
            }`}
          >
            Ashtakavarga SAV ({savEvidences.length})
          </button>
        </div>
      </div>

      {activeTab === 'shadbala' ? (
        planets.length === 0 ? (
          <div className="p-8 text-center bg-slate-950/40 rounded-2xl border border-slate-800 text-xs font-mono text-slate-400">
            Shadbala 6-Bala strength evidence unavailable.
          </div>
        ) : (
          <div className="space-y-4">
            <div className="overflow-x-auto rounded-2xl border border-slate-800/80">
              <table className="w-full text-left text-xs font-mono">
                <thead className="bg-slate-950/90 text-amber-300 text-[11px] uppercase tracking-wider sticky top-0 border-b border-slate-800">
                  <tr>
                    <th className="py-3 px-4">Graha</th>
                    <th className="py-3 px-4">Total Rupas</th>
                    <th className="py-3 px-4">Shashtiamsas</th>
                    <th className="py-3 px-4">Strength %</th>
                    <th className="py-3 px-4">Power Meter</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-slate-200">
                  {planets.map(p => {
                    const pct = Math.min(100, Math.max(0, p.strength_percentage || 50))
                    return (
                      <tr key={p.planet} className="hover:bg-slate-800/40 transition">
                        <td className="py-3 px-4 font-bold text-white flex items-center gap-2">
                          <span className="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
                          {p.planet}
                        </td>
                        <td className="py-3 px-4 font-bold text-amber-300 tabular-nums">{p.total_rupas} Rupas</td>
                        <td className="py-3 px-4 tabular-nums text-slate-300">{p.total_shashtiamsas} pts</td>
                        <td className="py-3 px-4 tabular-nums font-bold text-cyan-300">{pct.toFixed(1)}%</td>
                        <td className="py-3 px-4 w-48">
                          <div className="w-full bg-slate-950 rounded-full h-2 overflow-hidden border border-slate-800">
                            <div
                              className="bg-gradient-to-r from-amber-500 to-cyan-400 h-full rounded-full"
                              style={{ width: `${pct}%` }}
                            ></div>
                          </div>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )
      ) : (
        savEvidences.length === 0 ? (
          <div className="p-8 text-center bg-slate-950/40 rounded-2xl border border-slate-800 text-xs font-mono text-slate-400">
            Sarvashtakavarga (SAV) house bindu evidence unavailable.
          </div>
        ) : (
          <div className="space-y-6 font-mono">
            {ashtakavargaEvidence?.total_sav_bindus !== undefined && ashtakavargaEvidence.total_sav_bindus !== null && (
              <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 flex items-center justify-between">
                <span className="text-xs text-slate-400">Total Sarvashtakavarga Bindus (337 Standard)</span>
                <span className="text-base font-black text-amber-300 tabular-nums">
                  {ashtakavargaEvidence.total_sav_bindus} Bindus
                </span>
              </div>
            )}

            {/* SAV Heatmap Ratings Summary Bar */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
              <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-between text-emerald-300">
                <span>Strong Energy (30+ Bindus)</span>
                <span className="font-bold">Favorable Growth</span>
              </div>
              <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-between text-amber-300">
                <span>Balanced Energy (25–29)</span>
                <span className="font-bold">Stable Base</span>
              </div>
              <div className="p-3 rounded-xl bg-slate-800/80 border border-slate-700/80 flex items-center justify-between text-slate-300">
                <span>Caution (&lt; 25 Bindus)</span>
                <span className="font-bold">Discipline Area</span>
              </div>
            </div>

            {/* 12 House Heatmap Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
              {savEvidences.map(h => {
                const bindus = h.sav_bindus !== null ? h.sav_bindus : 28
                const isStrong = bindus >= 30
                const isAverage = bindus >= 25 && bindus < 30

                return (
                  <div
                    key={h.rashi_index}
                    className={`p-4 rounded-2xl border space-y-2 transition shadow-md ${
                      isStrong
                        ? 'bg-emerald-950/20 border-emerald-500/40 text-emerald-100'
                        : isAverage
                        ? 'bg-amber-950/20 border-amber-500/40 text-amber-100'
                        : 'bg-slate-950/60 border-slate-800/80 text-slate-300'
                    }`}
                  >
                    <div className="flex justify-between items-center text-xs">
                      <span className="text-slate-400">House {h.rashi_index}</span>
                      <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${
                        isStrong ? 'bg-emerald-500/30 text-emerald-300 border-emerald-500/50' :
                        isAverage ? 'bg-amber-500/30 text-amber-300 border-amber-500/50' :
                        'bg-slate-800 text-slate-400 border-slate-700'
                      }`}>
                        {bindus} Bindus
                      </span>
                    </div>
                    <p className="font-bold text-slate-100 text-sm">{h.rashi_name}</p>
                    <p className="text-[10px] text-slate-400 font-sans leading-relaxed line-clamp-2">
                      {h.strength_category || 'Neutral House'}
                    </p>
                  </div>
                )
              })}
            </div>
          </div>
        )
      )}
    </div>
  )
}
