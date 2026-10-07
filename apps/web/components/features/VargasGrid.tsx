import React from 'react'
import { Full16VargaSuite } from '../../types/api'

interface VargasGridProps {
  vargaSuite?: Full16VargaSuite
}

export const VargasGrid: React.FC<VargasGridProps> = ({ vargaSuite }) => {
  const vargas = vargaSuite?.vargas ? Object.values(vargaSuite.vargas) : []

  return (
    <div className="bg-[#17163A]/90 p-8 rounded-3xl border border-[#F3E5AB]/30 shadow-2xl space-y-6 w-full">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <h3 className="text-2xl font-extrabold text-[#F3E5AB]">16 Parashari Divisional Charts (D1 - D60)</h3>
        {vargaSuite?.vargottama_bodies && vargaSuite.vargottama_bodies.length > 0 && (
          <span className="px-3 py-1 bg-amber-500/20 border border-amber-400/40 text-amber-200 text-xs font-bold rounded-full">
            Vargottama Bodies: {vargaSuite.vargottama_bodies.join(', ')}
          </span>
        )}
      </div>

      {vargas.length === 0 ? (
        <p className="text-sm text-[#A0A5C0]">16 Vargas suite evidence unavailable.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {vargas.map(v => (
            <div key={v.division} className="p-4 bg-black/40 rounded-2xl border border-[#F3E5AB]/20 space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm font-extrabold text-[#F3E5AB]">{v.division}</span>
                <span className="text-[10px] text-[#A0A5C0]">{v.division_name}</span>
              </div>
              <p className="text-xs text-white font-bold">Lagna: {v.ascendant?.varga_sign || 'N/A'}</p>
              <div className="text-[11px] text-[#A0A5C0] space-y-0.5">
                <p>Sun: {v.placements?.Sun?.varga_sign || 'N/A'}</p>
                <p>Moon: {v.placements?.Moon?.varga_sign || 'N/A'}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
