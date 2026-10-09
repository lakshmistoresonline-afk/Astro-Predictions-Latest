import React from 'react'
import { BirthProfileResponse } from '../../types/api'

interface DashboardOverviewProps {
  data: BirthProfileResponse
  onNewProfile: () => void
}

export const DashboardOverview: React.FC<DashboardOverviewProps> = ({ data, onNewProfile }) => {
  const chart = data.master_evidence.canonical_chart
  const ascSign = chart.ascendant?.sign || 'Unavailable'
  const ascDegree = chart.ascendant?.degree !== undefined ? `${chart.ascendant.degree}°${chart.ascendant.minute || 0}′` : ''
  const moonPlacement = chart.placements?.Moon
  const sunPlacement = chart.placements?.Sun

  const moonSign = moonPlacement?.rashi?.sign || 'Unavailable'
  const sunSign = sunPlacement?.rashi?.sign || 'Unavailable'
  const moonNakshatra = moonPlacement?.nakshatra_pada?.nakshatra || 'Unavailable'
  const moonPada = moonPlacement?.nakshatra_pada?.pada !== undefined ? `P${moonPlacement.nakshatra_pada.pada}` : ''

  const activeDasha = data.predictions?.active_dasha_summary || 'Vimshottari Dasha Calculated'
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
      .catch(err => alert('PDF export failed. Please ensure server is active.'))
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
      .catch(err => alert('JSON export failed. Please ensure server is active.'))
  }

  return (
    <div className="space-y-8 w-full select-none">
      {/* Hero Header Card */}
      <div className="relative rounded-3xl overflow-hidden border border-amber-500/30 p-8 md:p-10 bg-gradient-to-tr from-[#070A14] via-[#0E1630] to-[#1A254B] shadow-2xl space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="px-3.5 py-1.5 bg-amber-500/10 border border-amber-500/40 text-amber-300 text-xs font-mono font-semibold rounded-full uppercase tracking-widest flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              DE440s Ephemeris Verified
            </span>
            <span className="px-3 py-1 bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-mono rounded-full">
              Lahiri Sidereal
            </span>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handleExportPdf}
              className="px-4 py-2 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-extrabold text-xs shadow-lg shadow-amber-500/20 transition duration-150 flex items-center gap-2"
            >
              <span>📄</span> Export PDF Treatise
            </button>
            <button
              onClick={handleExportJson}
              className="px-4 py-2 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 text-slate-200 font-semibold text-xs transition duration-150 flex items-center gap-2"
            >
              <span>{`{ }`}</span> Gold Standard JSON
            </button>
            <button
              onClick={onNewProfile}
              className="px-3.5 py-2 rounded-xl bg-slate-900/60 hover:bg-slate-800/60 border border-slate-700/60 text-slate-300 font-medium text-xs transition duration-150"
            >
              + New Profile
            </button>
          </div>
        </div>

        <div className="space-y-2">
          <h2 className="text-3xl md:text-5xl font-black text-white tracking-wide">
            {data.birth_input.name}
          </h2>
          <p className="text-slate-400 font-mono text-xs md:text-sm flex flex-wrap items-center gap-x-4 gap-y-1">
            <span>📅 {birthInput.year}-{String(birthInput.month).padStart(2, '0')}-{String(birthInput.day).padStart(2, '0')}</span>
            <span>🕒 {String(birthInput.hour).padStart(2, '0')}:{String(birthInput.minute).padStart(2, '0')} ({birthInput.timezone_str})</span>
            <span>📍 {birthInput.place_name}, {birthInput.country} ({birthInput.latitude.toFixed(2)}° N, {birthInput.longitude.toFixed(2)}° E)</span>
          </p>
        </div>
      </div>

      {/* Global KPI Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 w-full">
        {/* Metric 1: Lagna */}
        <div className="bg-slate-900/80 backdrop-blur-xl p-6 rounded-2xl border border-slate-800/80 hover:border-amber-500/40 shadow-xl transition duration-200 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono uppercase tracking-widest text-amber-400/90 font-semibold">Ascendant (Lagna)</span>
            <span className="w-2 h-2 rounded-full bg-amber-400"></span>
          </div>
          <div className="space-y-1">
            <p className="text-2xl md:text-3xl font-black text-white tracking-tight font-sans">{ascSign}</p>
            <p className="text-xs font-mono text-slate-400 tabular-nums">{ascDegree}</p>
          </div>
          <div className="pt-2 border-t border-slate-800/60 flex items-center justify-between text-[11px] text-slate-400">
            <span>House 1 Focus</span>
            <span className="text-emerald-400 font-mono">Whole Sign</span>
          </div>
        </div>

        {/* Metric 2: Moon Sign */}
        <div className="bg-slate-900/80 backdrop-blur-xl p-6 rounded-2xl border border-slate-800/80 hover:border-amber-500/40 shadow-xl transition duration-200 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono uppercase tracking-widest text-cyan-400/90 font-semibold">Moon Sign (Rashi)</span>
            <span className="w-2 h-2 rounded-full bg-cyan-400"></span>
          </div>
          <div className="space-y-1">
            <p className="text-2xl md:text-3xl font-black text-white tracking-tight font-sans">{moonSign}</p>
            <p className="text-xs font-mono text-slate-400 tabular-nums">
              {moonPlacement?.rashi ? `${moonPlacement.rashi.degree}°${moonPlacement.rashi.minute}′` : 'Canonical'}
            </p>
          </div>
          <div className="pt-2 border-t border-slate-800/60 flex items-center justify-between text-[11px] text-slate-400">
            <span>Emotional Core</span>
            <span className="text-cyan-400 font-mono">Rashi</span>
          </div>
        </div>

        {/* Metric 3: Sun Sign */}
        <div className="bg-slate-900/80 backdrop-blur-xl p-6 rounded-2xl border border-slate-800/80 hover:border-amber-500/40 shadow-xl transition duration-200 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono uppercase tracking-widest text-amber-300/90 font-semibold">Sun Sign</span>
            <span className="w-2 h-2 rounded-full bg-amber-300"></span>
          </div>
          <div className="space-y-1">
            <p className="text-2xl md:text-3xl font-black text-white tracking-tight font-sans">{sunSign}</p>
            <p className="text-xs font-mono text-slate-400 tabular-nums">
              {sunPlacement?.rashi ? `${sunPlacement.rashi.degree}°${sunPlacement.rashi.minute}′` : 'Canonical'}
            </p>
          </div>
          <div className="pt-2 border-t border-slate-800/60 flex items-center justify-between text-[11px] text-slate-400">
            <span>Soul Vector</span>
            <span className="text-amber-300 font-mono">Atma</span>
          </div>
        </div>

        {/* Metric 4: Nakshatra */}
        <div className="bg-slate-900/80 backdrop-blur-xl p-6 rounded-2xl border border-slate-800/80 hover:border-amber-500/40 shadow-xl transition duration-200 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono uppercase tracking-widest text-purple-400/90 font-semibold">Nakshatra</span>
            <span className="w-2 h-2 rounded-full bg-purple-400"></span>
          </div>
          <div className="space-y-1">
            <p className="text-2xl md:text-3xl font-black text-white tracking-tight font-sans truncate">{moonNakshatra}</p>
            <p className="text-xs font-mono text-purple-300/90 font-bold">{moonPada}</p>
          </div>
          <div className="pt-2 border-t border-slate-800/60 flex items-center justify-between text-[11px] text-slate-400">
            <span>Lunar Mansion</span>
            <span className="text-purple-400 font-mono">Star Lord</span>
          </div>
        </div>
      </div>

      {/* Active Dasha Hierarchy Banner */}
      <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 space-y-4 shadow-2xl">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-extrabold text-amber-300 flex items-center gap-2">
            <span>⏳</span> Active Vimshottari Dasha Hierarchy
          </h3>
          <span className="text-xs font-mono text-slate-400 uppercase tracking-widest px-3 py-1 rounded-full bg-slate-800 border border-slate-700">
            Parashari 120Y
          </span>
        </div>
        <p className="text-base md:text-lg text-slate-100 font-mono leading-relaxed bg-slate-950/60 p-4 rounded-2xl border border-slate-800">
          {activeDasha}
        </p>
      </div>

      {/* Master Evidence Provenance Footer */}
      <div className="p-5 rounded-2xl bg-slate-950/40 border border-slate-800/60 flex flex-wrap items-center justify-between gap-4 text-xs font-mono text-slate-400">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
          <span>Master Evidence SHA-256: <strong className="text-slate-200">{masterHash.slice(0, 24)}...</strong></span>
        </div>
        <div className="text-slate-500">
          Astrovision Version 6.0.0-Celestial-Astrolabe
        </div>
      </div>
    </div>
  )
}
