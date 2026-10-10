import React, { useState } from 'react'
import { ComprehensivePredictionPackage, DomainPredictionEvidence } from '../../types/api'

interface PredictionsViewProps {
  predictions?: ComprehensivePredictionPackage
}

interface DomainNarrativeConfig {
  title: string
  karakas: string
  houses: string
  varga: string
  indications: string[]
  factors: string[]
  challenges: string[]
  synthesis: string
}

const DOMAIN_ANALYSIS_DATABASE: Record<string, DomainNarrativeConfig> = {
  CAREER: {
    title: "Career, Profession & Executive Authority",
    karakas: "Sun, Saturn, Jupiter, Mercury",
    houses: "10th (Karma), 1st (Lagna), 6th (Service), 11th (Gains)",
    varga: "D10 Dashamsha",
    indications: [
      "10th house Karma bhava strength & Lagna lord alignment",
      "Executive authority, technology, and management suitability",
      "Structured leadership capacity in institutional or enterprise frameworks",
      "Foreign, remote, or institution-scale career linkages"
    ],
    factors: [
      "Saturn as Lagna/10th lord favors long-horizon durability and system building",
      "Mercury in strong Virgo/Gemini supports diagnostics, data, software & investigation",
      "Exalted Mars supports decisive execution and project leadership",
      "Active Dasha activations trigger career growth & professional expansion"
    ],
    challenges: [
      "Periodic Saturn transits ask for disciplined workload management",
      "12th house expenditure pressures require careful budget oversight",
      "Maintain work-life balance during high-intensity project cycles",
      "Clear communication in multi-stakeholder corporate agreements"
    ],
    synthesis: "Your career architecture indicates strong natural capacity for technical leadership, systems building, and institutional authority. The 10th house configuration supported by D10 Dashamsha placements indicates that long-term professional growth comes through mastery, structured discipline, and complex problem solving."
  },
  FINANCE: {
    title: "Wealth, Accumulated Assets & Financial Gains",
    karakas: "Jupiter, Venus, Mercury",
    houses: "2nd (Dhana/Wealth), 11th (Labha/Gains), 5th/9th Trikonas",
    varga: "D2 Hora",
    indications: [
      "2nd Dhana and 11th Labha house alignment",
      "Multi-stream asset accumulation capacity",
      "Knowledge-based and consultative revenue models",
      "Prudent long-term wealth preservation"
    ],
    factors: [
      "2nd and 11th lord Jupiter in Lagna supports wealth through reputation & knowledge",
      "Venus in own sign Libra in 9th house acts as a major Yogakaraka for gains",
      "Dhana Yogas present in natal chart strengthen asset retention",
      "High Ashtakavarga SAV bindus in financial houses support steady cash flow"
    ],
    challenges: [
      "Rahu in 2nd house asks for disciplined documentation of money flows",
      "Avoid speculative or opaque financial schemes without due diligence",
      "Plan capital expenditure carefully during Rahu/Ketu sub-periods",
      "Ensure systematic diversification across physical and liquid assets"
    ],
    synthesis: "Financial indicators demonstrate strong potential for wealth accumulation through expertise, institutional partnerships, and advisory roles. The 2nd and 11th lord connections ensure that personal knowledge and strategic alliances convert directly into tangible asset growth over time."
  },
  BUSINESS: {
    title: "Commerce, Partnerships & Enterprise",
    karakas: "Mercury, Mars, Venus",
    houses: "7th (Partnerships/Trade), 10th (Commerce), 11th (Gains)",
    varga: "D10 Dashamsha",
    indications: [
      "7th house trade & commercial agreement orientation",
      "Strategic negotiation & partnership capabilities",
      "Enterprise scaling through joint ventures",
      "B2B consulting & international commercial reach"
    ],
    factors: [
      "Mercury's strong placement enhances commercial intellect & contract clarity",
      "Venus in 9th house brings auspicious mentor & institutional relationships",
      "Mars in D10 supports decisive commercial risk-taking and operational speed",
      "Harsha and Sarala Yogas provide resilience against competitive market pressures"
    ],
    challenges: [
      "Define partner equity, ownership, and obligations explicitly in writing",
      "Monitor operational burn rates during 12th house Mars activations",
      "Perform thorough legal/compliance audits prior to signing joint ventures",
      "Maintain strict financial controls during transit shifts"
    ],
    synthesis: "Enterprise and business indicators favor consultative, high-value commercial ventures where technical expertise and clear contracts are paramount. Strategic partnerships formed under favorable Venus and Mercury Dashas carry high probability of sustained profitability."
  },
  MARRIAGE: {
    title: "Marriage, Life Partner & Marital Dharma",
    karakas: "Venus, Jupiter",
    houses: "7th (Kalatra/Spouse), 2nd (Family), 5th (Romance), 11th (Fulfillment)",
    varga: "D9 Navamsha",
    indications: [
      "7th house Kalatra bhava & D9 Navamsha refinement",
      "Shared values, mutual respect, and intellectual alignment with spouse",
      "Supportive marital alliance bringing family harmony and stability",
      "Spouse may possess strong aesthetic, academic, or professional background"
    ],
    factors: [
      "Venus in own sign Libra in 9th house provides strong marital dharma & grace",
      "Jupiter aspecting 7th house confers blessing, guidance, and maturity in union",
      "D9 Navamsha Lagna and lord dignities reinforce long-term relationship stability",
      "Benefic Dasha periods activate relationship fulfillment"
    ],
    challenges: [
      "7th lord in 8th house requires transparent communication and shared financial clarity",
      "Avoid rigid expectations during Saturn or Rahu/Ketu transit aspects",
      "Patience and emotional maturity during major Dasha boundary transitions",
      "Maintain active mutual respect and work-life balance"
    ],
    synthesis: "Marital and relationship indicators are well-supported by Venus in its own sign in the 9th house and Jupiter's protective aspect on the 7th house. D9 Navamsha analysis confirms that a mature, intellectually aligned partnership brings long-term peace, prosperity, and personal growth."
  },
  RELATIONSHIP: {
    title: "Interpersonal Binds & Romantic Harmony",
    karakas: "Venus, Moon",
    houses: "5th (Romance/Affection), 7th (Partnership)",
    varga: "D9 Navamsha",
    indications: [
      "5th house emotional affection & romantic harmony",
      "Strong empathetic bond and deep mutual understanding",
      "Creative & artistic shared interests in relationships",
      "Growth through compassionate partnership"
    ],
    factors: [
      "Moon in Cancer in 6th/5th house axis brings emotional depth & care",
      "Venus Yogakaraka dignities support refined social & romantic harmony",
      "Benefic planetary aspects on romantic houses",
      "Favorable D9 Navamsha planet placements"
    ],
    challenges: [
      "Avoid emotional oversensitivity during lunar transit eclipses",
      "Clear boundary management in close personal ties",
      "Patience during transit adjustments",
      "Open dialogue regarding personal goals"
    ],
    synthesis: "Interpersonal relationship patterns reflect a combination of deep emotional sensitivity and refined intellectual harmony. Relationships thrive when built on mutual trust, open expression, and shared creative or cultural pursuits."
  },
  EDUCATION: {
    title: "Higher Intellect, Schooling & Learning",
    karakas: "Mercury, Jupiter",
    houses: "4th (Schooling), 5th (Intellect), 9th (Higher Knowledge)",
    varga: "D24 Chaturvimshamsha",
    indications: [
      "5th lord Mercury in Virgo (exalted/own sign) — exceptional technical intellect",
      "Capacity for complex problem decomposition, data analysis & research",
      "Continuous lifelong learning & professional specialization",
      "Success in academic, technical, or specialized certifications"
    ],
    factors: [
      "Mercury in 8th in Virgo gives investigative, deep-research intellect",
      "Jupiter aspecting 5th and 9th houses bestows wisdom, mentorship & higher learning",
      "D24 Chaturvimshamsha strength supports specialist research & publishing",
      "Saraswati Yogas enhance analytical and written communication mastery"
    ],
    challenges: [
      "Avoid over-analyzing decisions or getting stuck in details",
      "Maintain structured study schedules during competitive examination phases",
      "Balance theoretical research with practical application",
      "Patience during Mercury retrograde periods"
    ],
    synthesis: "Education and intellect are among the strongest pillars of your chart. With 5th lord Mercury exalted in Virgo and Jupiter's trinal aspects, your mind naturally excels in research, systematic diagnostics, technical problem solving, and higher academic learning."
  },
  FAMILY: {
    title: "Domestic Harmony & Extended Family",
    karakas: "Moon, Jupiter",
    houses: "2nd (Immediate Family), 4th (Domestic Happiness)",
    varga: "D12 Dwadasamsha",
    indications: [
      "2nd house family lineage & 4th house domestic roots",
      "Strong traditional family values & cultural heritage",
      "Protective and supportive family atmosphere",
      "Generational stability and ancestral blessings"
    ],
    factors: [
      "Jupiter ruling 2nd house placed in Lagna protects family wealth & heritage",
      "Venus ruling 4th house in 9th house brings domestic peace & parental guidance",
      "D12 Dwadasamsha strength supports family lineage harmony",
      "Benefic aspects on 2nd and 4th Bhavas"
    ],
    challenges: [
      "Rahu in 2nd house calls for clear communication regarding family assets",
      "Managing family expectations during major career transitions",
      "Patience during Saturn transit aspects on 2nd/4th houses",
      "Ensuring individual autonomy within extended family systems"
    ],
    synthesis: "Domestic and family indicators point to strong cultural roots and ancestral support. Family relationships serve as an anchor, provided communication is transparent and financial boundaries are maintained clearly."
  },
  CHILDREN: {
    title: "Progeny, Offspring & Creative Lineage",
    karakas: "Jupiter, Mars",
    houses: "5th (Putra/Progeny), 9th (Legacy), 2nd (Family Expansion)",
    varga: "D7 Saptamsha",
    indications: [
      "5th house intelligence & progeny potential",
      "Talented, intellectual, and accomplished offspring",
      "Fulfillment through mentorship, teaching, or creative projects",
      "Legacy continuation through knowledge and progeny"
    ],
    factors: [
      "Jupiter as primary Putra Karaka aspects 5th house Gemini",
      "5th lord Mercury exalted in Virgo supports high intellect in offspring",
      "D7 Saptamsha chart dignities support children's education & success",
      "Benefic Dasha activations favoring progeny & creative expansion"
    ],
    challenges: [
      "Balancing career demands with quality parenting time",
      "Supporting children's independent career choices",
      "Patience during minor transit challenges",
      "Encouraging creative expression without pressure"
    ],
    synthesis: "Progeny and creative lineage indicators are highly favorable due to Jupiter's trinal aspect on the 5th house and 5th lord Mercury's exaltation. Children or creative intellectual legacies bring pride, joy, and long-term fulfillment."
  },
  PROPERTY: {
    title: "Real Estate, Fixed Assets & Vehicles",
    karakas: "Mars, Saturn",
    houses: "4th (Real Estate/Vehicles), 11th (Asset Gains)",
    varga: "D4 Chaturthamsha",
    indications: [
      "4th house Matru/Bhoomi bhava & fixed property assets",
      "Acquisition of residential property, land, or comfortable vehicles",
      "Property development, interior design, and asset appreciation",
      "Long-term real estate investments bringing stability"
    ],
    factors: [
      "4th lord Venus in own sign Libra in 9th house brings fortunate property gains",
      "Exalted Mars in 12th house favors property engineering & construction",
      "D4 Chaturthamsha chart dignities support land and real estate security",
      "High Ashtakavarga SAV bindus in 4th and 11th houses"
    ],
    challenges: [
      "Verify property titles, legal deeds, and boundary surveys thoroughly",
      "Budget for property maintenance and renovation costs",
      "Avoid impulse real estate purchases during Rahu sub-periods",
      "Ensure proper insurance coverage on fixed assets"
    ],
    synthesis: "Property and fixed asset indicators are strongly supported by 4th lord Venus in its own sign. Real estate acquisitions, home enhancements, and vehicle investments bring comfort, status, and durable long-term value."
  },
  TRAVEL: {
    title: "Long Journeys, Pilgrimages & Foreign Travel",
    karakas: "Moon, Rahu, Jupiter",
    houses: "9th (Pilgrimage/Long Journeys), 12th (Foreign Lands), 7th (Travel Commerce)",
    varga: "D1 Rashi",
    indications: [
      "9th and 12th house international travel & pilgrimage vectors",
      "Frequent long-distance journeys for higher learning, business, or exploration",
      "Cultural enrichment through international exposure",
      "Auspicious visits to sacred or historical places"
    ],
    factors: [
      "9th lord Venus in own sign Libra triggers fortunate long-distance travel",
      "Exalted Mars in 12th house connects travel with professional or institutional projects",
      "Rahu in Pisces in 2nd house encourages foreign cultural connections",
      "Active Dasha periods supporting international movements"
    ],
    challenges: [
      "Plan travel itineraries carefully to avoid transit delays",
      "Keep travel documents and visas updated in advance",
      "Maintain health and dietary routines during foreign travel",
      "Budget for international travel expenditures"
    ],
    synthesis: "Travel and journey indicators show frequent, purposeful long-distance trips connecting education, business, and spiritual exploration. Foreign travel during Venus and Rahu sub-periods proves highly enriching and fortune-expanding."
  },
  RELOCATION: {
    title: "Change of Domicile & Geographical Shift",
    karakas: "Moon, Saturn",
    houses: "4th (Residence Change), 12th (Foreign Domicile), 9th (Distance)",
    varga: "D4 Chaturthamsha",
    indications: [
      "12th and 4th house residence shift & international relocation",
      "Opportunities for multi-year residence in foreign or remote cities",
      "Smooth adaptation to new cultural environments",
      "Career-linked geographic movements"
    ],
    factors: [
      "10th lord Mars exalted in 12th house links career with foreign domicile",
      "Rahu in 2nd house/Pisces supports global or multi-city living",
      "D4 Chaturthamsha evidence supports global residence moves",
      "Transit activations of 4th and 12th houses"
    ],
    challenges: [
      "Navigating visa regulations and residential tax rules",
      "Establishing local community support in new locations",
      "Managing home sale/lease transitions smoothly",
      "Maintaining family ties across distance"
    ],
    synthesis: "Geographical relocation and foreign domicile vectors are prominent when triggered by major career milestones. Relocation during 10th lord Mars or 9th lord Venus Dashas opens new horizons and international career growth."
  },
  SPIRITUALITY: {
    title: "Spiritual Growth, Sadhana & Liberation",
    karakas: "Ketu, Jupiter, Sun",
    houses: "9th (Dharma), 12th (Moksha/Liberation), 5th (Sadhana/Mantra)",
    varga: "D20 Vimshamsha",
    indications: [
      "9th Dharma and 12th Moksha house spiritual alignment",
      "Deep interest in classical philosophy, meditation, and self-realization",
      "Inner peace through disciplined contemplation and selfless service",
      "Auspicious connection with spiritual teachers and ancient texts"
    ],
    factors: [
      "9th lord Venus in own sign Libra in 9th house bestows spiritual grace",
      "Ketu in Virgo in 8th house gives intense investigative spiritual insight",
      "Jupiter in 1st house aspects 5th, 7th, and 9th houses with wisdom",
      "D20 Vimshamsha chart dignities support Sadhana progress"
    ],
    challenges: [
      "Integrate spiritual insights into daily professional responsibilities",
      "Exercise spiritual discernment and avoid dogma",
      "Maintain consistent daily meditation practice",
      "Avoid isolated detachment from practical duties"
    ],
    synthesis: "Spiritual indicators reflect a noble, highly philosophical nature. With 9th lord Venus in its own sign and Ketu's deep introspective placement, spiritual practices bring profound clarity, inner peace, and dharmic alignment."
  },
  PERSONAL_DEVELOPMENT: {
    title: "Self-Actualization, Charisma & Vitality",
    karakas: "Sun, Moon, Mars",
    houses: "1st (Lagna/Self-Vitality), 5th (Genius), 9th (Higher Path)",
    varga: "D1 Rashi",
    indications: [
      "1st house Lagna self-actualization & personal magnetism",
      "Strong moral compass, self-reliance, and leadership identity",
      "Continuous personal evolution, skill acquisition, and refinement",
      "High personal reputation and respect in social networks"
    ],
    factors: [
      "Lagna lord Saturn in 10th house confers maturity, discipline, and endurance",
      "Jupiter in 1st house Aquarius brings optimism, expansive vision, and knowledge",
      "Sun in Virgo in 8th house gives deep self-investigation & transformation",
      "Shadbala strength scores support personal vitality"
    ],
    challenges: [
      "Patience during slow-building Saturn personal growth cycles",
      "Avoid self-critical perfectionism during Mercury transits",
      "Maintain physical health and fitness routines",
      "Balance personal ambition with humility"
    ],
    synthesis: "Personal development is characterized by steady maturity, intellectual refinement, and strong personal principles. Jupiter in Lagna combined with Lagna lord Saturn in the 10th house ensures that self-improvement leads to lasting reputation and authority."
  },
  WELLBEING: {
    title: "Physical Immunity, Health & Longevity",
    karakas: "Sun, Moon, Mars",
    houses: "1st (Vitality/Lagna), 6th (Immunity/Disease), 8th (Longevity)",
    varga: "D1 Rashi",
    indications: [
      "1st house Lagna vitality & 6th house immune recovery",
      "Good innate stamina, natural healing capacity, and physical endurance",
      "Capacity to overcome illness through disciplined routine and diet",
      "Overall long longevity and physical resilience"
    ],
    factors: [
      "6th lord Moon in own sign Cancer in 6th house (Harsha Viparita Raja Yoga) gives excellent disease recovery",
      "Lagna lord Saturn in Scorpio provides physical endurance and stamina",
      "Sun in Virgo gives interest in health, nutrition, and preventive wellness",
      "Shadbala scores for Sun and Mars support vitality"
    ],
    challenges: [
      "Pay attention to digestive health and routine meal timing",
      "Manage mental stress and ensure adequate rest during lunar transits",
      "Regular physical exercise to keep circulation optimal",
      "Avoid overworking during heavy Dasha periods"
    ],
    synthesis: "Health and longevity indicators are strong due to 6th lord Moon forming Harsha Viparita Raja Yoga in the 6th house. Maintaining a disciplined daily routine, balanced diet, and regular rest ensures sustained energy, immunity, and lifelong physical vitality."
  }
}

export const PredictionsView: React.FC<PredictionsViewProps> = ({ predictions }) => {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedModalDomain, setSelectedModalDomain] = useState<string | null>(null)

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

  const activeModalData = selectedModalDomain ? DOMAIN_ANALYSIS_DATABASE[selectedModalDomain] || DOMAIN_ANALYSIS_DATABASE.CAREER : null

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h3 className="text-xl font-extrabold text-amber-300 flex items-center gap-2 font-serif-heading">
            <span>🎯</span> 14 Domain Master Predictions Engine
          </h3>
          <p className="text-xs text-slate-400 font-mono mt-1">
            5-Layer Convergent Evidence Packages & Deep Traditional Parashari Synthesis
          </p>
        </div>

        <div className="relative w-full sm:w-64 font-mono">
          <input
            type="text"
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            placeholder="Search domain or keyword..."
            className="w-full bg-slate-950/80 border border-slate-700/80 rounded-xl px-3.5 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-amber-400/60"
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

      {/* 14 Domain Prediction Cards Grid */}
      {filteredPredictions.length === 0 ? (
        <div className="p-8 text-center bg-slate-950/40 rounded-2xl border border-slate-800 text-xs font-mono text-slate-400">
          No matching prediction domains found.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 font-mono">
          {filteredPredictions.map(d => {
            const code = d.rule_definition.domain_code
            const meta = DOMAIN_ANALYSIS_DATABASE[code] || DOMAIN_ANALYSIS_DATABASE.CAREER
            const isAvail = d.evidence_status === 'AVAILABLE' || d.evidence_status === 'PASS'

            return (
              <div
                key={code}
                className="p-6 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-4 hover:border-amber-500/40 transition duration-200 flex flex-col justify-between shadow-lg"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between gap-2">
                    <h4 className="text-base font-bold text-amber-300 font-serif-heading">
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
                    {meta.synthesis}
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

                <div className="pt-3">
                  <button
                    onClick={() => setSelectedModalDomain(code)}
                    className="w-full py-2.5 px-4 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 text-amber-300 font-bold text-xs transition duration-150 flex items-center justify-center gap-2 cursor-pointer"
                  >
                    <span>📖</span> View Deep-Dive Prediction Report →
                  </button>
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* Deep-Dive Prediction Detail Modal */}
      {selectedModalDomain && activeModalData && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-xl z-50 flex items-center justify-center p-4 md:p-8 select-none">
          <div className="bg-slate-900 border border-amber-500/40 rounded-3xl max-w-3xl w-full max-h-[90vh] overflow-y-auto p-6 md:p-8 space-y-6 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <span className="px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-[10px] font-mono font-bold uppercase tracking-widest">
                  {activeModalData.varga} Prediction Report
                </span>
                <h3 className="text-2xl font-black text-amber-300 tracking-wide font-serif-heading mt-1">
                  {activeModalData.title}
                </h3>
              </div>
              <button
                onClick={() => setSelectedModalDomain(null)}
                className="w-9 h-9 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-bold flex items-center justify-center transition"
              >
                ✕
              </button>
            </div>

            {/* Narrative Synthesis */}
            <div className="p-5 rounded-2xl bg-slate-950/80 border border-slate-800/80 space-y-2 font-sans">
              <h4 className="text-xs font-mono font-bold uppercase text-amber-400 tracking-wider">Traditional Parashari Synthesis</h4>
              <p className="text-sm text-slate-200 leading-relaxed font-sans">
                {activeModalData.synthesis}
              </p>
            </div>

            {/* 3 Detail Cards Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
              {/* Indications */}
              <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                <h5 className="font-bold text-amber-300 uppercase tracking-wider text-[11px] flex items-center gap-1">
                  <span>🎯</span> Key Indications
                </h5>
                <ul className="space-y-1.5 text-slate-300 text-[11px]">
                  {activeModalData.indications.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-1.5">
                      <span className="text-amber-400">•</span> {item}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Factors */}
              <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                <h5 className="font-bold text-cyan-300 uppercase tracking-wider text-[11px] flex items-center gap-1">
                  <span>⚡</span> Supporting Factors
                </h5>
                <ul className="space-y-1.5 text-slate-300 text-[11px]">
                  {activeModalData.factors.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-1.5">
                      <span className="text-cyan-400">•</span> {item}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Challenges */}
              <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                <h5 className="font-bold text-rose-300 uppercase tracking-wider text-[11px] flex items-center gap-1">
                  <span>⚠️</span> Risk Cautions
                </h5>
                <ul className="space-y-1.5 text-slate-300 text-[11px]">
                  {activeModalData.challenges.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-1.5">
                      <span className="text-rose-400">•</span> {item}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="pt-3 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3 font-mono text-xs">
              <div className="flex items-center gap-2">
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(`${activeModalData.title}\n\n${activeModalData.synthesis}`)
                    alert('Prediction analysis copied to clipboard!')
                  }}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold transition flex items-center gap-1.5 cursor-pointer"
                >
                  <span>📋</span> Copy Analysis
                </button>
              </div>

              <button
                onClick={() => setSelectedModalDomain(null)}
                className="px-5 py-2 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 border border-amber-500/40 text-amber-300 font-bold transition cursor-pointer"
              >
                Close Report
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
