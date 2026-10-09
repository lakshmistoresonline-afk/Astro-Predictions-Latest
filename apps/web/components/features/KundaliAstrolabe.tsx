import React from 'react'
import { BirthProfileResponse } from '../../types/api'

interface KundaliAstrolabeProps {
  svgChart: string | null
  data?: BirthProfileResponse | null
}

export const KundaliAstrolabe: React.FC<KundaliAstrolabeProps> = ({ svgChart, data }) => {
  const chart = data?.master_evidence?.canonical_chart
  const name = data?.birth_input?.name || 'Native'
  const dateStr = data?.birth_input ? `${data.birth_input.year}-${String(data.birth_input.month).padStart(2, '0')}-${String(data.birth_input.day).padStart(2, '0')}` : ''
  const timeStr = data?.birth_input ? `${String(data.birth_input.hour).padStart(2, '0')}:${String(data.birth_input.minute).padStart(2, '0')}` : ''
  const placeStr = data?.birth_input ? `${data.birth_input.place_name}, ${data.birth_input.country}` : ''

  const asc = chart?.ascendant
  const placements = chart?.placements ? Object.values(chart.placements) : []

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800/80 pb-5">
        <div>
          <span className="px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-mono font-bold uppercase tracking-widest">
            Canonical Rashi Chart
          </span>
          <h2 className="text-2xl md:text-3xl font-black text-slate-100 tracking-wide mt-1.5 font-serif-heading">
            Birth Chart — Rāśi (North Indian Style)
          </h2>
          {data && (
            <p className="text-xs text-slate-400 font-mono mt-1">
              {name} • {dateStr} • {timeStr} • {placeStr}
            </p>
          )}
        </div>

        <div className="flex items-center gap-3">
          <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-mono font-bold flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            JPL DE440s Validated
          </span>
        </div>
      </div>

      {/* Main Chart Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: SVG Astrolabe Chart (7 Cols) */}
        <div className="lg:col-span-7 bg-slate-950 p-6 rounded-2xl border border-slate-800/80 flex flex-col items-center justify-center min-h-[380px] shadow-inner relative">
          {svgChart ? (
            <div
              dangerouslySetInnerHTML={{ __html: svgChart }}
              className="w-full max-w-[420px] aspect-square flex justify-center items-center overflow-hidden"
            />
          ) : (
            <div className="text-center space-y-3 p-8">
              <span className="text-3xl text-amber-400">🌌</span>
              <p className="text-xs font-mono text-slate-400">Kundali SVG Chart Unavailable. Please calculate a birth profile first.</p>
            </div>
          )}
        </div>

        {/* Right Column: Chart Details Table (5 Cols) */}
        <div className="lg:col-span-5 bg-slate-950/60 p-5 rounded-2xl border border-slate-800/80 space-y-4 font-mono text-xs">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="font-bold text-amber-300 text-sm">Chart Details</h3>
            <span className="text-[10px] text-slate-500">Lahiri Ayanamsha</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead className="text-slate-500 uppercase text-[10px] border-b border-slate-800/60">
                <tr>
                  <th className="py-2 px-2">Point</th>
                  <th className="py-2 px-2">Sign</th>
                  <th className="py-2 px-2 text-right">Degree</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/40 text-slate-200">
                {asc && (
                  <tr className="bg-amber-500/10 font-bold">
                    <td className="py-2 px-2 text-amber-300">Ascendant</td>
                    <td className="py-2 px-2 text-amber-200">{asc.sign}</td>
                    <td className="py-2 px-2 text-right tabular-nums">{asc.degree}° {String(asc.minute).padStart(2, '0')}′</td>
                  </tr>
                )}
                {placements.map(p => (
                  <tr key={p.body_name} className="hover:bg-slate-900/60">
                    <td className="py-2 px-2 font-semibold text-slate-200">{p.body_name}</td>
                    <td className="py-2 px-2 text-slate-300">{p.rashi?.sign || 'N/A'}</td>
                    <td className="py-2 px-2 text-right tabular-nums text-slate-400">
                      {p.rashi?.degree !== undefined ? `${p.rashi.degree}° ${String(p.rashi.minute).padStart(2, '0')}′` : 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}
