import React, { useState, useMemo } from 'react'
import { CanonicalVedicChart, PlanetaryVedicPlacement } from '../../types/api'

interface PlanetaryPositionsTableProps {
  chart: CanonicalVedicChart
}

export const PlanetaryPositionsTable: React.FC<PlanetaryPositionsTableProps> = ({ chart }) => {
  const [searchTerm, setSearchTerm] = useState('')
  const [sortField, setSortField] = useState<'body_name' | 'sign' | 'degree' | 'house'>('body_name')
  const [sortAsc, setSortAsc] = useState(true)

  const placements = chart?.placements ? Object.values(chart.placements) : []

  const handleSort = (field: 'body_name' | 'sign' | 'degree' | 'house') => {
    if (sortField === field) {
      setSortAsc(!sortAsc)
    } else {
      setSortField(field)
      setSortAsc(true)
    }
  }

  const filteredAndSortedPlacements = useMemo(() => {
    return placements
      .filter(p => {
        if (!searchTerm.trim()) return true
        const q = searchTerm.toLowerCase()
        return (
          p.body_name.toLowerCase().includes(q) ||
          p.rashi?.sign.toLowerCase().includes(q) ||
          p.nakshatra_pada?.nakshatra.toLowerCase().includes(q)
        )
      })
      .sort((a, b) => {
        let valA: any = a.body_name
        let valB: any = b.body_name

        if (sortField === 'sign') {
          valA = a.rashi?.sign || ''
          valB = b.rashi?.sign || ''
        } else if (sortField === 'degree') {
          valA = a.sidereal_longitude || 0
          valB = b.sidereal_longitude || 0
        } else if (sortField === 'house') {
          valA = a.rashi?.sign_index || 0
          valB = b.rashi?.sign_index || 0
        }

        if (valA < valB) return sortAsc ? -1 : 1
        if (valA > valB) return sortAsc ? 1 : -1
        return 0
      })
  }, [placements, searchTerm, sortField, sortAsc])

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h3 className="text-xl font-extrabold text-amber-300 flex items-center gap-2">
            <span>🪐</span> Verified Planetary Ledger & Positions
          </h3>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Chitra Paksha (Lahiri Ayanamsha) Sidereal Longitudes & Whole-Sign Bhavas
          </p>
        </div>

        <div className="relative w-full sm:w-64">
          <input
            type="text"
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            placeholder="Search planet, sign, nakshatra..."
            className="w-full bg-slate-950/80 border border-slate-700/80 rounded-xl px-3.5 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-amber-400/60 font-mono"
          />
          {searchTerm && (
            <button
              onClick={() => setSearchTerm('')}
              className="absolute right-3 top-2.5 text-xs text-slate-400 hover:text-white"
            >
              ✕
            </button>
          )}
        </div>
      </div>

      {filteredAndSortedPlacements.length === 0 ? (
        <div className="p-8 text-center bg-slate-950/40 rounded-2xl border border-slate-800 text-xs font-mono text-slate-400">
          No matching planetary placements found.
        </div>
      ) : (
        <div className="overflow-x-auto rounded-2xl border border-slate-800/80">
          <table className="w-full text-left text-xs md:text-sm">
            <thead className="bg-slate-950/90 text-amber-300 font-mono text-[11px] uppercase tracking-wider sticky top-0 z-10 border-b border-slate-800">
              <tr>
                <th
                  onClick={() => handleSort('body_name')}
                  className="py-3 px-4 cursor-pointer hover:bg-slate-900 transition"
                >
                  Graha (Body) {sortField === 'body_name' ? (sortAsc ? '▲' : '▼') : ''}
                </th>
                <th
                  onClick={() => handleSort('sign')}
                  className="py-3 px-4 cursor-pointer hover:bg-slate-900 transition"
                >
                  Rashi (Sign) {sortField === 'sign' ? (sortAsc ? '▲' : '▼') : ''}
                </th>
                <th
                  onClick={() => handleSort('degree')}
                  className="py-3 px-4 cursor-pointer hover:bg-slate-900 transition"
                >
                  Degree {sortField === 'degree' ? (sortAsc ? '▲' : '▼') : ''}
                </th>
                <th
                  onClick={() => handleSort('house')}
                  className="py-3 px-4 cursor-pointer hover:bg-slate-900 transition"
                >
                  House {sortField === 'house' ? (sortAsc ? '▲' : '▼') : ''}
                </th>
                <th className="py-3 px-4">Nakshatra & Pada</th>
                <th className="py-3 px-4">Motion</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-200 font-mono text-xs">
              {filteredAndSortedPlacements.map(p => (
                <tr key={p.body_name} className="hover:bg-slate-800/40 transition">
                  <td className="py-3 px-4 font-bold text-white flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
                    {p.body_name}
                  </td>
                  <td className="py-3 px-4 font-semibold text-amber-200">{p.rashi?.sign || 'N/A'}</td>
                  <td className="py-3 px-4 tabular-nums">
                    {p.rashi?.degree !== undefined ? `${p.rashi.degree}° ${String(p.rashi.minute).padStart(2, '0')}′` : 'N/A'}
                  </td>
                  <td className="py-3 px-4 tabular-nums text-slate-300">
                    House {p.rashi?.sign_index || '-'}
                  </td>
                  <td className="py-3 px-4 text-purple-300">
                    {p.nakshatra_pada?.nakshatra || 'N/A'}{' '}
                    <span className="text-purple-400 font-bold">(P{p.nakshatra_pada?.pada || '-'})</span>
                  </td>
                  <td className="py-3 px-4">
                    <span className={`px-2.5 py-1 rounded-full text-[10px] font-extrabold tracking-wider ${p.retrograde ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40' : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'}`}>
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
