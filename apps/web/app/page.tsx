'use client'

import React, { useState } from 'react'

// Preset major cities with automatic coordinates, countries, and explicit IANA timezones
const CITIES = [
  { name: 'New Delhi', country: 'India', lat: 28.6139, lon: 77.2090, tz: 'Asia/Kolkata' },
  { name: 'Mumbai', country: 'India', lat: 18.9220, lon: 72.8347, tz: 'Asia/Kolkata' },
  { name: 'Bengaluru', country: 'India', lat: 12.9716, lon: 77.5946, tz: 'Asia/Kolkata' },
  { name: 'London', country: 'United Kingdom', lat: 51.5074, lon: -0.1278, tz: 'Europe/London' },
  { name: 'New York', country: 'United States', lat: 40.7128, lon: -74.0060, tz: 'America/New_York' },
  { name: 'Los Angeles', country: 'United States', lat: 34.0522, lon: -118.2437, tz: 'America/Los_Angeles' },
  { name: 'Tokyo', country: 'Japan', lat: 35.6762, lon: 139.6503, tz: 'Asia/Tokyo' },
  { name: 'Sydney', country: 'Australia', lat: -33.8688, lon: 151.2093, tz: 'Australia/Sydney' },
  { name: 'Paris', country: 'France', lat: 48.8566, lon: 2.3522, tz: 'Europe/Paris' },
  { name: 'Dubai', country: 'United Arab Emirates', lat: 25.2048, lon: 55.2708, tz: 'Asia/Dubai' },
  { name: 'Singapore', country: 'Singapore', lat: 1.3521, lon: 103.8198, tz: 'Asia/Singapore' },
  { name: 'Toronto', country: 'Canada', lat: 43.6532, lon: -79.3832, tz: 'America/Toronto' },
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

  // City selection & timezone state
  const [selectedCity, setSelectedCity] = useState(CITIES[0].name)
  const [latitude, setLatitude] = useState(CITIES[0].lat)
  const [longitude, setLongitude] = useState(CITIES[0].lon)
  const [placeName, setPlaceName] = useState(CITIES[0].name)
  const [country, setCountry] = useState(CITIES[0].country)
  const [timezoneStr, setTimezoneStr] = useState(CITIES[0].tz)
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
      setTimezoneStr(found.tz)
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
      const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const res = await fetch(`${API_BASE}/api/v1/birth-profile`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name, year, month, day, hour, minute, second: 0,
          timezone_str: timezoneStr,
          latitude, longitude,
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
      <aside className="w-80 bg-[#0A0D28]/95 border-r border-champagne/20 flex flex-col justify-between p-8 backdrop-blur-2xl shrink-0 hidden md:flex min-h-screen sticky top-0 shadow-2xl">
        <div className="space-y-10">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-champagne via-lightgold to-purple flex items-center justify-center text-midnight font-extrabold text-2xl shadow-xl border border-champagne/40">
              ✦
            </div>
            <div>
              <h1 className="text-2xl font-black text-champagne tracking-wider">Astrovision</h1>
              <p className="text-[10px] text-mutedtext uppercase tracking-widest font-semibold">NASA DE440s Ephemeris Engine</p>
            </div>
          </div>

          <nav className="space-y-1.5">
            {sidebarLinks.map(link => (
              <button
                key={link.id}
                onClick={() => setActiveTab(link.id)}
                className={`w-full text-left px-5 py-3.5 rounded-2xl transition duration-200 font-semibold text-sm flex items-center gap-3 ${
                  activeTab === link.id
                    ? 'bg-champagne/20 text-champagne border border-champagne/50 shadow-xl'
                    : 'text-mutedtext hover:text-ivory hover:bg-white/5'
                }`}
              >
                <span className="text-xs">✦</span>
                {link.label}
              </button>
            ))}
          </nav>
        </div>

        <div className="pt-6 border-t border-champagne/15 text-xs text-mutedtext space-y-1">
          <p className="font-bold text-champagne">Engine Version 6.0.0</p>
          <p>NASA JPL DE440s Sub-Arcsecond Kernel</p>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Loading Overlay */}
        {loading && (
          <div className="fixed inset-0 bg-midnight/95 backdrop-blur-2xl z-50 flex flex-col items-center justify-center p-8 space-y-8">
            <div className="relative w-32 h-32 flex items-center justify-center">
              <div className="absolute inset-0 rounded-full border-4 border-champagne/20 border-t-champagne animate-spin"></div>
              <div className="text-4xl text-champagne animate-pulse">✦</div>
            </div>
            <div className="text-center space-y-3 max-w-md">
              <h3 className="text-2xl font-extrabold text-champagne">Calculating Ephemeris State</h3>
              <p className="text-sm text-mutedtext">
                {loadingStep === 1 && 'Querying NASA JPL DE440s Ephemeris Kernel...'}
                {loadingStep === 2 && 'Normalizing Local Civil Time and Julian Day (UTC & TT)...'}
                {loadingStep === 3 && 'Evaluating 16 Parashari Vargas, Vimshottari Dashas & Yogas...'}
                {loadingStep === 4 && 'Synthesizing Canonical Astrology Evidence Package...'}
              </p>
            </div>
          </div>
        )}

        <main className="flex-1 p-10 space-y-10 w-full max-w-[1600px] mx-auto">
          {activeTab === 'chart-form' && (
            <div className="bg-[#17163A]/90 p-12 rounded-3xl border border-champagne/40 shadow-2xl max-w-4xl mx-auto backdrop-blur-2xl relative overflow-hidden w-full">
              <div className="absolute top-0 right-0 w-80 h-80 bg-purple/30 rounded-full blur-3xl pointer-events-none"></div>
              <h2 className="text-3xl font-extrabold mb-3 text-champagne">Enter Birth Details</h2>
              <p className="text-sm text-mutedtext mb-8">Enter your birth particulars to generate your personalized NASA JPL DE440s natal chart and astrological portrait.</p>

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

                <div className="grid grid-cols-2 gap-6">
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
                    <label className="block text-xs font-semibold uppercase tracking-widest text-mutedtext mb-2">IANA Timezone</label>
                    <input
                      type="text"
                      value={timezoneStr}
                      onChange={e => setTimezoneStr(e.target.value)}
                      placeholder="e.g. Asia/Kolkata"
                      className="w-full bg-[#050816] border border-champagne/40 rounded-2xl p-4 text-ivory focus:border-champagne outline-none transition text-base"
                      required
                    />
                  </div>
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
                  <p className="text-mutedtext text-base leading-relaxed">Please enter your exact birth particulars to calculate your NASA JPL DE440s natal chart and unlock your cosmic dashboard.</p>
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
                </>
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  )
}
