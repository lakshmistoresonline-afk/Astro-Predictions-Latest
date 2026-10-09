import React, { useState } from 'react'
import { YogaSuiteResult, DoshaSuiteResult } from '../../types/api'

interface YogasDoshasViewProps {
  yogaSuite?: YogaSuiteResult
  doshaSuite?: DoshaSuiteResult
}

export const YogasDoshasView: React.FC<YogasDoshasViewProps> = ({ yogaSuite, doshaSuite }) => {
  const [activeSubTab, setActiveSubTab] = useState<'yogas' | 'doshas'>('yogas')
  const yogas = yogaSuite?.detected_yogas || []
  const doshas = doshaSuite?.detected_doshas || []

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h3 className="text-xl font-extrabold text-amber-300 flex items-center gap-2">
            <span>⚖</span> Classical Yoga Audit & Doshas Evidence
          </h3>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Parashari Structural Conditions, Viparita Yogas & Cancellation Exceptions
          </p>
        </div>

        <div className="flex bg-slate-950 p-1 rounded-xl border border-slate-800 font-mono">
          <button
            onClick={() => setActiveSubTab('yogas')}
            className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition ${
              activeSubTab === 'yogas' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : 'text-slate-400 hover:text-white'
            }`}
          >
            Detected Yogas ({yogas.length})
          </button>
          <button
            onClick={() => setActiveSubTab('doshas')}
            className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition ${
              activeSubTab === 'doshas' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : 'text-slate-400 hover:text-white'
            }`}
          >
            Doshas & Exceptions ({doshas.length})
          </button>
        </div>
      </div>

      {activeSubTab === 'yogas' ? (
        yogas.length === 0 ? (
          <div className="p-8 text-center bg-slate-950/40 rounded-2xl border border-slate-800 text-xs font-mono text-slate-400">
            No classical Yogas detected for this natal configuration.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {yogas.map((y, i) => (
              <div key={i} className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-3 font-mono hover:border-amber-500/40 transition">
                <div className="flex justify-between items-start gap-2">
                  <div>
                    <h4 className="font-bold text-slate-100 text-base">{y.name}</h4>
                    {y.sanskrit_name && (
                      <p className="text-xs text-amber-300/80 italic font-sans">{y.sanskrit_name}</p>
                    )}
                  </div>
                  <span className="text-[10px] px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-bold shrink-0">
                    {y.category || 'DETECTED'}
                  </span>
                </div>

                <div className="text-xs text-slate-300 space-y-1.5 pt-2 border-t border-slate-800/60">
                  <p><span className="text-slate-500">Planets:</span> <strong className="text-amber-200">{y.participating_planets.join(', ') || 'None'}</strong></p>
                  <p><span className="text-slate-500">Houses:</span> <strong className="text-cyan-300">{y.participating_houses.join(', ') || 'None'}</strong></p>
                </div>
              </div>
            ))}
          </div>
        )
      ) : (
        doshas.length === 0 ? (
          <div className="p-8 text-center bg-slate-950/40 rounded-2xl border border-slate-800 text-xs font-mono text-slate-400">
            No classical Doshas detected for this natal configuration.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {doshas.map((d, i) => (
              <div key={i} className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-3 font-mono hover:border-amber-500/40 transition">
                <div className="flex justify-between items-start gap-2">
                  <h4 className="font-bold text-slate-100 text-base">{d.name}</h4>
                  <span className={`text-[10px] px-2.5 py-1 rounded-full font-bold border shrink-0 ${
                    d.status === 'CANCELLED'
                      ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                      : 'bg-rose-500/20 text-rose-300 border-rose-500/40'
                  }`}>
                    {d.status}
                  </span>
                </div>

                <div className="text-xs text-slate-300 space-y-1.5 pt-2 border-t border-slate-800/60">
                  <p><span className="text-slate-500">Participating Planets:</span> <strong className="text-amber-200">{d.participating_planets.join(', ') || 'None'}</strong></p>
                </div>
              </div>
            ))}
          </div>
        )
      )}
    </div>
  )
}
