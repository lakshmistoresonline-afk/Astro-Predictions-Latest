package com.astro.predictions.data.model

import com.google.gson.annotations.SerializedName

// --- Presets ---
data class CityPreset(
    val name: String,
    val country: String,
    val lat: Double,
    val lon: Double,
    val tz: String
)

val PRESET_CITIES = listOf(
    CityPreset("New Delhi", "India", 28.6139, 77.2090, "Asia/Kolkata"),
    CityPreset("Mumbai", "India", 18.9220, 72.8347, "Asia/Kolkata"),
    CityPreset("Bengaluru", "India", 12.9716, 77.5946, "Asia/Kolkata"),
    CityPreset("London", "United Kingdom", 51.5074, -0.1278, "Europe/London"),
    CityPreset("New York", "United States", 40.7128, -74.0060, "America/New_York"),
    CityPreset("Los Angeles", "United States", 34.0522, -118.2437, "America/Los_Angeles"),
    CityPreset("Tokyo", "Japan", 35.6762, 139.6503, "Asia/Tokyo"),
    CityPreset("Sydney", "Australia", -33.8688, 151.2093, "Australia/Sydney"),
    CityPreset("Paris", "France", 48.8566, 2.3522, "Europe/Paris"),
    CityPreset("Dubai", "United Arab Emirates", 25.2048, 55.2708, "Asia/Dubai"),
    CityPreset("Singapore", "Singapore", 1.3521, 103.8198, "Asia/Singapore"),
    CityPreset("Toronto", "Canada", 43.6532, -79.3832, "America/Toronto")
)

// --- API Requests ---
data class BirthProfileRequest(
    val name: String,
    val year: Int,
    val month: Int,
    val day: Int,
    val hour: Int,
    val minute: Int,
    val second: Int = 0,
    @SerializedName("timezone_str") val timezoneStr: String,
    val latitude: Double,
    val longitude: Double,
    @SerializedName("place_name") val placeName: String,
    val country: String,
    @SerializedName("zodiac_system") val zodiacSystem: String = "sidereal",
    val ayanamsha: String = "lahiri"
)

data class TransitRequest(
    @SerializedName("birth_input") val birthInput: BirthProfileRequest,
    @SerializedName("query_datetime_iso") val queryDatetimeIso: String? = null
)

data class AIInterpretationRequest(
    @SerializedName("birth_input") val birthInput: BirthProfileRequest,
    val prompt: String,
    val domain: String = "CAREER"
)

// --- API Main Response ---
data class BirthProfileResponse(
    val status: String,
    @SerializedName("birth_input") val birthInput: BirthProfileRequest,
    @SerializedName("master_evidence") val masterEvidence: CanonicalAstrologyEvidence,
    val predictions: ComprehensivePredictionPackage,
    @SerializedName("svg_chart") val svgChart: String? = null,
    val report: Map<String, Any>? = null
)

// --- Master Evidence Package ---
data class CanonicalAstrologyEvidence(
    @SerializedName("birth_input") val birthInput: BirthProfileRequest,
    @SerializedName("canonical_chart") val canonicalChart: CanonicalVedicChart,
    @SerializedName("varga_suite") val vargaSuite: Full16VargaSuite,
    @SerializedName("varga_evidence") val vargaEvidence: VargaSuiteEvidence?,
    @SerializedName("natal_dasha_suite") val natalDashaSuite: FullVimshottariDashaResult,
    @SerializedName("active_dasha_hierarchy") val activeDashaHierarchy: ActiveDashaHierarchy?,
    @SerializedName("yoga_suite") val yogaSuite: YogaSuiteResult,
    @SerializedName("dosha_suite") val doshaSuite: DoshaSuiteResult,
    @SerializedName("shadbala_suite") val shadbalaSuite: ShadbalaSuiteResult?,
    @SerializedName("shadbala_evidence") val shadbalaEvidence: ShadbalaEvidencePackage?,
    @SerializedName("ashtakavarga_suite") val ashtakavargaSuite: AshtakavargaSuiteResult?,
    @SerializedName("ashtakavarga_evidence") val ashtakavargaEvidence: AshtakavargaPredictiveEvidence?,
    @SerializedName("jaimini_suite") val jaiminiSuite: JaiminiSuiteResult?,
    @SerializedName("transit_snapshot") val transitSnapshot: TransitSnapshot?,
    val panchanga: PanchangaResult?,
    @SerializedName("muhurta_suite") val muhurtaSuite: MuhurtaSuiteResult?,
    @SerializedName("timing_suite") val timingSuite: TimingSuiteResult?,
    @SerializedName("natal_calculation_hash") val natalCalculationHash: String,
    @SerializedName("temporal_calculation_hash") val temporalCalculationHash: String?,
    @SerializedName("master_evidence_hash") val masterEvidenceHash: String
)

// --- Submodels ---
data class TimeNormalization(
    @SerializedName("local_datetime_iso") val localDatetimeIso: String,
    @SerializedName("timezone_identifier") val timezoneIdentifier: String,
    @SerializedName("utc_datetime_iso") val utcDatetimeIso: String,
    @SerializedName("utc_offset_hours") val utcOffsetHours: Double,
    @SerializedName("julian_day_utc") val julianDayUtc: Double,
    @SerializedName("julian_day_tt") val julianDayTt: Double,
    @SerializedName("time_scale") val timeScale: String
)

data class RashiPosition(
    @SerializedName("absolute_longitude") val absoluteLongitude: Double,
    val sign: String,
    @SerializedName("sign_index") val signIndex: Int,
    val degree: Int,
    val minute: Int,
    val second: Double
)

data class NakshatraPada(
    val nakshatra: String,
    @SerializedName("nakshatra_index") val nakshatraIndex: Int,
    @SerializedName("degree_within_nakshatra") val degreeWithinNakshatra: Double,
    val pada: Int
)

data class PlanetaryVedicPlacement(
    @SerializedName("body_name") val bodyName: String,
    @SerializedName("sidereal_longitude") val siderealLongitude: Double,
    @SerializedName("velocity_deg_day") val velocityDegDay: Double,
    val retrograde: Boolean,
    val rashi: RashiPosition,
    @SerializedName("nakshatra_pada") val nakshatraPada: NakshatraPada
)

data class WholeSignHouse(
    @SerializedName("house_number") val houseNumber: Int,
    val sign: String,
    @SerializedName("sign_index") val signIndex: Int,
    @SerializedName("start_longitude") val startLongitude: Double,
    @SerializedName("end_longitude") val endLongitude: Double
)

data class CanonicalVedicChart(
    @SerializedName("input_data") val inputData: BirthProfileRequest,
    @SerializedName("time_normalization") val timeNormalization: TimeNormalization,
    @SerializedName("ayanamsha_mode") val ayanamshaMode: String,
    @SerializedName("ayanamsha_value_deg") val ayanamshaValueDeg: Double,
    val ascendant: RashiPosition,
    val mc: RashiPosition,
    val placements: Map<String, PlanetaryVedicPlacement>,
    @SerializedName("whole_sign_houses") val wholeSignHouses: List<WholeSignHouse>,
    @SerializedName("calculation_hash") val calculationHash: String
)

data class VargaPlacement(
    @SerializedName("body_name") val bodyName: String,
    @SerializedName("varga_sign") val vargaSign: String,
    @SerializedName("varga_sign_index") val vargaSignIndex: Int,
    @SerializedName("varga_division_index") val vargaDivisionIndex: Int,
    @SerializedName("varga_degree_in_sign") val vargaDegreeInSign: Double,
    @SerializedName("is_vargottama") val isVargottama: Boolean
)

data class VargaChart(
    val division: String,
    @SerializedName("division_number") val divisionNumber: Int,
    @SerializedName("division_name") val divisionName: String,
    val ascendant: VargaPlacement,
    val placements: Map<String, VargaPlacement>,
    val convention: String,
    val source: String,
    @SerializedName("calculation_hash") val calculationHash: String
)

data class Full16VargaSuite(
    @SerializedName("chart_hash") val chartHash: String,
    val d1: VargaChart?,
    val d2: VargaChart?,
    val d3: VargaChart?,
    val d4: VargaChart?,
    val d7: VargaChart?,
    val d9: VargaChart?,
    val d10: VargaChart?,
    val d12: VargaChart?,
    val d16: VargaChart?,
    val d20: VargaChart?,
    val d24: VargaChart?,
    val d27: VargaChart?,
    val d30: VargaChart?,
    val d40: VargaChart?,
    val d45: VargaChart?,
    val d60: VargaChart?,
    val vargas: Map<String, VargaChart>,
    @SerializedName("vargottama_bodies") val vargottamaBodies: List<String>,
    @SerializedName("calculation_hash") val calculationHash: String
)

data class VargaDomainEvidence(
    @SerializedName("varga_code") val vargaCode: String,
    @SerializedName("domain_title") val domainTitle: String,
    @SerializedName("domain_description") val domainDescription: String,
    @SerializedName("evidence_status") val evidenceStatus: String = "AVAILABLE",
    @SerializedName("lagna_rashi_name") val lagnaRashiName: String,
    @SerializedName("lagna_lord_planet") val lagnaLordPlanet: String,
    @SerializedName("key_placements") val keyPlacements: Map<String, String>,
    @SerializedName("exalted_planets") val exaltedPlanets: List<String>,
    @SerializedName("debilitated_planets") val debilitatedPlanets: List<String>,
    @SerializedName("vargottama_planets") val vargottamaPlanets: List<String>,
    @SerializedName("summary_evidence") val summaryEvidence: String
)

data class VargaSuiteEvidence(
    @SerializedName("varga_evidences") val vargaEvidences: Map<String, VargaDomainEvidence>,
    @SerializedName("calculation_hash") val calculationHash: String
)

data class BirthNakshatraInfo(
    @SerializedName("nakshatra_index") val nakshatraIndex: Int,
    @SerializedName("nakshatra_name") val nakshatraName: String,
    @SerializedName("nakshatra_lord") val nakshatraLord: String,
    val pada: Int,
    @SerializedName("moon_sidereal_longitude_deg") val moonSiderealLongitudeDeg: Double,
    @SerializedName("elapsed_fraction") val elapsedFraction: Double,
    @SerializedName("remaining_fraction") val remainingFraction: Double
)

data class BirthDashaBalance(
    @SerializedName("mahadasha_lord") val mahadashaLord: String,
    @SerializedName("total_mahadasha_years") val totalMahadashaYears: Double,
    @SerializedName("remaining_years") val remainingYears: Double,
    @SerializedName("remaining_days") val remainingDays: Double,
    @SerializedName("birth_utc_datetime_iso") val birthUtcDatetimeIso: String,
    @SerializedName("first_mahadasha_end_utc_iso") val firstMahadashaEndUtcIso: String
)

data class DashaPeriodNode(
    val level: Int,
    @SerializedName("level_name") val levelName: String,
    val lord: String,
    @SerializedName("sequence_index") val sequenceIndex: Int,
    @SerializedName("start_utc_iso") val startUtcIso: String,
    @SerializedName("end_utc_iso") val endUtcIso: String,
    @SerializedName("duration_days") val durationDays: Double,
    @SerializedName("duration_years") val durationYears: Double
)

data class ActiveDashaHierarchy(
    @SerializedName("query_utc_iso") val queryUtcIso: String,
    @SerializedName("active_mahadasha") val activeMahadasha: DashaPeriodNode,
    @SerializedName("active_antardasha") val activeAntardasha: DashaPeriodNode?,
    @SerializedName("active_pratyantardasha") val activePratyantardasha: DashaPeriodNode?,
    @SerializedName("active_sookshma") val activeSookshma: DashaPeriodNode?,
    @SerializedName("active_prana") val activePrana: DashaPeriodNode?
)

data class FullVimshottariDashaResult(
    @SerializedName("birth_utc_datetime_iso") val birthUtcDatetimeIso: String,
    @SerializedName("moon_sidereal_longitude_deg") val moonSiderealLongitudeDeg: Double,
    @SerializedName("nakshatra_info") val nakshatraInfo: BirthNakshatraInfo,
    @SerializedName("birth_balance") val birthBalance: BirthDashaBalance,
    val mahadashas: List<DashaPeriodNode>,
    @SerializedName("active_hierarchy") val activeHierarchy: ActiveDashaHierarchy?,
    @SerializedName("calculation_hash") val calculationHash: String
)

data class RuleConditionEvidence(
    @SerializedName("condition_id") val conditionId: String,
    @SerializedName("condition_description") val conditionDescription: String,
    val status: Boolean
)

data class YogaResult(
    @SerializedName("rule_id") val ruleId: String,
    val name: String,
    @SerializedName("sanskrit_name") val sanskritName: String?,
    val category: String,
    val status: String,
    val conditions: List<RuleConditionEvidence>,
    @SerializedName("participating_planets") val participatingPlanets: List<String>,
    @SerializedName("participating_houses") val participatingHouses: List<Int>
)

data class YogaSuiteResult(
    @SerializedName("chart_hash") val chartHash: String,
    @SerializedName("detected_yogas") val detectedYogas: List<YogaResult>,
    @SerializedName("all_evaluated_yogas") val allEvaluatedYogas: List<YogaResult>,
    @SerializedName("summary_counts") val summaryCounts: Map<String, Any>,
    @SerializedName("rule_set_version") val ruleSetVersion: String
)

data class DoshaConditionEvidence(
    @SerializedName("condition_id") val conditionId: String,
    @SerializedName("condition_description") val conditionDescription: String,
    val status: Boolean
)

data class DoshaResult(
    @SerializedName("rule_id") val ruleId: String,
    val name: String,
    @SerializedName("sanskrit_name") val sanskritName: String?,
    val status: String,
    val conditions: List<DoshaConditionEvidence>,
    @SerializedName("cancellation_exceptions") val cancellationExceptions: List<DoshaConditionEvidence> = emptyList(),
    @SerializedName("participating_planets") val participatingPlanets: List<String>,
    @SerializedName("participating_houses") val participatingHouses: List<Int>
)

data class DoshaSuiteResult(
    @SerializedName("chart_hash") val chartHash: String,
    @SerializedName("detected_doshas") val detectedDoshas: List<DoshaResult>,
    @SerializedName("all_evaluated_doshas") val allEvaluatedDoshas: List<DoshaResult>,
    @SerializedName("summary_counts") val summaryCounts: Map<String, Any>,
    @SerializedName("rule_set_version") val ruleSetVersion: String
)

data class ShadbalaComponent(
    val name: String,
    @SerializedName("value_rupas") val valueRupas: Double,
    @SerializedName("value_shashtiamsas") val valueShashtiamsas: Double,
    @SerializedName("sub_components") val subComponents: Map<String, Double> = emptyMap()
)

data class PlanetShadbala(
    val planet: String,
    @SerializedName("sthana_bala") val sthanaBala: ShadbalaComponent,
    @SerializedName("dig_bala") val digBala: ShadbalaComponent,
    @SerializedName("kala_bala") val kalaBala: ShadbalaComponent,
    @SerializedName("cheshta_bala") val cheshtaBala: ShadbalaComponent,
    @SerializedName("naisargika_bala") val naisargikaBala: ShadbalaComponent,
    @SerializedName("drik_bala") val drikBala: ShadbalaComponent,
    @SerializedName("total_shashtiamsas") val totalShashtiamsas: Double,
    @SerializedName("total_rupas") val totalRupas: Double,
    @SerializedName("strength_percentage") val strengthPercentage: Double
)

data class ShadbalaSuiteResult(
    @SerializedName("chart_hash") val chartHash: String,
    val planets: Map<String, PlanetShadbala>,
    @SerializedName("calculation_hash") val calculationHash: String
)

data class PlanetStrengthEvidence(
    val planet: String,
    @SerializedName("total_shashtiamsas") val totalShashtiamsas: Double,
    @SerializedName("total_rupas") val totalRupas: Double,
    @SerializedName("is_sufficient_strength") val isSufficientStrength: Boolean,
    @SerializedName("relative_rank") val relativeRank: Int,
    @SerializedName("strongest_component") val strongestComponent: String,
    @SerializedName("weakest_component") val weakestComponent: String,
    @SerializedName("summary_evidence") val summaryEvidence: String
)

data class DomainStrengthEvidence(
    val domain: String,
    @SerializedName("domain_focus") val domainFocus: String,
    @SerializedName("relevant_planets") val relevantPlanets: List<String>,
    @SerializedName("average_domain_rupas") val averageDomainRupas: Double,
    @SerializedName("domain_strength_class") val domainStrengthClass: String,
    @SerializedName("detailed_strength_category") val detailedStrengthCategory: String?,
    val summary: String
)

data class ShadbalaEvidencePackage(
    @SerializedName("planet_strengths") val planetStrengths: Map<String, PlanetStrengthEvidence>,
    @SerializedName("domain_strengths") val domainStrengths: Map<String, DomainStrengthEvidence>,
    @SerializedName("strongest_planet") val strongestPlanet: String,
    @SerializedName("weakest_planet") val weakestPlanet: String,
    @SerializedName("calculation_hash") val calculationHash: String
)

data class BhinnashtakavargaResult(
    val planet: String,
    val bindus: List<Int>,
    val total: Int
)

data class SarvashtakavargaResult(
    val bindus: List<Int>,
    val total: Int
)

data class AshtakavargaSuiteResult(
    @SerializedName("chart_hash") val chartHash: String,
    val bav: Map<String, BhinnashtakavargaResult>,
    val sav: SarvashtakavargaResult,
    @SerializedName("calculation_hash") val calculationHash: String
)

data class HouseSAVEvidence(
    @SerializedName("rashi_index") val rashiIndex: Int,
    @SerializedName("rashi_name") val rashiName: String,
    @SerializedName("sav_bindus") val savBindus: Int?,
    @SerializedName("strength_category") val strengthCategory: String,
    @SerializedName("transit_recommendation") val transitRecommendation: String
)

data class AshtakavargaPredictiveEvidence(
    @SerializedName("house_sav_evidences") val houseSavEvidences: List<HouseSAVEvidence>,
    @SerializedName("total_sav_bindus") val totalSavBindus: Int?,
    @SerializedName("strongest_house_rashi") val strongestHouseRashi: String?,
    @SerializedName("weakest_house_rashi") val weakestHouseRashi: String?,
    @SerializedName("summary_evidence") val summaryEvidence: String,
    @SerializedName("calculation_hash") val calculationHash: String
)

data class CharaKarakaInfo(
    @SerializedName("karaka_code") val karakaCode: String,
    @SerializedName("karaka_name") val karakaName: String,
    val planet: String,
    @SerializedName("degree_in_sign") val degreeInSign: Double
)

data class RashiAspectInfo(
    @SerializedName("source_rashi_index") val sourceRashiIndex: Int,
    @SerializedName("source_rashi_name") val sourceRashiName: String,
    @SerializedName("aspected_rashi_indices") val aspectedRashiIndices: List<Int>,
    @SerializedName("aspected_rashi_names") val aspectedRashiNames: List<String>
)

data class JaiminiSuiteResult(
    @SerializedName("chart_hash") val chartHash: String,
    @SerializedName("atmakaraka_planet") val atmakarakaPlanet: String,
    @SerializedName("chara_karakas") val charaKarakas: Map<String, CharaKarakaInfo>,
    @SerializedName("arudha_lagna_rashi_index") val arudhaLagnaRashiIndex: Int,
    @SerializedName("arudha_lagna_rashi_name") val arudhaLagnaRashiName: String,
    @SerializedName("upapada_lagna_rashi_index") val upapadaLagnaRashiIndex: Int,
    @SerializedName("upapada_lagna_rashi_name") val upapadaLagnaRashiName: String,
    @SerializedName("karakamsha_rashi_index") val karakamshaRashiIndex: Int,
    @SerializedName("karakamsha_rashi_name") val karakamshaRashiName: String,
    @SerializedName("rashi_aspects") val rashiAspects: List<RashiAspectInfo>,
    @SerializedName("calculation_hash") val calculationHash: String
)

data class TithiInfo(
    @SerializedName("tithi_number") val tithiNumber: Int,
    @SerializedName("paksha_tithi_number") val pakshaTithiNumber: Int,
    @SerializedName("tithi_name") val tithiName: String,
    val paksha: String,
    @SerializedName("is_rikta") val isRikta: Boolean,
    @SerializedName("is_amavasya") val isAmavasya: Boolean,
    @SerializedName("is_purnima") val isPurnima: Boolean,
    @SerializedName("degree_elapsed_in_tithi") val degreeElapsedInTithi: Double,
    @SerializedName("percentage_elapsed") val percentageElapsed: Double
)

data class VaraInfo(
    @SerializedName("weekday_number") val weekdayNumber: Int,
    @SerializedName("day_name_english") val dayNameEnglish: String,
    @SerializedName("day_name_sanskrit") val dayNameSanskrit: String,
    @SerializedName("ruling_planet") val rulingPlanet: String
)

data class NityaYogaInfo(
    @SerializedName("yoga_number") val yogaNumber: Int,
    @SerializedName("yoga_name") val yogaName: String,
    val nature: String
)

data class KaranaInfo(
    @SerializedName("karana_number") val karanaNumber: Int,
    @SerializedName("karana_name") val karanaName: String,
    val type: String,
    val nature: String,
    @SerializedName("is_vishti") val isVishti: Boolean
)

data class TimingWindow(
    val name: String,
    @SerializedName("start_time_iso") val startTimeIso: String,
    @SerializedName("end_time_iso") val endTimeIso: String,
    val nature: String
)

data class PanchangaResult(
    @SerializedName("datetime_iso") val datetimeIso: String,
    @SerializedName("location_name") val locationName: String,
    val latitude: Double,
    val longitude: Double,
    val tithi: TithiInfo,
    val vara: VaraInfo,
    @SerializedName("nakshatra_name") val nakshatraName: String,
    @SerializedName("nakshatra_pada") val nakshatraPada: Int,
    @SerializedName("nitya_yoga") val nityaYoga: NityaYogaInfo,
    val karana: KaranaInfo,
    @SerializedName("sunrise_iso") val sunriseIso: String,
    @SerializedName("sunset_iso") val sunsetIso: String,
    @SerializedName("rahu_kalam") val rahuKalam: TimingWindow,
    val yamaganda: TimingWindow,
    @SerializedName("gulika_kalam") val gulikaKalam: TimingWindow,
    @SerializedName("abhijit_muhurta") val abhijitMuhurta: TimingWindow,
    @SerializedName("calculation_hash") val calculationHash: String
)

data class ActivityRuleResult(
    @SerializedName("rule_id") val ruleId: String,
    @SerializedName("factor_name") val factorName: String,
    @SerializedName("rule_category") val ruleCategory: String,
    val status: String,
    @SerializedName("is_hard_exclusion") val isHardExclusion: Boolean,
    val description: String
)

data class MuhurtaEvaluation(
    @SerializedName("activity_name") val activityName: String,
    @SerializedName("datetime_iso") val datetimeIso: String,
    val recommendation: String,
    @SerializedName("is_rahu_kalam_active") val isRahuKalamActive: Boolean,
    @SerializedName("is_abhijit_active") val isAbhijitActive: Boolean,
    @SerializedName("has_hard_exclusion") val hasHardExclusion: Boolean,
    @SerializedName("favorable_factor_count") val favorableFactorCount: Int,
    @SerializedName("unfavorable_factor_count") val unfavorableFactorCount: Int,
    @SerializedName("evaluated_factors") val evaluatedFactors: List<ActivityRuleResult>,
    val summary: String,
    @SerializedName("calculation_hash") val calculationHash: String
)

data class MuhurtaSuiteResult(
    @SerializedName("panchanga_hash") val panchangaHash: String,
    @SerializedName("datetime_iso") val datetimeIso: String,
    val evaluations: Map<String, MuhurtaEvaluation>,
    @SerializedName("calculation_hash") val calculationHash: String
)

data class TimingSuiteResult(
    @SerializedName("chart_hash") val chartHash: String,
    @SerializedName("query_datetime_iso") val queryDatetimeIso: String?,
    @SerializedName("evidence_status") val evidenceStatus: String,
    @SerializedName("active_mahadasha") val activeMahadasha: String,
    @SerializedName("active_antardasha") val activeAntardasha: String?,
    @SerializedName("ruleset_version") val rulesetVersion: String,
    @SerializedName("timing_windows") val timingWindows: List<TimingWindow> = emptyList(),
    @SerializedName("calculation_hash") val calculationHash: String
)

data class TransitPlacement(
    @SerializedName("planet_name") val planetName: String? = null,
    @SerializedName("sidereal_longitude") val siderealLongitude: Double,
    val rashi: RashiPosition,
    @SerializedName("house_from_lagna") val houseFromLagna: Int,
    @SerializedName("house_from_moon") val houseFromMoon: Int,
    val retrograde: Boolean
)

data class TransitSnapshot(
    @SerializedName("query_datetime_iso") val queryDatetimeIso: String,
    val placements: Map<String, TransitPlacement>,
    @SerializedName("calculation_hash") val calculationHash: String
)

data class DomainRuleDefinition(
    @SerializedName("domain_code") val domainCode: String,
    @SerializedName("domain_title") val domainTitle: String,
    @SerializedName("primary_karakas") val primaryKarakas: List<String>,
    @SerializedName("relevant_houses") val relevantHouses: List<Int>,
    @SerializedName("varga_code") val vargaCode: String,
    @SerializedName("rule_description") val ruleDescription: String
)

data class ObservedChartEvidence(
    @SerializedName("varga_evidence") val vargaEvidence: VargaDomainEvidence?,
    @SerializedName("detected_yogas") val detectedYogas: List<String> = emptyList(),
    @SerializedName("detected_doshas") val detectedDoshas: List<String> = emptyList(),
    @SerializedName("active_dasha_summary") val activeDashaSummary: String?,
    @SerializedName("active_transits_summary") val activeTransitsSummary: String?,
    @SerializedName("shadbala_domain_evidence") val shadbalaDomainEvidence: DomainStrengthEvidence?,
    @SerializedName("ashtakavarga_house_evidences") val ashtakavargaHouseEvidences: List<HouseSAVEvidence> = emptyList(),
    @SerializedName("jaimini_atmakaraka_info") val jaiminiAtmakarakaInfo: CharaKarakaInfo?,
    @SerializedName("jaimini_amatyakaraka_info") val jaiminiAmatyakarakaInfo: CharaKarakaInfo?,
    @SerializedName("jaimini_darakaraka_info") val jaiminiDarakarakaInfo: CharaKarakaInfo?,
    @SerializedName("timing_windows") val timingWindows: List<TimingWindow> = emptyList()
)

data class DomainPredictionEvidence(
    @SerializedName("rule_definition") val ruleDefinition: DomainRuleDefinition,
    @SerializedName("observed_evidence") val observedEvidence: ObservedChartEvidence,
    @SerializedName("evidence_status") val evidenceStatus: String,
    @SerializedName("evidence_strength_class") val evidenceStrengthClass: String?,
    @SerializedName("traditional_metadata") val traditionalMetadata: Map<String, String>
)

data class ComprehensivePredictionPackage(
    @SerializedName("master_evidence_hash") val masterEvidenceHash: String,
    @SerializedName("ruleset_version") val rulesetVersion: String,
    @SerializedName("domain_predictions") val domainPredictions: Map<String, DomainPredictionEvidence>,
    @SerializedName("active_dasha_summary") val activeDashaSummary: String?,
    @SerializedName("calculation_hash") val calculationHash: String
)

data class AIInterpretationResponse(
    val domain: String,
    val interpretation: String,
    @SerializedName("validation_status") val validationStatus: String
)
