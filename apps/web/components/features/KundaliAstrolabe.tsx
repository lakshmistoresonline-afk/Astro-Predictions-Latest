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

const SOUTH_INDIAN_BOXES = [
  { signIdx: 12, name: "Pisces", short: "Pi" },
  { signIdx: 1,  name: "Aries", short: "Ar" },
  { signIdx: 2,  name: "Taurus", short: "Ta" },
  { signIdx: 3,  name: "Gemini", short: "Ge" },
  { signIdx: 11, name: "Aquarius", short: "Aq" },
  { signIdx: 4,  name: "Cancer", short: "Ca" },
  { signIdx: 10, name: "Capricorn", short: "Cp" },
  { signIdx: 5,  name: "Leo", short: "Le" },
  { signIdx: 9,  name: "Sagittarius", short: "Sg" },
  { signIdx: 8,  name: "Scorpio", short: "Sc" },
  { signIdx: 7,  name: "Libra", short: "Li" },
  { signIdx: 6,  name: "Virgo", short: "Vi" }
]

export const KundaliAstrolabe: React.FC<KundaliAstrolabeProps> = ({ svgChart, data }) => {
  const [selectedHouse, setSelectedHouse] = useState<number | null>(1)
  const [chartStyle, setChartStyle] = useState<'north' | 'south'>('north')

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

  // Get occupants for a fixed sign_index (1..12) for South Indian Chart
  const getSignOccupants = (signIdx: number) => {
    const list: string[] = []
    if (ascSignIdx === signIdx) list.push("As")
    placements.forEach(p => {
      if (p.rashi?.sign_index === signIdx) {
        const glyph = p.body_name.slice(0, 2)
        if (p.retrograde) list.push(`${glyph}(R)`)
        else list.push(glyph)
      }
    })
    return list
  }

  const selectedHouseInfo = selectedHouse ? HOUSE_TITLES[selectedHouse] : null
  const selectedSignIdx = selectedHouse ? (ascSignIdx + selectedHouse - 2) % 12 + 1 : 1
  const selectedOccupants = selectedHouse ? getHouseOccupants(selectedHouse) : []

  const RASHI_NAMES = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
  const selectedSignName = RASHI_NAMES[selectedSignIdx - 1]

  const handleExportPdf = () => {
    if (!data?.birth_input) {
      alert('Please calculate a birth profile first.')
      return
    }
    const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    const savedToken = sessionStorage.getItem('astro_jwt_token')

    fetch(`${API_BASE}/api/v1/export/pdf`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(savedToken ? { 'Authorization': `Bearer ${savedToken}` } : {})
      },
      body: JSON.stringify(data.birth_input)
    })
      .then(res => res.blob())
      .then(blob => {
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `${data.birth_input.name.replace(/\s+/g, '_')}_Celestial_Dossier.pdf`
        a.click()
      })
      .catch(() => alert('PDF export failed. Please ensure server is active.'))
  }

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800/80 pb-5">
        <div>
          <span className="px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-mono font-bold uppercase tracking-widest">
            Canonical Rashi Chart
          </span>
          <h2 className="text-2xl md:text-3xl font-black text-slate-100 tracking-wide mt-1.5 font-serif-heading">
            Birth Chart — {chartStyle === 'north' ? 'Rāśi (North Indian Style)' : 'Rāśi (South Indian Grid Style)'}
          </h2>
          {data && (
            <p className="text-xs text-slate-400 font-mono mt-1">
              {name} • {dateStr} • {timeStr} • {placeStr}
            </p>
          )}
        </div>

        <div className="flex items-center gap-3 font-mono">
          <button
            onClick={handleExportPdf}
            className="px-4 py-2 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 text-amber-300 font-bold text-xs transition cursor-pointer flex items-center gap-1.5"
          >
            <span>📄</span> Export PDF
          </button>
          <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-bold flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            DE440s Validated
          </span>
        </div>
      </div>

      {/* Style Toggle & House Selector Quick Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-slate-950 p-2 rounded-2xl border border-slate-800/80 font-mono text-xs">
        <div className="flex bg-slate-900 p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setChartStyle('north')}
            className={`px-3 py-1 rounded-lg font-bold transition cursor-pointer ${
              chartStyle === 'north' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : 'text-slate-400 hover:text-white'
            }`}
          >
            North Indian (Diamond)
          </button>
          <button
            onClick={() => setChartStyle('south')}
            className={`px-3 py-1 rounded-lg font-bold transition cursor-pointer ${
              chartStyle === 'south' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : 'text-slate-400 hover:text-white'
            }`}
          >
            South Indian (Grid)
          </button>
        </div>

        <div className="flex items-center gap-1 overflow-x-auto">
          <span className="text-slate-500 text-[11px] px-2 font-bold uppercase shrink-0">Click House:</span>
          {Array.from({ length: 12 }, (_, i) => i + 1).map(h => (
            <button
              key={h}
              onClick={() => setSelectedHouse(h)}
              className={`px-2.5 py-1 rounded-lg font-bold transition cursor-pointer shrink-0 ${
                selectedHouse === h
                  ? 'bg-amber-500/20 text-amber-300 border border-amber-500/50 shadow-md'
                  : 'text-slate-400 hover:text-slate-100 hover:bg-slate-900'
              }`}
            >
              H{h}
            </button>
          ))}
        </div>
      </div>

      {/* Main Chart Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: SVG Astrolabe Chart (7 Cols) */}
        <div className="lg:col-span-7 bg-slate-950 p-6 rounded-2xl border border-slate-800/80 flex flex-col items-center justify-center min-h-[380px] shadow-inner relative">
          {chartStyle === 'north' ? (
            svgChart ? (
              <div
                dangerouslySetInnerHTML={{ __html: svgChart }}
                className="w-full max-w-[420px] aspect-square flex justify-center items-center overflow-hidden"
              />
            ) : (
              <div className="text-center space-y-3 p-8">
                <span className="text-3xl text-amber-400">🌌</span>
                <p className="text-xs font-mono text-slate-400">Kundali SVG Chart Unavailable. Please calculate a birth profile first.</p>
              </div>
            )
          ) : (
            /* South Indian Fixed Grid Chart */
            <div className="w-full max-w-[420px] aspect-square bg-[#070D1B] border-2 border-amber-500/30 rounded-2xl p-2 grid grid-cols-4 grid-rows-4 gap-1 font-mono text-xs shadow-2xl relative">
              {/* Outer 12 Boxes */}
              <div className="p-2 border border-slate-800 rounded-xl bg-slate-900/60 flex flex-col justify-between">
                <span className="text-[10px] text-amber-400 font-bold">Pi</span>
                <span className="text-xs font-bold text-slate-100">{getSignOccupants(12).join(' ') || '—'}</span>
              </div>
              <div className="p-2 border border-slate-800 rounded-xl bg-slate-900/60 flex flex-col justify-between">
                <span className="text-[10px] text-amber-400 font-bold">Ar</span>
                <span className="text-xs font-bold text-slate-100">{getSignOccupants(1).join(' ') || '—'}</span>
              </div>
              <div className="p-2 border border-slate-800 rounded-xl bg-slate-900/60 flex flex-col justify-between">
                <span className="text-[10px] text-amber-400 font-bold">Ta</span>
                <span className="text-xs font-bold text-slate-100">{getSignOccupants(2).join(' ') || '—'}</span>
              </div>
              <div className="p-2 border border-slate-800 rounded-xl bg-slate-900/60 flex flex-col justify-between">
                <span className="text-[10px] text-amber-400 font-bold">Ge</span>
                <span className="text-xs font-bold text-slate-100">{getSignOccupants(3).join(' ') || '—'}</span>
              </div>

              <div className="p-2 border border-slate-800 rounded-xl bg-slate-900/60 flex flex-col justify-between">
                <span className="text-[10px] text-amber-400 font-bold">Aq</span>
                <span className="text-xs font-bold text-slate-100">{getSignOccupants(11).join(' ') || '—'}</span>
              </div>
              {/* Center Watermark Box (2x2) */}
              <div className="col-span-2 row-span-2 bg-[#070D1B] border border-amber-500/20 rounded-xl flex flex-col items-center justify-center p-2 text-center">
                <span className="text-amber-400 text-base font-black font-serif-heading">ASTROVISION</span>
                <span className="text-[10px] text-slate-400">South Indian Grid</span>
              </div>
              <div className="p-2 border border-slate-800 rounded-xl bg-slate-900/60 flex flex-col justify-between">
                <span className="text-[10px] text-amber-400 font-bold">Ca</span>
                <span className="text-xs font-bold text-slate-100">{getSignOccupants(4).join(' ') || '—'}</span>
              </div>

              <div className="p-2 border border-slate-800 rounded-xl bg-slate-900/60 flex flex-col justify-between">
                <span className="text-[10px] text-amber-400 font-bold">Cp</span>
                <span className="text-xs font-bold text-slate-100">{getSignOccupants(10).join(' ') || '—'}</span>
              </div>
              <div className="p-2 border border-slate-800 rounded-xl bg-slate-900/60 flex flex-col justify-between">
                <span className="text-[10px] text-amber-400 font-bold">Le</span>
                <span className="text-xs font-bold text-slate-100">{getSignOccupants(5).join(' ') || '—'}</span>
              </div>

              <div className="p-2 border border-slate-800 rounded-xl bg-slate-900/60 flex flex-col justify-between">
                <span className="text-[10px] text-amber-400 font-bold">Sg</span>
                <span className="text-xs font-bold text-slate-100">{getSignOccupants(9).join(' ') || '—'}</span>
              </div>
              <div className="p-2 border border-slate-800 rounded-xl bg-slate-900/60 flex flex-col justify-between">
                <span className="text-[10px] text-amber-400 font-bold">Sc</span>
                <span className="text-xs font-bold text-slate-100">{getSignOccupants(8).join(' ') || '—'}</span>
              </div>
              <div className="p-2 border border-slate-800 rounded-xl bg-slate-900/60 flex flex-col justify-between">
                <span className="text-[10px] text-amber-400 font-bold">Li</span>
                <span className="text-xs font-bold text-slate-100">{getSignOccupants(7).join(' ') || '—'}</span>
              </div>
              <div className="p-2 border border-slate-800 rounded-xl bg-slate-900/60 flex flex-col justify-between">
                <span className="text-[10px] text-amber-400 font-bold">Vi</span>
                <span className="text-xs font-bold text-slate-100">{getSignOccupants(6).join(' ') || '—'}</span>
              </div>
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
