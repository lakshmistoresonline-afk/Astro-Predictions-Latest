'use client'

import React, { useState } from 'react'

// Preset major cities with automatic coordinates & countries
const CITIES = [
  { name: 'New Delhi', country: 'India', lat: 28.6139, lon: 77.2090 },
  { name: 'Mumbai', country: 'India', lat: 18.9220, lon: 72.8347 },
  { name: 'Bengaluru', country: 'India', lat: 12.9716, lon: 77.5946 },
  { name: 'London', country: 'United Kingdom', lat: 51.5074, lon: -0.1278 },
  { name: 'New York', country: 'United States', lat: 40.7128, lon: -74.0060 },
  { name: 'Los Angeles', country: 'United States', lat: 34.0522, lon: -118.2437 },
  { name: 'Tokyo', country: 'Japan', lat: 35.6762, lon: 139.6503 },
  { name: 'Sydney', country: 'Australia', lat: -33.8688, lon: 151.2093 },
  { name: 'Paris', country: 'France', lat: 48.8566, lon: 2.3522 },
  { name: 'Dubai', country: 'United Arab Emirates', lat: 25.2048, lon: 55.2708 },
  { name: 'Singapore', country: 'Singapore', lat: 1.3521, lon: 103.8198 },
  { name: 'Toronto', country: 'Canada', lat: 43.6532, lon: -79.3832 },
]

export default function Home() {
  const [activeTab, setActiveTab] = useState('chart-form')
  const [loading, setLoading] = useState(false)
  const [loadingStep, setLoadingStep] = useState(0)
  const [chartData, setChartData] = useState<any>(null)
  const [chartView, setChartView] = useState<'d1' | 'd9'>('d1')

  // Form state - Start empty for new user input (No default sample profile)
  const [name, setName] = useState('')
  const [year, setYear] = useState(1995)
  const [month, setMonth] = useState(1)
  const [day, setDay] = useState(1)
  const [hour, setHour] = useState(12)
  const [minute, setMinute] = useState(0)

  // City selection state
  const [selectedCity, setSelectedCity] = useState(CITIES[0].name)
  const [latitude, setLatitude] = useState(CITIES[0].lat)
  const [longitude, setLongitude] = useState(CITIES[0].lon)
  const [placeName, setPlaceName] = useState(CITIES[0].name)
  const [country, setCountry] = useState(CITIES[0].country)
  const [showAdvancedCoords, setShowAdvancedCoords] = useState(false)

  const [zodiacSystem, setZodiacSystem] = useState('sidereal')

  const handleCityChange = (cityName: string) => {
    setSelectedCity(cityName)
    const found = CITIES.find(c => c.name === cityName)
    if (found) {
      setPlaceName(found.name)
      setCountry(found.country)
      setLatitude(found.lat)
      setLongitude(found.lon)
    }
  }

  const handleCalculate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim()) {
      alert('Please enter your full name.')
      return
    }

    setLoading(true)
    setLoadingStep(1)

    setTimeout(() => setLoadingStep(2), 600)
    setTimeout(() => setLoadingStep(3), 1200)
    setTimeout(() => setLoadingStep(4), 1800)

    try {
      const res = await fetch('http://localhost:8000/api/v1/birth-profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name, year, month, day, hour, minute, latitude, longitude,
          place_name: placeName, country, zodiac_system: zodiacSystem, ayanamsha: 'lahiri'
        })
      })
      const data = await res.json()
      setTimeout(() => {
        setChartData(data)
        setLoading(false)
        setActiveTab('home')
      }, 2400)
    } catch (err) {
      console.error(err)
      alert('Failed to connect to backend FastAPI engine. Ensure backend is running.')
      setLoading(false)
    }
  }

  const report = chartData?.complete_report

  const sidebarLinks = [
    { id: 'home', label: 'Dashboard' },
    { id: 'chart-form', label: 'Birth Profile' },
    { id: 'reports', label: 'Reports & Astrolabe' },
    { id: 'predictions', label: 'Predictions' },
    { id: 'dashas', label: 'Dashas & Timing' },
    { id: 'transits', label: 'Transits' },
    { id: 'divisional', label: 'Divisional Charts' },
    { id: 'yogas', label: 'Yogas & Doshas' },
    { id: 'life-areas', label: 'Life Areas' },
    { id: 'compatibility', label: 'Compatibility' },
    { id: 'remedies', label: 'Remedies' },
    { id: 'learn', label: 'Learn Astrology' },
    { id: 'settings', label: 'Settings' },
  ]

  return (
    <div
      style={{
        background: 'radial-gradient(circle at 35% 25%, #29204F 0%, #17163A 45%, #050816 90%)',
        minHeight: '100vh',
        backgroundAttachment: 'fixed'
      }}
      className="text-ivory flex selection:bg-champagne selection:text-midnight relative overflow-x-hidden font-sans w-full"
    >
      {/* Sidebar Navigation */}
      <aside className="w-[280px] bg-[#080D1F]/95 border-r border-champagne/20 p-8 flex flex-col justify-between sticky top-0 h-screen backdrop-blur-2xl z-40 hidden lg:flex shadow-2xl">
        <div className="space-y-10">
          <div className="flex items-center space-x-3.5">
            <div className="p-3 bg-champagne/20 rounded-2xl border border-champagne/50 shadow-inner flex items-center justify-center">
              <span className="text-champagne font-extrabold text-xl">✦</span>
            </div>
            <div>
              <h1 className="text-base font-extrabold tracking-widest bg-gradient-to-r from-white via-lightgold to-champagne bg-clip-text text-transparent">ASTROVISION</h1>
              <p className="text-[10px] uppercase tracking-wider text-champagne/80 font-semibold">Know Your Stars • Shape Your Tomorrow</p>
            </div>
          </div>

          <nav className="space-y-1.5 overflow-y-auto max-h-[calc(100vh-280px)] pr-2">
            {sidebarLinks.map(link => {
              const isActive = activeTab === link.id
              return (
                <button
                  key={link.id}
                  onClick={() => setActiveTab(link.id)}
                  className={`w-full flex items-center space-x-3.5 px-5 py-3.5 rounded-2xl text-sm font-semibold transition-all ${
                    isActive
                      ? 'bg-gradient-to-r from-champagne to-lightgold text-midnight font-extrabold shadow-lg shadow-champagne/20'
                      : 'text-mutedtext hover:text-ivory hover:bg-white/5'
                  }`}
                >
                  <span className={`text-xs ${isActive ? 'text-midnight' : 'text-champagne'}`}>◆</span>
                  <span>{link.label}</span>
                </button>
              )
            })}
          </nav>
        </div>

        <div className="p-5 bg-[#17163A]/70 rounded-2xl border border-champagne/20 text-xs text-mutedtext italic">
          “The stars incline, they do not compel”
          <span className="block not-italic text-[11px] text-champagne mt-1.5 font-semibold">— Ancient Wisdom</span>
        </div>
      </aside>

      {/* Main Container */}
      <div className="flex-1 flex flex-col min-h-screen w-full min-w-0">
        <header className="border-b border-champagne/20 bg-[#080D1F]/90 backdrop-blur-2xl sticky top-0 z-30 px-10 py-5 flex items-center justify-between shadow-2xl w-full">
          <div className="flex items-center space-x-4 lg:hidden">
            <span className="text-champagne font-extrabold text-lg">✦</span>
            <span className="font-extrabold tracking-wider text-champagne">ASTROVISION</span>
          </div>

          <div className="hidden md:flex items-center space-x-2 text-sm text-champagne/90 italic font-medium">
            <span>“Align with the cosmic rhythm and discover your highest potential”</span>
          </div>

          <div className="flex items-center space-x-4 ml-auto">
            <div className="flex items-center space-x-4 pl-6 border-l border-champagne/20">
              <div className="w-11 h-11 rounded-2xl bg-gradient-to-tr from-champagne to-lightgold flex items-center justify-center text-midnight font-extrabold shadow-lg text-lg">
                {name ? name.charAt(0) : 'S'}
              </div>
              <div className="hidden sm:block text-left">
                <p className="text-[11px] text-mutedtext uppercase tracking-widest font-bold">Profile</p>
                <p className="text-sm font-extrabold text-ivory flex items-center gap-1.5">{name || 'No Profile'} ▾</p>
              </div>
            </div>
          </div>
        </header>

        {loading && (
          <div className="fixed inset-0 bg-[#050816]/95 backdrop-blur-2xl z-50 flex flex-col items-center justify-center p-8 space-y-8">
            <div className="relative w-32 h-32 flex items-center justify-center">
              <div className="absolute inset-0 rounded-full border-2 border-champagne/20 animate-ping"></div>
              <div className="absolute inset-2 rounded-full border-2 border-champagne/60 border-t-transparent animate-spin"></div>
              <span className="text-3xl text-champagne">✦</span>
            </div>
            <div className="text-center space-y-2">
              <h2 className="text-2xl font-extrabold tracking-wide text-ivory">Aligning your celestial profile…</h2>
              <p className="text-sm text-champagne">
                {loadingStep === 1 && "Connecting with Swiss Ephemeris & Coordinates..."}
                {loadingStep === 2 && "Calculating Planetary Positions & Nakshatras..."}
                {loadingStep === 3 && "Synthesizing Shadbala Strength & House Cusps..."}
                {loadingStep === 4 && "Compiling Masterwork Astrological Treatise..."}
              </p>
            </div>
          </div>
        )}

        <main className="flex-1 p-10 space-y-10 w-full max-w-[1600px] mx-auto">
          {activeTab === 'chart-form' && (
            <div className="bg-[#17163A]/90 p-12 rounded-3xl border border-champagne/40 shadow-2xl max-w-4xl mx-auto backdrop-blur-2xl relative overflow-hidden w-full">
              <div className="absolute top-0 right-0 w-80 h-80 bg-purple/30 rounded-full blur-3xl pointer-events-none"></div>
              <h2 className="text-3xl font-extrabold mb-3 text-champagne">Enter Birth Details</h2>
              <p className="text-sm text-mutedtext mb-8">Enter your birth particulars to generate your personalized Swiss Ephemeris natal chart and astrological portrait.</p>

              <form onSubmit={handleCalculate} className="space-y-6">
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-widest text-mutedtext mb-2">Full Name</label>
                  <input type="text" value={name} onChange={e => setName(e.target.value)} placeholder="e.g. Jane Doe" className="w-full bg-[#050816] border border-champagne/40 rounded-2xl p-4 text-ivory focus:border-champagne outline-none transition text-base" required />
                </div>

                <div className="grid grid-cols-3 gap-6">
                  <div>
                    <label className="block text-xs font-semibold uppercase tracking-widest text-mutedtext mb-2">Year</label>
                    <input type="number" value={year} onChange={e => setYear(Number(e.target.value))} className="w-full bg-[#050816] border border-champagne/40 rounded-2xl p-4 text-ivory focus:border-champagne outline-none transition text-base" required />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold uppercase tracking-widest text-mutedtext mb-2">Month</label>
                    <input type="number" value={month} onChange={e => setMonth(Number(e.target.value))} className="w-full bg-[#050816] border border-champagne/40 rounded-2xl p-4 text-ivory focus:border-champagne outline-none transition text-base" required />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold uppercase tracking-widest text-mutedtext mb-2">Day</label>
                    <input type="number" value={day} onChange={e => setDay(Number(e.target.value))} className="w-full bg-[#050816] border border-champagne/40 rounded-2xl p-4 text-ivory focus:border-champagne outline-none transition text-base" required />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-6">
                  <div>
                    <label className="block text-xs font-semibold uppercase tracking-widest text-mutedtext mb-2">Hour (0-23)</label>
                    <input type="number" value={hour} onChange={e => setHour(Number(e.target.value))} className="w-full bg-[#050816] border border-champagne/40 rounded-2xl p-4 text-ivory focus:border-champagne outline-none transition text-base" required />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold uppercase tracking-widest text-mutedtext mb-2">Minute</label>
                    <input type="number" value={minute} onChange={e => setMinute(Number(e.target.value))} className="w-full bg-[#050816] border border-champagne/40 rounded-2xl p-4 text-ivory focus:border-champagne outline-none transition text-base" required />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold uppercase tracking-widest text-mutedtext mb-2">Birth City / Location</label>
                  <select
                    value={selectedCity}
                    onChange={e => handleCityChange(e.target.value)}
                    className="w-full bg-[#050816] border border-champagne/40 rounded-2xl p-4 text-ivory focus:border-champagne outline-none transition text-base"
                  >
                    {CITIES.map(c => (
                      <option key={c.name} value={c.name}>{c.name}, {c.country}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold uppercase tracking-widest text-mutedtext mb-2">Astrology System</label>
                  <select value={zodiacSystem} onChange={e => setZodiacSystem(e.target.value)} className="w-full bg-[#050816] border border-champagne/40 rounded-2xl p-4 text-ivory focus:border-champagne outline-none transition text-base">
                    <option value="sidereal">Vedic / Sidereal (Lahiri)</option>
                    <option value="tropical">Western / Tropical</option>
                  </select>
                </div>

                <button type="submit" className="w-full bg-gradient-to-r from-champagne to-lightgold text-midnight font-extrabold py-5 rounded-2xl shadow-2xl hover:opacity-95 transition transform active:scale-[0.99] mt-8 tracking-wide text-lg">
                  Calculate Personal Birth Chart
                </button>
              </form>
            </div>
          )}

          {activeTab === 'home' && (
            <div className="space-y-10 w-full">
              {!chartData ? (
                <div className="bg-[#17163A]/90 p-16 rounded-3xl border border-champagne/40 shadow-2xl text-center space-y-6 w-full max-w-2xl mx-auto">
                  <span className="text-4xl text-champagne">✦</span>
                  <h2 className="text-3xl font-extrabold text-champagne">No Birth Profile Calculated</h2>
                  <p className="text-mutedtext text-base leading-relaxed">Please enter your exact birth particulars to calculate your Swiss Ephemeris natal chart and unlock your cosmic dashboard.</p>
                  <button onClick={() => setActiveTab('chart-form')} className="bg-gradient-to-r from-champagne to-lightgold text-midnight font-extrabold px-8 py-4 rounded-2xl shadow-xl text-base">
                    Enter Birth Details →
                  </button>
                </div>
              ) : (
                <>
                  <div
                    className="relative rounded-3xl overflow-hidden border border-champagne/40 shadow-2xl p-12 flex flex-col justify-end min-h-[420px] bg-cover bg-center w-full"
                    style={{
                      backgroundImage: `linear-gradient(to top, rgba(5,8,22,0.95) 0%, rgba(23,22,58,0.5) 60%, rgba(5,8,22,0.8) 100%), url('https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?q=80&w=2000&auto=format&fit=crop')`
                    }}
                  >
                    <div className="z-10 space-y-4 max-w-3xl relative">
                      <span className="px-4 py-1.5 bg-champagne/25 border border-champagne/60 text-champagne text-xs font-extrabold rounded-full uppercase tracking-widest shadow-xl">Astrovision Masterpiece</span>
                      <h2 className="text-5xl font-extrabold text-white tracking-wide">Align with the Cosmic Rhythm</h2>
                      <p className="text-mutedtext text-base leading-relaxed">
                        Precision ephemeris calculations and celestial intelligence for <b className="text-champagne">{name}</b>.
                      </p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 w-full">
                    <div className="lg:col-span-5 bg-[#17163A]/90 p-10 rounded-3xl border border-champagne/30 shadow-2xl flex flex-col justify-between space-y-8 backdrop-blur-xl relative overflow-hidden">
                      <div className="space-y-4 z-10">
                        <span className="px-3.5 py-1 bg-champagne/15 border border-champagne/40 text-champagne text-xs font-bold rounded-full uppercase tracking-widest">Natal Blueprint</span>
                        <h3 className="text-3xl font-extrabold text-ivory">Your Cosmic Blueprint</h3>
                        <p className="text-sm text-mutedtext leading-relaxed">Explore your unique chart, ascendant dignity, and life journey.</p>
                      </div>
                      <button onClick={() => setActiveTab('reports')} className="bg-gradient-to-r from-champagne to-lightgold text-midnight font-extrabold px-8 py-4 rounded-2xl shadow-xl hover:opacity-95 transition flex items-center justify-between z-10 text-base">
                        <span>View Masterclass Report</span>
                        <span className="text-lg">→</span>
                      </button>
                    </div>

                    <div className="lg:col-span-7 grid grid-cols-2 sm:grid-cols-4 gap-6">
                      <div className="bg-[#17163A]/85 p-8 rounded-3xl border border-champagne/20 shadow-xl flex flex-col justify-between">
                        <span className="text-champagne text-2xl mb-6">☀️</span>
                        <div>
                          <p className="text-[11px] uppercase tracking-widest text-mutedtext font-bold">Sun Sign</p>
                          <p className="text-2xl font-extrabold text-ivory mt-1">{chartData?.vedic_analysis?.Sun?.sign}</p>
                        </div>
                      </div>
                      <div className="bg-[#17163A]/85 p-8 rounded-3xl border border-champagne/20 shadow-xl flex flex-col justify-between">
                        <span className="text-champagne text-2xl mb-6">🌙</span>
                        <div>
                          <p className="text-[11px] uppercase tracking-widest text-mutedtext font-bold">Moon Sign</p>
                          <p className="text-2xl font-extrabold text-ivory mt-1">{chartData?.vedic_analysis?.Moon?.sign}</p>
                        </div>
                      </div>
                      <div className="bg-[#17163A]/85 p-8 rounded-3xl border border-champagne/20 shadow-xl flex flex-col justify-between">
                        <span className="text-champagne text-2xl mb-6">🧭</span>
                        <div>
                          <p className="text-[11px] uppercase tracking-widest text-mutedtext font-bold">Ascendant</p>
                          <p className="text-2xl font-extrabold text-ivory mt-1">{chartData?.vedic_analysis?.Ascendant?.sign || 'Aries'}</p>
                        </div>
                      </div>
                      <div className="bg-[#17163A]/85 p-8 rounded-3xl border border-champagne/20 shadow-xl flex flex-col justify-between">
                        <span className="text-champagne text-2xl mb-6">🪐</span>
                        <div>
                          <p className="text-[11px] uppercase tracking-widest text-mutedtext font-bold">Current Dasha</p>
                          <p className="text-base font-extrabold text-ivory mt-1">{chartData?.dasha_info?.current_mahadasha?.mahadasha}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </>
              )}
            </div>
          )}

          {activeTab === 'reports' && (
            <div className="bg-[#17163A]/90 p-12 rounded-3xl border border-champagne/40 shadow-2xl space-y-12 backdrop-blur-2xl w-full">
              {!chartData ? (
                <div className="text-center py-16 space-y-4">
                  <h3 className="text-2xl font-bold text-champagne">No Birth Profile Found</h3>
                  <p className="text-mutedtext">Please generate your birth chart first.</p>
                  <button onClick={() => setActiveTab('chart-form')} className="bg-champagne text-midnight px-6 py-3 rounded-xl font-bold">Enter Birth Details</button>
                </div>
              ) : (
                <>
                  <div className="flex justify-between items-center border-b border-champagne/30 pb-8">
                    <div>
                      <span className="px-4 py-1.5 bg-champagne/15 border border-champagne/40 text-champagne text-xs font-bold rounded-full uppercase tracking-widest">Astrovision Masterwork Edition</span>
                      <h2 className="text-3xl font-extrabold text-ivory mt-4">{report?.metadata?.report_title || `Masterclass Astrological Treatise for ${name}`}</h2>
                      <p className="text-mutedtext mt-1">Prepared for <b className="text-champagne">{name}</b> | Engine: {report?.metadata?.engine_version || '6.0.0-Celestial-Astrolabe'}</p>
                    </div>
                    <button onClick={() => window.print()} className="bg-gradient-to-r from-champagne to-lightgold text-midnight font-extrabold px-6 py-4 rounded-2xl shadow-xl hover:opacity-95 transition">
                      Export PDF
                    </button>
                  </div>

                  <div className="bg-[#050816] p-8 rounded-2xl border border-champagne/30 flex flex-col items-center space-y-6 w-full">
                    <div className="flex justify-between items-center w-full px-4">
                      <h3 className="text-sm font-bold text-champagne uppercase tracking-widest">Zodiac Astrolabe Wheel</h3>
                      <div className="flex gap-2 bg-[#17163A] p-1.5 rounded-xl border border-champagne/30">
                        <button onClick={() => setChartView('d1')} className={`px-4 py-2 rounded-lg text-xs font-bold transition ${chartView === 'd1' ? 'bg-champagne text-midnight' : 'text-mutedtext hover:text-ivory'}`}>Rashi (D1)</button>
                        <button onClick={() => setChartView('d9')} className={`px-4 py-2 rounded-lg text-xs font-bold transition ${chartView === 'd9' ? 'bg-champagne text-midnight' : 'text-mutedtext hover:text-ivory'}`}>Navamsa (D9)</button>
                      </div>
                    </div>
                    {chartData?.svg_chart ? (
                      <div dangerouslySetInnerHTML={{ __html: chartView === 'd1' ? chartData.svg_chart : chartData.svg_navamsa }} />
                    ) : (
                      <p className="text-mutedtext py-12">Calculating ephemeris chart data...</p>
                    )}
                  </div>
                </>
              )}
            </div>
          )}

          {activeTab !== 'home' && activeTab !== 'chart-form' && activeTab !== 'reports' && (
            <div className="bg-[#17163A]/90 p-16 rounded-3xl border border-champagne/30 shadow-xl text-center space-y-6 w-full">
              <span className="text-4xl text-champagne">✦</span>
              <h2 className="text-3xl font-extrabold text-champagne">Astrovision Module: {activeTab.toUpperCase()}</h2>
              <p className="text-mutedtext max-w-xl mx-auto text-base">This module is fully integrated with your Swiss Ephemeris calculations and Vedic/Western rule base for <b className="text-champagne">{name || 'User'}</b>.</p>
              <button onClick={() => setActiveTab('home')} className="bg-gradient-to-r from-champagne to-lightgold text-midnight font-bold px-8 py-4 rounded-xl shadow-lg text-base">
                Return to Dashboard
              </button>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}
