import React, { useState } from 'react'
import { PRESET_CITIES } from '../../types/api'

interface BirthProfileFormProps {
  name: string
  setName: (v: string) => void
  year: number
  setYear: (v: number) => void
  month: number
  setMonth: (v: number) => void
  day: number
  setDay: (v: number) => void
  hour: number
  setHour: (v: number) => void
  minute: number
  setMinute: (v: number) => void
  selectedCity: string
  handleCityChange: (city: string) => void
  timezoneStr: string
  setTimezoneStr: (v: string) => void
  zodiacSystem: string
  setZodiacSystem: (v: string) => void
  latitude: number
  setLatitude: (v: number) => void
  longitude: number
  setLongitude: (v: number) => void
  placeName: string
  setPlaceName: (v: string) => void
  country: string
  setCountry: (v: string) => void
  onSubmit: (e: React.FormEvent) => void
}

export const BirthProfileForm: React.FC<BirthProfileFormProps> = ({
  name, setName,
  year, setYear,
  month, setMonth,
  day, setDay,
  hour, setHour,
  minute, setMinute,
  selectedCity, handleCityChange,
  timezoneStr, setTimezoneStr,
  zodiacSystem, setZodiacSystem,
  latitude, setLatitude,
  longitude, setLongitude,
  placeName, setPlaceName,
  country, setCountry,
  onSubmit
}) => {
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [chartStyle, setChartStyle] = useState<'north' | 'south'>('north')
  const [saveProfile, setSaveProfile] = useState(true)

  // Popular quick selection cities
  const quickCities = [
    'Palakkad', 'New Delhi', 'Mumbai', 'Bengaluru', 'Chennai', 'Kochi', 'London', 'New York', 'Dubai'
  ]

  const filteredCities = PRESET_CITIES.filter(c =>
    c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    c.country.toLowerCase().includes(searchQuery.toLowerCase())
  )

  // Synchronized HTML Date Picker YYYY-MM-DD
  const datePickerValue = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`

  const handleDatePickerChange = (val: string) => {
    if (!val) return
    const parts = val.split('-')
    if (parts.length === 3) {
      const y = parseInt(parts[0], 10)
      const m = parseInt(parts[1], 10)
      const d = parseInt(parts[2], 10)
      if (!isNaN(y) && y >= 1850 && y <= 2150) setYear(y)
      if (!isNaN(m) && m >= 1 && m <= 12) setMonth(m)
      if (!isNaN(d) && d >= 1 && d <= 31) setDay(d)
    }
  }

  // Synchronized HTML Time Picker HH:MM
  const timePickerValue = `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`

  const handleTimePickerChange = (val: string) => {
    if (!val) return
    const parts = val.split(':')
    if (parts.length >= 2) {
      const h = parseInt(parts[0], 10)
      const m = parseInt(parts[1], 10)
      if (!isNaN(h) && h >= 0 && h <= 23) setHour(h)
      if (!isNaN(m) && m >= 0 && m <= 59) setMinute(m)
    }
  }

  const handleReset = () => {
    setName('')
    setYear(1995)
    setMonth(1)
    setDay(1)
    setHour(12)
    setMinute(0)
    handleCityChange(PRESET_CITIES[0].name)
  }

  return (
    <div className="w-full max-w-[1500px] mx-auto space-y-6">
      {/* Step Indicators Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-[#111B30]/90 border border-white/10 p-4 rounded-2xl backdrop-blur-xl font-mono text-xs">
        <div className="flex items-center gap-3">
          <span className="w-6 h-6 rounded-full bg-[#F5B942] text-[#070D1B] font-bold flex items-center justify-center text-xs">1</span>
          <span className="font-bold text-[#E8EDF7]">Birth Details</span>
          <span className="text-[#94A3B8]">→</span>
          <span className="w-6 h-6 rounded-full bg-white/10 text-[#94A3B8] font-bold flex items-center justify-center text-xs">2</span>
          <span className="text-[#94A3B8]">Location</span>
          <span className="text-[#94A3B8]">→</span>
          <span className="w-6 h-6 rounded-full bg-white/10 text-[#94A3B8] font-bold flex items-center justify-center text-xs">3</span>
          <span className="text-[#94A3B8]">Preview & Calculate</span>
        </div>
        <span className="text-[#34D399] font-bold flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-[#34D399] animate-pulse"></span>
          NASA DE440s Active
        </span>
      </div>

      {/* Spacious 2-Column Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* LEFT COLUMN: Birth Particulars Input Form (7 Cols) */}
        <div className="lg:col-span-7 bg-[#111B30]/90 backdrop-blur-2xl p-6 md:p-10 rounded-3xl border border-white/10 shadow-2xl space-y-6">
          <div className="border-b border-white/10 pb-5">
            <span className="px-3 py-1 rounded-full bg-[#F5B942]/10 border border-[#F5B942]/30 text-[#F5B942] text-xs font-mono font-bold uppercase tracking-widest">
              Natal Parameter Input
            </span>
            <h2 className="text-2xl md:text-3xl font-black text-[#E8EDF7] tracking-wide mt-2 font-serif-heading">
              Enter Birth Particulars
            </h2>
            <p className="text-xs text-[#94A3B8] font-sans mt-1 leading-relaxed">
              Provide accurate birth details to calculate your canonical astrological profile.
            </p>
          </div>

          <form onSubmit={onSubmit} className="space-y-6">
            {/* Full Name */}
            <div>
              <label className="block text-xs font-mono font-semibold uppercase tracking-wider text-[#94A3B8] mb-2">
                Full Name <span className="text-[#F5B942]">*</span>
              </label>
              <input
                type="text"
                value={name}
                onChange={e => setName(e.target.value)}
                placeholder="e.g. Subramanian T S"
                className="w-full bg-[#070D1B] border border-white/15 rounded-2xl px-4 py-3.5 text-[#E8EDF7] focus:border-[#F5B942] focus:ring-2 focus:ring-[#F5B942]/20 outline-none transition text-base font-sans"
                required
              />
            </div>

            {/* Date & Time Section */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {/* Easy Calendar Date Picker */}
              <div className="space-y-2">
                <label className="block text-xs font-mono font-semibold uppercase tracking-wider text-[#94A3B8]">
                  Date of Birth <span className="text-[#F5B942]">*</span>
                </label>
                <input
                  type="date"
                  value={datePickerValue}
                  onChange={e => handleDatePickerChange(e.target.value)}
                  className="w-full bg-[#070D1B] border border-white/15 rounded-2xl px-4 py-3 text-[#E8EDF7] focus:border-[#F5B942] outline-none font-mono text-sm cursor-pointer"
                  required
                />
                <p className="text-[11px] text-[#94A3B8] font-mono">
                  Selected: <strong className="text-[#F5B942]">{day} / {month} / {year}</strong>
                </p>
              </div>

              {/* Easy Time Picker (24-Hour Format) */}
              <div className="space-y-2">
                <label className="block text-xs font-mono font-semibold uppercase tracking-wider text-[#94A3B8]">
                  Time of Birth (24-Hour Format) <span className="text-[#F5B942]">*</span>
                </label>
                <input
                  type="time"
                  value={timePickerValue}
                  onChange={e => handleTimePickerChange(e.target.value)}
                  className="w-full bg-[#070D1B] border border-white/15 rounded-2xl px-4 py-3 text-[#E8EDF7] focus:border-[#F5B942] outline-none font-mono text-sm cursor-pointer"
                  required
                />
                <p className="text-[11px] text-[#94A3B8] font-mono">
                  Selected: <strong className="text-[#F5B942]">{String(hour).padStart(2, '0')}:{String(minute).padStart(2, '0')} (24h)</strong>
                </p>
              </div>
            </div>

            {/* Location Selector */}
            <div className="space-y-3 font-mono">
              <label className="block text-xs font-semibold uppercase tracking-wider text-[#94A3B8]">
                Select Birth Location
              </label>

              {/* Quick City Preset Chips */}
              <div className="flex flex-wrap items-center gap-2 pb-1">
                <span className="text-[11px] text-[#94A3B8] mr-1">Quick Select:</span>
                {quickCities.map(city => (
                  <button
                    key={city}
                    type="button"
                    onClick={() => handleCityChange(city)}
                    className={`px-3 py-1 rounded-xl text-xs transition border ${
                      selectedCity === city
                        ? 'bg-[#F5B942]/20 border-[#F5B942] text-[#F5B942] font-bold'
                        : 'bg-[#070D1B] border-white/10 text-[#94A3B8] hover:text-[#E8EDF7] hover:border-white/20'
                    }`}
                  >
                    {city}
                  </button>
                ))}
              </div>

              {/* Search Filter Box */}
              <input
                type="text"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                placeholder="Filter city list e.g. New Delhi, Mumbai, London, Tokyo..."
                className="w-full bg-[#070D1B] border border-white/15 rounded-2xl px-4 py-3 text-[#E8EDF7] placeholder-[#94A3B8] focus:border-[#F5B942] outline-none transition text-xs mb-2"
              />

              {/* City Dropdown */}
              <select
                value={selectedCity}
                onChange={e => handleCityChange(e.target.value)}
                className="w-full bg-[#070D1B] border border-white/15 rounded-2xl p-3.5 text-[#E8EDF7] focus:border-[#F5B942] outline-none transition text-xs font-semibold cursor-pointer"
              >
                {filteredCities.map(c => (
                  <option key={c.name} value={c.name} className="bg-[#070D1B] text-[#E8EDF7]">
                    {c.name}, {c.country} ({c.tz})
                  </option>
                ))}
              </select>

              {/* Selected Location Summary Card */}
              <div className="p-4 rounded-2xl bg-[#070D1B]/80 border border-white/10 flex items-center justify-between text-xs font-mono text-[#E8EDF7]">
                <div className="flex items-center gap-3">
                  <span className="text-base text-[#F5B942]">📍</span>
                  <div>
                    <p className="font-bold text-sm text-[#E8EDF7]">{placeName}, {country}</p>
                    <p className="text-[11px] text-[#94A3B8] tabular-nums">
                      {latitude.toFixed(4)}° N, {longitude.toFixed(4)}° E • {timezoneStr}
                    </p>
                  </div>
                </div>
                <span className="px-2.5 py-1 rounded-full bg-[#34D399]/10 text-[#34D399] border border-[#34D399]/30 text-[10px] font-bold">
                  CONFIRMED
                </span>
              </div>
            </div>

            {/* Advanced Options Toggle */}
            <div className="pt-2">
              <button
                type="button"
                onClick={() => setShowAdvanced(!showAdvanced)}
                className="text-xs font-mono text-[#F5B942] font-bold hover:underline flex items-center gap-1.5"
              >
                <span>{showAdvanced ? '▲' : '▼'}</span> Advanced coordinates & timezone
              </button>
            </div>

            {showAdvanced && (
              <div className="p-5 bg-[#070D1B] rounded-2xl border border-white/10 space-y-4 font-mono text-xs">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-[#94A3B8] mb-1">Place Name</label>
                    <input type="text" value={placeName} onChange={e => setPlaceName(e.target.value)} className="w-full bg-[#111B30] border border-white/10 rounded-xl p-2.5 text-[#E8EDF7]" />
                  </div>
                  <div>
                    <label className="block text-[#94A3B8] mb-1">Country</label>
                    <input type="text" value={country} onChange={e => setCountry(e.target.value)} className="w-full bg-[#111B30] border border-white/10 rounded-xl p-2.5 text-[#E8EDF7]" />
                  </div>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-[#94A3B8] mb-1">Latitude (°N)</label>
                    <input type="number" step="any" value={latitude} onChange={e => setLatitude(Number(e.target.value))} className="w-full bg-[#111B30] border border-white/10 rounded-xl p-2.5 text-[#E8EDF7] tabular-nums" />
                  </div>
                  <div>
                    <label className="block text-[#94A3B8] mb-1">Longitude (°E)</label>
                    <input type="number" step="any" value={longitude} onChange={e => setLongitude(Number(e.target.value))} className="w-full bg-[#111B30] border border-white/10 rounded-xl p-2.5 text-[#E8EDF7] tabular-nums" />
                  </div>
                  <div>
                    <label className="block text-[#94A3B8] mb-1">IANA Timezone</label>
                    <input type="text" value={timezoneStr} onChange={e => setTimezoneStr(e.target.value)} className="w-full bg-[#111B30] border border-white/10 rounded-xl p-2.5 text-[#E8EDF7]" />
                  </div>
                </div>
              </div>
            )}

            {/* Save Profile Checkbox */}
            <div className="flex items-center gap-3 pt-2">
              <input
                type="checkbox"
                id="saveProfile"
                checked={saveProfile}
                onChange={e => setSaveProfile(e.target.checked)}
                className="w-4 h-4 rounded border-white/20 text-[#F5B942] focus:ring-[#F5B942]"
              />
              <label htmlFor="saveProfile" className="text-xs font-mono text-[#94A3B8] cursor-pointer select-none">
                Save this profile for later <span className="text-[10px] text-[#94A3B8]/70 block">(Store securely in your account for quick access)</span>
              </label>
            </div>

            {/* Submit & Reset Actions */}
            <div className="pt-4 flex flex-col sm:flex-row items-center gap-4">
              <button
                type="submit"
                className="w-full sm:flex-1 bg-gradient-to-r from-[#F5B942] via-amber-400 to-[#E5A832] hover:from-amber-300 hover:to-[#F5B942] text-[#070D1B] font-black py-4 rounded-2xl shadow-xl shadow-[#F5B942]/20 text-xs font-mono uppercase tracking-wider transition duration-200 flex items-center justify-center gap-2 cursor-pointer"
              >
                <span>✦</span> Calculate Canonical Chart →
              </button>
              <button
                type="button"
                onClick={handleReset}
                className="text-xs font-mono text-[#94A3B8] hover:text-[#E8EDF7] py-2 px-4 underline"
              >
                Clear form
              </button>
            </div>
          </form>
        </div>

        {/* RIGHT COLUMN: Live Chart Preview Card (5 Cols) */}
        <div className="lg:col-span-5 bg-[#111B30]/90 backdrop-blur-2xl p-6 md:p-8 rounded-3xl border border-white/10 shadow-2xl space-y-6 sticky top-24">
          <div className="flex items-center justify-between border-b border-white/10 pb-4">
            <h3 className="text-lg font-extrabold text-[#F5B942] font-serif-heading flex items-center gap-2">
              <span>🌌</span> Chart Preview
            </h3>
            <span className="px-2.5 py-1 rounded-full bg-[#F5B942]/10 border border-[#F5B942]/30 text-[#F5B942] text-[10px] font-mono font-bold">
              ● Ready when details are complete
            </span>
          </div>

          {/* Style Selector */}
          <div className="flex bg-[#070D1B] p-1 rounded-xl border border-white/10 font-mono text-xs">
            <button
              type="button"
              onClick={() => setChartStyle('north')}
              className={`flex-1 py-1.5 rounded-lg font-semibold transition ${
                chartStyle === 'north' ? 'bg-[#F5B942]/20 text-[#F5B942] border border-[#F5B942]/40' : 'text-[#94A3B8] hover:text-white'
              }`}
            >
              North Indian (Rāśi)
            </button>
            <button
              type="button"
              onClick={() => setChartStyle('south')}
              className={`flex-1 py-1.5 rounded-lg font-semibold transition ${
                chartStyle === 'south' ? 'bg-[#F5B942]/20 text-[#F5B942] border border-[#F5B942]/40' : 'text-[#94A3B8] hover:text-white'
              }`}
            >
              South Indian
            </button>
          </div>

          {/* Interactive Astrolabe SVG Diagram */}
          <div className="p-6 rounded-2xl bg-[#070D1B] border border-[#F5B942]/20 flex flex-col items-center justify-center min-h-[300px] relative overflow-hidden shadow-inner">
            <div className="w-full max-w-[280px] aspect-square relative flex items-center justify-center">
              {/* Outer Rashi Diamond Grid */}
              <svg viewBox="0 0 300 300" className="w-full h-full text-[#F5B942]">
                <rect x="10" y="10" width="280" height="280" fill="none" stroke="currentColor" strokeWidth="2" opacity="0.8" />
                <line x1="10" y1="10" x2="290" y2="290" stroke="currentColor" strokeWidth="1.5" opacity="0.6" />
                <line x1="290" y1="10" x2="10" y2="290" stroke="currentColor" strokeWidth="1.5" opacity="0.6" />
                <polygon points="150,10 290,150 150,290 10,150" fill="none" stroke="currentColor" strokeWidth="1.5" opacity="0.8" />

                {/* House Labels */}
                <text x="150" y="70" textAnchor="middle" fill="#E8EDF7" fontSize="12" fontWeight="bold">1</text>
                <text x="80" y="40" textAnchor="middle" fill="#94A3B8" fontSize="10">2</text>
                <text x="40" y="80" textAnchor="middle" fill="#94A3B8" fontSize="10">3</text>
                <text x="70" y="150" textAnchor="middle" fill="#94A3B8" fontSize="10">4</text>
                <text x="40" y="220" textAnchor="middle" fill="#94A3B8" fontSize="10">5</text>
                <text x="80" y="260" textAnchor="middle" fill="#94A3B8" fontSize="10">6</text>
                <text x="150" y="230" textAnchor="middle" fill="#94A3B8" fontSize="10">7</text>
                <text x="220" y="260" textAnchor="middle" fill="#94A3B8" fontSize="10">8</text>
                <text x="260" y="220" textAnchor="middle" fill="#94A3B8" fontSize="10">9</text>
                <text x="230" y="150" textAnchor="middle" fill="#94A3B8" fontSize="10">10</text>
                <text x="260" y="80" textAnchor="middle" fill="#94A3B8" fontSize="10">11</text>
                <text x="220" y="40" textAnchor="middle" fill="#94A3B8" fontSize="10">12</text>

                {/* Center Symbol */}
                <text x="150" y="155" textAnchor="middle" fill="#F5B942" fontSize="22" fontWeight="bold">As</text>
              </svg>
            </div>
            <p className="text-[11px] font-mono text-[#94A3B8] text-center mt-3">
              This is a preview. The actual calculated chart will generate upon submission.
            </p>
          </div>

          {/* Engine Parameters Summary List */}
          <div className="space-y-2.5 font-mono text-xs">
            <div className="p-3 rounded-xl bg-[#070D1B]/80 border border-white/5 flex items-center justify-between text-[#E8EDF7]">
              <span className="text-[#94A3B8]">Timezone</span>
              <span className="font-bold text-[#F5B942]">{timezoneStr}</span>
            </div>
            <div className="p-3 rounded-xl bg-[#070D1B]/80 border border-white/5 flex items-center justify-between text-[#E8EDF7]">
              <span className="text-[#94A3B8]">Coordinates</span>
              <span className="font-bold tabular-nums">{latitude.toFixed(2)}° N, {longitude.toFixed(2)}° E</span>
            </div>
            <div className="p-3 rounded-xl bg-[#070D1B]/80 border border-white/5 flex items-center justify-between text-[#E8EDF7]">
              <span className="text-[#94A3B8]">Calculation Engine</span>
              <span className="font-bold text-[#34D399]">JPL DE440s (High Precision)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
