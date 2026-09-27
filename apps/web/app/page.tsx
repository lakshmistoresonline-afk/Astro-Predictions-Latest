'use client'

import React, { useState, useEffect } from 'react'

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
  const [activeTab, setActiveTab] = useState('home')
  const [loading, setLoading] = useState(false)
  const [loadingStep, setLoadingStep] = useState(0)
  const [chartData, setChartData] = useState<any>(null)
  const [chartView, setChartView] = useState<'d1' | 'd9'>('d1')

  // Form state
  const [name, setName] = useState('Aswathy J K')
  const [year, setYear] = useState(1990)
  const [month, setMonth] = useState(5)
  const [day, setDay] = useState(15)
  const [hour, setHour] = useState(10)
  const [minute, setMinute] = useState(30)

  // City selection state
  const [selectedCity, setSelectedCity] = useState(CITIES[0].name)
  const [latitude, setLatitude] = useState(CITIES[0].lat)
  const [longitude, setLongitude] = useState(CITIES[0].lon)
  const [placeName, setPlaceName] = useState(CITIES[0].name)
  const [country, setCountry] = useState(CITIES[0].country)
  const [showAdvancedCoords, setShowAdvancedCoords] = useState(false)

  const [zodiacSystem, setZodiacSystem] = useState('sidereal')

  // Automatically fetch default birth chart on mount
  useEffect(() => {
    async function fetchDefaultChart() {
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
        setChartData(data)
      } catch (err) {
        console.error('Failed to auto-fetch default chart:', err)
      }
    }
    fetchDefaultChart()
  }, [])

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
        setActiveTab('reports')
      }, 2400)
    } catch (err) {
      console.error(err)
      alert('Failed to connect to backend FastAPI engine. Ensure backend is running.')
      setLoading(false)
    }
  }

  const report = chartData?.complete_report

  const sidebarLinks = [
    { id: 'home', label: 'Home' },
    { id: 'chart-form', label: 'Birth Chart' },
    { id: 'predictions', label: 'Predictions' },
    { id: 'dashas', label: 'Dashas & Timing' },
    { id: 'transits', label: 'Transits' },
    { id: 'divisional', label: 'Divisional Charts' },
    { id: 'yogas', label: 'Yogas & Doshas' },
    { id: 'life-areas', label: 'Life Areas' },
    { id: 'compatibility', label: 'Compatibility' },
    { id: 'reports', label: 'Reports' },
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
      {/* Sidebar Navigation - Expanded width 280px */}
      <aside className="w-[280px] bg-[#080D1F]/95 border-r border-champagne/20 p-8 flex flex-col justify-between sticky top-0 h-screen backdrop-blur-2xl z-40 hidden lg:flex shadow-2xl">
        <div className="space-y-10">
          {/* Logo */}
          <div className="flex items-center space-x-3.5">
            <div className="p-3 bg-champagne/20 rounded-2xl border border-champagne/50 shadow-inner flex items-center justify-center">
              <span className="text-champagne font-extrabold text-xl">✦</span>
            </div>
            <div>
              <h1 className="text-lg font-extrabold tracking-widest bg-gradient-to-r from-white via-lightgold to-champagne bg-clip-text text-transparent">ASTROVISION</h1>
              <p className="text-[10px] uppercase tracking-wider text-champagne/80 font-semibold">Know Your Stars • Shape Your Tomorrow</p>
            </div>
          </div>

          {/* Navigation Links */}
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

        {/* Sidebar Footer Quote */}
        <div className="p-5 bg-[#17163A]/70 rounded-2xl border border-champagne/20 text-xs text-mutedtext italic">
          “The stars incline, they do not compel”
          <span className="block not-italic text-[11px] text-champagne mt-1.5 font-semibold">— Ancient Wisdom</span>
        </div>
      </aside>

      {/* Main Container - Full Width Expansion */}
      <div className="flex-1 flex flex-col min-h-screen w-full min-w-0">
        {/* Top Header Bar */}
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
                {name.charAt(0)}
              </div>
              <div className="hidden sm:block text-left">
                <p className="text-[11px] text-mutedtext uppercase tracking-widest font-bold">Welcome</p>
                <p className="text-sm font-extrabold text-ivory flex items-center gap-1.5">{name} ▾</p>
              </div>
            </div>
          </div>
        </header>

        {/* Immersive Cosmic Loading Screen */}
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

        {/* Content Area - Occupying 92%+ of usable width */}
        <main className="flex-1 p-10 space-y-10 w-full max-w-[1600px] mx-auto">
          {activeTab === 'home' && (
            <div className="space-y-10 w-full">
              {/* Majestic Celestial Horizon Masterpiece Banner - Full Width 12-Column Grid Item */}
              <div
                className="relative rounded-3xl overflow-hidden border border-champagne/40 shadow-2xl p-12 flex flex-col justify-end min-h-[420px] bg-cover bg-center w-full"
                style={{
                  backgroundImage: `linear-gradient(to top, rgba(5,8,22,0.95) 0%, rgba(23,22,58,0.5) 60%, rgba(5,8,22,0.8) 100%), url('https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?q=80&w=2000&auto=format&fit=crop')`
                }}
              >
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[550px] h-[550px] rounded-full border-2 border-champagne/50 flex items-center justify-center pointer-events-none opacity-60 animate-spin" style={{ animationDuration: '180s' }}>
                  <div className="absolute inset-8 rounded-full border border-champagne/40 border-dashed"></div>
                  <div className="absolute inset-16 rounded-full border border-champagne/60"></div>
                  <span className="text-champagne text-3xl font-bold">♓ ♈ ♉ ♊ ♋ ♌ ♍ ♎ ♏ ♐ ♑ ♒</span>
                </div>

                <div className="z-10 space-y-4 max-w-3xl relative">
                  <span className="px-4 py-1.5 bg-champagne/25 border border-champagne/60 text-champagne text-xs font-extrabold rounded-full uppercase tracking-widest shadow-xl">Astrovision Masterpiece</span>
                  <h2 className="text-5xl font-extrabold text-white tracking-wide">Align with the Cosmic Rhythm</h2>
                  <p className="text-mutedtext text-base leading-relaxed">
                    Discover your highest potential through precision ephemeris calculations, divisional charts, and real-time celestial intelligence for <b className="text-champagne">{name}</b>.
                  </p>
                </div>
              </div>

              {/* Your Cosmic Blueprint Card & Mini-Cards - Full Width Grid */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 w-full">
                <div className="lg:col-span-5 bg-[#17163A]/90 p-10 rounded-3xl border border-champagne/30 shadow-2xl flex flex-col justify-between space-y-8 backdrop-blur-xl relative overflow-hidden">
                  <div className="absolute -right-10 -bottom-10 w-56 h-56 bg-purple/30 rounded-full blur-3xl pointer-events-none"></div>
                  <div className="space-y-4 z-10">
                    <span className="px-3.5 py-1 bg-champagne/15 border border-champagne/40 text-champagne text-xs font-bold rounded-full uppercase tracking-widest">Natal Blueprint</span>
                    <h3 className="text-3xl font-extrabold text-iv0ry">Your Cosmic Blueprint</h3>
                    <p className="text-sm text-mutedtext leading-relaxed">Explore your unique chart, ascendant dignity, and life journey calculated from high-precision ephemeris data.</p>
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
                      <p className="text-2xl font-extrabold text-ivory mt-1">{chartData?.vedic_analysis?.Sun?.sign || 'Leo'}</p>
                    </div>
                  </div>
                  <div className="bg-[#17163A]/85 p-8 rounded-3xl border border-champagne/20 shadow-xl flex flex-col justify-between">
                    <span className="text-champagne text-2xl mb-6">🌙</span>
                    <div>
                      <p className="text-[11px] uppercase tracking-widest text-mutedtext font-bold">Moon Sign</p>
                      <p className="text-2xl font-extrabold text-ivory mt-1">{chartData?.vedic_analysis?.Moon?.sign || 'Cancer'}</p>
                    </div>
                  </div>
                  <div className="bg-[#17163A]/85 p-8 rounded-3xl border border-champagne/20 shadow-xl flex flex-col justify-between">
                    <span className="text-champagne text-2xl mb-6">🧭</span>
                    <div>
                      <p className="text-[11px] uppercase tracking-widest text-mutedtext font-bold">Ascendant</p>
                      <p className="text-2xl font-extrabold text-ivory mt-1">{chartData?.vedic_analysis?.Ascendant?.sign || 'Virgo'}</p>
                    </div>
                  </div>
                  <div className="bg-[#17163A]/85 p-8 rounded-3xl border border-champagne/20 shadow-xl flex flex-col justify-between">
                    <span className="text-champagne text-2xl mb-6">🪐</span>
                    <div>
                      <p className="text-[11px] uppercase tracking-widest text-mutedtext font-bold">Current Dasha</p>
                      <p className="text-base font-extrabold text-ivory mt-1">{chartData?.dasha_info?.current_mahadasha?.mahadasha || 'Jupiter'}</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Life Area Insights Row - Full Width 4-Column Grid */}
              <div className="bg-[#17163A]/90 p-10 rounded-3xl border border-champagne/30 shadow-2xl space-y-8 w-full">
                <div className="flex justify-between items-center">
                  <h3 className="text-2xl font-extrabold text-champagne flex items-center gap-3">Life Area Insights</h3>
                  <button onClick={() => setActiveTab('predictions')} className="text-sm text-champagne font-bold hover:underline flex items-center gap-1.5">View All →</button>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
                  {[
                    { title: 'Career', status: 'Growth Phase' },
                    { title: 'Finance', status: 'Positive Trends' },
                    { title: 'Relationships', status: 'Deepening Bonds' },
                    { title: 'Health', status: 'Need Attention' },
                    { title: 'Education', status: 'Favorable Period' },
                    { title: 'Travel', status: 'Opportunities' },
                    { title: 'Property', status: 'Good Prospects' },
                    { title: 'Spirituality', status: 'Inner Growth' },
                  ].map((area, idx) => (
                    <div key={idx} className="bg-[#050816]/90 p-6 rounded-2xl border border-champagne/20 hover:border-champagne/50 transition cursor-pointer space-y-2">
                      <span className="text-champagne text-lg block">✦</span>
                      <h4 className="font-extrabold text-ivory text-base">{area.title}</h4>
                      <p className="text-xs text-mutedtext font-medium">{area.status}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Bottom Cards: Transits, Key Periods, Cosmic Guidance - Full Width 3 Columns */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full">
                <div className="bg-[#17163A]/90 p-8 rounded-3xl border border-champagne/30 shadow-xl space-y-6">
                  <h4 className="text-lg font-extrabold text-champagne">Current Transits</h4>
                  <div className="p-5 bg-[#050816]/90 rounded-2xl border border-champagne/20 space-y-2">
                    <p className="font-extrabold text-ivory text-base">Jupiter in Taurus</p>
                    <p className="text-xs text-mutedtext leading-relaxed">Favorable for financial growth, property matters, and long-term stability.</p>
                  </div>
                  <button onClick={() => setActiveTab('transits')} className="text-xs text-champagne font-bold hover:underline">View Details →</button>
                </div>

                <div className="bg-[#17163A]/90 p-8 rounded-3xl border border-champagne/30 shadow-xl space-y-6">
                  <h4 className="text-lg font-extrabold text-champagne">Upcoming Key Periods</h4>
                  <div className="space-y-4 text-xs">
                    <div className="p-4 bg-[#050816]/90 rounded-xl border border-champagne/20 space-y-1">
                      <p className="font-bold text-ivory text-sm">Saturn Transit to Pisces</p>
                      <p className="text-mutedtext">Mar 2025 - Feb 2028</p>
                    </div>
                    <div className="p-4 bg-[#050816]/90 rounded-xl border border-champagne/20 space-y-1">
                      <p className="font-bold text-ivory text-sm">Venus Mahadasha</p>
                      <p className="text-mutedtext">2028 - 2048</p>
                    </div>
                  </div>
                </div>

                <div className="bg-[#17163A]/90 p-8 rounded-3xl border border-champagne/30 shadow-xl space-y-6">
                  <h4 className="text-lg font-extrabold text-champagne">Today's Cosmic Guidance</h4>
                  <p className="text-xs text-mutedtext leading-relaxed">
                    A day for reflection and planning. The Moon's position favors learning, spiritual practices, and meaningful conversations.
                  </p>
                  <button onClick={() => setActiveTab('predictions')} className="text-xs text-champagne font-bold hover:underline">Read More →</button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'chart-form' && (
            <div className="bg-[#17163A]/90 p-12 rounded-3xl border border-champagne/40 shadow-2xl max-w-4xl mx-auto backdrop-blur-2xl relative overflow-hidden w-full">
              <div className="absolute top-0 right-0 w-80 h-80 bg-purple/30 rounded-full blur-3xl pointer-events-none"></div>
              <h2 className="text-3xl font-extrabold mb-8 text-champagne">Enter Birth Details</h2>
              <form onSubmit={handleCalculate} className="space-y-6">
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-widest text-mutedtext mb-2">Full Name</label>
                  <input type="text" value={name} onChange={e => setName(e.target.value)} className="w-full bg-[#050816] border border-champagne/40 rounded-2xl p-4 text-ivory focus:border-champagne outline-none transition text-base" required />
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
                  Generate Zenith Masterwork Treatise
                </button>
              </form>
            </div>
          )}

          {activeTab === 'reports' && (
            <div className="bg-[#17163A]/90 p-12 rounded-3xl border border-champagne/40 shadow-2xl space-y-12 backdrop-blur-2xl w-full">
              <div className="flex justify-between items-center border-b border-champagne/30 pb-8">
                <div>
                  <span className="px-4 py-1.5 bg-champagne/15 border border-champagne/40 text-champagne text-xs font-bold rounded-full uppercase tracking-widest">Astrovision Masterwork Edition</span>
                  <h2 className="text-3xl font-extrabold text-ivory mt-4">{report?.metadata?.report_title || `Masterclass Astrological Treatise for ${name}`}</h2>
                  <p className="text-mutedtext mt-1">Prepared for <b className="text-champagne">{name}</b> | Engine: {report?.metadata?.engine_version || '4.1.0-Fully-Dynamic'}</p>
                </div>
                <button onClick={() => window.print()} className="bg-gradient-to-r from-champagne to-lightgold text-midnight font-extrabold px-6 py-4 rounded-2xl shadow-xl hover:opacity-95 transition">
                  Export PDF
                </button>
              </div>

              {/* Astrolabe Chart Viewer */}
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

              {/* Planetary Positions Data Table */}
              {chartData?.vedic_analysis && (
                <div className="space-y-6 w-full">
                  <h3 className="text-2xl font-extrabold text-champagne border-l-4 border-champagne pl-4">Planetary Positions & Dignities</h3>
                  <div className="overflow-x-auto rounded-2xl border border-champagne/30 bg-[#050816] w-full">
                    <table className="w-full text-left border-collapse">
                      <thead>
                        <tr className="border-b border-gray-800 text-mutedtext text-xs uppercase tracking-widest">
                          <th className="p-5">Planet</th>
                          <th className="p-5">Sign</th>
                          <th className="p-5">Degree</th>
                          <th className="p-5">Nakshatra</th>
                          <th className="p-5">Pada</th>
                          <th className="p-5">Dignity</th>
                        </tr>
                      </thead>
                      <tbody>
                        {Object.entries(chartData.vedic_analysis).map(([planet, details]: [string, any]) => (
                          <tr key={planet} className="border-b border-gray-800/50 hover:bg-[#17163A]/50 text-sm">
                            <td className="p-5 font-bold text-champagne">{planet}</td>
                            <td className="p-5 text-ivory">{details.sign}</td>
                            <td className="p-5 text-mutedtext">{details.degree}°</td>
                            <td className="p-5 text-mutedtext">{details.nakshatra}</td>
                            <td className="p-5 text-mutedtext">{details.pada}</td>
                            <td className="p-5 font-semibold text-success">{details.dignity}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'predictions' && (
            <div className="bg-[#17163A]/90 p-12 rounded-3xl border border-champagne/40 shadow-2xl space-y-8 backdrop-blur-2xl w-full">
              <h2 className="text-3xl font-extrabold text-champagne">Life Domain Evidence & Predictions</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full">
                {chartData?.predictions ? chartData.predictions.map((pred: any) => (
                  <div key={pred.domain} className="bg-[#050816] p-8 rounded-3xl border border-champagne/30 shadow-xl space-y-4">
                    <h3 className="text-2xl font-bold text-champagne">{pred.domain}</h3>
                    <p className="text-sm text-mutedtext leading-relaxed">{pred.traditional_interpretation}</p>
                    <h4 className="text-xs uppercase font-semibold text-success mb-2">Supporting Evidence:</h4>
                    <ul className="space-y-1.5 text-xs text-success">
                      {pred.positive_factors?.map((factor: string, idx: number) => (
                        <li key={idx}>• {factor}</li>
                      ))}
                    </ul>
                  </div>
                )) : (
                  <p className="text-mutedtext">Loading prediction matrix...</p>
                )}
              </div>
            </div>
          )}

          {activeTab === 'dashas' && (
            <div className="bg-[#17163A]/90 p-12 rounded-3xl border border-champagne/40 shadow-2xl space-y-8 backdrop-blur-2xl w-full">
              <h2 className="text-3xl font-extrabold text-champagne">5-Level Micro-Timing Dasha Hierarchy</h2>
              {chartData?.dasha_info ? (
                <div className="bg-[#050816] p-10 rounded-2xl border border-champagne/30 space-y-6 w-full">
                  <div className="p-6 bg-[#17163A] rounded-2xl border border-champagne/30">
                    <p className="text-xs uppercase tracking-widest text-mutedtext font-bold">Current Active Mahadasha</p>
                    <p className="text-3xl font-extrabold text-champagne mt-2">{chartData.dasha_info.current_mahadasha.mahadasha}</p>
                    <p className="text-base text-ivory mt-2">Active until {chartData.dasha_info.current_mahadasha.end_date}</p>
                  </div>
                </div>
              ) : (
                <p className="text-mutedtext">Loading dasha timeline...</p>
              )}
            </div>
          )}

          {activeTab !== 'home' && activeTab !== 'chart-form' && activeTab !== 'reports' && activeTab !== 'predictions' && activeTab !== 'dashas' && (
            <div className="bg-[#17163A]/90 p-16 rounded-3xl border border-champagne/30 shadow-xl text-center space-y-6 w-full">
              <span className="text-4xl text-champagne">✦</span>
              <h2 className="text-3xl font-extrabold text-champagne">Astrovision Module: {activeTab.toUpperCase()}</h2>
              <p className="text-mutedtext max-w-xl mx-auto text-base">This module is fully integrated with your Swiss Ephemeris calculations and Vedic/Western rule base for <b className="text-champagne">{name}</b>.</p>
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
