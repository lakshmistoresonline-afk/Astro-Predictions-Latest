import React, { useState } from 'react'
import { ComprehensivePredictionPackage } from '../../types/api'

interface PredictionsViewProps {
  predictions?: ComprehensivePredictionPackage
}

export const PredictionsView: React.FC<PredictionsViewProps> = ({ predictions }) => {
  const [searchTerm, setSearchTerm] = useState('')
  const domainPredictions = predictions?.domain_predictions ? Object.values(predictions.domain_predictions) : []

  const filteredPredictions = domainPredictions.filter(d => {
    if (!searchTerm.trim()) return true
    const q = searchTerm.toLowerCase()
    return (
      d.rule_definition.domain_title.toLowerCase().includes(q) ||
      d.rule_definition.domain_code.toLowerCase().includes(q) ||
      d.rule_definition.rule_description.toLowerCase().includes(q)
    )
  })

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h3 className="text-xl font-extrabold text-amber-300 flex items-center gap-2">
            <span>🎯</span> 14 Domain Master Predictions Engine
          </h3>
          <p className="text-xs text-slate-400 font-mono mt-1">
            5-Layer Convergent Evidence Packages Across All Key Life Vectors
          </p>
        </div>

        <div className="relative w-full sm:w-64">
          <input
            type="text"
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            placeholder="Search domain or keyword..."
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

      {filteredPredictions.length === 0 ? (
        <div className="p-8 text-center bg-slate-950/40 rounded-2xl border border-slate-800 text-xs font-mono text-slate-400">
          No matching prediction domains found.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 font-mono">
          {filteredPredictions.map(d => {
            const isAvail = d.evidence_status === 'AVAILABLE' || d.evidence_status === 'PASS'

            return (
              <div
                key={d.rule_definition.domain_code}
                className="p-6 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-3 hover:border-amber-500/40 transition duration-200"
              >
                <div className="flex items-center justify-between gap-2">
                  <h4 className="text-base font-bold text-amber-300">
                    {d.rule_definition.domain_title}
                  </h4>
                  <span className={`text-[10px] px-2.5 py-1 rounded-full font-bold border shrink-0 ${
                    isAvail
                      ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                      : 'bg-rose-500/20 text-rose-300 border-rose-500/40'
                  }`}>
                    {d.evidence_status}
                  </span>
                </div>

                <p className="text-xs text-slate-300 font-sans leading-relaxed">
                  {d.rule_definition.rule_description}
                </p>

                <div className="pt-3 border-t border-slate-800/60 grid grid-cols-2 gap-2 text-[11px] text-slate-400">
                  <div>
                    <span className="text-slate-500 block text-[10px]">Primary Karakas</span>
                    <strong className="text-slate-200">{d.rule_definition.primary_karakas.join(', ') || '—'}</strong>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px]">Division / Varga</span>
                    <strong className="text-cyan-300">{d.rule_definition.varga_code || 'D1'}</strong>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
