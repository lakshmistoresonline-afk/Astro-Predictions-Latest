import React, { useState, useEffect } from 'react'
import { BirthProfileRequest } from '../../types/api'
import { fetchYoginiDasha } from '../../services/apiClient'

interface YoginiDashaViewProps {
  birthInput?: BirthProfileRequest | null
}

export const YoginiDashaView: React.FC<YoginiDashaViewProps> = ({ birthInput }) => {
  const [loading, setLoading] = useState(false)
  const [yoginiData, setYoginiData] = useState<any>(null)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)

  const handleLoadYogini = async () => {
    if (!birthInput) return
    setLoading(true)
    setErrorMsg(null)
    try {
      const data = await fetchYoginiDasha(birthInput)
      setYoginiData(data)
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to calculate Yogini Dasha.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (birthInput) {
      handleLoadYogini()
    }
  }, [birthInput])

  if (!birthInput) {
    return (
      <div className="bg-slate-900/80 backdrop-blur-xl p-8 rounded-3xl border border-slate-800 text-center space-y-4 font-mono select-none">
        <span className="text-3xl text-amber-300">⌛</span>
        <h3 className="text-xl font-bold text-amber-300">Yogini Dasha Timeline (36-Year Cycle)</h3>
        <p className="text-slate-400 text-xs">Please calculate a birth profile first to view Yogini Dasha timelines.</p>
      </div>
    )
  }

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none font-mono">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-xl font-extrabold text-amber-300 flex items-center gap-2 font-serif-heading">
            <span>⌛</span> Yogini Dasha Sequence (36-Year Traditional Cycle)
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Secondary Verification Dasha System: 8 Yoginis (Mangala through Sankata)
          </p>
        </div>
      </div>

      {loading ? (
        <div className="p-8 text-center bg-slate-950/40 rounded-2xl border border-slate-800 text-xs text-amber-300 animate-pulse">
          Calculating 36-Year Yogini Dasha sequence...
        </div>
      ) : errorMsg ? (
        <div className="p-4 bg-rose-500/10 border border-rose-500/30 text-rose-300 rounded-2xl text-xs">
          {errorMsg}
        </div>
      ) : yoginiData ? (
        <div className="space-y-6">
          {/* Active Yogini Banner */}
          {yoginiData.active_yogini && (
            <div className="p-5 rounded-2xl bg-slate-950/60 border border-amber-500/30 space-y-2">
              <span className="text-[10px] text-amber-300 font-bold uppercase tracking-widest">Active Yogini Dasha (Current Period)</span>
              <p className="text-lg font-black text-amber-300">
                {yoginiData.active_yogini.yogini_name} Dasha (Ruled by {yoginiData.active_yogini.ruling_planet})
              </p>
              <p className="text-xs text-slate-300 tabular-nums">
                Active Period: {yoginiData.active_yogini.start_date_iso} to {yoginiData.active_yogini.end_date_iso} ({yoginiData.active_yogini.duration_years} Years)
              </p>
            </div>
          )}

          {/* Yogini Sequence Table */}
          <div className="space-y-3">
            <h4 className="text-sm font-bold text-amber-300 font-serif-heading">Yogini Dasha Timeline Sequence</h4>
            <div className="overflow-x-auto rounded-2xl border border-slate-800 max-h-[500px] overflow-y-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-950 text-amber-300 text-[11px] uppercase tracking-wider sticky top-0 border-b border-slate-800">
                  <tr>
                    <th className="py-3 px-4">Yogini Name</th>
                    <th className="py-3 px-4">Ruling Planet</th>
                    <th className="py-3 px-4">Start Date</th>
                    <th className="py-3 px-4">End Date</th>
                    <th className="py-3 px-4">Duration (Years)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-slate-200">
                  {yoginiData.yogini_periods?.map((p: any, idx: number) => {
                    const isActive = yoginiData.active_yogini && yoginiData.active_yogini.yogini_name === p.yogini_name && yoginiData.active_yogini.start_date_iso === p.start_date_iso
                    return (
                      <tr key={idx} className={`hover:bg-slate-800/40 transition ${isActive ? 'bg-amber-500/10 font-bold text-amber-300' : ''}`}>
                        <td className="py-3 px-4 font-bold text-white flex items-center gap-2">
                          <span className={`w-1.5 h-1.5 rounded-full ${isActive ? 'bg-amber-400 animate-ping' : 'bg-slate-600'}`}></span>
                          {p.yogini_name}
                        </td>
                        <td className="py-3 px-4 text-cyan-300">{p.ruling_planet}</td>
                        <td className="py-3 px-4 text-slate-300 tabular-nums">{p.start_date_iso}</td>
                        <td className="py-3 px-4 text-slate-300 tabular-nums">{p.end_date_iso}</td>
                        <td className="py-3 px-4 font-bold text-slate-300 tabular-nums">{p.duration_years} Yrs</td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  )
}
