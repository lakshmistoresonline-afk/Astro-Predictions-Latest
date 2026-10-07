import { PRESET_CITIES } from '../types/api'

describe('Web API Types and Presets', () => {
  it('contains valid preset cities with IANA timezones', () => {
    expect(PRESET_CITIES.length).toBeGreaterThan(0)
    PRESET_CITIES.forEach(city => {
      expect(city.name).toBeTruthy()
      expect(city.tz).toContain('/')
      expect(typeof city.lat).toBe('number')
      expect(typeof city.lon).toBe('number')
    })
  })
})
