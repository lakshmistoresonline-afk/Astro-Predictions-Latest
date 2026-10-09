import React, { useState } from 'react'
import { Full16VargaSuite, VargaChart } from '../../types/api'

interface VargasGridProps {
  vargaSuite?: Full16VargaSuite
}

export const VargasGrid: React.FC<VargasGridProps> = ({ vargaSuite }) => {
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('table')
  const vargas = vargaSuite?.vargas ? Object.values(vargaSuite.vargas) : []
  const vargottamaList = vargaSuite?.vargottama_bodies || []

  const planetsList = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h3 className="text-xl font-extrabold text-amber-300 flex items-center gap-2">
            <span>❖</span> 16 Parashari Divisional Charts (Shodasha Varga Atlas)
          </h3>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Complete D1 through D60 Micro-Zodiac Harmonic Sign Placements
          </p>
        </div>

        <div className="flex items-center gap-3">
          {vargottamaList.length > 0 && (
            <span className="px-3.5 py-1.5 bg-amber-500/10 border border-amber-500/40 text-amber-300 text-xs font-mono font-bold rounded-full flex items-center gap-1.5">
              <span>✦</span> Vargottama: {vargottamaList.join(', ')}
            </span>
          )}

          <div className="flex bg-slate-950 p-1 rounded-xl border border-slate-800">
            <button
              onClick={() => setViewMode('table')}
              className={`px-3 py-1 rounded-lg text-xs font-mono font-semibold transition ${
                viewMode === 'table' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : 'text-slate-400 hover:text-white'
              }`}
            >
              Atlas Table
            </button>
            <button
              onClick={() => setViewMode('grid')}
              className={`px-3 py-1 rounded-lg text-xs font-mono font-semibold transition ${
                viewMode === 'grid' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : 'text-slate-400 hover:text-white'
              }`}
            >
              Grid View
            </button>
          </div>
        </div>
      </div>

      {vargas.length === 0 ? (
        <div className="p-8 text-center bg-slate-950/40 rounded-2xl border border-slate-800 text-xs font-mono text-slate-400">
          Shodasha Varga suite evidence unavailable.
        </div>
      ) : viewMode === 'table' ? (
        <div className="overflow-x-auto rounded-2xl border border-slate-800/80">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-slate-950/90 text-amber-300 text-[11px] uppercase tracking-wider sticky top-0 border-b border-slate-800">
              <tr>
                <th className="py-3 px-4">Point / Graha</th>
                {vargas.map(v => (
                  <th key={v.division} className="py-3 px-3 text-center border-l border-slate-800/60">
                    <span className="font-bold text-amber-300 block">{v.division}</span>
                    <span className="text-[9px] text-slate-500 normal-case block font-normal">{v.division_name?.slice(0, 10)}</span>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-200">
              {/* Ascendant Row */}
              <tr className="bg-slate-950/40 font-bold">
                <td className="py-3 px-4 text-amber-300">Ascendant (Lagna)</td>
                {vargas.map(v => (
                  <td key={v.division} className="py-3 px-3 text-center border-l border-slate-800/60 text-slate-100">
                    {v.ascendant?.varga_sign || '—'}
                  </td>
                ))}
              </tr>

              {/* Planet Rows */}
              {planetsList.map(planet => (
                <tr key={planet} className="hover:bg-slate-800/40 transition">
                  <td className="py-3 px-4 font-bold text-slate-100 flex items-center gap-1.5">
                    {vargottamaList.includes(planet) && <span className="text-amber-400 text-xs">✦</span>}
                    {planet}
                  </td>
                  {vargas.map(v => {
                    const pl = v.placements?.[planet]
                    const signName = pl?.varga_sign || '—'
                    const isVargottama = pl?.is_vargottama || vargottamaList.includes(planet)

                    return (
                      <td
                        key={v.division}
                        className={`py-3 px-3 text-center border-l border-slate-800/60 ${
                          isVargottama ? 'bg-amber-500/10 text-amber-300 font-bold' : 'text-slate-300'
                        }`}
                      >
                        {signName}
                      </td>
                    )
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {vargas.map(v => (
            <div key={v.division} className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-2 font-mono hover:border-amber-500/40 transition">
              <div className="flex justify-between items-center border-b border-slate-800/60 pb-2">
                <span className="text-sm font-bold text-amber-300">{v.division}</span>
                <span className="text-[10px] text-slate-400">{v.division_name}</span>
              </div>
              <p className="text-xs text-white font-bold">Lagna: <span className="text-amber-200">{v.ascendant?.varga_sign || 'N/A'}</span></p>
              <div className="text-[11px] text-slate-400 space-y-1 pt-1">
                <p>Sun: <span className="text-slate-200">{v.placements?.Sun?.varga_sign || 'N/A'}</span></p>
                <p>Moon: <span className="text-slate-200">{v.placements?.Moon?.varga_sign || 'N/A'}</span></p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
