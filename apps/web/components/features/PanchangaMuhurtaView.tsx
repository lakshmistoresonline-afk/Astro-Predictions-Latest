import React from 'react'
import { PanchangaResult, MuhurtaSuiteResult } from '../../types/api'

interface PanchangaMuhurtaViewProps {
  panchanga?: PanchangaResult
  muhurtaSuite?: MuhurtaSuiteResult
}

export const PanchangaMuhurtaView: React.FC<PanchangaMuhurtaViewProps> = ({ panchanga, muhurtaSuite }) => {
  const evaluations = muhurtaSuite?.evaluations ? Object.values(muhurtaSuite.evaluations) : []

  return (
    <div className="space-y-8 w-full">
      {/* Panchanga */}
      <div className="bg-[#17163A]/90 p-8 rounded-3xl border border-[#F3E5AB]/30 shadow-2xl space-y-6">
        <h3 className="text-2xl font-extrabold text-[#F3E5AB]">Live Astronomical Panchanga</h3>

        {!panchanga ? (
          <p className="text-sm text-[#A0A5C0]">Panchanga evidence unavailable.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="p-4 bg-black/40 rounded-2xl border border-[#F3E5AB]/20 space-y-1">
              <span className="text-xs uppercase font-bold text-[#A0A5C0]">Tithi</span>
              <p className="text-lg font-bold text-white">{panchanga.tithi?.tithi_name || 'Unavailable'} ({panchanga.tithi?.paksha || ''})</p>
            </div>
            <div className="p-4 bg-black/40 rounded-2xl border border-[#F3E5AB]/20 space-y-1">
              <span className="text-xs uppercase font-bold text-[#A0A5C0]">Vara</span>
              <p className="text-lg font-bold text-white">{panchanga.vara?.day_name_english || 'Unavailable'} ({panchanga.vara?.day_name_sanskrit || ''})</p>
            </div>
            <div className="p-4 bg-black/40 rounded-2xl border border-[#F3E5AB]/20 space-y-1">
              <span className="text-xs uppercase font-bold text-[#A0A5C0]">Nakshatra & Pada</span>
              <p className="text-lg font-bold text-white">{panchanga.nakshatra_name || 'Unavailable'} (Pada {panchanga.nakshatra_pada || ''})</p>
            </div>
            <div className="p-4 bg-black/40 rounded-2xl border border-[#F3E5AB]/20 space-y-1">
              <span className="text-xs uppercase font-bold text-[#A0A5C0]">Nitya Yoga</span>
              <p className="text-lg font-bold text-white">{panchanga.nitya_yoga?.yoga_name || 'Unavailable'}</p>
            </div>
            <div className="p-4 bg-black/40 rounded-2xl border border-[#F3E5AB]/20 space-y-1">
              <span className="text-xs uppercase font-bold text-[#A0A5C0]">Karana</span>
              <p className="text-lg font-bold text-white">{panchanga.karana?.karana_name || 'Unavailable'}</p>
            </div>
            <div className="p-4 bg-black/40 rounded-2xl border border-[#F3E5AB]/20 space-y-1">
              <span className="text-xs uppercase font-bold text-[#A0A5C0]">Rahu Kalam Window</span>
              <p className="text-xs font-bold text-white">
                {panchanga.rahu_kalam?.start_time_iso ? `${panchanga.rahu_kalam.start_time_iso.slice(11, 16)} - ${panchanga.rahu_kalam.end_time_iso.slice(11, 16)}` : 'Unavailable'}
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Activity Muhurtas */}
      <div className="bg-[#17163A]/90 p-8 rounded-3xl border border-[#F3E5AB]/30 shadow-2xl space-y-6">
        <h3 className="text-2xl font-extrabold text-[#F3E5AB]">Activity Muhurtas & Precedence Recommendations</h3>

        {evaluations.length === 0 ? (
          <p className="text-sm text-[#A0A5C0]">Muhurta evaluations unavailable.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {evaluations.map(m => (
              <div key={m.activity_name} className="p-4 bg-black/40 rounded-2xl border border-[#F3E5AB]/20 space-y-2">
                <div className="flex justify-between items-center">
                  <h4 className="font-extrabold text-white text-base">{m.activity_name}</h4>
                  <span className={`text-[10px] px-2.5 py-0.5 rounded-full font-black ${m.recommendation === 'RECOMMENDED' ? 'bg-emerald-500/20 text-emerald-300' : (m.recommendation === 'EXCLUDED' ? 'bg-rose-500/20 text-rose-300' : 'bg-amber-500/20 text-amber-200')}`}>
                    {m.recommendation}
                  </span>
                </div>
                <p className="text-xs text-[#A0A5C0]">{m.summary}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
