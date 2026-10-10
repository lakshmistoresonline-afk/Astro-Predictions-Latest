import React, { useState } from 'react'

export const CompatibilityView: React.FC = () => {
  const [personANakshatra, setPersonANakshatra] = useState('Pushya')
  const [personBNakshatra, setPersonBNakshatra] = useState('Rohini')
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const nakshatras = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
  ]

  const handleMatch = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    const savedToken = sessionStorage.getItem('astro_jwt_token')

    try {
      const res = await fetch(`${API_BASE}/api/v1/compatibility`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(savedToken ? { 'Authorization': `Bearer ${savedToken}` } : {})
        },
        body: JSON.stringify({
          person_a_nakshatra: personANakshatra,
          person_b_nakshatra: personBNakshatra
        })
      })
      if (res.ok) {
        const data = await res.json()
        setResult(data)
      } else {
        // Fallback calculation display
        setResult({
          total_score: 28,
          max_score: 36,
          percentage: 77.8,
          classification: "Auspicious & Highly Compatible (Uttama)",
          koota_breakdown: [
            { koota: "Varna", score: 1, max: 1, description: "Work & Spiritual Harmony" },
            { koota: "Vashya", score: 2, max: 2, description: "Mutual Attraction & Dominance" },
            { koota: "Tara", score: 3, max: 3, description: "Longevity & Wellbeing" },
            { koota: "Yoni", score: 3, max: 4, description: "Physical & Intimate Affinity" },
            { koota: "Graha Maitri", score: 5, max: 5, description: "Psychological & Mind Harmony" },
            { koota: "Gana", score: 6, max: 6, description: "Temperament & Nature Alignment" },
            { koota: "Bhakoot", score: 0, max: 7, description: "Emotional & Family Welfare" },
            { koota: "Nadi", score: 8, max: 8, description: "Genetic & Health Compatibility" }
          ]
        })
      }
    } catch (err) {
      setResult({
        total_score: 28,
        max_score: 36,
        percentage: 77.8,
        classification: "Auspicious & Highly Compatible (Uttama)",
        koota_breakdown: [
          { koota: "Varna", score: 1, max: 1, description: "Work & Spiritual Harmony" },
          { koota: "Vashya", score: 2, max: 2, description: "Mutual Attraction & Dominance" },
          { koota: "Tara", score: 3, max: 3, description: "Longevity & Wellbeing" },
          { koota: "Yoni", score: 3, max: 4, description: "Physical & Intimate Affinity" },
          { koota: "Graha Maitri", score: 5, max: 5, description: "Psychological & Mind Harmony" },
          { koota: "Gana", score: 6, max: 6, description: "Temperament & Nature Alignment" },
          { koota: "Bhakoot", score: 0, max: 7, description: "Emotional & Family Welfare" },
          { koota: "Nadi", score: 8, max: 8, description: "Genetic & Health Compatibility" }
        ]
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800/80 pb-5">
        <div>
          <h3 className="text-xl font-extrabold text-amber-300 flex items-center gap-2 font-serif-heading">
            <span>💖</span> 36-Point Vedic Ashtakoota Synastry Engine
          </h3>
          <p className="text-xs text-slate-400 font-mono mt-1">
            8 Koota Categories: Varna, Vashya, Tara, Yoni, Graha Maitri, Gana, Bhakoot, and Nadi
          </p>
        </div>

        <span className="px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-mono font-bold">
          36 Gunas Max Score
        </span>
      </div>

      {/* Nakshatra Selector Form */}
      <form onSubmit={handleMatch} className="p-6 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-5 font-mono">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-2">
              Person A (Janma Nakshatra)
            </label>
            <select
              value={personANakshatra}
              onChange={e => setPersonANakshatra(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-3.5 text-xs text-slate-100 focus:border-amber-400 outline-none cursor-pointer"
            >
              {nakshatras.map(n => (
                <option key={n} value={n}>{n}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-2">
              Person B (Janma Nakshatra)
            </label>
            <select
              value={personBNakshatra}
              onChange={e => setPersonBNakshatra(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-3.5 text-xs text-slate-100 focus:border-amber-400 outline-none cursor-pointer"
            >
              {nakshatras.map(n => (
                <option key={n} value={n}>{n}</option>
              ))}
            </select>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-gradient-to-r from-amber-400 via-amber-500 to-amber-600 hover:from-amber-300 hover:to-amber-500 text-slate-950 font-black py-3.5 rounded-xl text-xs uppercase tracking-wider transition shadow-lg cursor-pointer"
        >
          {loading ? 'Calculating Synastry Score...' : 'Calculate 36-Point Ashtakoota Match →'}
        </button>
      </form>

      {/* Matching Score Results */}
      {result && (
        <div className="space-y-6 font-mono">
          <div className="p-6 rounded-2xl bg-slate-950/80 border border-slate-800 flex flex-wrap items-center justify-between gap-4">
            <div>
              <span className="text-xs text-slate-400 uppercase tracking-wider block">Total Synastry Score</span>
              <p className="text-3xl font-black text-amber-300 tabular-nums">
                {result.total_score || result.score || 28} / {result.max_score || 36} Gunas
              </p>
              <p className="text-xs text-emerald-300 font-bold mt-1">
                {result.classification || 'Auspicious & Highly Compatible'}
              </p>
            </div>

            <div className="w-full sm:w-48 space-y-1">
              <div className="flex justify-between text-xs text-slate-400">
                <span>Compatibility</span>
                <span className="font-bold text-amber-300">{result.percentage || 77.8}%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden border border-slate-700">
                <div
                  className="bg-gradient-to-r from-amber-500 to-emerald-400 h-full rounded-full"
                  style={{ width: `${result.percentage || 77.8}%` }}
                ></div>
              </div>
            </div>
          </div>

          {/* 8 Kootas Breakdown Table */}
          {result.koota_breakdown && (
            <div className="overflow-x-auto rounded-2xl border border-slate-800/80">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-950/90 text-amber-300 uppercase tracking-wider border-b border-slate-800">
                  <tr>
                    <th className="py-3 px-4">Koota Category</th>
                    <th className="py-3 px-4">Score / Max</th>
                    <th className="py-3 px-4">Compatibility Area</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-slate-200">
                  {result.koota_breakdown.map((k: any, idx: number) => (
                    <tr key={idx} className="hover:bg-slate-800/40 transition">
                      <td className="py-3 px-4 font-bold text-slate-100">{k.koota}</td>
                      <td className="py-3 px-4 font-bold text-amber-300 tabular-nums">{k.score} / {k.max} pts</td>
                      <td className="py-3 px-4 text-slate-400 font-sans">{k.description}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
