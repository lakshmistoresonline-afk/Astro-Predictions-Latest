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
    return () => clearInterval(timer)
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
        setActiveTab('home')
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
    { id: 'home', label: 'Dashboard Overview', icon: '⚡' },
    { id: 'chart-form', label: 'Birth Profile Form', icon: '📝' },
    { id: 'reports', label: 'Kundali Astrolabe', icon: '🌌' },
    { id: 'planets', label: 'Planetary Positions', icon: '🪐' },
    { id: 'vargas', label: '16 Vargas Atlas', icon: '❖' },
    { id: 'dashas', label: 'Vimshottari Dashas', icon: '⌛' },
    { id: 'yogas', label: 'Yogas & Doshas', icon: '⚖' },
    { id: 'strength', label: 'Shadbala & SAV', icon: '📊' },
    { id: 'jaimini', label: 'Jaimini Sutras', icon: '📜' },
    { id: 'panchanga', label: 'Panchanga & Muhurta', icon: '☀️' },
    { id: 'predictions', label: '14 Domain Predictions', icon: '🎯' },
    { id: 'ai', label: 'AI Evidence Synthesis', icon: '🤖' },
  ]

  const loadingStepMessage =
    loadingStep === 1 ? 'Querying NASA JPL DE440s Ephemeris Kernel...' :
    loadingStep === 2 ? 'Normalizing Local Civil Time and Julian Day (UTC & TT)...' :
    loadingStep === 3 ? 'Evaluating 16 Parashari Vargas, Vimshottari Dashas & Yogas...' :
    'Synthesizing Canonical Astrology Evidence Package...'

  return (
    <div
      style={{
        background: 'radial-gradient(circle at 40% 20%, #171B36 0%, #0B0E20 50%, #050711 100%)',
        minHeight: '100vh',
        backgroundAttachment: 'fixed'
      }}
      className="text-slate-100 flex flex-col md:flex-row selection:bg-amber-400 selection:text-slate-950 relative overflow-x-hidden font-sans w-full"
    >
      {/* Sidebar Navigation */}
      <aside className="w-80 bg-slate-950/90 border-r border-slate-800/80 flex flex-col justify-between p-6 backdrop-blur-2xl shrink-0 hidden md:flex min-h-screen sticky top-0 shadow-2xl z-30 select-none">
        <div className="space-y-8">
          <div className="flex items-center gap-3.5">
            <div className="w-11 h-11 rounded-2xl bg-gradient-to-tr from-amber-400 via-amber-500 to-amber-600 flex items-center justify-center text-slate-950 font-black text-xl shadow-lg shadow-amber-500/20">
              ✦
            </div>
            <div>
              <h1 className="text-xl font-black text-amber-300 tracking-wider">Astrovision</h1>
              <p className="text-[10px] text-slate-400 uppercase tracking-widest font-mono font-semibold">NASA DE440s Engine</p>
            </div>
          </div>

          <nav className="space-y-1">
            {sidebarLinks.map(link => {
              const isActive = activeTab === link.id
              return (
                <button
                  key={link.id}
                  onClick={() => setActiveTab(link.id)}
                  className={`w-full text-left px-4 py-3 rounded-xl transition duration-150 font-mono text-xs flex items-center gap-3 ${
                    isActive
                      ? 'bg-amber-500/15 text-amber-300 border border-amber-500/40 shadow-lg shadow-amber-500/5 font-bold'
                      : 'text-slate-400 hover:text-slate-100 hover:bg-slate-900/60'
                  }`}
                >
                  <span className="text-base">{link.icon}</span>
                  <span>{link.label}</span>
                </button>
              )
            })}
          </nav>
        </div>

        <div className="pt-4 border-t border-slate-800/80 text-[11px] font-mono text-slate-400 space-y-1">
          <div className="flex items-center justify-between text-amber-300 font-bold">
            <span>Version 6.0.0</span>
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          </div>
          <p className="text-slate-500">DE440s Kernel • Lahiri Sidereal</p>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Header Bar */}
        <header className="bg-slate-950/80 border-b border-slate-800/80 px-6 py-3.5 flex items-center justify-between sticky top-0 z-40 backdrop-blur-xl select-none">
          <div className="flex items-center gap-3">
            <span className="md:hidden text-xl text-amber-300">✦</span>
            <span className="md:hidden font-extrabold text-amber-300 text-sm">Astrovision</span>
            <span className="hidden md:inline-flex items-center gap-2 text-xs font-mono text-slate-400 bg-slate-900/80 px-3 py-1 rounded-full border border-slate-800">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
              Live Ephemeris Clock: <strong className="text-slate-200 tabular-nums">{utcClock}</strong>
            </span>
          </div>

          <div className="flex items-center gap-3">
            {chartData && (
              <span className="text-xs font-mono text-amber-300/90 font-bold bg-amber-500/10 border border-amber-500/30 px-3 py-1 rounded-full hidden sm:inline-block">
                Active: {chartData.birth_input.name}
              </span>
            )}

            {/* Mobile Navigation Dropdown */}
            <select
              value={activeTab}
              onChange={e => setActiveTab(e.target.value as NavigationTab)}
              className="md:hidden bg-slate-900 border border-slate-700 rounded-xl px-3 py-1.5 text-xs text-amber-300 font-mono"
            >
              {sidebarLinks.map(l => (
                <option key={l.id} value={l.id}>{l.icon} {l.label}</option>
              ))}
            </select>
          </div>
        </header>

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
                />
              ) : (
                <div className="bg-slate-900/80 p-12 md:p-16 rounded-3xl border border-slate-800/80 shadow-2xl text-center space-y-6 w-full max-w-2xl mx-auto backdrop-blur-xl select-none">
                  <span className="text-4xl text-amber-300">✦</span>
                  <h2 className="text-3xl font-black text-amber-300 tracking-wide">No Birth Profile Calculated</h2>
                  <p className="text-slate-400 text-sm leading-relaxed font-sans">
                    Please enter your exact birth particulars to calculate your NASA JPL DE440s natal chart and unlock your cosmic dashboard.
                  </p>
                  <button
                    onClick={() => setActiveTab('chart-form')}
                    className="bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black px-8 py-3.5 rounded-2xl shadow-xl shadow-amber-500/20 text-sm uppercase tracking-wider transition duration-150"
                  >
                    Enter Birth Details →
                  </button>
                </div>
              )}
            </WidgetErrorBoundary>
          )}

          {activeTab === 'reports' && (
            <WidgetErrorBoundary title="Kundali Astrolabe Error">
              <KundaliAstrolabe svgChart={chartData?.svg_chart || null} />
            </WidgetErrorBoundary>
          )}

          {activeTab === 'planets' && (
            <WidgetErrorBoundary title="Planetary Positions Error">
              {masterEv?.canonical_chart ? (
                <PlanetaryPositionsTable chart={masterEv.canonical_chart} />
              ) : (
                <div className="text-center py-12 font-mono text-slate-400 text-xs">Please calculate a birth profile first.</div>
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
              <AiInterpretationView onInterpret={handleAiInterpret} />
            </WidgetErrorBoundary>
          )}
        </main>
      </div>
    </div>
  )
}
