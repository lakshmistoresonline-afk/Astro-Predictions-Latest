import React from 'react'
import { ShadbalaSuiteResult, AshtakavargaPredictiveEvidence } from '../../types/api'

interface ShadbalaAshtakavargaViewProps {
  shadbalaSuite?: ShadbalaSuiteResult
  ashtakavargaEvidence?: AshtakavargaPredictiveEvidence
}

export const ShadbalaAshtakavargaView: React.FC<ShadbalaAshtakavargaViewProps> = ({
  shadbalaSuite,
  ashtakavargaEvidence
}) => {
  const planets = shadbalaSuite?.planets ? Object.values(shadbalaSuite.planets) : []
  const savEvidences = ashtakavargaEvidence?.house_sav_evidences || []

  return (
    <div className="space-y-8 w-full">
      {/* Shadbala Strengths Table */}
      <div className="bg-[#17163A]/90 p-8 rounded-3xl border border-[#F3E5AB]/30 shadow-2xl space-y-6">
        <h3 className="text-2xl font-extrabold text-[#F3E5AB]">Shadbala Six-Fold Planetary Strengths</h3>

        {planets.length === 0 ? (
          <p className="text-sm text-[#A0A5C0]">Shadbala strength evidence unavailable.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs md:text-sm">
              <thead>
                <tr className="border-b border-[#F3E5AB]/30 text-[#F3E5AB] uppercase tracking-wider">
                  <th className="pb-3 px-2">Planet</th>
                  <th className="pb-3 px-2">Total Rupas</th>
                  <th className="pb-3 px-2">Shashtiamsas</th>
                  <th className="pb-3 px-2">Strength %</th>
                  <th className="pb-3 px-2">Strongest Component</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#F3E5AB]/10 text-white">
                {planets.map(p => (
                  <tr key={p.planet} className="hover:bg-white/5 transition">
                    <td className="py-3 px-2 font-bold">{p.planet}</td>
                    <td className="py-3 px-2 font-bold text-[#F3E5AB]">{p.total_rupas} Rupas</td>
                    <td className="py-3 px-2">{p.total_shashtiamsas} pts</td>
                    <td className="py-3 px-2">{p.strength_percentage}%</td>
                    <td className="py-3 px-2 text-[#A0A5C0]">{p.sthana_bala.name}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Ashtakavarga SAV Strengths */}
      <div className="bg-[#17163A]/90 p-8 rounded-3xl border border-[#F3E5AB]/30 shadow-2xl space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <h3 className="text-2xl font-extrabold text-[#F3E5AB]">Sarvashtakavarga (SAV) House Bindus</h3>
          {ashtakavargaEvidence?.total_sav_bindus !== null && ashtakavargaEvidence?.total_sav_bindus !== undefined && (
            <span className="px-3 py-1 bg-[#F3E5AB]/20 text-[#F3E5AB] text-xs font-bold rounded-full">
              Total SAV Bindus: {ashtakavargaEvidence.total_sav_bindus}
            </span>
          )}
        </div>

        {savEvidences.length === 0 ? (
          <p className="text-sm text-[#A0A5C0]">Ashtakavarga SAV evidence unavailable.</p>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            {savEvidences.map(h => (
              <div key={h.rashi_index} className="p-4 bg-black/40 rounded-2xl border border-[#F3E5AB]/20 text-center space-y-1">
                <span className="text-[10px] uppercase font-bold text-[#A0A5C0]">{h.rashi_name}</span>
                <p className="text-2xl font-black text-white">{h.sav_bindus !== null ? `${h.sav_bindus} pts` : 'N/A'}</p>
                <span className="text-[9px] px-2 py-0.5 rounded-full bg-[#F3E5AB]/10 text-[#F3E5AB] font-bold block truncate">
                  {h.strength_category}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
