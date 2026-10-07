# Astrovision /api/v1 Canonical API Contract Specification

## 1. Overview
Astrovision Version 6.0.0 exposes a versioned `/api/v1` REST contract backed by FastAPI and Pydantic v2.

- **OpenAPI Schema**: Machine-readable OpenAPI 3.0 specification served live at `/openapi.json`.
- **System Architecture**:
  `Client Request → FastAPI Pydantic Validation → CanonicalEvidencePipeline → PredictionEngine → Output Response`

## 2. Configurable Fields & Governance
- **`zodiac_system`**: Supported values: `'sidereal'` (Vedic Lahiri) or `'tropical'` (Western). Defaults to `'sidereal'`.
- **`ayanamsha`**: Supported values: `'lahiri'` (Chitra Paksha Ayanamsha). Defaults to `'lahiri'`.
- **`timezone_str`**: Authoritative IANA timezone key (e.g. `'Asia/Kolkata'`, `'Europe/London'`, `'America/New_York'`). Mandatory.

## 3. Endpoint Catalog

### `POST /api/v1/birth-profile`
Calculates master canonical astrology evidence, domain predictions, SVG North Indian chart, and comprehensive report.
- **Request Body**: `BirthProfileRequest`
- **Response**: `BirthProfileResponse` (`status`, `birth_input`, `master_evidence`, `predictions`, `svg_chart`, `report`)

### `POST /api/v1/transits`
Calculates transit snapshot at `query_datetime_iso` relative to natal chart.
- **Request Body**: `TransitRequest`
- **Response**: `TransitSnapshot`

### `POST /api/v1/panchanga`
Calculates exact Panchanga and solar timing windows for observer location.
- **Request Body**: `TransitRequest`
- **Response**: `PanchangaResult`

### `POST /api/v1/muhurta`
Evaluates Panchanga suitability and hard exclusions for all 6 major activities.
- **Request Body**: `TransitRequest`
- **Response**: `MuhurtaSuiteResult`

### `POST /api/v1/jaimini`
Calculates 7 Chara Karakas, Arudha Lagna, Upapada Lagna, Karakamsha, and Rashi aspects.
- **Request Body**: `BirthProfileRequest`
- **Response**: `JaiminiSuiteResult`

### `POST /api/v1/timing-windows`
Calculates convergent predictive timing windows across domains.
- **Request Body**: `TransitRequest`
- **Response**: `TimingSuiteResult`

### `POST /api/v1/interpret-evidence`
Server-owned AI evidence synthesis. Client prompt acts strictly as an interpretation topic query.
- **Request Body**: `AIInterpretationRequest`
- **Response**: `AIInterpretationResponse` (`domain`, `interpretation`, `validation_status`)

### `POST /api/v1/compatibility`
Computes 36-point Vedic Ashtakoota compatibility matching.
- **Request Body**: `CompatibilityRequest`
- **Response**: `AshtakootaResult`

### `POST /api/v1/rectification`
Evaluates birth time candidate offsets against life events.
- **Request Body**: `RectificationApiRequest`
- **Response**: `RectificationResult`

### `POST /api/v1/export/pdf`
Exports PDF report artifact.
- **Request Body**: `ExportPDFRequest`
- **Response**: `application/pdf` HTML/PDF content stream

## 4. Structured Error Response Shape
All error responses return a structured JSON shape:
```json
{
  "detail": "Error message explanation",
  "error_code": "HTTP_ERROR_400",
  "timestamp_iso": "2026-10-06T19:15:00.000000+00:00"
}
```
