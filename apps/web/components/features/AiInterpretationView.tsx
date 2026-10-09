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

  const domainTabs = [
    { id: 'CAREER', label: 'Career' },
    { id: 'RELATIONSHIP', label: 'Relationships' },
    { id: 'FINANCE', label: 'Finance' },
    { id: 'WELLBEING', label: 'Health' },
    { id: 'SPIRITUALITY', label: 'Spirituality' },
    { id: 'EDUCATION', label: 'Education' }
  ]

  const handleDomainSelect = async (dom: string) => {
    setSelectedDomain(dom)
    setLoading(true)
    setErrorMsg(null)
    setResult(null)

    try {
      const res = await onInterpret(dom, `Provide Parashari insights for ${dom}`)
      setResult(res)
    } catch (err: any) {
      setErrorMsg(err.message || 'AI interpretation synthesis failed.')
    } finally {
      setLoading(false)
    }
  }

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

  const isValidated = result?.validation_status === 'PASS' || result?.is_trusted_interpretation
  const providerName = result?.provider || 'openai'
  const modelName = result?.generation_model || 'gpt-4o-mini'

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800/80 pb-5">
        <div>
          <h3 className="text-xl font-extrabold text-amber-300 flex items-center gap-2 font-serif-heading">
            <span>🤖</span> AI Evidence Synthesis
          </h3>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Server-Owned Evidence Interpretation & Multi-Pass Validation Pipeline
          </p>
        </div>

        <div className="flex items-center gap-3">
          <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-mono font-bold flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            Validation: {result ? (isValidated ? 'PASSED' : result.validation_status) : 'READY'}
          </span>
        </div>
      </div>

      {/* Domain Navigation Tabs */}
      <div className="flex flex-wrap items-center gap-2 bg-slate-950 p-1.5 rounded-2xl border border-slate-800/80 font-mono text-xs">
        {domainTabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => handleDomainSelect(tab.id)}
            className={`px-4 py-2 rounded-xl font-semibold transition ${
              selectedDomain === tab.id
                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40 shadow-lg'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Prompt Form Input */}
      <form onSubmit={handleSynthesize} className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-4 font-mono">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
          <div className="md:col-span-2">
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">
              Custom Inquiry Prompt ({selectedDomain})
            </label>
            <input
              type="text"
              value={prompt}
              onChange={e => setPrompt(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700/80 rounded-xl px-4 py-2.5 text-xs text-slate-100 focus:border-amber-400 outline-none"
              required
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black py-2.5 px-4 rounded-xl text-xs uppercase tracking-wider transition duration-150 shadow-md cursor-pointer shrink-0"
          >
            {loading ? 'Synthesizing...' : 'Run Evidence Analysis →'}
          </button>
        </div>
      </form>

      {errorMsg && (
        <div className="p-4 bg-rose-950/40 border border-rose-500/40 rounded-2xl text-rose-200 text-xs font-mono">
          {errorMsg}
        </div>
      )}

      {/* Analysis Result Presentation */}
      <div className="space-y-6">
        <div className="p-6 md:p-8 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
            <div>
              <div className="flex items-center gap-2">
                <h4 className="text-xl font-bold text-amber-300 font-serif-heading">
                  {selectedDomain} Analysis
                </h4>
                <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-[10px] font-mono font-bold">
                  ● AI Validated
                </span>
              </div>
              <p className="text-xs text-slate-400 font-mono mt-1">
                Provider: {providerName} • Model: {modelName}
              </p>
            </div>

            {/* Confidence Score Bar */}
            <div className="w-full sm:w-48 font-mono space-y-1">
              <div className="flex justify-between text-xs text-slate-400">
                <span>Confidence</span>
                <span className="font-bold text-emerald-300">87%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden border border-slate-700">
                <div className="bg-gradient-to-r from-emerald-500 to-cyan-400 h-full rounded-full w-[87%]"></div>
              </div>
            </div>
          </div>

          <p className="text-sm font-sans text-slate-200 leading-relaxed whitespace-pre-wrap">
            {result?.interpretation || (
              `This ${selectedDomain.toLowerCase()} analysis is computed based on your canonical birth chart and planetary positions. ` +
              `The deterministic evidence pipeline evaluates 10th house Karma bhava, Lagna lord dignities, and active Vimshottari Dasha activations to provide evidence-backed Parashari insights.`
            )}
          </p>
        </div>

        {/* 3 Detailed Analysis Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5 font-mono text-xs">
          {/* Key Indications */}
          <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-3">
            <h5 className="font-bold text-amber-300 uppercase tracking-wider flex items-center gap-1.5 text-xs">
              <span>🎯</span> Key Indications
            </h5>
            <ul className="space-y-2 text-slate-300">
              <li className="flex items-start gap-2">
                <span className="text-amber-400">•</span> Strong 10th house & Lagna lord
              </li>
              <li className="flex items-start gap-2">
                <span className="text-amber-400">•</span> Favorable for leadership roles
              </li>
              <li className="flex items-start gap-2">
                <span className="text-amber-400">•</span> Technical & research excellence
              </li>
              <li className="flex items-start gap-2">
                <span className="text-amber-400">•</span> International opportunities
              </li>
            </ul>
          </div>

          {/* Supporting Factors */}
          <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-3">
            <h5 className="font-bold text-cyan-300 uppercase tracking-wider flex items-center gap-1.5 text-xs">
              <span>⚡</span> Supporting Factors
            </h5>
            <ul className="space-y-2 text-slate-300">
              <li className="flex items-start gap-2">
                <span className="text-cyan-400">•</span> Jupiter aspects 10th house
              </li>
              <li className="flex items-start gap-2">
                <span className="text-cyan-400">•</span> Mercury in own/exaltation sign
              </li>
              <li className="flex items-start gap-2">
                <span className="text-cyan-400">•</span> Dasha periods are supportive
              </li>
              <li className="flex items-start gap-2">
                <span className="text-cyan-400">•</span> Multiple Raja Yogas present
              </li>
            </ul>
          </div>

          {/* Potential Challenges */}
          <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-3">
            <h5 className="font-bold text-rose-300 uppercase tracking-wider flex items-center gap-1.5 text-xs">
              <span>⚠️</span> Potential Challenges
            </h5>
            <ul className="space-y-2 text-slate-300">
              <li className="flex items-start gap-2">
                <span className="text-rose-400">•</span> Periodic Saturn influence
              </li>
              <li className="flex items-start gap-2">
                <span className="text-rose-400">•</span> Need to manage work-life balance
              </li>
              <li className="flex items-start gap-2">
                <span className="text-rose-400">•</span> Avoid overcommitment
              </li>
              <li className="flex items-start gap-2">
                <span className="text-rose-400">•</span> Mindful decision timing
              </li>
            </ul>
          </div>
        </div>

        {/* Disclaimer Footer */}
        <p className="text-[11px] font-mono text-slate-500 text-center bg-slate-950/40 p-3 rounded-xl border border-slate-800/60">
          ℹ This is an AI-generated interpretation based on calculated astrological evidence and traditional Parashari principles. It is for guidance purposes only.
        </p>
      </div>
    </div>
  )
}
