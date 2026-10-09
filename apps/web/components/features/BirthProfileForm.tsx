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
    <div className="bg-slate-900/90 backdrop-blur-2xl p-8 md:p-12 rounded-3xl border border-slate-800/80 shadow-2xl max-w-4xl mx-auto relative overflow-hidden w-full select-none">
      <div className="flex items-center justify-between border-b border-slate-800/80 pb-6 mb-8">
        <div>
          <span className="px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-mono font-bold uppercase tracking-widest">
            Natal Parameter Input
          </span>
          <h2 className="text-2xl md:text-3xl font-black text-slate-100 tracking-wide mt-2">
            Enter Birth Particulars
          </h2>
        </div>
        <div className="w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-300 text-2xl shrink-0">
          ✦
        </div>
      </div>

      <form onSubmit={onSubmit} className="space-y-6">
        <div>
          <label className="block text-xs font-mono font-semibold uppercase tracking-wider text-slate-400 mb-2">
            Native Full Name
          </label>
          <input
            type="text"
            value={name}
            onChange={e => setName(e.target.value)}
            placeholder="e.g. Subramanian T S"
            className="w-full bg-slate-950/80 border border-slate-700/80 rounded-2xl p-4 text-slate-100 focus:border-amber-400/80 outline-none transition text-base font-sans"
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 font-mono">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Year (YYYY)</label>
            <input
              type="number"
              value={year}
              onChange={e => setYear(Number(e.target.value))}
              className="w-full bg-slate-950/80 border border-slate-700/80 rounded-2xl p-4 text-slate-100 focus:border-amber-400/80 outline-none transition text-base tabular-nums"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Month (1-12)</label>
            <input
              type="number"
              value={month}
              onChange={e => setMonth(Number(e.target.value))}
              className="w-full bg-slate-950/80 border border-slate-700/80 rounded-2xl p-4 text-slate-100 focus:border-amber-400/80 outline-none transition text-base tabular-nums"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Day (1-31)</label>
            <input
              type="number"
              value={day}
              onChange={e => setDay(Number(e.target.value))}
              className="w-full bg-slate-950/80 border border-slate-700/80 rounded-2xl p-4 text-slate-100 focus:border-amber-400/80 outline-none transition text-base tabular-nums"
              required
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 font-mono">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Hour (0-23)</label>
            <input
              type="number"
              value={hour}
              onChange={e => setHour(Number(e.target.value))}
              className="w-full bg-slate-950/80 border border-slate-700/80 rounded-2xl p-4 text-slate-100 focus:border-amber-400/80 outline-none transition text-base tabular-nums"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Minute (0-59)</label>
            <input
              type="number"
              value={minute}
              onChange={e => setMinute(Number(e.target.value))}
              className="w-full bg-slate-950/80 border border-slate-700/80 rounded-2xl p-4 text-slate-100 focus:border-amber-400/80 outline-none transition text-base tabular-nums"
              required
            />
          </div>
        </div>

        {/* Location Search / Preset Selector */}
        <div className="space-y-3 font-mono">
          <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400">
            Birth Location Search
          </label>
          <input
            type="text"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            placeholder="Filter city e.g. New Delhi, Palakkad, London, Tokyo..."
            className="w-full bg-slate-950/80 border border-slate-700/80 rounded-2xl p-3.5 text-slate-100 placeholder-slate-500 focus:border-amber-400/80 outline-none transition text-sm mb-2"
          />

          <select
            value={selectedCity}
            onChange={e => handleCityChange(e.target.value)}
            className="w-full bg-slate-950/80 border border-slate-700/80 rounded-2xl p-4 text-slate-100 focus:border-amber-400/80 outline-none transition text-base cursor-pointer"
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
            className="text-xs font-mono text-amber-300 font-bold hover:underline"
          >
            {showAdvanced ? '▲ Hide Advanced Coordinates & Custom Timezone' : '▼ Advanced: Manual Coordinates & Custom Timezone'}
          </button>
        </div>

        {showAdvanced && (
          <div className="p-6 bg-slate-950/80 rounded-2xl border border-slate-800 space-y-4 font-mono">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Place Name</label>
                <input type="text" value={placeName} onChange={e => setPlaceName(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs text-slate-100" />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Country</label>
                <input type="text" value={country} onChange={e => setCountry(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs text-slate-100" />
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Latitude (°N)</label>
                <input type="number" step="any" value={latitude} onChange={e => setLatitude(Number(e.target.value))} className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs text-slate-100 tabular-nums" />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Longitude (°E)</label>
                <input type="number" step="any" value={longitude} onChange={e => setLongitude(Number(e.target.value))} className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs text-slate-100 tabular-nums" />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">IANA Timezone</label>
                <input type="text" value={timezoneStr} onChange={e => setTimezoneStr(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs text-slate-100" />
              </div>
            </div>
          </div>
        )}

        <div className="pt-4">
          <button
            type="submit"
            className="w-full bg-gradient-to-r from-amber-400 via-amber-500 to-amber-600 hover:from-amber-300 hover:to-amber-500 text-slate-950 font-black py-4 rounded-2xl shadow-xl shadow-amber-500/20 text-base transition duration-200 uppercase tracking-wider flex items-center justify-center gap-2"
          >
            <span>✦</span> Calculate Canonical Astrological Profile
          </button>
        </div>
      </form>
    </div>
  )
}
