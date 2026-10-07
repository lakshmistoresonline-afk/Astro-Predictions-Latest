import React from 'react'
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
  onSubmit
}) => {
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

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-widest text-[#A0A5C0] mb-2">Birth City / Location</label>
            <select
              value={selectedCity}
              onChange={e => handleCityChange(e.target.value)}
              className="w-full bg-[#050816] border border-[#F3E5AB]/40 rounded-2xl p-4 text-[#FFFFF0] focus:border-[#F3E5AB] outline-none transition text-base"
            >
              {PRESET_CITIES.map(c => (
                <option key={c.name} value={c.name}>{c.name}, {c.country}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-widest text-[#A0A5C0] mb-2">IANA Timezone Key</label>
            <input
              type="text"
              value={timezoneStr}
              onChange={e => setTimezoneStr(e.target.value)}
              placeholder="e.g. Asia/Kolkata"
              className="w-full bg-[#050816] border border-[#F3E5AB]/40 rounded-2xl p-4 text-[#FFFFF0] focus:border-[#F3E5AB] outline-none transition text-base"
              required
            />
          </div>
        </div>

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
