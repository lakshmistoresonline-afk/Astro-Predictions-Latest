import React, { useState } from 'react'

interface AiInterpretationViewProps {
  onInterpret: (domain: string, prompt: string) => Promise<any>
}

export const AiInterpretationView: React.FC<AiInterpretationViewProps> = ({ onInterpret }) => {
  const [selectedDomain, setSelectedDomain] = useState('CAREER')
  const [prompt, setPrompt] = useState('Provide clear Parashari insights for this domain.')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)

  const domains = [
    'CAREER', 'FINANCE', 'BUSINESS', 'MARRIAGE', 'RELATIONSHIP',
    'EDUCATION', 'FAMILY', 'CHILDREN', 'PROPERTY', 'TRAVEL',
    'RELOCATION', 'SPIRITUALITY', 'PERSONAL_DEVELOPMENT', 'WELLBEING'
  ]

  const handleSynthesize = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setErrorMsg(null)
    setResult(null)

    try {
      const res = await onInterpret(selectedDomain, prompt)
      setResult(res)
    } catch (err: any) {
      setErrorMsg(err.message || 'AI interpretation synthesis failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-[#17163A]/90 p-8 md:p-12 rounded-3xl border border-[#F3E5AB]/30 shadow-2xl space-y-6 w-full max-w-4xl mx-auto">
      <h3 className="text-2xl font-extrabold text-[#F3E5AB]">Server-Owned AI Evidence Interpretation</h3>
      <p className="text-xs text-[#A0A5C0]">The server owns all astrological evidence. AI interprets server-generated facts without calculation override.</p>

      <form onSubmit={handleSynthesize} className="space-y-4">
        <div>
          <label className="block text-xs font-bold uppercase tracking-widest text-[#A0A5C0] mb-2">Select Prediction Domain</label>
          <select
            value={selectedDomain}
            onChange={e => setSelectedDomain(e.target.value)}
            className="w-full bg-[#050816] border border-[#F3E5AB]/40 rounded-2xl p-4 text-[#FFFFF0] focus:border-[#F3E5AB] outline-none transition text-sm"
          >
            {domains.map(d => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-xs font-bold uppercase tracking-widest text-[#A0A5C0] mb-2">Topic / Question Prompt</label>
          <input
            type="text"
            value={prompt}
            onChange={e => setPrompt(e.target.value)}
            className="w-full bg-[#050816] border border-[#F3E5AB]/40 rounded-2xl p-4 text-[#FFFFF0] focus:border-[#F3E5AB] outline-none transition text-sm"
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-gradient-to-r from-[#F3E5AB] to-[#F7E792] text-[#050816] font-extrabold py-4 rounded-2xl shadow-xl hover:opacity-95 transition"
        >
          {loading ? 'Synthesizing AI Interpretation...' : `Interpret Domain Evidence (${selectedDomain})`}
        </button>
      </form>

      {errorMsg && (
        <div className="p-4 bg-rose-950/80 border border-rose-500/50 rounded-2xl text-rose-200 text-xs">
          {errorMsg}
        </div>
      )}

      {result && (
        <div className="p-6 bg-black/40 rounded-2xl border border-[#F3E5AB]/30 space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm font-bold text-[#F3E5AB]">Interpretation for {result.domain}</span>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-bold">
              Status: {result.validation_status}
            </span>
          </div>
          <p className="text-xs text-[#A0A5C0]">Provider: {result.provider} | Model: {result.generation_model}</p>
          <div className="pt-3 border-t border-[#F3E5AB]/10 text-xs text-[#FFFFF0] leading-relaxed whitespace-pre-wrap">
            {result.interpretation}
          </div>
        </div>
      )}
    </div>
  )
}
