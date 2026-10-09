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

  const handleYearInput = (val: string) => {
    if (val === '') { setYear(1995); return }
    const num = parseInt(val, 10)
    if (!isNaN(num)) {
      setYear(Math.min(2150, Math.max(1850, num)))
    }
  }

  const handleMonthInput = (val: string) => {
    if (val === '') { setMonth(1); return }
    const num = parseInt(val, 10)
    if (!isNaN(num)) {
      setMonth(Math.min(12, Math.max(1, num)))
    }
  }

  const handleDayInput = (val: string) => {
    if (val === '') { setDay(1); return }
    const num = parseInt(val, 10)
    if (!isNaN(num)) {
      setDay(Math.min(31, Math.max(1, num)))
    }
  }

  const handleHourInput = (val: string) => {
    if (val === '') { setHour(12); return }
    const num = parseInt(val, 10)
    if (!isNaN(num)) {
      setHour(Math.min(23, Math.max(0, num)))
    }
  }

  const handleMinuteInput = (val: string) => {
    if (val === '') { setMinute(0); return }
    const num = parseInt(val, 10)
    if (!isNaN(num)) {
      setMinute(Math.min(59, Math.max(0, num)))
    }
  }

  return (
    <div className="bg-slate-900/90 backdrop-blur-2xl p-6 md:p-10 rounded-3xl border border-slate-800 shadow-2xl max-w-3xl mx-auto relative overflow-hidden w-full">
      <div className="flex items-center justify-between border-b border-slate-800 pb-5 mb-8">
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
          <label className="block text-xs font-mono font-semibold uppercase tracking-wider text-slate-300 mb-2">
            Native Full Name
          </label>
          <input
            type="text"
            value={name}
            onChange={e => setName(e.target.value)}
            placeholder="e.g. Subramanian T S"
            className="w-full bg-slate-950 border border-slate-700/80 rounded-2xl px-4 py-3.5 text-slate-100 focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 outline-none transition text-base font-sans"
            required
          />
        </div>

        {/* Date Inputs */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-5 font-mono">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">Year (1850 - 2150)</label>
            <input
              type="number"
              min={1850}
              max={2150}
              value={year}
              onChange={e => handleYearInput(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700/80 rounded-2xl px-4 py-3.5 text-slate-100 focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 outline-none transition text-base tabular-nums font-bold"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">Month (1 - 12)</label>
            <input
              type="number"
              min={1}
              max={12}
              value={month}
              onChange={e => handleMonthInput(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700/80 rounded-2xl px-4 py-3.5 text-slate-100 focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 outline-none transition text-base tabular-nums font-bold"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">Day (1 - 31)</label>
            <input
              type="number"
              min={1}
              max={31}
              value={day}
              onChange={e => handleDayInput(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700/80 rounded-2xl px-4 py-3.5 text-slate-100 focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 outline-none transition text-base tabular-nums font-bold"
              required
            />
          </div>
        </div>

        {/* Time Inputs */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 font-mono">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">Hour (0 - 23 24h format)</label>
            <input
              type="number"
              min={0}
              max={23}
              value={hour}
              onChange={e => handleHourInput(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700/80 rounded-2xl px-4 py-3.5 text-slate-100 focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 outline-none transition text-base tabular-nums font-bold"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">Minute (0 - 59)</label>
            <input
              type="number"
              min={0}
              max={59}
              value={minute}
              onChange={e => handleMinuteInput(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700/80 rounded-2xl px-4 py-3.5 text-slate-100 focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 outline-none transition text-base tabular-nums font-bold"
              required
            />
          </div>
        </div>

        {/* Location Search / Preset Selector */}
        <div className="space-y-3 font-mono">
          <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300">
            Select Birth Location
          </label>
          <input
            type="text"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            placeholder="Filter city list e.g. New Delhi, Mumbai, London, Tokyo..."
            className="w-full bg-slate-950 border border-slate-700/80 rounded-2xl px-4 py-3 text-slate-100 placeholder-slate-500 focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 outline-none transition text-sm mb-2"
          />

          <select
            value={selectedCity}
            onChange={e => handleCityChange(e.target.value)}
            className="w-full bg-slate-950 border border-slate-700/80 rounded-2xl px-4 py-3.5 text-slate-100 focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 outline-none transition text-sm font-semibold cursor-pointer"
          >
            {filteredCities.map(c => (
              <option key={c.name} value={c.name} className="bg-slate-900 text-slate-100">
                {c.name}, {c.country} ({c.tz})
              </option>
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
          <div className="p-6 bg-slate-950 rounded-2xl border border-slate-800 space-y-4 font-mono">
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
            className="w-full bg-gradient-to-r from-amber-400 via-amber-500 to-amber-600 hover:from-amber-300 hover:to-amber-500 text-slate-950 font-black py-4 rounded-2xl shadow-xl shadow-amber-500/20 text-base transition duration-200 uppercase tracking-wider flex items-center justify-center gap-2 cursor-pointer"
          >
            <span>✦</span> Calculate Canonical Astrological Profile
          </button>
        </div>
      </form>
    </div>
  )
}
