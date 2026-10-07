import React from 'react'
import { JaiminiSuiteResult } from '../../types/api'

interface JaiminiViewProps {
  jaiminiSuite?: JaiminiSuiteResult
}

export const JaiminiView: React.FC<JaiminiViewProps> = ({ jaiminiSuite }) => {
  const karakas = jaiminiSuite?.chara_karakas ? Object.values(jaiminiSuite.chara_karakas) : []

  return (
    <div className="bg-[#17163A]/90 p-8 rounded-3xl border border-[#F3E5AB]/30 shadow-2xl space-y-6 w-full">
      <h3 className="text-2xl font-extrabold text-[#F3E5AB]">Jaimini Sutra Astrolabe & 7 Chara Karakas</h3>

      {!jaiminiSuite ? (
        <p className="text-sm text-[#A0A5C0]">Jaimini suite evidence unavailable.</p>
      ) : (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 bg-black/40 rounded-2xl border border-[#F3E5AB]/20 space-y-1">
              <span className="text-xs uppercase font-extrabold text-[#F3E5AB]">Arudha Lagna (AL)</span>
              <p className="text-2xl font-bold text-white">{jaiminiSuite.arudha_lagna_rashi_name} (Sign {jaiminiSuite.arudha_lagna_rashi_index})</p>
            </div>
            <div className="p-6 bg-black/40 rounded-2xl border border-[#F3E5AB]/20 space-y-1">
              <span className="text-xs uppercase font-extrabold text-[#F3E5AB]">Upapada Lagna (UL)</span>
              <p className="text-2xl font-bold text-white">{jaiminiSuite.upapada_lagna_rashi_name} (Sign {jaiminiSuite.upapada_lagna_rashi_index})</p>
            </div>
            <div className="p-6 bg-black/40 rounded-2xl border border-[#F3E5AB]/20 space-y-1">
              <span className="text-xs uppercase font-extrabold text-[#F3E5AB]">Karakamsha (D9 AK Sign)</span>
              <p className="text-2xl font-bold text-white">{jaiminiSuite.karakamsha_rashi_name} (Sign {jaiminiSuite.karakamsha_rashi_index})</p>
            </div>
          </div>

          <div className="space-y-3">
            <h4 className="text-lg font-bold text-white">7 Chara Karaka Assignments</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {karakas.map(k => (
                <div key={k.karaka_code} className="p-4 bg-black/30 rounded-xl border border-[#F3E5AB]/20 space-y-1">
                  <div className="flex justify-between items-center">
                    <span className="text-xs font-black text-[#F3E5AB]">{k.karaka_code}</span>
                    <span className="text-[10px] text-[#A0A5C0]">{k.karaka_name}</span>
                  </div>
                  <p className="text-lg font-bold text-white">{k.planet}</p>
                  <p className="text-[11px] text-[#A0A5C0]">{k.degree_in_sign}° in sign</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
