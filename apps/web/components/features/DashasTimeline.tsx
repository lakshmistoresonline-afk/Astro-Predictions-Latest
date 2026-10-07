import React from 'react'
import { FullVimshottariDashaResult } from '../../types/api'

interface DashasTimelineProps {
  dashaSuite?: FullVimshottariDashaResult
}

export const DashasTimeline: React.FC<DashasTimelineProps> = ({ dashaSuite }) => {
  const mahadashas = dashaSuite?.mahadashas || []
  const balance = dashaSuite?.birth_balance

  return (
    <div className="bg-[#17163A]/90 p-8 rounded-3xl border border-[#F3E5AB]/30 shadow-2xl space-y-6 w-full">
      <h3 className="text-2xl font-extrabold text-[#F3E5AB]">Vimshottari Dasha 120-Year Timeline</h3>

      {balance && (
        <div className="p-4 bg-black/40 rounded-2xl border border-[#F3E5AB]/20 text-xs md:text-sm text-[#A0A5C0] space-y-1">
          <p><b className="text-[#F3E5AB]">Birth Balance Lord:</b> {balance.mahadasha_lord}</p>
          <p><b className="text-[#F3E5AB]">Remaining Years at Birth:</b> {balance.remaining_years} Years ({balance.remaining_days} Days)</p>
          <p><b className="text-[#F3E5AB]">First Mahadasha End (UTC):</b> {balance.first_mahadasha_end_utc_iso.slice(0, 10)}</p>
        </div>
      )}

      {mahadashas.length === 0 ? (
        <p className="text-sm text-[#A0A5C0]">Dasha timeline evidence unavailable.</p>
      ) : (
        <div className="space-y-3">
          {mahadashas.map((md, i) => (
            <div key={i} className="p-4 bg-black/30 rounded-xl border border-[#F3E5AB]/20 flex justify-between items-center text-xs md:text-sm">
              <div>
                <p className="font-bold text-white text-base">Mahadasha: {md.lord}</p>
                <p className="text-[#A0A5C0] text-xs">{md.start_utc_iso.slice(0, 10)} to {md.end_utc_iso.slice(0, 10)}</p>
              </div>
              <span className="px-3 py-1 bg-[#F3E5AB]/10 text-[#F3E5AB] font-bold rounded-full text-xs">
                {md.duration_years} Years
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
