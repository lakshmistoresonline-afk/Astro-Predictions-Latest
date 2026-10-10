import React, { useState } from 'react'

export const DigestView: React.FC = () => {
  const [email, setEmail] = useState('user@astrovision.test')
  const [frequency, setFrequency] = useState('weekly')
  const [subscribed, setSubscribed] = useState(false)

  const handleSubscribe = (e: React.FormEvent) => {
    e.preventDefault()
    setSubscribed(true)
  }

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none font-mono">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800/80 pb-5">
        <div>
          <h3 className="text-xl font-extrabold text-amber-300 flex items-center gap-2 font-serif-heading">
            <span>📫</span> Personalized Weekly Transit Digest
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Automated planetary transit impacts, Dasha boundary shifts, and auspicious timings delivered to your inbox
          </p>
        </div>

        <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-bold">
          Active Subscription Ready
        </span>
      </div>

      {/* Subscription Form */}
      <form onSubmit={handleSubscribe} className="p-6 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-4 text-xs">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-slate-400 mb-1.5 font-semibold">Notification Email Address</label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-slate-100 outline-none"
              required
            />
          </div>

          <div>
            <label className="block text-slate-400 mb-1.5 font-semibold">Digest Frequency</label>
            <select
              value={frequency}
              onChange={e => setFrequency(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-slate-100 outline-none"
            >
              <option value="weekly">Weekly Transit Digest (Every Monday)</option>
              <option value="monthly">Monthly Planetary Forecast (1st of Month)</option>
              <option value="major_transits">Major Transits Only (Jupiter, Saturn, Rahu)</option>
            </select>
          </div>
        </div>

        <button
          type="submit"
          className="w-full bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black py-3 rounded-xl text-xs uppercase tracking-wider shadow-lg cursor-pointer"
        >
          {subscribed ? '✓ Digest Subscription Active' : 'Activate Transit Email Digest →'}
        </button>
      </form>

      {/* Sample Transit Digest Preview */}
      <div className="p-6 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-3">
        <div className="flex justify-between items-center border-b border-slate-800 pb-3">
          <span className="font-bold text-amber-300 text-sm font-serif-heading">Weekly Digest Sample Preview</span>
          <span className="text-[10px] text-slate-500">October 2026 Forecast</span>
        </div>
        <p className="text-xs text-slate-300 font-sans leading-relaxed">
          <b>Jupiter in Taurus (4th House):</b> Transiting Jupiter forms a favorable trine to your natal Moon in Cancer, bringing harmony in domestic projects, real estate, and financial expansion.
        </p>
        <p className="text-xs text-slate-300 font-sans leading-relaxed">
          <b>Active Dasha Focus:</b> Your Venus Mahadasha continues with strong 9th house dharma support. Favorable days for career agreements: <i>12–15 October 2026</i>.
        </p>
      </div>
    </div>
  )
}
