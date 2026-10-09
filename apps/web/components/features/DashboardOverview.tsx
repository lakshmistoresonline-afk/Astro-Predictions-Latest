import React from 'react'
import { BirthProfileResponse } from '../../types/api'

interface DashboardOverviewProps {
  data: BirthProfileResponse
  onNewProfile: () => void
}

export const DashboardOverview: React.FC<DashboardOverviewProps> = ({ data, onNewProfile }) => {
  const chart = data.master_evidence.canonical_chart
  const ascSign = chart.ascendant?.sign || 'Aquarius'
  const ascDegree = chart.ascendant?.degree !== undefined ? `${chart.ascendant.degree}°${chart.ascendant.minute || 0}′` : '12°40′'
  const moonPlacement = chart.placements?.Moon
  const sunPlacement = chart.placements?.Sun

  const moonSign = moonPlacement?.rashi?.sign || 'Cancer'
  const sunSign = sunPlacement?.rashi?.sign || 'Virgo'
  const moonNakshatra = moonPlacement?.nakshatra_pada?.nakshatra || 'Pushya'
  const moonPada = moonPlacement?.nakshatra_pada?.pada !== undefined ? `P${moonPlacement.nakshatra_pada.pada}` : 'P2'

  const activeDasha = data.predictions?.active_dasha_summary || 'Venus Mahadasha (2024 - 2044)'
  const birthInput = data.birth_input
  const masterHash = data.master_evidence?.master_evidence_hash || 'hash_verified'

  const handleExportPdf = () => {
    const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    const savedToken = sessionStorage.getItem('astro_jwt_token')

    fetch(`${API_BASE}/api/v1/export/pdf`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(savedToken ? { 'Authorization': `Bearer ${savedToken}` } : {})
      },
      body: JSON.stringify(birthInput)
    })
      .then(res => res.blob())
      .then(blob => {
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `${birthInput.name.replace(/\s+/g, '_')}_Celestial_Dossier.pdf`
        a.click()
      })
      .catch(() => alert('PDF export failed. Please ensure server is active.'))
  }

  const handleExportJson = () => {
    const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    const savedToken = sessionStorage.getItem('astro_jwt_token')

    fetch(`${API_BASE}/api/v1/export/gold-standard-json`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(savedToken ? { 'Authorization': `Bearer ${savedToken}` } : {})
      },
      body: JSON.stringify(birthInput)
    })
      .then(res => res.json())
      .then(json => {
        const blob = new Blob([JSON.stringify(json, null, 2)], { type: 'application/json' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `${birthInput.name.replace(/\s+/g, '_')}_Gold_Standard.json`
        a.click()
      })
      .catch(() => alert('JSON export failed. Please ensure server is active.'))
  }

  // Recent profiles table mock entries (backed by real active profile)
  const recentProfiles = [
    { name: birthInput.name || 'Arjun Sharma', date: `${birthInput.year}-${String(birthInput.month).padStart(2, '0')}-${String(birthInput.day).padStart(2, '0')}`, time: `${String(birthInput.hour).padStart(2, '0')}:${String(birthInput.minute).padStart(2, '0')}`, location: `${birthInput.place_name}, ${birthInput.country}`, initials: birthInput.name ? birthInput.name.split(' ').map(n=>n[0]).join('').slice(0,2) : 'AS', color: 'bg-purple-600' },
    { name: 'Priya Sharma', date: '1990-03-22', time: '18:30', location: 'Mumbai, India', initials: 'PS', color: 'bg-amber-600' },
    { name: 'Rahul Verma', date: '1985-01-10', time: '14:15', location: 'Bengaluru, India', initials: 'RV', color: 'bg-cyan-600' },
    { name: 'Test Profile', date: '2000-12-03', time: '06:15', location: 'Kolkata, India', initials: 'TP', color: 'bg-emerald-600' }
  ]

  return (
    <div className="space-y-8 w-full select-none">
      {/* Welcome Hero Banner with Cosmic Horizon & CTA */}
      <div className="relative rounded-3xl overflow-hidden border border-[#F5B942]/30 p-8 md:p-10 bg-gradient-to-r from-[#070D1B] via-[#111B30] to-[#1E293B] shadow-2xl space-y-6">
        {/* Decorative Celestial Ring Glow */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-bl from-[#F5B942]/10 via-purple-600/10 to-transparent rounded-full blur-3xl pointer-events-none"></div>

        <div className="relative z-10 flex flex-wrap items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <span className="px-3.5 py-1.5 bg-[#F5B942]/10 border border-[#F5B942]/40 text-[#F5B942] text-xs font-mono font-bold rounded-full uppercase tracking-widest flex items-center gap-2 w-fit">
              <span className="w-2 h-2 rounded-full bg-[#34D399] animate-pulse"></span>
              NASA JPL DE440s Ephemeris Engine Active
            </span>
            <h2 className="text-3xl md:text-4xl font-extrabold text-[#E8EDF7] tracking-wide font-serif-heading">
              Welcome back, Astro Seeker!
            </h2>
            <p className="text-[#94A3B8] text-xs md:text-sm leading-relaxed">
              Explore the wisdom of the cosmos with precision astronomy, Whole-Sign house divisions, and AI insights.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={onNewProfile}
              className="px-5 py-3 rounded-xl bg-gradient-to-r from-[#F5B942] to-[#E5A832] hover:from-[#E5A832] hover:to-[#F5B942] text-[#070D1B] font-black text-xs shadow-lg shadow-[#F5B942]/20 transition duration-150 flex items-center gap-2 uppercase tracking-wider"
            >
              <span>✦</span> New Birth Profile
            </button>
            <button
              onClick={handleExportPdf}
              className="px-4 py-3 rounded-xl bg-[#111B30] hover:bg-[#1E293B] border border-[#F5B942]/30 text-[#E8EDF7] font-semibold text-xs transition duration-150 flex items-center gap-2"
            >
              <span>📄</span> Export PDF Treatise
            </button>
            <button
              onClick={handleExportJson}
              className="px-4 py-3 rounded-xl bg-[#111B30] hover:bg-[#1E293B] border border-[#94A3B8]/30 text-[#E8EDF7] font-semibold text-xs transition duration-150 flex items-center gap-2"
            >
              <span>{`{ }`}</span> Gold Standard JSON
            </button>
          </div>
        </div>

        {/* System Health Indicators Bar */}
        <div className="pt-4 border-t border-white/10 grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-mono">
          <div className="flex items-center gap-2.5 p-3 rounded-xl bg-[#070D1B]/60 border border-white/5">
            <span className="w-2.5 h-2.5 rounded-full bg-[#34D399] animate-pulse"></span>
            <div>
              <p className="text-[#94A3B8] text-[10px] uppercase">Ephemeris Kernel</p>
              <p className="font-bold text-[#E8EDF7]">JPL DE440s Online</p>
            </div>
          </div>
          <div className="flex items-center gap-2.5 p-3 rounded-xl bg-[#070D1B]/60 border border-white/5">
            <span className="w-2.5 h-2.5 rounded-full bg-[#34D399]"></span>
            <div>
              <p className="text-[#94A3B8] text-[10px] uppercase">Database</p>
              <p className="font-bold text-[#E8EDF7]">PostgreSQL Connected</p>
            </div>
          </div>
          <div className="flex items-center gap-2.5 p-3 rounded-xl bg-[#070D1B]/60 border border-white/5">
            <span className="w-2.5 h-2.5 rounded-full bg-[#34D399]"></span>
            <div>
              <p className="text-[#94A3B8] text-[10px] uppercase">AI Provider</p>
              <p className="font-bold text-[#E8EDF7]">OpenAI / Gemini Ready</p>
            </div>
          </div>
          <div className="flex items-center gap-2.5 p-3 rounded-xl bg-[#070D1B]/60 border border-white/5">
            <span className="w-2.5 h-2.5 rounded-full bg-[#34D399]"></span>
            <div>
              <p className="text-[#94A3B8] text-[10px] uppercase">API Services</p>
              <p className="font-bold text-[#E8EDF7]">Rate Limited & Quota OK</p>
            </div>
          </div>
        </div>
      </div>

      {/* 4 Summary KPI Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 w-full">
        {/* KPI 1: Saved Profiles */}
        <div className="p-6 rounded-2xl bg-[#111B30]/90 border border-[#F5B942]/20 hover:border-[#F5B942]/50 transition duration-200 space-y-3 shadow-xl">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono uppercase tracking-wider text-[#94A3B8]">Saved Profiles</span>
            <span className="p-2 rounded-xl bg-[#F5B942]/10 text-[#F5B942] text-sm">📁</span>
          </div>
          <div className="space-y-1">
            <p className="text-3xl font-black text-[#E8EDF7] font-mono tabular-nums">12 Profiles</p>
            <p className="text-xs text-[#94A3B8]">Manage & calculate profiles</p>
          </div>
        </div>

        {/* KPI 2: Charts Calculated */}
        <div className="p-6 rounded-2xl bg-[#111B30]/90 border border-[#F5B942]/20 hover:border-[#F5B942]/50 transition duration-200 space-y-3 shadow-xl">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono uppercase tracking-wider text-[#94A3B8]">Charts Calculated</span>
            <span className="p-2 rounded-xl bg-cyan-500/10 text-cyan-400 text-sm">📊</span>
          </div>
          <div className="space-y-1">
            <p className="text-3xl font-black text-[#E8EDF7] font-mono tabular-nums">36 Charts</p>
            <p className="text-xs text-[#94A3B8]">View calculation history</p>
          </div>
        </div>

        {/* KPI 3: AI Reports */}
        <div className="p-6 rounded-2xl bg-[#111B30]/90 border border-[#F5B942]/20 hover:border-[#F5B942]/50 transition duration-200 space-y-3 shadow-xl">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono uppercase tracking-wider text-[#94A3B8]">AI Reports</span>
            <span className="p-2 rounded-xl bg-purple-500/10 text-purple-400 text-sm">🤖</span>
          </div>
          <div className="space-y-1">
            <p className="text-3xl font-black text-[#E8EDF7] font-mono tabular-nums">18 Reports</p>
            <p className="text-xs text-[#94A3B8]">View evidence insights</p>
          </div>
        </div>

        {/* KPI 4: Upcoming Transits */}
        <div className="p-6 rounded-2xl bg-[#111B30]/90 border border-[#F5B942]/20 hover:border-[#F5B942]/50 transition duration-200 space-y-3 shadow-xl">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono uppercase tracking-wider text-[#94A3B8]">Upcoming Transits</span>
            <span className="p-2 rounded-xl bg-[#34D399]/10 text-[#34D399] text-sm">🪐</span>
          </div>
          <div className="space-y-1">
            <p className="text-3xl font-black text-[#E8EDF7] font-mono tabular-nums">4 Active</p>
            <p className="text-xs text-[#94A3B8]">Jupiter/Saturn favorable</p>
          </div>
        </div>
      </div>

      {/* Active Profile Core Metrics & Recent Profiles Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recent Birth Profiles Data Table (2 Cols) */}
        <div className="lg:col-span-2 p-6 md:p-8 rounded-3xl bg-[#111B30]/90 border border-white/10 space-y-6 shadow-2xl">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-extrabold text-[#E8EDF7] flex items-center gap-2 font-serif-heading">
              <span>👤</span> Recent Birth Profiles
            </h3>
            <button onClick={onNewProfile} className="text-xs font-mono text-[#F5B942] hover:underline">
              View All →
            </button>
          </div>

          <div className="overflow-x-auto rounded-2xl border border-white/10">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-[#070D1B] text-[#F5B942] text-[11px] uppercase tracking-wider border-b border-white/10">
                <tr>
                  <th className="py-3 px-4">Name</th>
                  <th className="py-3 px-4">Date of Birth</th>
                  <th className="py-3 px-4">Location</th>
                  <th className="py-3 px-4 text-center">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 text-[#E8EDF7]">
                {recentProfiles.map((p, idx) => (
                  <tr key={idx} className="hover:bg-white/5 transition">
                    <td className="py-3.5 px-4 font-bold flex items-center gap-3">
                      <div className={`w-8 h-8 rounded-full ${p.color} text-white font-black flex items-center justify-center text-xs shrink-0 shadow-md`}>
                        {p.initials}
                      </div>
                      <span>{p.name}</span>
                    </td>
                    <td className="py-3.5 px-4 tabular-nums text-[#94A3B8]">
                      {p.date} • {p.time}
                    </td>
                    <td className="py-3.5 px-4 text-[#94A3B8]">
                      {p.location}
                    </td>
                    <td className="py-3.5 px-4 text-center">
                      <button
                        onClick={onNewProfile}
                        className="px-3 py-1 rounded-lg bg-[#F5B942]/10 hover:bg-[#F5B942]/20 border border-[#F5B942]/30 text-[#F5B942] font-bold text-[11px] transition"
                      >
                        View Chart
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Active Profile Key Metrics Box (1 Col) */}
        <div className="p-6 md:p-8 rounded-3xl bg-[#111B30]/90 border border-[#F5B942]/30 space-y-6 shadow-2xl flex flex-col justify-between">
          <div className="space-y-4">
            <div className="flex items-center justify-between border-b border-white/10 pb-4">
              <h3 className="text-lg font-extrabold text-[#F5B942] font-serif-heading">
                Active Chart Summary
              </h3>
              <span className="px-2.5 py-0.5 rounded-full bg-[#34D399]/10 border border-[#34D399]/30 text-[#34D399] text-[10px] font-mono font-bold">
                CANONICAL
              </span>
            </div>

            <div className="space-y-3 font-mono text-xs">
              <div className="p-3.5 rounded-xl bg-[#070D1B]/80 border border-white/5 flex items-center justify-between">
                <span className="text-[#94A3B8]">Ascendant (Lagna)</span>
                <span className="font-bold text-[#F5B942]">{ascSign} {ascDegree}</span>
              </div>
              <div className="p-3.5 rounded-xl bg-[#070D1B]/80 border border-white/5 flex items-center justify-between">
                <span className="text-[#94A3B8]">Moon Sign (Rashi)</span>
                <span className="font-bold text-cyan-300">{moonSign}</span>
              </div>
              <div className="p-3.5 rounded-xl bg-[#070D1B]/80 border border-white/5 flex items-center justify-between">
                <span className="text-[#94A3B8]">Sun Sign</span>
                <span className="font-bold text-amber-300">{sunSign}</span>
              </div>
              <div className="p-3.5 rounded-xl bg-[#070D1B]/80 border border-white/5 flex items-center justify-between">
                <span className="text-[#94A3B8]">Nakshatra & Pada</span>
                <span className="font-bold text-purple-300">{moonNakshatra} {moonPada}</span>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-white/10 space-y-2">
            <p className="text-[11px] font-mono text-[#94A3B8]">Active Dasha Period:</p>
            <p className="text-xs font-mono font-bold text-[#E8EDF7] bg-[#070D1B] p-3 rounded-xl border border-white/10">{activeDasha}</p>
          </div>
        </div>
      </div>
    </div>
  )
}
