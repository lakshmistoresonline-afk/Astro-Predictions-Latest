# Astrovision Calculation Architecture

## 1. Pipeline Flow
```
User Input (DOB, Time, Place)
  ↓
BirthDataEngine (Timezone, UTC, Julian Day)
  ↓
AstronomicalEngine (Meeus Ephemeris & Lahiri Ayanamsha)
  ↓
VedicEngine / HouseEngine (Sidereal Rashi, Lagna, Houses)
  ↓
DashaEngine (Vimshottari with Birth Nakshatra Balance)
  ↓
MasterworkEngine (Divisional Vargas D1-D60, Shadbala, Ashtakavarga)
  ↓
YogaEngine & DoshaEngine (Rule Registries)
  ↓
PredictionEngine & EvidenceAggregator (Domain Evidence)
  ↓
ReportGeneratorEngine (Canonical Report JSON Schema)
  ↓
AI Service (Ollama Local Interpretation & Validation)
  ↓
User-Scoped Storage & UI Rendering
```
