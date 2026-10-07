import React from 'react'
import { CanonicalVedicChart } from '../../types/api'

interface PlanetaryPositionsTableProps {
  chart: CanonicalVedicChart
}

export const PlanetaryPositionsTable: React.FC<PlanetaryPositionsTableProps> = ({ chart }) => {
  const placements = chart?.placements ? Object.values(chart.placements) : []

  return (
    <div className="bg-[#17163A]/90 p-8 rounded-3xl border border-[#F3E5AB]/30 shadow-2xl space-y-6 w-full">
      <h3 className="text-2xl font-extrabold text-[#F3E5AB]">Planetary Positions & Dignities</h3>

      {placements.length === 0 ? (
        <p className="text-sm text-[#A0A5C0]">Planetary placements unavailable.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs md:text-sm">
            <thead>
              <tr className="border-b border-[#F3E5AB]/30 text-[#F3E5AB] uppercase tracking-wider">
                <th className="pb-3 px-2">Body</th>
                <th className="pb-3 px-2">Rashi (Sign)</th>
                <th className="pb-3 px-2">Degree</th>
                <th className="pb-3 px-2">Nakshatra & Pada</th>
                <th className="pb-3 px-2">Motion</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#F3E5AB]/10 text-white">
              {placements.map(p => (
                <tr key={p.body_name} className="hover:bg-white/5 transition">
                  <td className="py-3 px-2 font-bold">{p.body_name}</td>
                  <td className="py-3 px-2">{p.rashi?.sign || 'N/A'}</td>
                  <td className="py-3 px-2">{p.rashi?.degree !== undefined ? `${p.rashi.degree}° ${p.rashi.minute}'` : 'N/A'}</td>
                  <td className="py-3 px-2">{p.nakshatra_pada?.nakshatra || 'N/A'} (P{p.nakshatra_pada?.pada || '-'})</td>
                  <td className="py-3 px-2">
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-extrabold ${p.retrograde ? 'bg-rose-500/20 text-rose-300' : 'bg-emerald-500/20 text-emerald-300'}`}>
                      {p.retrograde ? 'RETROGRADE' : 'DIRECT'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
