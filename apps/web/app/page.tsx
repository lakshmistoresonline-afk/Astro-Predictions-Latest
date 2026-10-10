'use client'

import React, { useState, useEffect } from 'react'
import { PRESET_CITIES, BirthProfileResponse } from '../types/api'
import { calculateBirthProfile, interpretEvidenceAi } from '../services/apiClient'

import { LoadingState } from '../components/ui/LoadingState'
import { ErrorState } from '../components/ui/ErrorState'
import { WidgetErrorBoundary } from '../components/ui/WidgetErrorBoundary'
import { BirthProfileForm } from '../components/features/BirthProfileForm'
import { DashboardOverview } from '../components/features/DashboardOverview'
import { KundaliAstrolabe } from '../components/features/KundaliAstrolabe'
import { PlanetaryPositionsTable } from '../components/features/PlanetaryPositionsTable'
import { VargasGrid } from '../components/features/VargasGrid'
import { DashasTimeline } from '../components/features/DashasTimeline'
import { YogasDoshasView } from '../components/features/YogasDoshasView'
import { ShadbalaAshtakavargaView } from '../components/features/ShadbalaAshtakavargaView'
import { JaiminiView } from '../components/features/JaiminiView'
import { PanchangaMuhurtaView } from '../components/features/PanchangaMuhurtaView'
import { PredictionsView } from '../components/features/PredictionsView'
import { AiInterpretationView } from '../components/features/AiInterpretationView'

type NavigationTab =
  | 'home'
  | 'chart-form'
  | 'reports'
  | 'predictions'
  | 'planets'
  | 'vargas'
  | 'dashas'
  | 'yogas'
  | 'strength'
  | 'jaimini'
  | 'panchanga'
  | 'ai'

export default function Home() {
  const [activeTab, setActiveTab] = useState<NavigationTab>('chart-form')
  const [loading, setLoading] = useState(false)
  const [loadingStep, setLoadingStep] = useState(0)
  const [chartData, setChartData] = useState<BirthProfileResponse | null>(null)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)
  const [utcClock, setUtcClock] = useState<string>('')
  const [globalSearch, setGlobalSearch] = useState<string>('')
  const [showCommandPalette, setShowCommandPalette] = useState(false)

  // Form state
  const [name, setName] = useState('')
  const [year, setYear] = useState(1995)
  const [month, setMonth] = useState(1)
  const [day, setDay] = useState(1)
  const [hour, setHour] = useState(12)
  const [minute, setMinute] = useState(0)

  // Location & Timezone
  const [selectedCity, setSelectedCity] = useState(PRESET_CITIES[0].name)
  const [latitude, setLatitude] = useState(PRESET_CITIES[0].lat)
  const [longitude, setLongitude] = useState(PRESET_CITIES[0].lon)
  const [placeName, setPlaceName] = useState(PRESET_CITIES[0].name)
  const [country, setCountry] = useState(PRESET_CITIES[0].country)
  const [timezoneStr, setTimezoneStr] = useState(PRESET_CITIES[0].tz)

  const [zodiacSystem, setZodiacSystem] = useState('sidereal')

  useEffect(() => {
    const timer = setInterval(() => {
      setUtcClock(new Date().toUTCString().slice(17, 25) + ' UTC')
    }, 1000)
    setUtcClock(new Date().toUTCString().slice(17, 25) + ' UTC')

    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault()
        setShowCommandPalette(prev => !prev)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => {
      clearInterval(timer)
      window.removeEventListener('keydown', handleKeyDown)
    }
  }, [])

  const handleCityChange = (cityName: string) => {
    setSelectedCity(cityName)
    const found = PRESET_CITIES.find(c => c.name === cityName)
    if (found) {
      setPlaceName(found.name)
      setCountry(found.country)
      setLatitude(found.lat)
      setLongitude(found.lon)
      setTimezoneStr(found.tz)
    }
  }

  const handleCalculate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim()) {
      alert('Please enter your full birth name.')
      return
    }

    setLoading(true)
    setErrorMsg(null)
    setLoadingStep(1)

    setTimeout(() => setLoadingStep(2), 600)
    setTimeout(() => setLoadingStep(3), 1200)
    setTimeout(() => setLoadingStep(4), 1800)

    try {
      const data = await calculateBirthProfile({
        name,
        year,
        month,
        day,
        hour,
        minute,
        second: 0,
        timezone_str: timezoneStr,
        latitude,
        longitude,
        place_name: placeName,
        country,
        zodiac_system: zodiacSystem,
        ayanamsha: 'lahiri'
      })

      setTimeout(() => {
        setChartData(data)
        setLoading(false)
        setActiveTab('reports')
      }, 2200)
    } catch (err: any) {
      console.error(err)
      setErrorMsg(err.message || 'Failed to connect to backend FastAPI engine.')
      setLoading(false)
    }
  }

  const handleAiInterpret = async (domain: string, prompt: string) => {
    if (!chartData) throw new Error('Please calculate birth profile first.')
    return await interpretEvidenceAi(chartData.birth_input, domain, prompt)
  }

  const masterEv = chartData?.master_evidence

  const sidebarLinks: { id: NavigationTab; label: string; icon: string }[] = [
    { id: 'home', label: 'Overview', icon: '⚡' },
    { id: 'chart-form', label: 'Birth Profile', icon: '📝' },
    { id: 'reports', label: 'Kundli & Astrology', icon: '🌌' },
    { id: 'planets', label: 'Planetary Positions', icon: '🪐' },
    { id: 'vargas', label: '16 Vargas', icon: '❖' },
    { id: 'dashas', label: 'Vimshottari Dasha', icon: '⌛' },
    { id: 'yogas', label: 'Yogas & Doshas', icon: '⚖' },
    { id: 'strength', label: 'Shadbala & SAV', icon: '📊' },
    { id: 'jaimini', label: 'Jaimini', icon: '📜' },
    { id: 'panchanga', label: 'Panchanga & Muhurta', icon: '☀️' },
    { id: 'predictions', label: 'Domain Predictions', icon: '🎯' },
    { id: 'ai', label: 'AI Evidence Synthesis', icon: '🤖' },
  ]

  const loadingStepMessage =
    loadingStep === 1 ? 'Querying NASA JPL DE440s Ephemeris Kernel...' :
    loadingStep === 2 ? 'Normalizing Local Civil Time and Julian Day (UTC & TT)...' :
    loadingStep === 3 ? 'Evaluating 16 Parashari Vargas, Vimshottari Dashas & Yogas...' :
    'Synthesizing Canonical Astrology Evidence Package...'

  const filteredLinks = sidebarLinks.filter(l =>
    l.label.toLowerCase().includes(globalSearch.toLowerCase())
  )

  return (
    <div className="min-h-screen bg-[#070D1B] text-[#E8EDF7] flex flex-col md:flex-row selection:bg-[#F5B942] selection:text-[#070D1B] relative overflow-x-hidden font-sans w-full">
      {/* Sidebar Navigation */}
      <aside className="w-72 bg-[#111B30]/95 border-r border-[#F5B942]/20 flex flex-col justify-between p-6 backdrop-blur-2xl shrink-0 hidden md:flex min-h-screen sticky top-0 shadow-2xl z-30 select-none">
        <div className="space-y-8">
          {/* Branding Logo */}
          <div className="flex items-center gap-3.5">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-[#F5B942] via-[#E5A832] to-[#B8860B] flex items-center justify-center text-[#070D1B] font-black text-xl shadow-lg shadow-[#F5B942]/20">
              ✦
            </div>
            <div>
              <h1 className="text-xl font-black text-[#F5B942] tracking-wider font-serif-heading">Astrovision</h1>
              <p className="text-[9px] text-[#94A3B8] uppercase tracking-widest font-mono font-semibold">NASA DE440s Ephemeris</p>
            </div>
          </div>

          {/* Nav Links */}
          <nav className="space-y-1">
            {sidebarLinks.map(link => {
              const isActive = activeTab === link.id
              return (
                <button
                  key={link.id}
                  onClick={() => setActiveTab(link.id)}
                  className={`w-full text-left px-3.5 py-2.5 rounded-xl transition duration-150 font-mono text-xs flex items-center gap-3 cursor-pointer ${
                    isActive
                      ? 'bg-[#F5B942]/15 text-[#F5B942] border border-[#F5B942]/40 shadow-lg shadow-[#F5B942]/5 font-bold'
                      : 'text-[#94A3B8] hover:text-[#E8EDF7] hover:bg-white/5'
                  }`}
                >
                  <span className="text-sm">{link.icon}</span>
                  <span>{link.label}</span>
                </button>
              )
            })}
          </nav>
        </div>

        {/* Bottom System Status */}
        <div className="pt-4 border-t border-white/10 text-[11px] font-mono space-y-2">
          <div className="flex items-center gap-2 text-[#34D399] font-semibold text-[10px] uppercase tracking-wider">
            <span className="w-2 h-2 rounded-full bg-[#34D399] animate-pulse"></span>
            <span>All systems operational</span>
          </div>
          <p className="text-[#94A3B8] text-[10px]">Ephemeris • Database • AI Services</p>
          <p className="text-[#F5B942] font-bold text-[10px]">Version 6.0.0</p>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Header Bar */}
        <header className="bg-[#111B30]/90 border-b border-[#F5B942]/20 px-6 py-3.5 flex items-center justify-between sticky top-0 z-40 backdrop-blur-xl select-none">
          <div className="flex items-center gap-4 flex-1 max-w-xl">
            <div className="flex items-center gap-2 md:hidden">
              <span className="text-lg text-[#F5B942]">✦</span>
              <span className="font-extrabold text-[#F5B942] text-sm font-serif-heading">Astrovision</span>
            </div>

            {/* Global Search Input Button */}
            <div
              onClick={() => setShowCommandPalette(true)}
              className="relative w-full max-w-md hidden sm:flex items-center justify-between bg-[#070D1B]/80 border border-white/10 hover:border-[#F5B942]/50 rounded-xl px-3.5 py-2 text-xs text-[#94A3B8] cursor-pointer transition font-mono"
            >
              <div className="flex items-center gap-2">
                <span>🔍</span>
                <span>Search profiles, reports, features...</span>
              </div>
              <span className="text-[10px] text-[#94A3B8] border border-white/10 px-1.5 py-0.5 rounded bg-white/5">Ctrl K</span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* Live Ephemeris Badge */}
            <span className="hidden lg:inline-flex items-center gap-2 text-xs font-mono text-[#94A3B8] bg-[#070D1B]/80 px-3 py-1 rounded-full border border-white/10">
              <span className="w-1.5 h-1.5 rounded-full bg-[#34D399]"></span>
              Live Ephemeris: <strong className="text-[#E8EDF7]">JPL DE440s</strong> <span className="tabular-nums text-[#F5B942]">{utcClock}</span>
            </span>

            {/* User Profile Avatar */}
            <div className="flex items-center gap-2 bg-[#070D1B]/80 p-1.5 pr-3 rounded-full border border-white/10">
              <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-[#F5B942] to-amber-600 text-[#070D1B] font-black text-xs flex items-center justify-center">
                AK
              </div>
              <span className="text-xs font-mono font-semibold text-[#E8EDF7] hidden sm:inline-block">Astro Seeker</span>
            </div>

            {/* Mobile Navigation Dropdown */}
            <select
              value={activeTab}
              onChange={e => setActiveTab(e.target.value as NavigationTab)}
              className="md:hidden bg-[#070D1B] border border-[#F5B942]/40 rounded-xl px-3 py-1.5 text-xs text-[#F5B942] font-mono"
            >
              {sidebarLinks.map(l => (
                <option key={l.id} value={l.id}>{l.icon} {l.label}</option>
              ))}
            </select>
          </div>
        </header>

        {/* Command Palette Modal */}
        {showCommandPalette && (
          <div className="fixed inset-0 bg-[#070D1B]/80 backdrop-blur-xl z-50 flex items-start justify-center pt-20 p-4 font-mono select-none">
            <div className="bg-[#111B30] border border-[#F5B942]/40 rounded-3xl max-w-xl w-full p-6 space-y-4 shadow-2xl">
              <div className="flex items-center justify-between border-b border-white/10 pb-3">
                <div className="flex items-center gap-2 text-xs text-[#F5B942]">
                  <span>🔍</span>
                  <span className="font-bold">Astrovision Command Palette</span>
                </div>
                <button
                  onClick={() => setShowCommandPalette(false)}
                  className="text-xs text-[#94A3B8] hover:text-white"
                >
                  ESC ✕
                </button>
              </div>

              <input
                type="text"
                value={globalSearch}
                onChange={e => setGlobalSearch(e.target.value)}
                placeholder="Type module or feature name..."
                className="w-full bg-[#070D1B] border border-white/10 rounded-xl p-3 text-xs text-[#E8EDF7] placeholder-[#94A3B8] focus:border-[#F5B942] outline-none"
                autoFocus
              />

              <div className="space-y-1 max-h-64 overflow-y-auto">
                {filteredLinks.map(link => (
                  <div
                    key={link.id}
                    onClick={() => {
                      setActiveTab(link.id)
                      setShowCommandPalette(false)
                    }}
                    className="p-3 rounded-xl hover:bg-white/5 transition flex items-center justify-between cursor-pointer text-xs"
                  >
                    <div className="flex items-center gap-2">
                      <span>{link.icon}</span>
                      <span className="font-bold text-[#E8EDF7]">{link.label}</span>
                    </div>
                    <span className="text-[10px] text-[#94A3B8]">Jump →</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Loading Overlay */}
        {loading && <LoadingState stepMessage={loadingStepMessage} />}

        <main className="flex-1 p-6 md:p-10 space-y-8 w-full max-w-[1600px] mx-auto">
          {errorMsg && (
            <ErrorState
              message={errorMsg}
              onRetry={() => setErrorMsg(null)}
            />
          )}

          {activeTab === 'chart-form' && (
            <WidgetErrorBoundary title="Birth Profile Input Error">
              <BirthProfileForm
                name={name} setName={setName}
                year={year} setYear={setYear}
                month={month} setMonth={setMonth}
                day={day} setDay={setDay}
                hour={hour} setHour={setHour}
                minute={minute} setMinute={setMinute}
                selectedCity={selectedCity} handleCityChange={handleCityChange}
                timezoneStr={timezoneStr} setTimezoneStr={setTimezoneStr}
                zodiacSystem={zodiacSystem} setZodiacSystem={setZodiacSystem}
                latitude={latitude} setLatitude={setLatitude}
                longitude={longitude} setLongitude={setLongitude}
                placeName={placeName} setPlaceName={setPlaceName}
                country={country} setCountry={setCountry}
                onSubmit={handleCalculate}
              />
            </WidgetErrorBoundary>
          )}

          {activeTab === 'home' && (
            <WidgetErrorBoundary title="Dashboard Overview Error">
              {chartData ? (
                <DashboardOverview
                  data={chartData}
                  onNewProfile={() => setActiveTab('chart-form')}
                  onViewChart={() => setActiveTab('reports')}
                  onViewPredictions={() => setActiveTab('predictions')}
                />
              ) : (
                <div className="bg-[#111B30]/90 p-12 md:p-16 rounded-3xl border border-white/10 shadow-2xl text-center space-y-6 w-full max-w-2xl mx-auto backdrop-blur-xl">
                  <span className="text-4xl text-[#F5B942]">✦</span>
                  <h2 className="text-3xl font-extrabold text-[#F5B942] font-serif-heading">No Birth Profile Calculated</h2>
                  <p className="text-[#94A3B8] text-sm leading-relaxed font-sans">
                    Please enter your exact birth particulars to calculate your NASA JPL DE440s natal chart and unlock your cosmic dashboard.
                  </p>
                  <button
                    onClick={() => setActiveTab('chart-form')}
                    className="bg-gradient-to-r from-[#F5B942] to-[#E5A832] hover:from-[#E5A832] hover:to-[#F5B942] text-[#070D1B] font-black px-8 py-3.5 rounded-2xl shadow-xl shadow-[#F5B942]/20 text-xs uppercase tracking-wider transition duration-150 cursor-pointer"
                  >
                    Enter Birth Details →
                  </button>
                </div>
              )}
            </WidgetErrorBoundary>
          )}

          {activeTab === 'reports' && (
            <WidgetErrorBoundary title="Kundali Astrolabe Error">
              <KundaliAstrolabe svgChart={chartData?.svg_chart || null} data={chartData} />
            </WidgetErrorBoundary>
          )}

          {activeTab === 'planets' && (
            <WidgetErrorBoundary title="Planetary Positions Error">
              {masterEv?.canonical_chart ? (
                <PlanetaryPositionsTable chart={masterEv.canonical_chart} />
              ) : (
                <div className="text-center py-12 font-mono text-[#94A3B8] text-xs">Please calculate a birth profile first.</div>
              )}
            </WidgetErrorBoundary>
          )}

          {activeTab === 'vargas' && (
            <WidgetErrorBoundary title="Vargas Grid Error">
              <VargasGrid vargaSuite={masterEv?.varga_suite} />
            </WidgetErrorBoundary>
          )}

          {activeTab === 'dashas' && (
            <WidgetErrorBoundary title="Dashas Timeline Error">
              <DashasTimeline dashaSuite={masterEv?.natal_dasha_suite} />
            </WidgetErrorBoundary>
          )}

          {activeTab === 'yogas' && (
            <WidgetErrorBoundary title="Yogas & Doshas Error">
              <YogasDoshasView yogaSuite={masterEv?.yoga_suite} doshaSuite={masterEv?.dosha_suite} />
            </WidgetErrorBoundary>
          )}

          {activeTab === 'strength' && (
            <WidgetErrorBoundary title="Shadbala & Ashtakavarga Error">
              <ShadbalaAshtakavargaView
                shadbalaSuite={masterEv?.shadbala_suite}
                ashtakavargaEvidence={masterEv?.ashtakavarga_evidence}
              />
            </WidgetErrorBoundary>
          )}

          {activeTab === 'jaimini' && (
            <WidgetErrorBoundary title="Jaimini View Error">
              <JaiminiView jaiminiSuite={masterEv?.jaimini_suite} />
            </WidgetErrorBoundary>
          )}

          {activeTab === 'panchanga' && (
            <WidgetErrorBoundary title="Panchanga & Muhurta Error">
              <PanchangaMuhurtaView
                panchanga={masterEv?.panchanga}
                muhurtaSuite={masterEv?.muhurta_suite}
              />
            </WidgetErrorBoundary>
          )}

          {activeTab === 'predictions' && (
            <WidgetErrorBoundary title="Predictions View Error">
              <PredictionsView predictions={chartData?.predictions} />
            </WidgetErrorBoundary>
          )}

          {activeTab === 'ai' && (
            <WidgetErrorBoundary title="AI Interpretation Error">
              <AiInterpretationView onInterpret={handleAiInterpret} predictions={chartData?.predictions} />
            </WidgetErrorBoundary>
          )}
        </main>
      </div>
    </div>
  )
}
