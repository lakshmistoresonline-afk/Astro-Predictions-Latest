# Astrovision Android Feature-by-Feature Verification Specification

## 1. Feature Verification Matrix

| Screen Feature | Backend API Endpoint | Primary Data Model | Null / Unavailable Handling | Component View |
| :--- | :--- | :--- | :--- | :--- |
| **Birth Profile Entry** | `/api/v1/birth-profile` | `BirthProfileRequest` | Validation error message displayed | `BirthProfileFormScreen` |
| **Dashboard Overview** | `/api/v1/birth-profile` | `BirthProfileResponse` | Displays "Unavailable" text for missing fields | `DashboardOverview` |
| **Kundali Astrolabe** | `/api/v1/birth-profile` | `svg_chart: String?` | Renders "Kundali Chart SVG Unavailable" if null | `KundaliChartView` |
| **Planetary Positions**| `/api/v1/birth-profile` | `CanonicalVedicChart` | Renders "Planetary placements unavailable" | `PlanetaryPositionsView` |
| **16 Vargas Suite** | `/api/v1/birth-profile` | `Full16VargaSuite` | Renders "16 Vargas suite evidence unavailable" | `VargasView` |
| **Vimshottari Dashas** | `/api/v1/birth-profile` | `FullVimshottariDashaResult` | Renders "Dasha timeline evidence unavailable" | `DashasView` |
| **Yogas & Doshas** | `/api/v1/birth-profile` | `YogaSuiteResult`, `DoshaSuiteResult` | Renders "No classical Yogas/Doshas detected" | `YogasDoshasView` |
| **Shadbala & SAV** | `/api/v1/birth-profile` | `ShadbalaSuiteResult`, `AshtakavargaPredictiveEvidence` | Renders "Shadbala/SAV evidence unavailable" | `ShadbalaAshtakavargaView` |
| **Jaimini Sutras** | `/api/v1/jaimini` | `JaiminiSuiteResult` | Renders "Jaimini suite evidence unavailable" | `JaiminiView` |
| **Panchanga & Muhurta**| `/api/v1/panchanga`, `/api/v1/muhurta` | `PanchangaResult`, `MuhurtaSuiteResult` | Renders "Panchanga/Muhurta evidence unavailable" | `PanchangaMuhurtaView` |
| **Domain Predictions** | `/api/v1/birth-profile` | `ComprehensivePredictionPackage` | Renders "Domain predictions unavailable" | `PredictionsView` |
| **AI Interpretation** | `/api/v1/interpret-evidence` | `AIInterpretationResponse` | Displays explicit service error banner | `AiInterpretationView` |

## 2. Verification Criteria
1. **Zero Hardcoded Values**: All displayed astrological signs, degrees, Nakshatras, Padas, Dashas, Vargas, Yogas, and Muhurtas are derived 100% from live backend API response payloads.
2. **Zero Fabricated Fallbacks**: Missing evidence fields render as explicit `"Unavailable"` text rather than fake signs or sample numbers.
3. **UI States**:
   - `Loading`: Displays full-screen loading dialog with progress indicator and step message (`AstrovisionUiState.Loading`).
   - `Error`: Displays error banner with user-friendly error message and retry button (`AstrovisionUiState.Error`).
   - `Success`: Renders live calculated evidence package.
4. **Environment Build Types**:
   - `debug`: `BuildConfig.BASE_URL = "http://10.0.2.2:8000/"` (Emulator local host) with HTTP basic logging.
   - `release`: `BuildConfig.BASE_URL = "https://api.astrovision.io/"` with HTTP logging disabled to protect user privacy.
