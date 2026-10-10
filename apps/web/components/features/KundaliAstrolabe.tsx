import React, { useState } from 'react'
import { BirthProfileResponse } from '../../types/api'

interface KundaliAstrolabeProps {
  svgChart: string | null
  data?: BirthProfileResponse | null
}

const HOUSE_TITLES: Record<number, { title: string; Sanskrit: string; significations: string }> = {
  1: { title: "House 1 — Tanu Bhava", Sanskrit: "Tanu Bhava", significations: "Self, Physical Constitution, Vitality, Personality, Temperament" },
  2: { title: "House 2 — Dhana Bhava", Sanskrit: "Dhana Bhava", significations: "Wealth, Family, Speech, Assets, Primary Education" },
  3: { title: "House 3 — Sahaja Bhava", Sanskrit: "Sahaja Bhava", significations: "Siblings, Courage, Initiative, Short Travel, Communication" },
  4: { title: "House 4 — Matru Bhava", Sanskrit: "Matru Bhava", significations: "Mother, Real Estate, Vehicles, Domestic Peace, Schooling" },
  5: { title: "House 5 — Putra Bhava", Sanskrit: "Putra Bhava", significations: "Children, Intellect, Speculation, Creativity, Past Karma" },
  6: { title: "House 6 — Ari Bhava", Sanskrit: "Ari Bhava", significations: "Health, Enemies, Service, Competition, Overcoming Obstacles" },
  7: { title: "House 7 — Kalatra Bhava", Sanskrit: "Kalatra Bhava", significations: "Spouse, Marriage, Business Partnerships, Trade, Contracts" },
  8: { title: "House 8 — Randhra Bhava", Sanskrit: "Randhra Bhava", significations: "Longevity, Transformation, Research, Shared Assets, Mysticism" },
  9: { title: "House 9 — Dharma Bhava", Sanskrit: "Dharma Bhava", significations: "Fortune, Higher Learning, Mentors, Pilgrimage, Spirituality" },
  10: { title: "House 10 — Karma Bhava", Sanskrit: "Karma Bhava", significations: "Career, Executive Authority, Public Reputation, Profession" },
  11: { title: "House 11 — Labha Bhava", Sanskrit: "Labha Bhava", significations: "Gains, Financial Networks, Ambition Fulfillment, Older Siblings" },
  12: { title: "House 12 — Vyaya Bhava", Sanskrit: "Vyaya Bhava", significations: "Moksha, Expenditure, Foreign Residence, Isolation, Rejuvenation" }
}

export const KundaliAstrolabe: React.FC<KundaliAstrolabeProps> = ({ svgChart, data }) => {
  const [selectedHouse, setSelectedHouse] = useState<number | null>(1)

  const chart = data?.master_evidence?.canonical_chart
  const name = data?.birth_input?.name || 'Native'
  const dateStr = data?.birth_input ? `${data.birth_input.year}-${String(data.birth_input.month).padStart(2, '0')}-${String(data.birth_input.day).padStart(2, '0')}` : ''
  const timeStr = data?.birth_input ? `${String(data.birth_input.hour).padStart(2, '0')}:${String(data.birth_input.minute).padStart(2, '0')}` : ''
  const placeStr = data?.birth_input ? `${data.birth_input.place_name}, ${data.birth_input.country}` : ''

  const asc = chart?.ascendant
  const ascSignIdx = asc?.sign_index || 11
  const placements = chart?.placements ? Object.values(chart.placements) : []

  // Compute house occupants for selected house
  const getHouseOccupants = (hNum: number) => {
    return placements.filter(p => {
      const pSignIdx = p.rashi?.sign_index || 1
      const houseCalculated = (pSignIdx - ascSignIdx + 12) % 12 + 1
      return houseCalculated === hNum
    })
  }

  const selectedHouseInfo = selectedHouse ? HOUSE_TITLES[selectedHouse] : null
  const selectedSignIdx = selectedHouse ? (ascSignIdx + selectedHouse - 2) % 12 + 1 : 1
  const selectedOccupants = selectedHouse ? getHouseOccupants(selectedHouse) : []

  const RASHI_NAMES = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
  const selectedSignName = RASHI_NAMES[selectedSignIdx - 1]

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

        <div className="flex items-center gap-3 font-mono">
          <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-bold flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            JPL DE440s Validated
          </span>
        </div>
      </div>

      {/* House Selector Quick Bar */}
      <div className="flex flex-wrap items-center gap-1.5 bg-slate-950 p-2 rounded-2xl border border-slate-800/80 font-mono text-xs">
        <span className="text-slate-500 text-[11px] px-2 font-bold uppercase">Click House:</span>
        {Array.from({ length: 12 }, (_, i) => i + 1).map(h => (
          <button
            key={h}
            onClick={() => setSelectedHouse(h)}
            className={`px-3 py-1.5 rounded-xl font-bold transition cursor-pointer ${
              selectedHouse === h
                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/50 shadow-md'
                : 'text-slate-400 hover:text-slate-100 hover:bg-slate-900'
            }`}
          >
            H{h}
          </button>
        ))}
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

        {/* Right Column: Interactive House Detail & Chart Details (5 Cols) */}
        <div className="lg:col-span-5 space-y-5 font-mono text-xs">
          {/* Selected House Slide-Over Drawer */}
          {selectedHouseInfo && (
            <div className="p-5 rounded-2xl bg-slate-950/80 border border-amber-500/30 space-y-3 shadow-xl">
              <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                <span className="text-amber-300 font-bold text-sm font-serif-heading">
                  {selectedHouseInfo.title}
                </span>
                <span className="px-2.5 py-0.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-[10px] font-bold">
                  Sign: {selectedSignName}
                </span>
              </div>

              <p className="text-[11px] text-slate-400 font-sans leading-relaxed">
                <strong className="text-slate-200">Significations:</strong> {selectedHouseInfo.significations}
              </p>

              <div className="pt-2 border-t border-slate-800 space-y-1.5">
                <span className="text-[10px] text-slate-500 uppercase tracking-wider block font-bold">
                  House Occupants ({selectedOccupants.length}):
                </span>
                {selectedOccupants.length === 0 ? (
                  <p className="text-slate-500 italic text-[11px]">No planets positioned in House {selectedHouse}.</p>
                ) : (
                  <div className="space-y-1">
                    {selectedOccupants.map(p => (
                      <div key={p.body_name} className="flex items-center justify-between p-2 rounded-lg bg-slate-900 border border-slate-800 text-[11px]">
                        <span className="font-bold text-slate-100 flex items-center gap-1.5">
                          <span className="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
                          {p.body_name} {p.retrograde && <span className="text-rose-400 text-[10px]">(R)</span>}
                        </span>
                        <span className="text-slate-400 tabular-nums">
                          {p.rashi?.degree}° {String(p.rashi?.minute).padStart(2, '0')}′
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Full Chart Details Table */}
          <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-3">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <h3 className="font-bold text-amber-300 text-sm">Placements Ledger</h3>
              <span className="text-[10px] text-slate-500">Lahiri Sidereal</span>
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
    </div>
  )
}
