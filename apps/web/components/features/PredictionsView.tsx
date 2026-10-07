import React from 'react'
import { ComprehensivePredictionPackage } from '../../types/api'

interface PredictionsViewProps {
  predictions?: ComprehensivePredictionPackage
}

export const PredictionsView: React.FC<PredictionsViewProps> = ({ predictions }) => {
  const domainPredictions = predictions?.domain_predictions ? Object.values(predictions.domain_predictions) : []

  return (
    <div className="bg-[#17163A]/90 p-8 rounded-3xl border border-[#F3E5AB]/30 shadow-2xl space-y-6 w-full">
      <h3 className="text-2xl font-extrabold text-[#F3E5AB]">14 Domain Prediction Evidence Packages</h3>

      {domainPredictions.length === 0 ? (
        <p className="text-sm text-[#A0A5C0]">Domain predictions unavailable.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {domainPredictions.map(d => (
            <div key={d.rule_definition.domain_code} className="p-6 bg-black/40 rounded-2xl border border-[#F3E5AB]/20 space-y-3">
              <div className="flex justify-between items-center">
                <h4 className="text-lg font-bold text-[#F3E5AB]">{d.rule_definition.domain_title}</h4>
                <span className={`text-xs px-3 py-1 rounded-full font-bold ${d.evidence_status === 'AVAILABLE' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'}`}>
                  {d.evidence_status}
                </span>
              </div>
              <p className="text-xs text-[#A0A5C0] leading-relaxed">{d.rule_definition.rule_description}</p>
              <div className="text-[11px] text-[#A0A5C0] pt-2 border-t border-[#F3E5AB]/10 space-y-1">
                <p><b>Primary Karakas:</b> {d.rule_definition.primary_karakas.join(', ')}</p>
                <p><b>Strength Class:</b> {d.evidence_strength_class || 'None'}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
