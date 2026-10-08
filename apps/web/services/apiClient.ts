import {
  BirthProfileRequest,
  BirthProfileResponse,
  AIInterpretationResponse
} from '../types/api'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

let authToken: string | null = null

export function setAuthToken(token: string | null) {
  authToken = token
  if (typeof window !== 'undefined') {
    if (token) {
      sessionStorage.setItem('astro_jwt_token', token)
    } else {
      sessionStorage.removeItem('astro_jwt_token')
    }
  }
}

export function initAuthTokenFromSession() {
  if (typeof window !== 'undefined') {
    const saved = sessionStorage.getItem('astro_jwt_token')
    if (saved) {
      authToken = saved
    }
  }
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

export interface TokenResponse {
  access_token: string
  token_type: string
  expires_in_hours: number
  user_id: string
  email: string
  full_name: string
}

export interface UserProfileResponse {
  id: string
  email: string
  full_name: string
  created_at: string
}

export async function registerUser(email: string, password: string, fullName: string): Promise<TokenResponse> {
  const res = await fetch(`${API_BASE}/api/v1/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, full_name: fullName })
  })

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}))
    throw new Error(errorData.detail || `Registration failed (HTTP ${res.status}).`)
  }

  const data: TokenResponse = await res.json()
  setAuthToken(data.access_token)
  return data
}

export async function loginUser(email: string, password: string): Promise<TokenResponse> {
  const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  })

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}))
    throw new Error(errorData.detail || `Login failed (HTTP ${res.status}).`)
  }

  const data: TokenResponse = await res.json()
  setAuthToken(data.access_token)
  return data
}

export async function fetchMyProfile(): Promise<UserProfileResponse> {
  initAuthTokenFromSession()
  const res = await fetch(`${API_BASE}/api/v1/auth/me`, {
    method: 'GET',
    headers: getAuthHeaders()
  })

  if (!res.ok) {
    if (res.status === 401) {
      setAuthToken(null)
    }
    const errorData = await res.json().catch(() => ({}))
    throw new Error(errorData.detail || `Failed to load profile (HTTP ${res.status}).`)
  }

  return res.json()
}

export async function calculateBirthProfile(
  request: BirthProfileRequest
): Promise<BirthProfileResponse> {
  initAuthTokenFromSession()
  const res = await fetch(`${API_BASE}/api/v1/birth-profile`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(request)
  })

  if (!res.ok) {
    if (res.status === 401) {
      setAuthToken(null)
    }
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
  initAuthTokenFromSession()
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
    if (res.status === 401) {
      setAuthToken(null)
    }
    const errorData = await res.json().catch(() => ({}))
    throw new Error(errorData.detail || `AI interpretation failed (HTTP ${res.status}).`)
  }

  return res.json()
}
