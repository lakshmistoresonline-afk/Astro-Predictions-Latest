import React, { useState, useEffect } from 'react'
import { BirthProfileRequest } from '../../types/api'
import { fetchVarshaphal } from '../../services/apiClient'

interface TajikaVarshaphalViewProps {
  birthInput?: BirthProfileRequest | null
}

export const TajikaVarshaphalView: React.FC<TajikaVarshaphalViewProps> = ({ birthInput }) => {
  const currentYear = new Date().getFullYear()
  const [targetYear, setTargetYear] = useState<number>(currentYear)
  const [loading, setLoading] = useState(false)
  const [varshaphalData, setVarshaphalData] = useState<any>(null)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)

  const handleCalculateVarshaphal = async (yearVal: number) => {
    if (!birthInput) return
    setLoading(true)
    setErrorMsg(null)
    try {
      const data = await fetchVarshaphal(birthInput, yearVal)
      setVarshaphalData(data)
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to calculate Tajika Varshaphal.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (birthInput) {
      handleCalculateVarshaphal(targetYear)
    }
  }, [birthInput])

  if (!birthInput) {
    return (
      <div className="bg-slate-900/80 backdrop-blur-xl p-8 rounded-3xl border border-slate-800 text-center space-y-4 font-mono select-none">
        <span className="text-3xl text-amber-300">☀️</span>
        <h3 className="text-xl font-bold text-amber-300">Tajika Varshaphal Annual Return</h3>
        <p className="text-slate-400 text-xs">Please calculate a birth profile first to view annual solar return predictions.</p>
      </div>
    )
  }

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h3 className="text-xl font-extrabold text-amber-300 flex items-center gap-2 font-serif-heading">
            <span>☀️</span> Tajika Varshaphal (Annual Solar Return Engine)
          </h3>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Annual Solar Return Chart, Muntha Sign, Varsheshwara & Mudda Dasha Sequence
          </p>
        </div>

        {/* Year Switcher */}
        <div className="flex items-center gap-2 font-mono bg-slate-950 p-1.5 rounded-xl border border-slate-800">
          <button
            onClick={() => {
              const prev = targetYear - 1
              setTargetYear(prev)
              handleCalculateVarshaphal(prev)
            }}
            className="px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold transition"
          >
            ← {targetYear - 1}
          </button>
          <span className="px-3 py-1 text-xs font-black text-amber-300 bg-amber-500/10 border border-amber-500/30 rounded-lg">
            {targetYear} (Age {targetYear - birthInput.year})
          </span>
          <button
            onClick={() => {
              const next = targetYear + 1
              setTargetYear(next)
              handleCalculateVarshaphal(next)
            }}
            className="px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold transition"
          >
            {targetYear + 1} →
          </button>
        </div>
      </div>

      {loading ? (
        <div className="p-8 text-center bg-slate-950/40 rounded-2xl border border-slate-800 font-mono text-xs text-amber-300 animate-pulse">
          Calculating Tajika Varshaphal for Year {targetYear}...
        </div>
      ) : errorMsg ? (
        <div className="p-4 bg-rose-500/10 border border-rose-500/30 text-rose-300 rounded-2xl font-mono text-xs">
          {errorMsg}
        </div>
      ) : varshaphalData ? (
        <div className="space-y-6 font-mono">
          {/* Key Metric Highlights Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-1">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider">Annual Target Age</span>
              <p className="text-xl font-black text-amber-300">{varshaphalData.native_age} Years Old</p>
            </div>
            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-1">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider">Varsha Lagna (Rising Sign)</span>
              <p className="text-xl font-black text-cyan-300">{varshaphalData.varsha_lagna_sign}</p>
            </div>
            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-1">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider">Varsheshwara (Year Lord)</span>
              <p className="text-xl font-black text-emerald-300">{varshaphalData.varsheshwara_year_lord}</p>
            </div>
            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-1">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider">Muntha Sign & House</span>
              <p className="text-xl font-black text-purple-300">{varshaphalData.muntha_rashi_name} (House {varshaphalData.muntha_house_from_varsha_lagna})</p>
            </div>
          </div>

          {/* Annual Executive Summary */}
          <div className="p-5 rounded-2xl bg-slate-950/60 border border-amber-500/30 space-y-2">
            <h4 className="text-sm font-bold text-amber-300 font-serif-heading">Annual Strategic Summary ({targetYear})</h4>
            <p className="text-xs text-slate-200 font-sans leading-relaxed">{varshaphalData.annual_summary}</p>
          </div>

          {/* Mudda Dasha 365-Day Timeline Table */}
          <div className="space-y-3">
            <h4 className="text-sm font-bold text-amber-300 font-serif-heading">Mudda Dasha Sequence ({targetYear} Solar Year)</h4>
            <div className="overflow-x-auto rounded-2xl border border-slate-800">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-950 text-amber-300 text-[11px] uppercase tracking-wider border-b border-slate-800">
                  <tr>
                    <th className="py-3 px-4">Mudda Dasha Lord</th>
                    <th className="py-3 px-4">Start Date</th>
                    <th className="py-3 px-4">End Date</th>
                    <th className="py-3 px-4">Duration (Days)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-slate-200">
                  {varshaphalData.mudda_dasha_timeline?.map((p: any, idx: number) => (
                    <tr key={idx} className="hover:bg-slate-800/40 transition">
                      <td className="py-3 px-4 font-bold text-white flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
                        {p.lord}
                      </td>
                      <td className="py-3 px-4 text-cyan-300 tabular-nums">{p.start_date_iso}</td>
                      <td className="py-3 px-4 text-cyan-300 tabular-nums">{p.end_date_iso}</td>
                      <td className="py-3 px-4 font-bold text-slate-300 tabular-nums">{p.duration_days} Days</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  )
}
