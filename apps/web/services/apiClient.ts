import {
  BirthProfileRequest,
  BirthProfileResponse,
  AIInterpretationResponse
} from '../types/api'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

let authToken: string | null = null

export function setAuthToken(token: string | null) {
  authToken = token
}

function getAuthHeaders(): Record<string, string> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json'
  }
  if (authToken) {
    headers['Authorization'] = `Bearer ${authToken}`
  }
  return headers
}

export async function calculateBirthProfile(
  request: BirthProfileRequest
): Promise<BirthProfileResponse> {
  const res = await fetch(`${API_BASE}/api/v1/birth-profile`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(request)
  })

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}))
    throw new Error(errorData.detail || `Birth profile calculation failed (HTTP ${res.status}).`)
  }

  return res.json()
}

export async function interpretEvidenceAi(
  birthInput: BirthProfileRequest,
  domain: string,
  prompt: string = 'Explain domain predictions'
): Promise<AIInterpretationResponse> {
  const res = await fetch(`${API_BASE}/api/v1/interpret-evidence`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({
      birth_input: birthInput,
      domain,
      prompt
    })
  })

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}))
    throw new Error(errorData.detail || `AI interpretation failed (HTTP ${res.status}).`)
  }

  return res.json()
}
