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

  const filteredCities = PRESET_CITIES.filter(c =>
    c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    c.country.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="bg-[#17163A]/90 p-8 md:p-12 rounded-3xl border border-[#F3E5AB]/40 shadow-2xl max-w-4xl mx-auto backdrop-blur-2xl relative overflow-hidden w-full">
      <div className="absolute top-0 right-0 w-80 h-80 bg-purple-900/30 rounded-full blur-3xl pointer-events-none"></div>
      <h2 className="text-2xl md:text-3xl font-extrabold mb-3 text-[#F3E5AB]">Enter Birth Details</h2>
      <p className="text-xs md:text-sm text-[#A0A5C0] mb-8">Enter your birth particulars to generate your personalized NASA JPL DE440s natal chart and astrological portrait.</p>

      <form onSubmit={onSubmit} className="space-y-6">
        <div>
          <label className="block text-xs font-semibold uppercase tracking-widest text-[#A0A5C0] mb-2">Full Name</label>
          <input
            type="text"
            value={name}
            onChange={e => setName(e.target.value)}
            placeholder="e.g. Jane Doe"
            className="w-full bg-[#050816] border border-[#F3E5AB]/40 rounded-2xl p-4 text-[#FFFFF0] focus:border-[#F3E5AB] outline-none transition text-base"
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-widest text-[#A0A5C0] mb-2">Year</label>
            <input
              type="number"
              value={year}
              onChange={e => setYear(Number(e.target.value))}
              className="w-full bg-[#050816] border border-[#F3E5AB]/40 rounded-2xl p-4 text-[#FFFFF0] focus:border-[#F3E5AB] outline-none transition text-base"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-widest text-[#A0A5C0] mb-2">Month (1-12)</label>
            <input
              type="number"
              value={month}
              onChange={e => setMonth(Number(e.target.value))}
              className="w-full bg-[#050816] border border-[#F3E5AB]/40 rounded-2xl p-4 text-[#FFFFF0] focus:border-[#F3E5AB] outline-none transition text-base"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-widest text-[#A0A5C0] mb-2">Day (1-31)</label>
            <input
              type="number"
              value={day}
              onChange={e => setDay(Number(e.target.value))}
              className="w-full bg-[#050816] border border-[#F3E5AB]/40 rounded-2xl p-4 text-[#FFFFF0] focus:border-[#F3E5AB] outline-none transition text-base"
              required
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-widest text-[#A0A5C0] mb-2">Hour (0-23)</label>
            <input
              type="number"
              value={hour}
              onChange={e => setHour(Number(e.target.value))}
              className="w-full bg-[#050816] border border-[#F3E5AB]/40 rounded-2xl p-4 text-[#FFFFF0] focus:border-[#F3E5AB] outline-none transition text-base"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-widest text-[#A0A5C0] mb-2">Minute (0-59)</label>
            <input
              type="number"
              value={minute}
              onChange={e => setMinute(Number(e.target.value))}
              className="w-full bg-[#050816] border border-[#F3E5AB]/40 rounded-2xl p-4 text-[#FFFFF0] focus:border-[#F3E5AB] outline-none transition text-base"
              required
            />
          </div>
        </div>

        {/* Location Search / Preset Selector */}
        <div className="space-y-3">
          <label className="block text-xs font-semibold uppercase tracking-widest text-[#A0A5C0]">Birth Location Search</label>
          <input
            type="text"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            placeholder="Search city e.g. New Delhi, Palakkad, London, Tokyo..."
            className="w-full bg-[#050816] border border-[#F3E5AB]/40 rounded-2xl p-4 text-[#FFFFF0] focus:border-[#F3E5AB] outline-none transition text-sm mb-2"
          />

          <select
            value={selectedCity}
            onChange={e => handleCityChange(e.target.value)}
            className="w-full bg-[#050816] border border-[#F3E5AB]/40 rounded-2xl p-4 text-[#FFFFF0] focus:border-[#F3E5AB] outline-none transition text-base"
          >
            {filteredCities.map(c => (
              <option key={c.name} value={c.name}>{c.name}, {c.country} ({c.tz})</option>
            ))}
          </select>
        </div>

        {/* Advanced Options Toggle */}
        <div className="pt-2">
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="text-xs text-[#F3E5AB] font-bold hover:underline"
          >
            {showAdvanced ? '▲ Hide Advanced Coordinates & Timezone' : '▼ Advanced: Manual Coordinates & Custom Timezone'}
          </button>
        </div>

        {showAdvanced && (
          <div className="p-6 bg-[#050816] rounded-2xl border border-[#F3E5AB]/30 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-[#A0A5C0] mb-1">Place Name</label>
                <input type="text" value={placeName} onChange={e => setPlaceName(e.target.value)} className="w-full bg-[#17163A] border border-[#F3E5AB]/30 rounded-xl p-3 text-xs text-[#FFFFF0]" />
              </div>
              <div>
                <label className="block text-xs font-semibold text-[#A0A5C0] mb-1">Country</label>
                <input type="text" value={country} onChange={e => setCountry(e.target.value)} className="w-full bg-[#17163A] border border-[#F3E5AB]/30 rounded-xl p-3 text-xs text-[#FFFFF0]" />
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-semibold text-[#A0A5C0] mb-1">Latitude (°N)</label>
                <input type="number" step="any" value={latitude} onChange={e => setLatitude(Number(e.target.value))} className="w-full bg-[#17163A] border border-[#F3E5AB]/30 rounded-xl p-3 text-xs text-[#FFFFF0]" />
              </div>
              <div>
                <label className="block text-xs font-semibold text-[#A0A5C0] mb-1">Longitude (°E)</label>
                <input type="number" step="any" value={longitude} onChange={e => setLongitude(Number(e.target.value))} className="w-full bg-[#17163A] border border-[#F3E5AB]/30 rounded-xl p-3 text-xs text-[#FFFFF0]" />
              </div>
              <div>
                <label className="block text-xs font-semibold text-[#A0A5C0] mb-1">IANA Timezone</label>
                <input type="text" value={timezoneStr} onChange={e => setTimezoneStr(e.target.value)} className="w-full bg-[#17163A] border border-[#F3E5AB]/30 rounded-xl p-3 text-xs text-[#FFFFF0]" />
              </div>
            </div>
          </div>
        )}

        <div>
          <label className="block text-xs font-semibold uppercase tracking-widest text-[#A0A5C0] mb-2">Astrology System</label>
          <select
            value={zodiacSystem}
            onChange={e => setZodiacSystem(e.target.value)}
            className="w-full bg-[#050816] border border-[#F3E5AB]/40 rounded-2xl p-4 text-[#FFFFF0] focus:border-[#F3E5AB] outline-none transition text-base"
          >
            <option value="sidereal">Vedic / Sidereal (Lahiri Ayanamsha)</option>
            <option value="tropical">Western / Tropical</option>
          </select>
        </div>

        <button
          type="submit"
          className="w-full bg-gradient-to-r from-[#F3E5AB] to-[#F7E792] text-[#050816] font-extrabold py-5 rounded-2xl shadow-2xl hover:opacity-95 transition transform active:scale-[0.99] mt-8 tracking-wide text-lg"
        >
          Calculate Personal Birth Chart
        </button>
      </form>
    </div>
  )
}
