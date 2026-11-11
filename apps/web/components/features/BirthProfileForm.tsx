import React, { useState, useEffect } from 'react'
import { CASCADING_LOCATIONS, CountryItem, StateItem, DistrictCityItem } from '../../types/locationData'

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

  // Local string state to allow full backspace & custom typing
  const [yearStr, setYearStr] = useState<string>(year ? String(year) : '1995')
  const [monthStr, setMonthStr] = useState<string>(month ? String(month) : '1')
  const [dayStr, setDayStr] = useState<string>(day ? String(day) : '1')
  const [hourStr, setHourStr] = useState<string>(hour !== undefined ? String(hour) : '12')
  const [minuteStr, setMinuteStr] = useState<string>(minute !== undefined ? String(minute) : '0')

  // 3-Tier Cascading Location State
  const [selectedCountryName, setSelectedCountryName] = useState('India')
  const [selectedStateName, setSelectedStateName] = useState('Kerala')
  const [selectedDistrictName, setSelectedDistrictName] = useState('Palakkad')

  // Initialize and synchronize location state on component mount
  useEffect(() => {
    const foundC = CASCADING_LOCATIONS.find(c => c.country_name === selectedCountryName) || CASCADING_LOCATIONS[0]
    const foundS = foundC.states.find(s => s.state_name === selectedStateName) || foundC.states[0]
    const foundD = foundS.districts.find(d => d.district === selectedDistrictName) || foundS.districts[0]

    if (foundD) {
      setPlaceName(`${foundD.district}, ${foundS.state_name}`)
      setCountry(foundC.country_name)
      setLatitude(foundD.latitude)
      setLongitude(foundD.longitude)
      setTimezoneStr(foundD.timezone_str)
    }
  }, [])

  // Derive active Country object
  const activeCountry = CASCADING_LOCATIONS.find(c => c.country_name === selectedCountryName) || CASCADING_LOCATIONS[0]
  // Derive active State object
  const activeState = activeCountry.states.find(s => s.state_name === selectedStateName) || activeCountry.states[0]
  // Active Districts list
  const activeDistricts = activeState ? activeState.districts : []

  // Sync cascading selections to parent form state
  const handleCountrySelect = (cName: string) => {
    setSelectedCountryName(cName)
    const foundC = CASCADING_LOCATIONS.find(c => c.country_name === cName) || CASCADING_LOCATIONS[0]
    const firstState = foundC.states[0]
    if (firstState) {
      setSelectedStateName(firstState.state_name)
      const firstDistrict = firstState.districts[0]
      if (firstDistrict) {
        setSelectedDistrictName(firstDistrict.district)
        setPlaceName(`${firstDistrict.district}, ${firstState.state_name}`)
        setCountry(foundC.country_name)
        setLatitude(firstDistrict.latitude)
        setLongitude(firstDistrict.longitude)
        setTimezoneStr(firstDistrict.timezone_str)
      }
    }
  }

  const handleStateSelect = (sName: string) => {
    setSelectedStateName(sName)
    const foundS = activeCountry.states.find(s => s.state_name === sName)
    if (foundS && foundS.districts.length > 0) {
      const firstDistrict = foundS.districts[0]
      setSelectedDistrictName(firstDistrict.district)
      setPlaceName(`${firstDistrict.district}, ${foundS.state_name}`)
      setCountry(activeCountry.country_name)
      setLatitude(firstDistrict.latitude)
      setLongitude(firstDistrict.longitude)
      setTimezoneStr(firstDistrict.timezone_str)
    }
  }

  const handleDistrictSelect = (dName: string) => {
    setSelectedDistrictName(dName)
    const foundD = activeDistricts.find(d => d.district === dName)
    if (foundD) {
      setPlaceName(`${foundD.district}, ${activeState.state_name}`)
      setCountry(activeCountry.country_name)
      setLatitude(foundD.latitude)
      setLongitude(foundD.longitude)
      setTimezoneStr(foundD.timezone_str)
    }
  }

  // Real Calendar Days in Month Helper (handles leap years)
  const getMaxDaysInMonth = (y: number, m: number): number => {
    if (!m || m < 1 || m > 12) return 31
    return new Date(y || 2026, m, 0).getDate()
  }

  // Strict Calendar Date Validation
  const validateCurrentDate = (): string | null => {
    const y = parseInt(yearStr, 10)
    const m = parseInt(monthStr, 10)
    const d = parseInt(dayStr, 10)

    if (isNaN(y) || isNaN(m) || isNaN(d)) return null

    if (y < 1850 || y > 2150) return `Birth year (${y}) is outside supported ephemeris horizon [1850, 2150].`
    if (m < 1 || m > 12) return `Birth month (${m}) is outside valid range [1, 12].`

    const maxDays = getMaxDaysInMonth(y, m)
    if (d < 1 || d > maxDays) {
      return `Invalid birth date: day ${d} does not exist in month ${m} for year ${y} (max days in month: ${maxDays}).`
    }
    return null
  }

  const dateError = validateCurrentDate()

  // Smooth Date Input Handlers
  const handleYearInput = (val: string) => {
    setYearStr(val)
    if (val === '') return
    const num = parseInt(val, 10)
    if (!isNaN(num)) setYear(num)
  }

  const handleYearBlur = () => {
    if (yearStr === '') return
    const num = parseInt(yearStr, 10)
    if (!isNaN(num)) {
      const clamped = Math.min(2150, Math.max(1850, num))
      setYear(clamped)
      setYearStr(String(clamped))
    }
  }

  const handleMonthInput = (val: string) => {
    setMonthStr(val)
    if (val === '') return
    const num = parseInt(val, 10)
    if (!isNaN(num)) setMonth(num)
  }

  const handleMonthBlur = () => {
    if (monthStr === '') return
    const num = parseInt(monthStr, 10)
    if (!isNaN(num)) {
      const clamped = Math.min(12, Math.max(1, num))
      setMonth(clamped)
      setMonthStr(String(clamped))
    }
  }

  const handleDayInput = (val: string) => {
    setDayStr(val)
    if (val === '') return
    const num = parseInt(val, 10)
    if (!isNaN(num)) setDay(num)
  }

  const handleDayBlur = () => {
    if (dayStr === '') return
    const num = parseInt(dayStr, 10)
    if (!isNaN(num)) {
      const clamped = Math.min(31, Math.max(1, num))
      setDay(clamped)
      setDayStr(String(clamped))
    }
  }

  // Smooth Time Input Handlers
  const handleHourInput = (val: string) => {
    setHourStr(val)
    if (val === '') return
    const num = parseInt(val, 10)
    if (!isNaN(num)) setHour(num)
  }

  const handleHourBlur = () => {
    if (hourStr === '') return
    const num = parseInt(hourStr, 10)
    if (!isNaN(num)) {
      const clamped = Math.min(23, Math.max(0, num))
      setHour(clamped)
      setHourStr(String(clamped))
    }
  }

  const handleMinuteInput = (val: string) => {
    setMinuteStr(val)
    if (val === '') return
    const num = parseInt(val, 10)
    if (!isNaN(num)) setMinute(num)
  }

  const handleMinuteBlur = () => {
    if (minuteStr === '') return
    const num = parseInt(minuteStr, 10)
    if (!isNaN(num)) {
      const clamped = Math.min(59, Math.max(0, num))
      setMinute(clamped)
      setMinuteStr(String(clamped))
    }
  }

  const handleCalendarPickerChange = (val: string) => {
    if (!val) return
    const parts = val.split('-')
    if (parts.length === 3) {
      const y = parseInt(parts[0], 10)
      const m = parseInt(parts[1], 10)
      const d = parseInt(parts[2], 10)
      if (!isNaN(y) && y >= 1850 && y <= 2150) { setYear(y); setYearStr(String(y)); }
      if (!isNaN(m) && m >= 1 && m <= 12) { setMonth(m); setMonthStr(String(m)); }
      if (!isNaN(d) && d >= 1 && d <= 31) { setDay(d); setDayStr(String(d)); }
    }
  }

  const handleReset = () => {
    setName('')
    setYear(1995)
    setMonth(1)
    setDay(1)
    setHour(12)
    setMinute(0)
    setYearStr('1995')
    setMonthStr('1')
    setDayStr('1')
    setHourStr('12')
    setMinuteStr('0')
    handleCountrySelect('India')
  }

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (dateError) {
      alert(dateError)
      return
    }
    if (!yearStr || !monthStr || !dayStr || hourStr === '' || minuteStr === '') {
      alert('Please fill out complete Date and Time parameters.')
      return
    }
    onSubmit(e)
  }

  const datePickerValue = (year >= 1000 && year <= 9999 && month >= 1 && month <= 12 && day >= 1 && day <= 31)
    ? `${String(year).padStart(4, '0')}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`
    : ''

  return (
    <div className="w-full max-w-[1500px] mx-auto space-y-8 font-sans">
      {/* Modern Step Indicators Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-[#0D1527]/90 border border-white/10 p-5 rounded-3xl backdrop-blur-2xl text-sm shadow-xl">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="w-7 h-7 rounded-full bg-[#F5B942] text-[#050814] font-black flex items-center justify-center text-xs shadow-md shadow-[#F5B942]/20">1</span>
            <span className="font-bold text-[#F8FAFC]">Birth Details</span>
          </div>
          <span className="text-[#94A3B8]">→</span>
          <div className="flex items-center gap-2">
            <span className="w-7 h-7 rounded-full bg-white/10 text-[#94A3B8] font-bold flex items-center justify-center text-xs">2</span>
            <span className="text-[#94A3B8] font-medium">Location & Timezone</span>
          </div>
          <span className="text-[#94A3B8]">→</span>
          <div className="flex items-center gap-2">
            <span className="w-7 h-7 rounded-full bg-white/10 text-[#94A3B8] font-bold flex items-center justify-center text-xs">3</span>
            <span className="text-[#94A3B8] font-medium">Preview & Calculate</span>
          </div>
        </div>
        <span className="text-[#34D399] font-bold text-xs flex items-center gap-2 bg-[#34D399]/10 border border-[#34D399]/30 px-3 py-1 rounded-full">
          <span className="w-2 h-2 rounded-full bg-[#34D399] animate-pulse"></span>
          NASA DE440s Active
        </span>
      </div>

      {/* Spacious 2-Column Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* LEFT COLUMN: Birth Particulars Input Form (7 Cols) */}
        <div className="lg:col-span-7 bg-[#0D1527]/90 backdrop-blur-2xl p-8 md:p-10 rounded-3xl border border-white/10 shadow-2xl space-y-6">
          <div className="border-b border-white/10 pb-5">
            <span className="px-3.5 py-1.5 rounded-full bg-[#F5B942]/10 border border-[#F5B942]/30 text-[#F5B942] text-xs font-mono font-bold uppercase tracking-widest">
              Natal Parameter Input
            </span>
            <h2 className="text-2xl md:text-3xl font-black text-[#F8FAFC] tracking-wide mt-2 font-serif-heading">
              Enter Birth Particulars
            </h2>
            <p className="text-sm text-[#94A3B8] font-sans mt-1 leading-relaxed">
              Provide accurate birth details to calculate your canonical astrological profile.
            </p>
          </div>

          <form onSubmit={handleFormSubmit} className="space-y-6 font-sans">
            {/* Full Name */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-[#94A3B8] mb-2">
                Full Name <span className="text-[#F5B942]">*</span>
              </label>
              <input
                type="text"
                value={name}
                onChange={e => setName(e.target.value)}
                placeholder="Enter full birth name..."
                className="w-full bg-[#050814] border border-white/15 rounded-2xl px-4 py-3.5 text-[#F8FAFC] focus:border-[#F5B942] focus:ring-2 focus:ring-[#F5B942]/20 outline-none transition text-base font-sans"
                required
              />
            </div>

            {/* Inline Gregorian Date Error Banner */}
            {dateError && (
              <div className="p-4 rounded-2xl bg-rose-950/80 border border-rose-500/50 text-rose-200 text-xs font-sans flex items-center gap-2">
                <span className="text-base">⚠️</span>
                <span>{dateError}</span>
              </div>
            )}

            {/* Date & Time Grid Section */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {/* Date Input Box */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <label className="block text-xs font-bold uppercase tracking-wider text-[#94A3B8]">
                    Date of Birth (DD / MM / YYYY) <span className="text-[#F5B942]">*</span>
                  </label>
                  <input
                    type="date"
                    value={datePickerValue}
                    onChange={e => handleCalendarPickerChange(e.target.value)}
                    className="opacity-70 hover:opacity-100 cursor-pointer w-5 h-5 bg-transparent"
                    title="Select Date from Calendar Picker"
                  />
                </div>
                <div className="grid grid-cols-3 gap-2">
                  <div>
                    <span className="text-[11px] text-[#94A3B8] block mb-1">Day (DD)</span>
                    <input
                      type="text"
                      inputMode="numeric"
                      value={dayStr}
                      onChange={e => handleDayInput(e.target.value)}
                      onBlur={handleDayBlur}
                      placeholder="DD"
                      className={`w-full bg-[#050814] border rounded-2xl px-3 py-3 text-[#F8FAFC] outline-none text-sm tabular-nums font-bold text-center ${
                        dateError ? 'border-rose-500/80 focus:border-rose-400' : 'border-white/15 focus:border-[#F5B942]'
                      }`}
                      required
                    />
                  </div>
                  <div>
                    <span className="text-[11px] text-[#94A3B8] block mb-1">Month (MM)</span>
                    <input
                      type="text"
                      inputMode="numeric"
                      value={monthStr}
                      onChange={e => handleMonthInput(e.target.value)}
                      onBlur={handleMonthBlur}
                      placeholder="MM"
                      className={`w-full bg-[#050814] border rounded-2xl px-3 py-3 text-[#F8FAFC] outline-none text-sm tabular-nums font-bold text-center ${
                        dateError ? 'border-rose-500/80 focus:border-rose-400' : 'border-white/15 focus:border-[#F5B942]'
                      }`}
                      required
                    />
                  </div>
                  <div>
                    <span className="text-[11px] text-[#94A3B8] block mb-1">Year (YYYY)</span>
                    <input
                      type="text"
                      inputMode="numeric"
                      value={yearStr}
                      onChange={e => handleYearInput(e.target.value)}
                      onBlur={handleYearBlur}
                      placeholder="YYYY"
                      className={`w-full bg-[#050814] border rounded-2xl px-3 py-3 text-[#F8FAFC] outline-none text-sm tabular-nums font-bold text-center ${
                        dateError ? 'border-rose-500/80 focus:border-rose-400' : 'border-white/15 focus:border-[#F5B942]'
                      }`}
                      required
                    />
                  </div>
                </div>
              </div>

              {/* Time Input Box */}
              <div className="space-y-2">
                <label className="block text-xs font-bold uppercase tracking-wider text-[#94A3B8]">
                  Time of Birth (24-Hour IST) <span className="text-[#F5B942]">*</span>
                </label>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <span className="text-[11px] text-[#94A3B8] block mb-1">Hour (HH 0-23)</span>
                    <input
                      type="text"
                      inputMode="numeric"
                      value={hourStr}
                      onChange={e => handleHourInput(e.target.value)}
                      onBlur={handleHourBlur}
                      placeholder="HH"
                      className="w-full bg-[#050814] border border-white/15 rounded-2xl px-3 py-3 text-[#F8FAFC] focus:border-[#F5B942] outline-none text-sm tabular-nums font-bold text-center"
                      required
                    />
                  </div>
                  <div>
                    <span className="text-[11px] text-[#94A3B8] block mb-1">Minute (MM 0-59)</span>
                    <input
                      type="text"
                      inputMode="numeric"
                      value={minuteStr}
                      onChange={e => handleMinuteInput(e.target.value)}
                      onBlur={handleMinuteBlur}
                      placeholder="MM"
                      className="w-full bg-[#050814] border border-white/15 rounded-2xl px-3 py-3 text-[#F8FAFC] focus:border-[#F5B942] outline-none text-sm tabular-nums font-bold text-center"
                      required
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* 3-Tier Cascading Dropdown Location System */}
            <div className="space-y-4">
              <span className="block text-xs font-bold uppercase tracking-wider text-[#94A3B8]">
                Hierarchical Location Selection <span className="text-[#F5B942]">*</span>
              </span>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {/* Tier 1: Country Dropdown */}
                <div>
                  <label className="block text-xs text-[#94A3B8] mb-1 font-medium">1. Select Country</label>
                  <select
                    value={selectedCountryName}
                    onChange={e => handleCountrySelect(e.target.value)}
                    className="w-full bg-[#050814] border border-white/15 rounded-2xl p-3.5 text-[#F8FAFC] focus:border-[#F5B942] outline-none text-xs font-bold cursor-pointer"
                  >
                    {CASCADING_LOCATIONS.map(c => (
                      <option key={c.country_name} value={c.country_name} className="bg-[#050814] text-[#F8FAFC]">
                        {c.country_name}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Tier 2: State / Region Dropdown */}
                <div>
                  <label className="block text-xs text-[#94A3B8] mb-1 font-medium">2. Select State / Region</label>
                  <select
                    value={selectedStateName}
                    onChange={e => handleStateSelect(e.target.value)}
                    className="w-full bg-[#050814] border border-white/15 rounded-2xl p-3.5 text-[#F8FAFC] focus:border-[#F5B942] outline-none text-xs font-bold cursor-pointer"
                  >
                    {activeCountry.states.map(s => (
                      <option key={s.state_name} value={s.state_name} className="bg-[#050814] text-[#F8FAFC]">
                        {s.state_name}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Tier 3: District / City Dropdown */}
                <div>
                  <label className="block text-xs text-[#94A3B8] mb-1 font-medium">3. Select District / City</label>
                  <select
                    value={selectedDistrictName}
                    onChange={e => handleDistrictSelect(e.target.value)}
                    className="w-full bg-[#050814] border border-white/15 rounded-2xl p-3.5 text-[#F8FAFC] focus:border-[#F5B942] outline-none text-xs font-bold cursor-pointer"
                  >
                    {activeDistricts.map(d => (
                      <option key={d.district} value={d.district} className="bg-[#050814] text-[#F8FAFC]">
                        {d.district}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Resolved Location Badge */}
              <div className="p-4 rounded-2xl bg-[#050814] border border-[#F5B942]/30 flex flex-wrap items-center justify-between gap-3">
                <div className="space-y-0.5">
                  <p className="text-xs font-bold text-[#F5B942] flex items-center gap-1.5">
                    <span>📍</span> {placeName}, {country}
                  </p>
                  <p className="text-[11px] text-[#94A3B8] tabular-nums">
                    {latitude}° N, {longitude}° E • {timezoneStr}
                  </p>
                </div>
                <span className="text-[10px] bg-[#34D399]/20 text-[#34D399] border border-[#34D399]/40 px-2.5 py-1 rounded-full font-bold">
                  ● Coordinates Loaded
                </span>
              </div>
            </div>

            {/* Advanced Calculation Options Toggle */}
            <div className="pt-2 border-t border-white/10 space-y-4">
              <button
                type="button"
                onClick={() => setShowAdvanced(!showAdvanced)}
                className="text-xs text-[#F5B942] font-bold hover:underline flex items-center gap-2 cursor-pointer"
              >
                <span>{showAdvanced ? '▼' : '►'}</span> Advanced Coordinates & Timezone Controls
              </button>

              {showAdvanced && (
                <div className="p-5 rounded-2xl bg-[#050814] border border-white/10 space-y-4 text-xs font-sans">
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-[11px] text-[#94A3B8] mb-1">Custom Latitude (°N)</label>
                      <input
                        type="number"
                        step="0.0001"
                        value={latitude}
                        onChange={e => setLatitude(parseFloat(e.target.value) || 0)}
                        className="w-full bg-[#0D1527] border border-white/15 rounded-xl p-2.5 text-[#F8FAFC] outline-none"
                      />
                    </div>
                    <div>
                      <label className="block text-[11px] text-[#94A3B8] mb-1">Custom Longitude (°E)</label>
                      <input
                        type="number"
                        step="0.0001"
                        value={longitude}
                        onChange={e => setLongitude(parseFloat(e.target.value) || 0)}
                        className="w-full bg-[#0D1527] border border-white/15 rounded-xl p-2.5 text-[#F8FAFC] outline-none"
                      />
                    </div>
                    <div>
                      <label className="block text-[11px] text-[#94A3B8] mb-1">IANA Timezone String</label>
                      <input
                        type="text"
                        value={timezoneStr}
                        onChange={e => setTimezoneStr(e.target.value)}
                        className="w-full bg-[#0D1527] border border-white/15 rounded-xl p-2.5 text-[#F8FAFC] outline-none"
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
                  className="rounded border-white/20 bg-[#050814] text-[#F5B942] focus:ring-[#F5B942]"
                />
                <label htmlFor="saveProfile" className="cursor-pointer">Save this natal profile for future calculations</label>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="pt-4 flex items-center gap-4">
              <button
                type="submit"
                disabled={Boolean(dateError)}
                className="flex-1 py-4 px-8 rounded-2xl bg-gradient-to-r from-[#F5B942] via-[#E5A832] to-[#B8860B] hover:from-[#E5A832] hover:to-[#F5B942] text-[#050814] font-black text-sm uppercase tracking-wider shadow-xl shadow-[#F5B942]/20 transition duration-150 flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
              >
                <span>✦</span> Calculate Canonical Chart
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
            <span className="text-[10px] bg-[#F5B942]/10 border border-[#F5B942]/30 text-[#F5B942] px-3 py-1 rounded-full font-bold uppercase tracking-wider">
              Whole-Sign Bhava
            </span>
          </div>

          {/* Style Selector Buttons */}
          <div className="flex bg-[#050814] p-1.5 rounded-2xl border border-white/10 text-xs">
            <button
              onClick={() => setChartStyle('north')}
              className={`flex-1 py-2 rounded-xl font-bold transition cursor-pointer ${
                chartStyle === 'north' ? 'bg-[#F5B942]/20 text-[#F5B942] border border-[#F5B942]/40 shadow-md' : 'text-[#94A3B8] hover:text-[#F8FAFC]'
              }`}
            >
              North Indian (Rāśi)
            </button>
            <button
              onClick={() => setChartStyle('south')}
              className={`flex-1 py-2 rounded-xl font-bold transition cursor-pointer ${
                chartStyle === 'south' ? 'bg-[#F5B942]/20 text-[#F5B942] border border-[#F5B942]/40 shadow-md' : 'text-[#94A3B8] hover:text-[#F8FAFC]'
              }`}
            >
              South Indian
            </button>
          </div>

          {/* SVG Astrolabe Preview Container */}
          <div className="p-6 bg-[#050814] rounded-3xl border border-[#F5B942]/20 flex items-center justify-center shadow-inner min-h-[320px]">
            <div className="w-full max-w-[280px] aspect-square border border-[#F5B942]/40 rounded-2xl p-4 flex flex-col justify-between relative bg-gradient-to-b from-[#0D1527] to-[#050814] shadow-xl">
              <div className="flex justify-between text-[11px] font-bold text-[#F5B942]/80">
                <span>12</span>
                <span>1</span>
                <span>2</span>
              </div>
              <div className="flex justify-between items-center text-xs font-bold text-[#F5B942]">
                <span>11</span>
                <div className="text-center font-serif-heading">
                  <span className="text-2xl text-[#F5B942] font-black block">As</span>
                  <span className="text-[10px] text-[#38BDF8]">{placeName.split(',')[0] || 'Lagna'}</span>
                </div>
                <span>3</span>
              </div>
              <div className="flex justify-between text-[11px] font-bold text-[#F5B942]/80">
                <span>10</span>
                <span>7</span>
                <span>4</span>
              </div>
            </div>
          </div>

          {/* Summary Particulars Card */}
          <div className="p-4 rounded-2xl bg-[#050814] border border-white/10 space-y-2 text-xs">
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
