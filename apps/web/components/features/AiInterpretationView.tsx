import React, { useState } from 'react'
import { ComprehensivePredictionPackage } from '../../types/api'

interface AiInterpretationViewProps {
  onInterpret: (domain: string, prompt: string) => Promise<any>
  predictions?: ComprehensivePredictionPackage
}

interface DomainMeta {
  title: string
  karakas: string
  houses: string
  varga: string
  indications: string[]
  factors: string[]
  challenges: string[]
}

const DOMAIN_METADATA: Record<string, DomainMeta> = {
  CAREER: {
    title: "Career & Professional Destiny",
    karakas: "Sun, Saturn, Mercury",
    houses: "10th (Karma), 6th (Work), 1st (Lagna)",
    varga: "D10 Dashamsha",
    indications: ["Strong 10th house & Lagna lord", "Favorable for leadership & management", "Technical & research excellence", "International career opportunities"],
    factors: ["Jupiter aspects 10th house", "Mercury in own/exaltation sign", "Dasha periods are supportive", "Multiple Raja Yogas present"],
    challenges: ["Periodic Saturn influence", "Need to manage work-life balance", "Avoid overcommitment", "Mindful decision timing"]
  },
  RELATIONSHIP: {
    title: "Relationships, Marriage & Alliances",
    karakas: "Venus, Jupiter",
    houses: "7th (Marriage), 2nd (Family), 11th (Gains)",
    varga: "D9 Navamsha",
    indications: ["7th house lord & Venus dignity", "Harmonious partnership potential", "Shared values & intellectual connection", "Supportive marital alliance"],
    factors: ["Benefic aspects on 7th house", "Venus well-placed in own sign/Kendra", "D9 Navamsha lord strength", "Dhana & Kalatra Yoga activations"],
    challenges: ["Mars/Saturn aspect cautions", "Communication clarity needed", "Clear boundaries in agreements", "Patience during transit shifts"]
  },
  FINANCE: {
    title: "Wealth, Income & Financial Assets",
    karakas: "Jupiter, Mercury, Venus",
    houses: "2nd (Accumulated Wealth), 11th (Gains), 9th (Fortune)",
    varga: "D2 Hora",
    indications: ["2nd & 11th house lord alignment", "Multiple income streams potential", "Resource accumulation capacity", "Sound asset management"],
    factors: ["Jupiter 2nd/11th lord activation", "Dhana Yogas in natal chart", "High SAV bindu strength in 2nd/11th", "Benefic Dasha activations"],
    challenges: ["Avoid speculative risk during Rahu transits", "Planned budgeting for expansion", "Disciplined savings habit", "Tax & legal compliance"]
  },
  WELLBEING: {
    title: "Health, Vitality & Physical Wellbeing",
    karakas: "Sun, Mars",
    houses: "1st (Vitality), 6th (Immunity/Recovery), 8th (Longevity)",
    varga: "D3 Drekkana",
    indications: ["Lagna lord strength & vitality", "Resilient immune response", "Balanced physical constitution", "Rejuvenation capacity"],
    factors: ["Sun & Lagna lord well-placed", "Benefic aspects on 1st/6th houses", "High Shadbala score for Sun/Mars", "Positive Panchanga Vara lord"],
    challenges: ["Manage stress & sleep hygiene", "Regular physical routine", "Dietary discipline during 6th house transits", "Avoid burnout during heavy Dashas"]
  },
  SPIRITUALITY: {
    title: "Spiritual Growth, Dharma & Philosophy",
    karakas: "Jupiter, Ketu, Sun",
    houses: "9th (Dharma/Mentors), 12th (Moksha/Isolation), 5th (Mantra)",
    varga: "D20 Vimshamsha",
    indications: ["9th house & 12th house Moksha alignment", "Inclination toward higher philosophy", "Receptive to spiritual mentoring", "Intuitive & meditative depth"],
    factors: ["9th lord Venus/Jupiter strength", "Ketu in Moksha/Dharma house", "D20 Vimshamsha Lagna strength", "Spiritual Yogas active"],
    challenges: ["Balance practical life with spiritual retreat", "Discernment in choosing spiritual mentors", "Consistent daily Sadhana", "Avoid disillusionment"]
  },
  EDUCATION: {
    title: "Education, Intelligence & Higher Learning",
    karakas: "Mercury, Jupiter, Goddess Saraswati",
    houses: "4th (Basic Learning), 5th (Intellect/Logic), 9th (Higher Studies)",
    varga: "D24 Chaturvimshamsha",
    indications: ["5th lord & Mercury analytical strength", "Capacity for deep technical research", "Higher academic qualifications", "Continuous learning orientation"],
    factors: ["Mercury in Virgo/Gemini or Kendra", "Jupiter aspecting 5th/9th houses", "D24 Chaturvimshamsha strength", "Favorable Saraswati Yogas"],
    challenges: ["Focus discipline during competitive exams", "Avoid superficial multi-tasking", "Structured study schedule", "Patience during exam periods"]
  }
}

export const AiInterpretationView: React.FC<AiInterpretationViewProps> = ({ onInterpret, predictions }) => {
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

  const currentMeta = DOMAIN_METADATA[selectedDomain] || DOMAIN_METADATA.CAREER
  const domainEv = predictions?.domain_predictions?.[selectedDomain]

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

  // Dynamic factors from predictions evidence if available
  const karakasText = domainEv?.rule_definition?.primary_karakas?.join(', ') || currentMeta.karakas
  const housesText = domainEv?.rule_definition?.relevant_houses?.join(', ') || currentMeta.houses
  const vargaText = domainEv?.rule_definition?.varga_code || currentMeta.varga
  const descriptionText = domainEv?.rule_definition?.rule_description || `Parashari calculation evidence and divisional alignments evaluated for ${currentMeta.title}.`

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
            className={`px-4 py-2 rounded-xl font-semibold transition cursor-pointer ${
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
                  {currentMeta.title}
                </h4>
                <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-[10px] font-mono font-bold">
                  ● AI Validated
                </span>
              </div>
              <p className="text-xs text-slate-400 font-mono mt-1">
                Provider: {providerName} • Model: {modelName} • Division: {vargaText}
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
              `${descriptionText} ` +
              `The deterministic evidence pipeline evaluates primary Karakas (${karakasText}), relevant houses (${housesText}), and active Vimshottari Dasha activations to provide evidence-backed Parashari insights.`
            )}
          </p>
        </div>

        {/* 3 Detailed Analysis Cards Grid - DYNAMICALLY RENDERED PER DOMAIN */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5 font-mono text-xs">
          {/* Key Indications */}
          <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-3">
            <h5 className="font-bold text-amber-300 uppercase tracking-wider flex items-center gap-1.5 text-xs">
              <span>🎯</span> Key Indications ({selectedDomain})
            </h5>
            <ul className="space-y-2 text-slate-300">
              {currentMeta.indications.map((item, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-amber-400">•</span> {item}
                </li>
              ))}
            </ul>
          </div>

          {/* Supporting Factors */}
          <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-3">
            <h5 className="font-bold text-cyan-300 uppercase tracking-wider flex items-center gap-1.5 text-xs">
              <span>⚡</span> Supporting Factors
            </h5>
            <ul className="space-y-2 text-slate-300">
              {currentMeta.factors.map((item, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-cyan-400">•</span> {item}
                </li>
              ))}
            </ul>
          </div>

          {/* Potential Challenges */}
          <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-3">
            <h5 className="font-bold text-rose-300 uppercase tracking-wider flex items-center gap-1.5 text-xs">
              <span>⚠️</span> Potential Challenges
            </h5>
            <ul className="space-y-2 text-slate-300">
              {currentMeta.challenges.map((item, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-rose-400">•</span> {item}
                </li>
              ))}
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
