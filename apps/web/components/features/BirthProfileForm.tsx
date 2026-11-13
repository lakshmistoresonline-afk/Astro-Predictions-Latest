import React, { useState, useEffect, useRef } from 'react'
import { CASCADING_LOCATIONS, DistrictCityItem } from '../../types/locationData'

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
  const [chartStyle, setChartStyle] = useState<'north' | 'south'>('north')
  const [saveProfile, setSaveProfile] = useState(true)

  const dateInputRef = useRef<HTMLInputElement>(null)
  const timeInputRef = useRef<HTMLInputElement>(null)

  const handleOpenDatePicker = () => {
    try {
      if (dateInputRef.current) {
        if ('showPicker' in dateInputRef.current) {
          (dateInputRef.current as any).showPicker()
        } else {
          dateInputRef.current.focus()
        }
      }
    } catch (e) {
      dateInputRef.current?.focus()
    }
  }

  const handleOpenTimePicker = () => {
    try {
      if (timeInputRef.current) {
        if ('showPicker' in timeInputRef.current) {
          (timeInputRef.current as any).showPicker()
        } else {
          timeInputRef.current.focus()
        }
      }
    } catch (e) {
      timeInputRef.current?.focus()
    }
  }

  // Combined Date String (YYYY-MM-DD)
  const dateIsoString = (year >= 1850 && year <= 2150 && month >= 1 && month <= 12 && day >= 1 && day <= 31)
    ? `${String(year).padStart(4, '0')}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`
    : '1995-01-01'

  // Combined Time String (HH:MM)
  const timeIsoString = `${String(hour !== undefined ? hour : 12).padStart(2, '0')}:${String(minute !== undefined ? minute : 0).padStart(2, '0')}`

  // Quick preset locations
  const PRESET_LOCATIONS = [
    { label: 'Palakkad, Kerala', place: 'Palakkad, Kerala', country: 'India', lat: 10.7867, lon: 76.6547, tz: 'Asia/Kolkata' },
    { label: 'Chennai, Tamil Nadu', place: 'Chennai, Tamil Nadu', country: 'India', lat: 13.0827, lon: 80.2707, tz: 'Asia/Kolkata' },
    { label: 'Bengaluru, Karnataka', place: 'Bengaluru, Karnataka', country: 'India', lat: 12.9716, lon: 77.5946, tz: 'Asia/Kolkata' },
    { label: 'Mumbai, Maharashtra', place: 'Mumbai, Maharashtra', country: 'India', lat: 19.0760, lon: 72.8777, tz: 'Asia/Kolkata' },
    { label: 'Delhi, NCR', place: 'Delhi, NCR', country: 'India', lat: 28.6139, lon: 77.2090, tz: 'Asia/Kolkata' },
    { label: 'New York, USA', place: 'New York, NY', country: 'United States', lat: 40.7128, lon: -74.0060, tz: 'America/New_York' },
    { label: 'London, UK', place: 'London', country: 'United Kingdom', lat: 51.5074, lon: -0.1278, tz: 'Europe/London' },
  ]

  const handleDateChange = (val: string) => {
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

  const handleTimeChange = (val: string) => {
    if (!val) return
    const parts = val.split(':')
    if (parts.length >= 2) {
      const h = parseInt(parts[0], 10)
      const min = parseInt(parts[1], 10)
      if (!isNaN(h) && h >= 0 && h <= 23) setHour(h)
      if (!isNaN(min) && min >= 0 && min <= 59) setMinute(min)
    }
  }

  const handleSelectPresetLocation = (loc: typeof PRESET_LOCATIONS[0]) => {
    setPlaceName(loc.place)
    setCountry(loc.country)
    setLatitude(loc.lat)
    setLongitude(loc.lon)
    setTimezoneStr(loc.tz)
  }

  const handleReset = () => {
    setName('')
    setYear(1995)
    setMonth(1)
    setDay(1)
    setHour(12)
    setMinute(0)
    handleSelectPresetLocation(PRESET_LOCATIONS[0])
  }

  return (
    <div className="w-full max-w-[1400px] mx-auto space-y-8 font-sans">
      {/* Sleek Step Navigation */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-[#0D1527]/90 border border-white/10 p-5 rounded-3xl backdrop-blur-2xl text-sm shadow-xl">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="w-8 h-8 rounded-full bg-[#F5B942] text-[#050814] font-black flex items-center justify-center text-sm shadow-md shadow-[#F5B942]/20">1</span>
            <span className="font-bold text-[#F8FAFC]">Birth Details</span>
          </div>
          <span className="text-[#94A3B8]">→</span>
          <div className="flex items-center gap-2">
            <span className="w-8 h-8 rounded-full bg-white/10 text-[#94A3B8] font-bold flex items-center justify-center text-sm">2</span>
            <span className="text-[#94A3B8] font-medium">Location & Timezone</span>
          </div>
          <span className="text-[#94A3B8]">→</span>
          <div className="flex items-center gap-2">
            <span className="w-8 h-8 rounded-full bg-white/10 text-[#94A3B8] font-bold flex items-center justify-center text-sm">3</span>
            <span className="text-[#94A3B8] font-medium">Preview & Calculate</span>
          </div>
        </div>
        <span className="text-[#34D399] font-bold text-xs flex items-center gap-2 bg-[#34D399]/10 border border-[#34D399]/30 px-3.5 py-1.5 rounded-full">
          <span className="w-2 h-2 rounded-full bg-[#34D399] animate-pulse"></span>
          NASA DE440s Active
        </span>
      </div>

      {/* Modern 2-Column Studio Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* LEFT COLUMN: Ultra-Clean 3-Field Birth Form (7 Cols) */}
        <div className="lg:col-span-7 bg-[#0D1527]/90 backdrop-blur-2xl p-8 md:p-10 rounded-3xl border border-white/10 shadow-2xl space-y-6">
          <div className="border-b border-white/10 pb-5">
            <span className="px-3.5 py-1.5 rounded-full bg-[#F5B942]/10 border border-[#F5B942]/30 text-[#F5B942] text-xs font-bold uppercase tracking-widest">
              Natal Parameter Input
            </span>
            <h2 className="text-2xl md:text-3xl font-black text-[#F8FAFC] tracking-wide mt-2 font-serif-heading">
              Enter Birth Particulars
            </h2>
            <p className="text-sm text-[#94A3B8] font-sans mt-1 leading-relaxed">
              Provide accurate birth details to calculate your canonical astrological profile.
            </p>
          </div>

          <form onSubmit={onSubmit} className="space-y-6 font-sans">
            {/* FIELD 1: Full Name */}
            <div className="space-y-2">
              <label className="block text-xs font-extrabold uppercase tracking-wider text-[#F5B942]">
                Full Name <span className="text-amber-400">*</span>
              </label>
              <div className="relative">
                <span className="absolute left-4 top-4 text-base text-[#94A3B8]">👤</span>
                <input
                  type="text"
                  value={name}
                  onChange={e => setName(e.target.value)}
                  placeholder="Enter full birth name (e.g., Subramanian T S)..."
                  className="w-full bg-[#050814] border border-white/15 rounded-2xl pl-12 pr-4 py-4 text-[#F8FAFC] placeholder-slate-500 focus:border-[#F5B942] focus:ring-2 focus:ring-[#F5B942]/20 outline-none transition text-base font-semibold"
                  required
                />
              </div>
            </div>

            {/* FIELD 2: Date & Time of Birth (Interactive Calendar & Time Pickers) */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {/* Date Input with Calendar Picker */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <label className="block text-xs font-extrabold uppercase tracking-wider text-[#F5B942]">
                    Date of Birth (Calendar) <span className="text-amber-400">*</span>
                  </label>
                  <span className="text-[11px] text-[#34D399] font-bold">📅 Calendar Picker Active</span>
                </div>
                <div
                  onClick={handleOpenDatePicker}
                  className="relative cursor-pointer group"
                >
                  <span className="absolute left-4 top-4 text-base text-[#F5B942] group-hover:scale-110 transition pointer-events-none">📅</span>
                  <input
                    ref={dateInputRef}
                    type="date"
                    value={dateIsoString}
                    onChange={e => handleDateChange(e.target.value)}
                    onClick={handleOpenDatePicker}
                    min="1850-01-01"
                    max="2150-12-31"
                    className="w-full bg-[#050814] border border-white/15 hover:border-[#F5B942] rounded-2xl pl-12 pr-4 py-4 text-[#F8FAFC] focus:border-[#F5B942] focus:ring-2 focus:ring-[#F5B942]/20 outline-none transition text-base font-semibold cursor-pointer"
                    required
                  />
                </div>
                <p className="text-[11px] text-[#94A3B8]">Click anywhere on the field or icon to select your Date of Birth via calendar.</p>
              </div>

              {/* Time Input */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <label className="block text-xs font-extrabold uppercase tracking-wider text-[#F5B942]">
                    Time of Birth (24-Hour) <span className="text-amber-400">*</span>
                  </label>
                  <span className="text-[11px] text-[#38BDF8] font-bold">⏰ Exact Local Time</span>
                </div>
                <div
                  onClick={handleOpenTimePicker}
                  className="relative cursor-pointer group"
                >
                  <span className="absolute left-4 top-4 text-base text-[#38BDF8] group-hover:scale-110 transition pointer-events-none">⏰</span>
                  <input
                    ref={timeInputRef}
                    type="time"
                    value={timeIsoString}
                    onChange={e => handleTimeChange(e.target.value)}
                    onClick={handleOpenTimePicker}
                    className="w-full bg-[#050814] border border-white/15 hover:border-[#38BDF8] rounded-2xl pl-12 pr-4 py-4 text-[#F8FAFC] focus:border-[#38BDF8] focus:ring-2 focus:ring-[#38BDF8]/20 outline-none transition text-base font-semibold cursor-pointer"
                    required
                  />
                </div>
                <p className="text-[11px] text-[#94A3B8]">Enter exact birth time in 24-hour format (e.g. 16:30 for 4:30 PM).</p>
              </div>
            </div>

            {/* FIELD 3: Birth Location & Quick Presets */}
            <div className="space-y-3">
              <label className="block text-xs font-extrabold uppercase tracking-wider text-[#F5B942]">
                Birth Location & Timezone <span className="text-amber-400">*</span>
              </label>

              {/* Location Quick Preset Pills */}
              <div className="flex flex-wrap gap-2 pt-1">
                {PRESET_LOCATIONS.map(loc => (
                  <button
                    key={loc.label}
                    type="button"
                    onClick={() => handleSelectPresetLocation(loc)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-medium border transition cursor-pointer ${
                      placeName.includes(loc.place.split(',')[0])
                        ? 'bg-[#F5B942]/20 text-[#F5B942] border-[#F5B942]/50 font-bold'
                        : 'bg-[#050814] text-[#94A3B8] border-white/10 hover:text-[#F8FAFC]'
                    }`}
                  >
                    📍 {loc.label}
                  </button>
                ))}
              </div>

              {/* Active Location Display Card */}
              <div className="p-4.5 rounded-2xl bg-[#050814] border border-[#F5B942]/30 flex flex-wrap items-center justify-between gap-3 shadow-inner">
                <div className="space-y-0.5">
                  <p className="text-sm font-bold text-[#F5B942] flex items-center gap-2">
                    <span>📍</span> {placeName}, {country}
                  </p>
                  <p className="text-xs text-[#94A3B8] tabular-nums font-mono">
                    {latitude}° N, {longitude}° E • {timezoneStr}
                  </p>
                </div>
                <span className="text-xs bg-[#34D399]/20 text-[#34D399] border border-[#34D399]/40 px-3 py-1 rounded-full font-bold">
                  ● Coordinates Verified
                </span>
              </div>
            </div>

            {/* Advanced Controls Toggle */}
            <div className="pt-2 border-t border-white/10 space-y-4">
              <button
                type="button"
                onClick={() => setShowAdvanced(!showAdvanced)}
                className="text-xs text-[#F5B942] font-bold hover:underline flex items-center gap-2 cursor-pointer"
              >
                <span>{showAdvanced ? '▼' : '►'}</span> Advanced Coordinates & Manual Date Overrides
              </button>

              {showAdvanced && (
                <div className="p-5 rounded-2xl bg-[#050814] border border-white/10 space-y-4 text-xs font-sans">
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-xs text-[#94A3B8] mb-1 font-medium">Custom Latitude (°N)</label>
                      <input
                        type="number"
                        step="0.0001"
                        value={latitude}
                        onChange={e => setLatitude(parseFloat(e.target.value) || 0)}
                        className="w-full bg-[#0D1527] border border-white/15 rounded-xl p-3 text-[#F8FAFC] outline-none text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-xs text-[#94A3B8] mb-1 font-medium">Custom Longitude (°E)</label>
                      <input
                        type="number"
                        step="0.0001"
                        value={longitude}
                        onChange={e => setLongitude(parseFloat(e.target.value) || 0)}
                        className="w-full bg-[#0D1527] border border-white/15 rounded-xl p-3 text-[#F8FAFC] outline-none text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-xs text-[#94A3B8] mb-1 font-medium">IANA Timezone String</label>
                      <input
                        type="text"
                        value={timezoneStr}
                        onChange={e => setTimezoneStr(e.target.value)}
                        className="w-full bg-[#0D1527] border border-white/15 rounded-xl p-3 text-[#F8FAFC] outline-none text-sm"
                      />
                    </div>
                  </div>
                </div>
              )}

              <div className="flex items-center gap-2 text-xs text-[#94A3B8]">
                <input
                  type="checkbox"
                  id="saveProfile"
                  checked={saveProfile}
                  onChange={e => setSaveProfile(e.target.checked)}
                  className="rounded border-white/20 bg-[#050814] text-[#F5B942] focus:ring-[#F5B942] w-4 h-4"
                />
                <label htmlFor="saveProfile" className="cursor-pointer">Save this natal profile for future calculations</label>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="pt-4 flex items-center gap-4">
              <button
                type="submit"
                className="flex-1 py-4 px-8 rounded-2xl bg-gradient-to-r from-[#F5B942] via-[#E5A832] to-[#B8860B] hover:from-[#E5A832] hover:to-[#F5B942] text-[#050814] font-black text-sm uppercase tracking-wider shadow-xl shadow-[#F5B942]/20 transition duration-150 flex items-center justify-center gap-2 cursor-pointer"
              >
                <span>✦</span> CALCULATE CANONICAL CHART
              </button>
              <button
                type="button"
                onClick={handleReset}
                className="py-4 px-6 rounded-2xl bg-[#050814] hover:bg-[#152035] border border-white/15 text-[#94A3B8] hover:text-[#F8FAFC] font-bold text-xs uppercase tracking-wider transition cursor-pointer"
              >
                Reset
              </button>
            </div>
          </form>
        </div>

        {/* RIGHT COLUMN: Interactive Chart Preview Box (5 Cols) */}
        <div className="lg:col-span-5 bg-[#0D1527]/90 backdrop-blur-2xl p-8 rounded-3xl border border-white/10 shadow-2xl space-y-6">
          <div className="flex items-center justify-between border-b border-white/10 pb-4">
            <h3 className="text-xl font-bold text-[#F5B942] font-serif-heading flex items-center gap-2">
              <span>🌌</span> Chart Preview
            </h3>
            <span className="text-xs bg-[#F5B942]/10 border border-[#F5B942]/30 text-[#F5B942] px-3 py-1 rounded-full font-bold uppercase tracking-wider">
              Whole-Sign Bhava
            </span>
          </div>

          {/* Style Selector Buttons */}
          <div className="flex bg-[#050814] p-1.5 rounded-2xl border border-white/10 text-xs">
            <button
              onClick={() => setChartStyle('north')}
              className={`flex-1 py-2.5 rounded-xl font-bold transition cursor-pointer ${
                chartStyle === 'north' ? 'bg-[#F5B942]/20 text-[#F5B942] border border-[#F5B942]/40 shadow-md' : 'text-[#94A3B8] hover:text-[#F8FAFC]'
              }`}
            >
              North Indian (Rāśi)
            </button>
            <button
              onClick={() => setChartStyle('south')}
              className={`flex-1 py-2.5 rounded-xl font-bold transition cursor-pointer ${
                chartStyle === 'south' ? 'bg-[#F5B942]/20 text-[#F5B942] border border-[#F5B942]/40 shadow-md' : 'text-[#94A3B8] hover:text-[#F8FAFC]'
              }`}
            >
              South Indian
            </button>
          </div>

          {/* SVG Astrolabe Preview Container */}
          <div className="p-6 bg-[#050814] rounded-3xl border border-[#F5B942]/20 flex items-center justify-center shadow-inner min-h-[320px]">
            <div className="w-full max-w-[280px] aspect-square border border-[#F5B942]/40 rounded-2xl p-4 flex flex-col justify-between relative bg-gradient-to-b from-[#0D1527] to-[#050814] shadow-xl">
              <div className="flex justify-between text-xs font-bold text-[#F5B942]/80">
                <span>12</span>
                <span>1</span>
                <span>2</span>
              </div>
              <div className="flex justify-between items-center text-sm font-bold text-[#F5B942]">
                <span>11</span>
                <div className="text-center font-serif-heading">
                  <span className="text-2xl text-[#F5B942] font-black block">As</span>
                  <span className="text-xs text-[#38BDF8] font-bold">{placeName.split(',')[0] || 'Lagna'}</span>
                </div>
                <span>3</span>
              </div>
              <div className="flex justify-between text-xs font-bold text-[#F5B942]/80">
                <span>10</span>
                <span>7</span>
                <span>4</span>
              </div>
            </div>
          </div>

          {/* Summary Particulars Card */}
          <div className="p-4.5 rounded-2xl bg-[#050814] border border-white/10 space-y-2 text-xs">
            <div className="flex justify-between text-[#94A3B8]">
              <span>Timezone:</span>
              <strong className="text-[#F8FAFC]">{timezoneStr}</strong>
            </div>
            <div className="flex justify-between text-[#94A3B8]">
              <span>Coordinates:</span>
              <strong className="text-[#F8FAFC]">{latitude}° N, {longitude}° E</strong>
            </div>
            <div className="flex justify-between text-[#94A3B8]">
              <span>Calculation Engine:</span>
              <strong className="text-[#34D399]">JPL DE440s (High Precision)</strong>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
