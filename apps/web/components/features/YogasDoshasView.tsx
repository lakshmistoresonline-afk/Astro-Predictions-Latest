import React from 'react'
import { YogaSuiteResult, DoshaSuiteResult } from '../../types/api'

interface YogasDoshasViewProps {
  yogaSuite?: YogaSuiteResult
  doshaSuite?: DoshaSuiteResult
}

export const YogasDoshasView: React.FC<YogasDoshasViewProps> = ({ yogaSuite, doshaSuite }) => {
  const yogas = yogaSuite?.detected_yogas || []
  const doshas = doshaSuite?.detected_doshas || []

  return (
    <div className="space-y-8 w-full">
      {/* Detected Yogas */}
      <div className="bg-[#17163A]/90 p-8 rounded-3xl border border-[#F3E5AB]/30 shadow-2xl space-y-4">
        <h3 className="text-2xl font-extrabold text-[#F3E5AB]">Detected Classical Yogas ({yogas.length})</h3>
        {yogas.length === 0 ? (
          <p className="text-sm text-[#A0A5C0]">No classical Yogas detected for this chart.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {yogas.map((y, i) => (
              <div key={i} className="p-4 bg-black/30 rounded-2xl border border-[#F3E5AB]/20 space-y-2">
                <div className="flex justify-between items-center">
                  <h4 className="font-bold text-white text-base">{y.name}</h4>
                  <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-[#F3E5AB]/20 text-[#F3E5AB] font-extrabold">
                    {y.category}
                  </span>
                </div>
                {y.sanskrit_name && (
                  <p className="text-xs text-[#A0A5C0] italic">{y.sanskrit_name}</p>
                )}
                <div className="text-[11px] text-[#A0A5C0] space-y-1 pt-1 border-t border-[#F3E5AB]/10">
                  <p><b>Planets:</b> {y.participating_planets.join(', ') || 'None'}</p>
                  <p><b>Houses:</b> {y.participating_houses.join(', ') || 'None'}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Detected Doshas */}
      <div className="bg-[#17163A]/90 p-8 rounded-3xl border border-[#F3E5AB]/30 shadow-2xl space-y-4">
        <h3 className="text-2xl font-extrabold text-[#F3E5AB]">Detected Doshas ({doshas.length})</h3>
        {doshas.length === 0 ? (
          <p className="text-sm text-[#A0A5C0]">No classical Doshas detected for this chart.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {doshas.map((d, i) => (
              <div key={i} className="p-4 bg-black/30 rounded-2xl border border-[#F3E5AB]/20 space-y-2">
                <div className="flex justify-between items-center">
                  <h4 className="font-bold text-white text-base">{d.name}</h4>
                  <span className={`text-[10px] px-2.5 py-0.5 rounded-full font-extrabold ${d.status === 'CANCELLED' ? 'bg-amber-500/20 text-amber-200' : 'bg-rose-500/20 text-rose-200'}`}>
                    {d.status}
                  </span>
                </div>
                <p className="text-xs text-[#A0A5C0]"><b>Planets:</b> {d.participating_planets.join(', ') || 'None'}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
