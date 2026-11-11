import React, { useState } from 'react'
import { evaluatePrashna } from '../../services/apiClient'

export const PrashnaView: React.FC = () => {
  const [selectedDomain, setSelectedDomain] = useState('CAREER')
  const [loading, setLoading] = useState(false)
  const [prashnaResult, setPrashnaResult] = useState<any>(null)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)

  const handleEvaluate = async () => {
    setLoading(true)
    setErrorMsg(null)
    try {
      const data = await evaluatePrashna(selectedDomain, 13.0827, 80.2707)
      setPrashnaResult(data)
    } catch (err: any) {
      setErrorMsg(err.message || 'Prashna evaluation failed.')
    } finally {
      setLoading(false)
    }
  }

  const domainOptions = [
    { code: 'CAREER', title: 'Career / Job Offer' },
    { code: 'FINANCE', title: 'Wealth / Money Gains' },
    { code: 'MARRIAGE', title: 'Marriage / Relationship' },
    { code: 'PROPERTY', title: 'Real Estate / Vehicle' },
    { code: 'HEALTH', title: 'Health / Immunity' },
    { code: 'TRAVEL', title: 'Foreign Journey' },
    { code: 'LITIGATION', title: 'Legal Dispute / Competition' }
  ]

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none font-mono">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-xl font-extrabold text-amber-300 flex items-center gap-2 font-serif-heading">
            <span>🔮</span> Prashna (Query-Time Horary Astrology)
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Real-time Horary Chart, Ithasala/Esarpha Yogas & Karya Siddhi Probability Score
          </p>
        </div>

        <button
          onClick={handleEvaluate}
          disabled={loading}
          className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-500 text-slate-950 font-black text-xs uppercase tracking-wider shadow-lg shadow-amber-500/20 transition cursor-pointer"
        >
          {loading ? 'Evaluating Instant Chart...' : '🔮 Ask Question Now'}
        </button>
      </div>

      {/* Query Domain Selector */}
      <div className="space-y-2">
        <label className="text-xs font-bold text-slate-300 uppercase tracking-wider block">Select Query Domain:</label>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {domainOptions.map(opt => (
            <button
              key={opt.code}
              onClick={() => setSelectedDomain(opt.code)}
              className={`p-3 rounded-xl border text-xs text-left transition cursor-pointer ${
                selectedDomain === opt.code
                  ? 'bg-amber-500/20 text-amber-300 border-amber-500/50 font-bold'
                  : 'bg-slate-950/60 text-slate-400 border-slate-800 hover:text-white'
              }`}
            >
              {opt.title}
            </button>
          ))}
        </div>
      </div>

      {errorMsg && (
        <div className="p-4 bg-rose-500/10 border border-rose-500/30 text-rose-300 rounded-2xl text-xs">
          {errorMsg}
        </div>
      )}

      {/* Prashna Result Display */}
      {prashnaResult && (
        <div className="space-y-6 pt-2">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-1">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider">Prashna Lagna</span>
              <p className="text-lg font-black text-cyan-300">{prashnaResult.prashna_lagna_sign} ({prashnaResult.lagna_lord})</p>
            </div>
            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-1">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider">Karya Bhava & Lord</span>
              <p className="text-lg font-black text-amber-300">{prashnaResult.karya_lord} ({prashnaResult.karya_house_description})</p>
            </div>
            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-1">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider">Ithasala Aspect Yoga</span>
              <p className={`text-lg font-black ${prashnaResult.ithasala_yoga_present ? 'text-emerald-300' : 'text-slate-400'}`}>
                {prashnaResult.ithasala_yoga_present ? 'PRESENT (Applying)' : 'ABSENT'}
              </p>
            </div>
            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-1">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider">Karya Siddhi Score</span>
              <p className="text-lg font-black text-emerald-300">{prashnaResult.karya_siddhi_score}% ({prashnaResult.verdict})</p>
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-slate-950/60 border border-amber-500/30 space-y-2">
            <h4 className="text-sm font-bold text-amber-300 font-serif-heading">Horary Prashna Guidance</h4>
            <p className="text-xs text-slate-200 font-sans leading-relaxed">{prashnaResult.guidance_summary}</p>
          </div>
        </div>
      )}
    </div>
  )
}
