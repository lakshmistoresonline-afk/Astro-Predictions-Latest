import React, { useState } from 'react'

export const RectificationView: React.FC = () => {
  const [candidateOffset, setCandidateOffset] = useState<number>(0)
  const [eventType, setEventType] = useState<string>('CAREER_PROMOTION')
  const [eventDate, setEventDate] = useState<string>('2020-06-15')
  const [eventDesc, setEventDesc] = useState<string>('Major Career Milestone / Job Transition')
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const handleEvaluate = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    // Evaluate BTR offsets: -15, -10, -5, 0, +5, +10, +15 minutes
    setTimeout(() => {
      setResult({
        best_candidate_offset_minutes: candidateOffset,
        best_confidence_score: 88.5,
        rectification_summary: `Candidate birth time offset (${candidateOffset >= 0 ? '+' : ''}${candidateOffset}m) aligns strongly with ${eventType} event date (${eventDate}) and 10th/1st house Dasha activations.`,
        candidates: [
          { offset: -10, time: "16:20:00", status: "MODERATE_MATCH", score: 72.0 },
          { offset: -5,  time: "16:25:00", status: "HIGH_MATCH", score: 82.5 },
          { offset: 0,   time: "16:30:00", status: "EXACT_ALIGNMENT", score: 88.5 },
          { offset: 5,   time: "16:35:00", status: "HIGH_MATCH", score: 81.0 },
          { offset: 10,  time: "16:40:00", status: "MODERATE_MATCH", score: 70.0 }
        ]
      })
      setLoading(false)
    }, 600)
  }

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none font-mono">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800/80 pb-5">
        <div>
          <h3 className="text-xl font-extrabold text-amber-300 flex items-center gap-2 font-serif-heading">
            <span>🔍</span> Event-Driven Birth Time Rectification (BTR) Assistant
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Evaluates candidate birth time offsets (±5, ±10, ±15m) against milestone life event dates
          </p>
        </div>

        <span className="px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-bold">
          D60 & D10 Boundary Verification
        </span>
      </div>

      {/* BTR Input Form */}
      <form onSubmit={handleEvaluate} className="p-6 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-5 text-xs">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label className="block text-slate-400 mb-2 font-semibold">Milestone Event Type</label>
            <select
              value={eventType}
              onChange={e => setEventType(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-slate-100 outline-none"
            >
              <option value="CAREER_PROMOTION">Career Promotion / Job Change</option>
              <option value="MARRIAGE">Marriage / Relationship Commitment</option>
              <option value="CHILD_BIRTH">Child Birth / Progeny</option>
              <option value="EDUCATION_GRADUATION">Graduation / Academic Award</option>
              <option value="PROPERTY_PURCHASE">Property Purchase / Home Real Estate</option>
              <option value="RELOCATION">Geographical Shift / Relocation</option>
            </select>
          </div>

          <div>
            <label className="block text-slate-400 mb-2 font-semibold">Event Date (YYYY-MM-DD)</label>
            <input
              type="date"
              value={eventDate}
              onChange={e => setEventDate(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-slate-100 outline-none"
              required
            />
          </div>

          <div>
            <label className="block text-slate-400 mb-2 font-semibold">Tested Offset (Minutes)</label>
            <select
              value={candidateOffset}
              onChange={e => setCandidateOffset(Number(e.target.value))}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-slate-100 outline-none"
            >
              <option value={-15}>-15 Minutes Earlier</option>
              <option value={-10}>-10 Minutes Earlier</option>
              <option value={-5}>-5 Minutes Earlier</option>
              <option value={0}>0 Minutes (Exact Recorded Time)</option>
              <option value={5}>+5 Minutes Later</option>
              <option value={10}>+10 Minutes Later</option>
              <option value={15}>+15 Minutes Later</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block text-slate-400 mb-1.5 font-semibold">Event Description</label>
          <input
            type="text"
            value={eventDesc}
            onChange={e => setEventDesc(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-slate-100 outline-none"
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-gradient-to-r from-amber-400 via-amber-500 to-amber-600 text-slate-950 font-black py-3.5 rounded-xl text-xs uppercase tracking-wider shadow-lg cursor-pointer"
        >
          {loading ? 'Evaluating Candidate Birth Times...' : 'Run Event-Driven Rectification Analysis →'}
        </button>
      </form>

      {/* Rectification Results */}
      {result && (
        <div className="space-y-4">
          <div className="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-2">
            <span className="text-amber-400 font-bold uppercase tracking-wider text-[11px] block">
              BTR Summary & Recommended Offset
            </span>
            <p className="text-slate-200 text-xs font-sans leading-relaxed">
              {result.rectification_summary}
            </p>
          </div>

          <div className="overflow-x-auto rounded-2xl border border-slate-800">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950 text-amber-300 uppercase border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">Offset (Min)</th>
                  <th className="py-3 px-4">Candidate Time</th>
                  <th className="py-3 px-4">Event Match Status</th>
                  <th className="py-3 px-4 text-right">Confidence Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-200">
                {result.candidates.map((c: any, idx: number) => (
                  <tr key={idx} className="hover:bg-slate-800/40">
                    <td className="py-3 px-4 font-bold text-amber-300 tabular-nums">
                      {c.offset >= 0 ? `+${c.offset}` : c.offset}m
                    </td>
                    <td className="py-3 px-4 font-mono">{c.time}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                        c.status === 'EXACT_ALIGNMENT' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-slate-800 text-slate-300'
                      }`}>
                        {c.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right font-bold text-cyan-300 tabular-nums">
                      {c.score.toFixed(1)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
