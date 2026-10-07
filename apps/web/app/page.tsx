'use client'

import React, { useState } from 'react'
import { PRESET_CITIES, BirthProfileResponse } from '../types/api'
import { calculateBirthProfile, interpretEvidenceAi } from '../services/apiClient'

import { LoadingState } from '../components/ui/LoadingState'
import { ErrorState } from '../components/ui/ErrorState'
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
      }, 2400)
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

  const sidebarLinks: { id: NavigationTab; label: string }[] = [
    { id: 'home', label: 'Dashboard' },
    { id: 'chart-form', label: 'Birth Profile' },
    { id: 'reports', label: 'Kundali Astrolabe' },
    { id: 'planets', label: 'Planetary Positions' },
    { id: 'vargas', label: '16 Vargas' },
    { id: 'dashas', label: 'Vimshottari Dashas' },
    { id: 'yogas', label: 'Yogas & Doshas' },
    { id: 'strength', label: 'Shadbala & SAV' },
    { id: 'jaimini', label: 'Jaimini Sutras' },
    { id: 'panchanga', label: 'Panchanga & Muhurta' },
    { id: 'predictions', label: '14 Domain Predictions' },
    { id: 'ai', label: 'AI Interpretation' },
  ]

  const loadingStepMessage =
    loadingStep === 1 ? 'Querying NASA JPL DE440s Ephemeris Kernel...' :
    loadingStep === 2 ? 'Normalizing Local Civil Time and Julian Day (UTC & TT)...' :
    loadingStep === 3 ? 'Evaluating 16 Parashari Vargas, Vimshottari Dashas & Yogas...' :
    'Synthesizing Canonical Astrology Evidence Package...'

  return (
    <div
      style={{
        background: 'radial-gradient(circle at 35% 25%, #29204F 0%, #17163A 45%, #050816 90%)',
        minHeight: '100vh',
        backgroundAttachment: 'fixed'
      }}
      className="text-[#FFFFF0] flex selection:bg-[#F3E5AB] selection:text-[#050816] relative overflow-x-hidden font-sans w-full"
    >
      {/* Sidebar Navigation */}
      <aside className="w-80 bg-[#0A0D28]/95 border-r border-[#F3E5AB]/20 flex flex-col justify-between p-8 backdrop-blur-2xl shrink-0 hidden md:flex min-h-screen sticky top-0 shadow-2xl">
        <div className="space-y-10">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-[#F3E5AB] via-[#F7E792] to-purple-600 flex items-center justify-center text-[#050816] font-extrabold text-2xl shadow-xl border border-[#F3E5AB]/40">
              ✦
            </div>
            <div>
              <h1 className="text-2xl font-black text-[#F3E5AB] tracking-wider">Astrovision</h1>
              <p className="text-[10px] text-[#A0A5C0] uppercase tracking-widest font-semibold">NASA DE440s Ephemeris Engine</p>
            </div>
          </div>

          <nav className="space-y-1.5">
            {sidebarLinks.map(link => (
              <button
                key={link.id}
                onClick={() => setActiveTab(link.id)}
                className={`w-full text-left px-5 py-3.5 rounded-2xl transition duration-200 font-semibold text-sm flex items-center gap-3 ${
                  activeTab === link.id
                    ? 'bg-[#F3E5AB]/20 text-[#F3E5AB] border border-[#F3E5AB]/50 shadow-xl'
                    : 'text-[#A0A5C0] hover:text-[#FFFFF0] hover:bg-white/5'
                }`}
              >
                <span className="text-xs">✦</span>
                {link.label}
              </button>
            ))}
          </nav>
        </div>

        <div className="pt-6 border-t border-[#F3E5AB]/15 text-xs text-[#A0A5C0] space-y-1">
          <p className="font-bold text-[#F3E5AB]">Engine Version 6.0.0</p>
          <p>NASA JPL DE440s Sub-Arcsecond Kernel</p>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Mobile Navigation Bar */}
        <header className="md:hidden bg-[#0A0D28]/95 border-b border-[#F3E5AB]/20 p-4 flex justify-between items-center sticky top-0 z-40 backdrop-blur-xl">
          <div className="flex items-center gap-2">
            <span className="text-xl text-[#F3E5AB]">✦</span>
            <span className="font-extrabold text-[#F3E5AB]">Astrovision</span>
          </div>
          <select
            value={activeTab}
            onChange={e => setActiveTab(e.target.value as NavigationTab)}
            className="bg-[#050816] border border-[#F3E5AB]/40 rounded-xl p-2 text-xs text-[#FFFFF0]"
          >
            {sidebarLinks.map(l => (
              <option key={l.id} value={l.id}>{l.label}</option>
            ))}
          </select>
        </header>

        {/* Loading Overlay */}
        {loading && <LoadingState stepMessage={loadingStepMessage} />}

        <main className="flex-1 p-6 md:p-10 space-y-10 w-full max-w-[1600px] mx-auto">
          {errorMsg && (
            <ErrorState
              message={errorMsg}
              onRetry={() => setErrorMsg(null)}
            />
          )}

          {activeTab === 'chart-form' && (
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
              onSubmit={handleCalculate}
            />
          )}

          {activeTab === 'home' && (
            chartData ? (
              <DashboardOverview
                data={chartData}
                onNewProfile={() => setActiveTab('chart-form')}
              />
            ) : (
              <div className="bg-[#17163A]/90 p-16 rounded-3xl border border-[#F3E5AB]/40 shadow-2xl text-center space-y-6 w-full max-w-2xl mx-auto">
                <span className="text-4xl text-[#F3E5AB]">✦</span>
                <h2 className="text-3xl font-extrabold text-[#F3E5AB]">No Birth Profile Calculated</h2>
                <p className="text-[#A0A5C0] text-base leading-relaxed">
                  Please enter your exact birth particulars to calculate your NASA JPL DE440s natal chart and unlock your cosmic dashboard.
                </p>
                <button
                  onClick={() => setActiveTab('chart-form')}
                  className="bg-gradient-to-r from-[#F3E5AB] to-[#F7E792] text-[#050816] font-extrabold px-8 py-4 rounded-2xl shadow-xl text-base"
                >
                  Enter Birth Details →
                </button>
              </div>
            )
          )}

          {activeTab === 'reports' && (
            <KundaliAstrolabe svgChart={chartData?.svg_chart || null} />
          )}

          {activeTab === 'planets' && (
            masterEv?.canonical_chart ? (
              <PlanetaryPositionsTable chart={masterEv.canonical_chart} />
            ) : (
              <div className="text-center py-12 text-[#A0A5C0]">Please calculate a birth profile first.</div>
            )
          )}

          {activeTab === 'vargas' && (
            <VargasGrid vargaSuite={masterEv?.varga_suite} />
          )}

          {activeTab === 'dashas' && (
            <DashasTimeline dashaSuite={masterEv?.natal_dasha_suite} />
          )}

          {activeTab === 'yogas' && (
            <YogasDoshasView yogaSuite={masterEv?.yoga_suite} doshaSuite={masterEv?.dosha_suite} />
          )}

          {activeTab === 'strength' && (
            <ShadbalaAshtakavargaView
              shadbalaSuite={masterEv?.shadbala_suite}
              ashtakavargaEvidence={masterEv?.ashtakavarga_evidence}
            />
          )}

          {activeTab === 'jaimini' && (
            <JaiminiView jaiminiSuite={masterEv?.jaimini_suite} />
          )}

          {activeTab === 'panchanga' && (
            <PanchangaMuhurtaView
              panchanga={masterEv?.panchanga}
              muhurtaSuite={masterEv?.muhurta_suite}
            />
          )}

          {activeTab === 'predictions' && (
            <PredictionsView predictions={chartData?.predictions} />
          )}

          {activeTab === 'ai' && (
            <AiInterpretationView onInterpret={handleAiInterpret} />
          )}
        </main>
      </div>
    </div>
  )
}
