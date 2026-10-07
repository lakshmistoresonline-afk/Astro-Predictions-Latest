export interface CityPreset {
  name: string
  country: string
  lat: number
  lon: number
  tz: string
}

export const PRESET_CITIES: CityPreset[] = [
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

export interface BirthProfileRequest {
  name: string
  year: number
  month: number
  day: number
  hour: number
  minute: number
  second?: number
  timezone_str: string
  latitude: number
  longitude: number
  place_name: string
  country: string
  zodiac_system?: string
  ayanamsha?: string
}

export interface RashiPosition {
  absolute_longitude: number
  sign: string
  sign_index: number
  degree: number
  minute: number
  second: number
}

export interface NakshatraPada {
  nakshatra: string
  nakshatra_index: number
  degree_within_nakshatra: number
  pada: number
}

export interface PlanetaryVedicPlacement {
  body_name: string
  sidereal_longitude: number
  velocity_deg_day: number
  retrograde: boolean
  rashi: RashiPosition
  nakshatra_pada: NakshatraPada
}

export interface WholeSignHouse {
  house_number: number
  sign: string
  sign_index: number
  start_longitude: number
  end_longitude: number
}

export interface CanonicalVedicChart {
  input_data: BirthProfileRequest
  ayanamsha_mode: string
  ayanamsha_value_deg: number
  ascendant: RashiPosition
  mc: RashiPosition
  placements: Record<string, PlanetaryVedicPlacement>
  whole_sign_houses: WholeSignHouse[]
  calculation_hash: string
}

export interface VargaPlacement {
  body_name: string
  varga_sign: string
  varga_sign_index: number
  varga_division_index: number
  varga_degree_in_sign: number
  is_vargottama: boolean
}

export interface VargaChart {
  division: string
  division_number: number
  division_name: string
  ascendant: VargaPlacement
  placements: Record<string, VargaPlacement>
  convention: string
  source: string
  calculation_hash: string
}

export interface Full16VargaSuite {
  chart_hash: string
  vargas: Record<string, VargaChart>
  vargottama_bodies: string[]
  calculation_hash: string
}

export interface BirthDashaBalance {
  mahadasha_lord: string
  total_mahadasha_years: number
  remaining_years: number
  remaining_days: number
  birth_utc_datetime_iso: string
  first_mahadasha_end_utc_iso: string
}

export interface DashaPeriodNode {
  level: number
  level_name: string
  lord: string
  sequence_index: number
  start_utc_iso: string
  end_utc_iso: string
  duration_days: number
  duration_years: number
}

export interface FullVimshottariDashaResult {
  birth_utc_datetime_iso: string
  moon_sidereal_longitude_deg: number
  birth_balance: BirthDashaBalance
  mahadashas: DashaPeriodNode[]
  calculation_hash: string
}

export interface RuleConditionEvidence {
  condition_id: string
  condition_description: string
  status: boolean
}

export interface YogaResult {
  rule_id: string
  name: string
  sanskrit_name?: string
  category: string
  status: string
  conditions: RuleConditionEvidence[]
  participating_planets: string[]
  participating_houses: number[]
}

export interface YogaSuiteResult {
  chart_hash: string
  detected_yogas: YogaResult[]
  all_evaluated_yogas: YogaResult[]
  summary_counts: Record<string, number>
  rule_set_version: string
}

export interface DoshaResult {
  rule_id: string
  name: string
  sanskrit_name?: string
  status: string
  conditions: RuleConditionEvidence[]
  cancellation_exceptions: RuleConditionEvidence[]
  participating_planets: string[]
  participating_houses: number[]
}

export interface DoshaSuiteResult {
  chart_hash: string
  detected_doshas: DoshaResult[]
  all_evaluated_doshas: DoshaResult[]
  summary_counts: Record<string, number>
  rule_set_version: string
}

export interface ShadbalaComponent {
  name: string
  value_rupas: number
  value_shashtiamsas: number
  sub_components?: Record<string, number>
}

export interface PlanetShadbala {
  planet: string
  sthana_bala: ShadbalaComponent
  dig_bala: ShadbalaComponent
  kala_bala: ShadbalaComponent
  cheshta_bala: ShadbalaComponent
  naisargika_bala: ShadbalaComponent
  drik_bala: ShadbalaComponent
  total_shashtiamsas: number
  total_rupas: number
  strength_percentage: number
}

export interface ShadbalaSuiteResult {
  chart_hash: string
  planets: Record<string, PlanetShadbala>
  calculation_hash: string
}

export interface HouseSAVEvidence {
  rashi_index: number
  rashi_name: string
  sav_bindus: number | null
  strength_category: string
  transit_recommendation: string
}

export interface AshtakavargaPredictiveEvidence {
  house_sav_evidences: HouseSAVEvidence[]
  total_sav_bindus: number | null
  strongest_house_rashi: string | null
  weakest_house_rashi: string | null
  summary_evidence: string
  calculation_hash: string
}

export interface CharaKarakaInfo {
  karaka_code: string
  karaka_name: string
  planet: string
  degree_in_sign: number
}

export interface JaiminiSuiteResult {
  chart_hash: string
  atmakaraka_planet: string
  chara_karakas: Record<string, CharaKarakaInfo>
  arudha_lagna_rashi_index: number
  arudha_lagna_rashi_name: string
  upapada_lagna_rashi_index: number
  upapada_lagna_rashi_name: string
  karakamsha_rashi_index: number
  karakamsha_rashi_name: string
  calculation_hash: string
}

export interface TithiInfo {
  tithi_number: number
  paksha_tithi_number: number
  tithi_name: string
  paksha: string
  is_rikta: boolean
  is_amavasya: boolean
  is_purnima: boolean
}

export interface VaraInfo {
  weekday_number: number
  day_name_english: string
  day_name_sanskrit: string
  ruling_planet: string
}

export interface NityaYogaInfo {
  yoga_number: number
  yoga_name: string
  nature: string
}

export interface KaranaInfo {
  karana_number: number
  karana_name: string
  type: string
  nature: string
  is_vishti: boolean
}

export interface TimingWindow {
  name: string
  start_time_iso: string
  end_time_iso: string
  nature: string
}

export interface PanchangaResult {
  datetime_iso: string
  location_name: string
  latitude: number
  longitude: number
  tithi: TithiInfo
  vara: VaraInfo
  nakshatra_name: string
  nakshatra_pada: number
  nitya_yoga: NityaYogaInfo
  karana: KaranaInfo
  sunrise_iso: string
  sunset_iso: string
  rahu_kalam: TimingWindow
  yamaganda: TimingWindow
  gulika_kalam: TimingWindow
  abhijit_muhurta: TimingWindow
  calculation_hash: string
}

export interface ActivityRuleResult {
  rule_id: string
  factor_name: string
  rule_category: string
  status: string
  is_hard_exclusion: boolean
  description: string
}

export interface MuhurtaEvaluation {
  activity_name: string
  datetime_iso: string
  recommendation: string
  is_rahu_kalam_active: boolean
  is_abhijit_active: boolean
  has_hard_exclusion: boolean
  favorable_factor_count: number
  unfavorable_factor_count: number
  evaluated_factors: ActivityRuleResult[]
  summary: string
  calculation_hash: string
}

export interface MuhurtaSuiteResult {
  panchanga_hash: string
  datetime_iso: string
  evaluations: Record<string, MuhurtaEvaluation>
  calculation_hash: string
}

export interface CanonicalAstrologyEvidence {
  birth_input: BirthProfileRequest
  canonical_chart: CanonicalVedicChart
  varga_suite: Full16VargaSuite
  natal_dasha_suite: FullVimshottariDashaResult
  yoga_suite: YogaSuiteResult
  dosha_suite: DoshaSuiteResult
  shadbala_suite?: ShadbalaSuiteResult
  ashtakavarga_evidence?: AshtakavargaPredictiveEvidence
  jaimini_suite?: JaiminiSuiteResult
  panchanga?: PanchangaResult
  muhurta_suite?: MuhurtaSuiteResult
  master_evidence_hash: string
}

export interface DomainRuleDefinition {
  domain_code: string
  domain_title: string
  primary_karakas: string[]
  relevant_houses: number[]
  varga_code: string
  rule_description: string
}

export interface DomainPredictionEvidence {
  rule_definition: DomainRuleDefinition
  evidence_status: string
  evidence_strength_class: string | null
  traditional_metadata: Record<string, string>
}

export interface ComprehensivePredictionPackage {
  master_evidence_hash: string
  ruleset_version: string
  domain_predictions: Record<string, DomainPredictionEvidence>
  active_dasha_summary: string | null
  calculation_hash: string
}

export interface BirthProfileResponse {
  status: string
  birth_input: BirthProfileRequest
  master_evidence: CanonicalAstrologyEvidence
  predictions: ComprehensivePredictionPackage
  svg_chart: string | null
  report: Record<string, any> | null
}

export interface AIInterpretationResponse {
  domain: string
  interpretation: string
  provider: string
  generation_model: string
  validation_model: string
  validation_status: string
}
