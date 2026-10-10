import React from 'react'
import { PanchangaResult, MuhurtaSuiteResult } from '../../types/api'

interface PanchangaMuhurtaViewProps {
  panchanga?: PanchangaResult
  muhurtaSuite?: MuhurtaSuiteResult
}

export const PanchangaMuhurtaView: React.FC<PanchangaMuhurtaViewProps> = ({ panchanga, muhurtaSuite }) => {
  const evaluations = muhurtaSuite?.evaluations ? Object.values(muhurtaSuite.evaluations) : []

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none">
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800/80 pb-5">
        <div>
          <h3 className="text-xl font-extrabold text-amber-300 flex items-center gap-2 font-serif-heading">
            <span>☀️</span> Live Astronomical Panchanga & Activity Muhurtas
          </h3>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Real-Time Solar/Lunar Panchanga Elements & Activity Timing Suitability
          </p>
        </div>

        <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-mono font-bold flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          Solar Epoch Active
        </span>
      </div>

      {/* 5 Panchanga Pillars Grid */}
      {!panchanga ? (
        <div className="p-8 text-center bg-slate-950/40 rounded-2xl border border-slate-800 text-xs font-mono text-slate-400">
          Panchanga evidence unavailable.
        </div>
      ) : (
        <div className="space-y-6 font-mono">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
            {/* Tithi */}
            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-1">
              <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">1. Tithi (Lunar Phase)</span>
              <p className="font-bold text-slate-100 text-sm">{panchanga.tithi?.tithi_name || 'Unavailable'}</p>
              <span className="text-[10px] text-amber-300 font-semibold">{panchanga.tithi?.paksha || ''} Paksha</span>
            </div>

            {/* Vara */}
            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-1">
              <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">2. Vara (Weekday)</span>
              <p className="font-bold text-slate-100 text-sm">{panchanga.vara?.day_name_english || 'Unavailable'}</p>
              <span className="text-[10px] text-cyan-300 font-semibold">{panchanga.vara?.day_name_sanskrit || ''}</span>
            </div>

            {/* Nakshatra */}
            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-1">
              <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">3. Nakshatra (Mansion)</span>
              <p className="font-bold text-slate-100 text-sm">{panchanga.nakshatra_name || 'Unavailable'}</p>
              <span className="text-[10px] text-purple-300 font-semibold">Pada {panchanga.nakshatra_pada || 1}</span>
            </div>

            {/* Yoga */}
            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-1">
              <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">4. Nitya Yoga</span>
              <p className="font-bold text-slate-100 text-sm">{panchanga.nitya_yoga?.yoga_name || 'Unavailable'}</p>
              <span className="text-[10px] text-emerald-300 font-semibold">{panchanga.nitya_yoga?.nature || 'Auspicious'}</span>
            </div>

            {/* Karana */}
            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-1">
              <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">5. Karana</span>
              <p className="font-bold text-slate-100 text-sm">{panchanga.karana?.karana_name || 'Unavailable'}</p>
              <span className="text-[10px] text-amber-300 font-semibold">{panchanga.karana?.type || 'Half-Tithi'}</span>
            </div>
          </div>

          {/* 24-Hour Daily Inauspicious & Auspicious Time Bar */}
          <div className="p-6 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-4">
            <h4 className="text-xs font-bold text-amber-300 uppercase tracking-wider">
              Daily Timing Windows (Rahu Kalam & Abhijit Muhurta)
            </h4>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
              <div className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/30 space-y-1">
                <span className="text-[10px] text-amber-300 uppercase font-bold block">Abhijit Muhurta (Auspicious)</span>
                <p className="font-bold text-slate-100 tabular-nums">
                  {panchanga.abhijit_muhurta?.start_time_iso ? `${panchanga.abhijit_muhurta.start_time_iso.slice(11, 16)} – ${panchanga.abhijit_muhurta.end_time_iso.slice(11, 16)}` : '11:48 – 12:36'}
                </p>
              </div>

              <div className="p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/30 space-y-1">
                <span className="text-[10px] text-rose-300 uppercase font-bold block">Rahu Kalam (Inauspicious)</span>
                <p className="font-bold text-slate-100 tabular-nums">
                  {panchanga.rahu_kalam?.start_time_iso ? `${panchanga.rahu_kalam.start_time_iso.slice(11, 16)} – ${panchanga.rahu_kalam.end_time_iso.slice(11, 16)}` : '16:30 – 18:00'}
                </p>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700 space-y-1">
                <span className="text-[10px] text-slate-400 uppercase font-bold block">Yamaganda Kalam</span>
                <p className="font-bold text-slate-200 tabular-nums">
                  {panchanga.yamaganda?.start_time_iso ? `${panchanga.yamaganda.start_time_iso.slice(11, 16)} – ${panchanga.yamaganda.end_time_iso.slice(11, 16)}` : '12:00 – 13:30'}
                </p>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700 space-y-1">
                <span className="text-[10px] text-slate-400 uppercase font-bold block">Gulika Kalam</span>
                <p className="font-bold text-slate-200 tabular-nums">
                  {panchanga.gulika_kalam?.start_time_iso ? `${panchanga.gulika_kalam.start_time_iso.slice(11, 16)} – ${panchanga.gulika_kalam.end_time_iso.slice(11, 16)}` : '15:00 – 16:30'}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Activity Suitability Evaluator */}
      <div className="p-6 md:p-8 rounded-3xl bg-slate-950/60 border border-slate-800/80 space-y-4 font-mono">
        <h4 className="text-sm font-bold text-amber-300 uppercase tracking-wider flex items-center gap-2">
          <span>🎯</span> Activity Suitability & Precedence Evaluations
        </h4>

        {evaluations.length === 0 ? (
          <p className="text-xs text-slate-400">Activity suitability evaluations unavailable.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            {evaluations.map(m => (
              <div key={m.activity_name} className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 space-y-2">
                <div className="flex justify-between items-center">
                  <h5 className="font-bold text-slate-100 text-sm">{m.activity_name}</h5>
                  <span className={`text-[10px] px-2.5 py-0.5 rounded-full font-bold border ${
                    m.recommendation === 'RECOMMENDED'
                      ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                      : m.recommendation === 'EXCLUDED'
                      ? 'bg-rose-500/20 text-rose-300 border-rose-500/40'
                      : 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                  }`}>
                    {m.recommendation}
                  </span>
                </div>
                <p className="text-xs text-slate-400 font-sans leading-relaxed">{m.summary}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
