'use client'

import React, { useState, useEffect, useRef } from 'react'
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
import { CompatibilityView } from '../components/features/CompatibilityView'
import { RectificationView } from '../components/features/RectificationView'
import { DigestView } from '../components/features/DigestView'
import { TransitScrubberView } from '../components/features/TransitScrubberView'
import { TajikaVarshaphalView } from '../components/features/TajikaVarshaphalView'
import { PrashnaView } from '../components/features/PrashnaView'
import { YoginiDashaView } from '../components/features/YoginiDashaView'
import { GemstonePariharaView } from '../components/features/GemstonePariharaView'
import { TRANSLATIONS, SupportedLanguage } from '../types/i18n'

type NavigationTab =
  | 'home'
  | 'chart-form'
  | 'reports'
  | 'predictions'
  | 'planets'
  | 'vargas'
  | 'dashas'
  | 'yogini'
  | 'yogas'
  | 'gemstones'
  | 'strength'
  | 'jaimini'
  | 'panchanga'
  | 'varshaphal'
  | 'prashna'
  | 'compatibility'
  | 'rectification'
  | 'digest'
  | 'scrubber'
  | 'ai'

export default function Home() {
  const [activeTab, setActiveTab] = useState<NavigationTab>('chart-form')
  const [loading, setLoading] = useState(false)
  const [loadingStep, setLoadingStep] = useState(0)
  const [chartData, setChartData] = useState<BirthProfileResponse | null>(null)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)
  const [istClock, setIstClock] = useState<string>('')
  const [globalSearch, setGlobalSearch] = useState<string>('')
  const [showCommandPalette, setShowCommandPalette] = useState(false)
  const [showProfileDrawer, setShowProfileDrawer] = useState(false)
  const [openDropdown, setOpenDropdown] = useState<string | null>(null)
  const [lang, setLang] = useState<SupportedLanguage>('en')

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

  const t = TRANSLATIONS[lang]

  useEffect(() => {
    const updateIstClock = () => {
      const now = new Date()
      const timeStr = now.toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata', hour12: false })
      setIstClock(`${timeStr} IST`)
    }
    const timer = setInterval(updateIstClock, 1000)
    updateIstClock()

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

  const navGroups = [
    {
      label: 'Kundli & Charts',
      icon: '🌌',
      items: [
        { id: 'chart-form' as NavigationTab, label: t.ui.birth_profile, icon: '📝' },
        { id: 'reports' as NavigationTab, label: t.ui.kundli, icon: '🌌' },
        { id: 'planets' as NavigationTab, label: t.ui.planets, icon: '🪐' },
        { id: 'vargas' as NavigationTab, label: t.ui.vargas, icon: '❖' },
      ]
    },
    {
      label: 'Predictions & AI',
      icon: '🎯',
      items: [
        { id: 'predictions' as NavigationTab, label: t.ui.predictions, icon: '🎯' },
        { id: 'prashna' as NavigationTab, label: 'Prashna Horary', icon: '🔮' },
        { id: 'ai' as NavigationTab, label: t.ui.ai, icon: '🤖' },
        { id: 'digest' as NavigationTab, label: t.ui.digest, icon: '📫' },
        { id: 'scrubber' as NavigationTab, label: 'Transit Scrubber', icon: '📅' },
      ]
    },
    {
      label: 'Dasha & Timing',
      icon: '⌛',
      items: [
        { id: 'dashas' as NavigationTab, label: t.ui.dashas, icon: '⌛' },
        { id: 'yogini' as NavigationTab, label: 'Yogini Dasha', icon: '⏳' },
        { id: 'varshaphal' as NavigationTab, label: 'Tajika Varshaphal', icon: '☀️' },
      ]
    },
    {
      label: 'Strengths & Remedies',
      icon: '📊',
      items: [
        { id: 'strength' as NavigationTab, label: t.ui.strength, icon: '📊' },
        { id: 'yogas' as NavigationTab, label: t.ui.yogas, icon: '⚖' },
        { id: 'gemstones' as NavigationTab, label: 'Gemstones & Pariharas', icon: '💎' },
        { id: 'jaimini' as NavigationTab, label: t.ui.jaimini, icon: '📜' },
      ]
    },
    {
      label: 'Tools',
      icon: '🛠️',
      items: [
        { id: 'panchanga' as NavigationTab, label: t.ui.panchanga, icon: '☀️' },
        { id: 'compatibility' as NavigationTab, label: t.ui.compatibility, icon: '💖' },
        { id: 'rectification' as NavigationTab, label: t.ui.rectification, icon: '🔍' },
      ]
    }
  ]

  const quickPillTabs: { id: NavigationTab; label: string; icon: string }[] = [
    { id: 'home', label: 'Dashboard', icon: '⚡' },
    { id: 'chart-form', label: 'Birth Profile', icon: '📝' },
    { id: 'reports', label: 'Kundli', icon: '🌌' },
    { id: 'planets', label: 'Planets', icon: '🪐' },
    { id: 'vargas', label: '16 Vargas', icon: '❖' },
    { id: 'dashas', label: 'Dashas', icon: '⌛' },
    { id: 'predictions', label: '14 Domains', icon: '🎯' },
    { id: 'gemstones', label: 'Gemstones', icon: '💎' },
    { id: 'varshaphal', label: 'Varshaphal', icon: '☀️' },
    { id: 'prashna', label: 'Prashna', icon: '🔮' },
    { id: 'ai', label: 'AI Assistant', icon: '🤖' },
  ]

  const loadingStepMessage =
    loadingStep === 1 ? 'Querying NASA JPL DE440s Ephemeris Kernel...' :
    loadingStep === 2 ? 'Normalizing Local Civil Time and Julian Day (UTC & TT)...' :
    loadingStep === 3 ? 'Evaluating 16 Parashari Vargas, Vimshottari Dashas & Yogas...' :
    'Synthesizing Canonical Astrology Evidence Package...'

  return (
    <div className="min-h-screen bg-[#050814] text-[#F8FAFC] selection:bg-[#F5B942] selection:text-[#050814] font-sans w-full flex flex-col relative overflow-x-hidden">
      {/* Option 1: Top Floating Glassmorphic Header */}
      <header className="bg-[#0D1527]/90 border-b border-[#F5B942]/20 px-6 py-3.5 sticky top-0 z-50 backdrop-blur-2xl shadow-xl select-none">
        <div className="max-w-[1600px] mx-auto flex items-center justify-between gap-6">
          {/* Logo & Brand */}
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab('home')}>
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-[#F5B942] via-[#E5A832] to-[#B8860B] flex items-center justify-center text-[#050814] font-black text-xl shadow-lg shadow-[#F5B942]/20 gold-glow">
              ✦
            </div>
            <div>
              <h1 className="text-xl font-black text-[#F5B942] tracking-wider font-serif-heading">{t.ui.app_title}</h1>
              <p className="text-[10px] text-[#94A3B8] uppercase tracking-widest font-mono">NASA JPL DE440s</p>
            </div>
          </div>

          {/* Top Dropdown Mega Menu Navigation (Desktop) */}
          <nav className="hidden lg:flex items-center gap-2 font-sans text-sm">
            <button
              onClick={() => { setActiveTab('home'); setOpenDropdown(null); }}
              className={`px-4 py-2 rounded-xl transition font-semibold flex items-center gap-2 cursor-pointer ${
                activeTab === 'home' ? 'bg-[#F5B942]/20 text-[#F5B942] border border-[#F5B942]/40' : 'text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-white/5'
              }`}
            >
              <span>⚡</span> Dashboard
            </button>

            {navGroups.map(group => {
              const isGroupActive = group.items.some(i => i.id === activeTab)
              const isOpen = openDropdown === group.label

              return (
                <div key={group.label} className="relative">
                  <button
                    onClick={() => setOpenDropdown(isOpen ? null : group.label)}
                    className={`px-4 py-2 rounded-xl transition font-semibold flex items-center gap-2 cursor-pointer ${
                      isGroupActive ? 'bg-[#F5B942]/20 text-[#F5B942] border border-[#F5B942]/40' : 'text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-white/5'
                    }`}
                  >
                    <span>{group.icon}</span>
                    <span>{group.label}</span>
                    <span className="text-xs text-[#94A3B8]">▾</span>
                  </button>

                  {isOpen && (
                    <div
                      onMouseLeave={() => setOpenDropdown(null)}
                      className="absolute top-full left-0 mt-2 w-56 bg-[#0D1527] border border-[#F5B942]/30 rounded-2xl shadow-2xl p-2 z-50 space-y-1 font-sans text-xs backdrop-blur-2xl"
                    >
                      {group.items.map(item => (
                        <button
                          key={item.id}
                          onClick={() => {
                            setActiveTab(item.id)
                            setOpenDropdown(null)
                          }}
                          className={`w-full text-left px-3.5 py-2.5 rounded-xl transition flex items-center gap-3 cursor-pointer ${
                            activeTab === item.id ? 'bg-[#F5B942]/20 text-[#F5B942] font-bold' : 'text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-white/5'
                          }`}
                        >
                          <span>{item.icon}</span>
                          <span>{item.label}</span>
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              )
            })}
          </nav>

          {/* Right Header Badges & Search */}
          <div className="flex items-center gap-4">
            {/* Global Search Bar Trigger */}
            <div
              onClick={() => setShowCommandPalette(true)}
              className="hidden md:flex items-center gap-3 bg-[#050814] border border-white/10 hover:border-[#F5B942]/50 rounded-2xl px-4 py-2 text-xs text-[#94A3B8] cursor-pointer transition font-mono"
            >
              <span>🔍 Search...</span>
              <span className="text-[10px] bg-white/5 px-2 py-0.5 rounded border border-white/10">Ctrl K</span>
            </div>

            {/* Language Selector */}
            <select
              value={lang}
              onChange={e => setLang(e.target.value as SupportedLanguage)}
              className="bg-[#050814] border border-white/15 rounded-xl px-3 py-1.5 text-xs text-[#F5B942] font-mono cursor-pointer outline-none"
            >
              <option value="en">English</option>
              <option value="hi">हिंदी (Hindi)</option>
              <option value="sa">संस्कृतम् (Sanskrit)</option>
            </select>

            {/* Live IST Badge */}
            <span className="hidden xl:inline-flex items-center gap-2 text-xs font-mono text-[#94A3B8] bg-[#050814] px-3.5 py-1.5 rounded-full border border-white/10">
              <span className="w-2 h-2 rounded-full bg-[#34D399] animate-pulse"></span>
              JPL DE440s <span className="tabular-nums text-[#F5B942] font-bold">{istClock}</span>
            </span>

            {/* User Avatar */}
            <div
              onClick={() => setShowProfileDrawer(true)}
              className="flex items-center gap-2.5 bg-[#050814] hover:bg-[#152035] p-1.5 pr-3.5 rounded-full border border-white/10 cursor-pointer transition"
            >
              <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-[#F5B942] to-amber-600 text-[#050814] font-black text-xs flex items-center justify-center">
                AK
              </div>
              <span className="text-xs font-semibold text-[#F8FAFC] hidden sm:inline-block">Astro Seeker ▾</span>
            </div>
          </div>
        </div>
      </header>

      {/* Quick Action Navigation Bar */}
      <div className="bg-[#0D1527]/70 border-b border-white/5 px-6 py-2.5 sticky top-[65px] z-40 backdrop-blur-xl overflow-x-auto select-none">
        <div className="max-w-[1600px] mx-auto flex items-center gap-2 font-sans text-xs">
          {quickPillTabs.map(pill => {
            const isActive = activeTab === pill.id
            return (
              <button
                key={pill.id}
                onClick={() => setActiveTab(pill.id)}
                className={`px-3.5 py-1.5 rounded-xl transition duration-150 whitespace-nowrap flex items-center gap-2 cursor-pointer font-medium ${
                  isActive
                    ? 'bg-[#F5B942]/20 text-[#F5B942] border border-[#F5B942]/40 shadow-sm font-bold'
                    : 'text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-white/5'
                }`}
              >
                <span>{pill.icon}</span>
                <span>{pill.label}</span>
              </button>
            )
          })}
        </div>
      </div>

      {/* Main View Area */}
      <main className="flex-1 p-6 md:p-10 max-w-[1600px] w-full mx-auto space-y-8">
        {loading ? (
          <LoadingState stepMessage={loadingStepMessage} />
        ) : errorMsg ? (
          <ErrorState message={errorMsg} onRetry={() => setErrorMsg(null)} />
        ) : (
          <>
            {activeTab === 'chart-form' && (
              <WidgetErrorBoundary title="Birth Profile Form Error">
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
                  <div className="bg-[#0D1527]/90 p-12 md:p-16 rounded-3xl border border-white/10 shadow-2xl text-center space-y-6 max-w-2xl mx-auto backdrop-blur-2xl">
                    <span className="text-4xl text-[#F5B942]">✦</span>
                    <h2 className="text-3xl font-extrabold text-[#F5B942] font-serif-heading">No Birth Profile Calculated</h2>
                    <p className="text-[#94A3B8] text-sm leading-relaxed font-sans">
                      Please enter your birth particulars to calculate your NASA JPL DE440s natal chart and unlock your cosmic dashboard.
                    </p>
                    <button
                      onClick={() => setActiveTab('chart-form')}
                      className="bg-gradient-to-r from-[#F5B942] to-[#E5A832] hover:from-[#E5A832] hover:to-[#F5B942] text-[#050814] font-black px-8 py-3.5 rounded-2xl shadow-xl shadow-[#F5B942]/20 text-xs uppercase tracking-wider transition duration-150 cursor-pointer"
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
                  <div className="text-center py-12 font-sans text-[#94A3B8] text-sm">Please calculate a birth profile first.</div>
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

            {activeTab === 'yogini' && (
              <WidgetErrorBoundary title="Yogini Dasha Error">
                <YoginiDashaView birthInput={chartData?.birth_input} />
              </WidgetErrorBoundary>
            )}

            {activeTab === 'varshaphal' && (
              <WidgetErrorBoundary title="Varshaphal Error">
                <TajikaVarshaphalView birthInput={chartData?.birth_input} />
              </WidgetErrorBoundary>
            )}

            {activeTab === 'prashna' && (
              <WidgetErrorBoundary title="Prashna Horary Error">
                <PrashnaView />
              </WidgetErrorBoundary>
            )}

            {activeTab === 'yogas' && (
              <WidgetErrorBoundary title="Yogas & Doshas Error">
                <YogasDoshasView yogaSuite={masterEv?.yoga_suite} doshaSuite={masterEv?.dosha_suite} />
              </WidgetErrorBoundary>
            )}

            {activeTab === 'gemstones' && (
              <WidgetErrorBoundary title="Gemstones & Pariharas Error">
                <GemstonePariharaView birthInput={chartData?.birth_input} />
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

            {activeTab === 'compatibility' && (
              <WidgetErrorBoundary title="Compatibility View Error">
                <CompatibilityView />
              </WidgetErrorBoundary>
            )}

            {activeTab === 'rectification' && (
              <WidgetErrorBoundary title="Rectification Error">
                <RectificationView />
              </WidgetErrorBoundary>
            )}

            {activeTab === 'digest' && (
              <WidgetErrorBoundary title="Digest View Error">
                <DigestView />
              </WidgetErrorBoundary>
            )}

            {activeTab === 'scrubber' && (
              <WidgetErrorBoundary title="Transit Scrubber Error">
                <TransitScrubberView />
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
          </>
        )}
      </main>

      {/* Command Palette Modal (Ctrl+K) */}
      {showCommandPalette && (
        <div className="fixed inset-0 bg-[#050814]/80 backdrop-blur-xl z-50 flex items-start justify-center pt-24 p-4 font-sans select-none">
          <div className="bg-[#0D1527] border border-[#F5B942]/30 rounded-3xl max-w-xl w-full p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b border-white/10 pb-3">
              <span className="font-bold text-[#F5B942] text-sm">Search Features & Reports</span>
              <button onClick={() => setShowCommandPalette(false)} className="text-xs text-[#94A3B8] hover:text-white">✕ Esc</button>
            </div>
            <input
              type="text"
              value={globalSearch}
              onChange={e => setGlobalSearch(e.target.value)}
              placeholder="Type feature name (e.g., Dashas, Gemstones, Varshaphal)..."
              className="w-full bg-[#050814] border border-white/15 rounded-2xl px-4 py-3 text-sm text-[#F8FAFC] outline-none"
              autoFocus
            />
            <div className="space-y-1 max-h-60 overflow-y-auto">
              {navGroups.flatMap(g => g.items).filter(l => l.label.toLowerCase().includes(globalSearch.toLowerCase())).map(l => (
                <button
                  key={l.id}
                  onClick={() => {
                    setActiveTab(l.id)
                    setShowCommandPalette(false)
                  }}
                  className="w-full text-left px-4 py-2.5 rounded-xl hover:bg-[#F5B942]/10 hover:text-[#F5B942] text-xs font-semibold text-[#F8FAFC] flex items-center justify-between transition"
                >
                  <span>{l.icon} {l.label}</span>
                  <span className="text-[10px] text-[#94A3B8]">Jump →</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Profile Drawer */}
      {showProfileDrawer && (
        <div className="fixed inset-0 bg-[#050814]/80 backdrop-blur-xl z-50 flex justify-end font-sans select-none">
          <div className="bg-[#0D1527] border-l border-[#F5B942]/30 w-full max-w-md h-full p-6 space-y-6 shadow-2xl flex flex-col justify-between overflow-y-auto">
            <div className="space-y-6">
              <div className="flex items-center justify-between border-b border-white/10 pb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-[#F5B942] to-amber-600 text-[#050814] font-black text-sm flex items-center justify-center">
                    AK
                  </div>
                  <div>
                    <h3 className="font-bold text-[#F8FAFC] text-sm">Astro Seeker Account</h3>
                    <p className="text-[10px] text-[#94A3B8]">Authenticated Profile Session</p>
                  </div>
                </div>
                <button onClick={() => setShowProfileDrawer(false)} className="text-xs text-[#94A3B8] hover:text-white">✕</button>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between items-center text-xs">
                  <span className="font-bold text-[#F5B942] uppercase tracking-wider">Active Natal Profile</span>
                  <span className="text-[10px] text-[#34D399] font-bold">● DE440s Loaded</span>
                </div>

                <div className="p-4 rounded-2xl bg-[#050814] border border-[#F5B942]/30 space-y-2">
                  <p className="font-bold text-sm text-[#F8FAFC]">{name || 'Subramanian T S'}</p>
                  <p className="text-xs text-[#94A3B8] tabular-nums">
                    {year}-{String(month).padStart(2, '0')}-{String(day).padStart(2, '0')} • {String(hour).padStart(2, '0')}:{String(minute).padStart(2, '0')}
                  </p>
                  <p className="text-xs text-[#94A3B8]">{placeName}, {country}</p>
                </div>
              </div>
            </div>

            <button
              onClick={() => setShowProfileDrawer(false)}
              className="w-full py-3 rounded-2xl bg-white/10 hover:bg-white/20 text-[#F8FAFC] font-bold text-xs uppercase tracking-wider transition"
            >
              Close Drawer
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
