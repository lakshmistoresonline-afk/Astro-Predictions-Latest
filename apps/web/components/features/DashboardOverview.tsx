import React from 'react'
import { BirthProfileResponse } from '../../types/api'

interface DashboardOverviewProps {
  data: BirthProfileResponse
  onNewProfile: () => void
}

export const DashboardOverview: React.FC<DashboardOverviewProps> = ({ data, onNewProfile }) => {
  const chart = data.master_evidence.canonical_chart
  const ascSign = chart.ascendant?.sign || 'Unavailable'
  const ascDegree = chart.ascendant?.degree !== undefined ? `${chart.ascendant.degree}°` : ''
  const moonPlacement = chart.placements?.Moon
  const sunPlacement = chart.placements?.Sun

  const moonSign = moonPlacement?.rashi?.sign || 'Unavailable'
  const sunSign = sunPlacement?.rashi?.sign || 'Unavailable'
  const moonNakshatra = moonPlacement?.nakshatra_pada?.nakshatra || 'Unavailable'
  const moonPada = moonPlacement?.nakshatra_pada?.pada !== undefined ? `P${moonPlacement.nakshatra_pada.pada}` : ''

  const activeDasha = data.predictions.active_dasha_summary || 'Unavailable'

  return (
    <div className="space-y-8 w-full">
      {/* Local Hero Header */}
      <div className="relative rounded-3xl overflow-hidden border border-[#F3E5AB]/40 shadow-2xl p-8 md:p-12 flex flex-col justify-end min-h-[260px] bg-gradient-to-tr from-[#050816] via-[#17163A] to-[#29204F] w-full">
        <div className="z-10 space-y-3 max-w-3xl relative">
          <span className="px-4 py-1.5 bg-[#F3E5AB]/25 border border-[#F3E5AB]/60 text-[#F3E5AB] text-xs font-extrabold rounded-full uppercase tracking-widest shadow-xl">
            Astrovision Masterpiece
          </span>
          <h2 className="text-3xl md:text-5xl font-extrabold text-white tracking-wide">
            Cosmic Profile for {data.birth_input.name}
          </h2>
          <p className="text-[#A0A5C0] text-xs md:text-sm leading-relaxed">
            Deterministic NASA JPL DE440s calculation results. Zero fabricated astrological fallbacks.
          </p>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 w-full">
        <div className="bg-[#17163A]/90 p-6 rounded-2xl border border-[#F3E5AB]/30 space-y-2 shadow-xl">
          <span className="text-xs uppercase font-extrabold tracking-widest text-[#F3E5AB]">Ascendant (Lagna)</span>
          <p className="text-2xl font-bold text-white">{ascSign} {ascDegree}</p>
        </div>
        <div className="bg-[#17163A]/90 p-6 rounded-2xl border border-[#F3E5AB]/30 space-y-2 shadow-xl">
          <span className="text-xs uppercase font-extrabold tracking-widest text-[#F3E5AB]">Moon Sign (Rashi)</span>
          <p className="text-2xl font-bold text-white">{moonSign}</p>
        </div>
        <div className="bg-[#17163A]/90 p-6 rounded-2xl border border-[#F3E5AB]/30 space-y-2 shadow-xl">
          <span className="text-xs uppercase font-extrabold tracking-widest text-[#F3E5AB]">Sun Sign</span>
          <p className="text-2xl font-bold text-white">{sunSign}</p>
        </div>
        <div className="bg-[#17163A]/90 p-6 rounded-2xl border border-[#F3E5AB]/30 space-y-2 shadow-xl">
          <span className="text-xs uppercase font-extrabold tracking-widest text-[#F3E5AB]">Nakshatra & Pada</span>
          <p className="text-2xl font-bold text-white">{moonNakshatra} {moonPada}</p>
        </div>
      </div>

      {/* Active Dasha Banner */}
      <div className="bg-[#17163A]/90 p-8 rounded-3xl border border-[#F3E5AB]/30 space-y-3 shadow-2xl">
        <h3 className="text-xl font-extrabold text-[#F3E5AB]">Active Vimshottari Dasha Hierarchy</h3>
        <p className="text-base md:text-lg text-white font-semibold leading-relaxed">{activeDasha}</p>
      </div>
    </div>
  )
}
