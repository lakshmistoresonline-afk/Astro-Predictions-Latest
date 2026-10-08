import React, { useState } from 'react'
import { registerUser, loginUser, TokenResponse } from '../../services/apiClient'

interface AuthModalProps {
  isOpen: boolean
  onClose: () => void
  onAuthSuccess: (user: TokenResponse) => void
}

export const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose, onAuthSuccess }) => {
  const [isLoginMode, setIsLoginMode] = useState(true)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [errorMsg, setErrorMsg] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  if (!isOpen) return null

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setErrorMsg('')
    setIsLoading(true)

    try {
      let res: TokenResponse
      if (isLoginMode) {
        res = await loginUser(email, password)
      } else {
        res = await registerUser(email, password, fullName)
      }
      setIsLoading(false)
      onAuthSuccess(res)
      onClose()
    } catch (err: any) {
      setIsLoading(false)
      setErrorMsg(err.message || 'Authentication failed. Check your credentials.')
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-4">
      <div className="bg-[#17163A] border border-[#F3E5AB]/40 rounded-3xl p-8 max-w-md w-full shadow-2xl relative text-[#FFFFF0]">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-[#A0A5C0] hover:text-[#F3E5AB] font-bold text-lg"
        >
          ✕
        </button>

        <h2 className="text-2xl font-extrabold text-[#F3E5AB] mb-2">
          {isLoginMode ? 'Astrovision Sign In' : 'Create Account'}
        </h2>
        <p className="text-xs text-[#A0A5C0] mb-6">
          {isLoginMode
            ? 'Access saved birth profiles, reports, and persistent chart history.'
            : 'Register your account to unlock persistent chart storage and PDF reports.'}
        </p>

        {errorMsg && (
          <div className="p-3 mb-4 bg-red-900/40 border border-red-500/50 rounded-xl text-red-200 text-xs">
            {errorMsg}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLoginMode && (
            <div>
              <label className="block text-xs font-semibold text-[#A0A5C0] mb-1">Full Name</label>
              <input
                type="text"
                value={fullName}
                onChange={e => setFullName(e.target.value)}
                className="w-full bg-[#050816] border border-[#F3E5AB]/30 rounded-xl p-3 text-sm text-[#FFFFF0] outline-none focus:border-[#F3E5AB]"
                required
              />
            </div>
          )}

          <div>
            <label className="block text-xs font-semibold text-[#A0A5C0] mb-1">Email Address</label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              className="w-full bg-[#050816] border border-[#F3E5AB]/30 rounded-xl p-3 text-sm text-[#FFFFF0] outline-none focus:border-[#F3E5AB]"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-[#A0A5C0] mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              className="w-full bg-[#050816] border border-[#F3E5AB]/30 rounded-xl p-3 text-sm text-[#FFFFF0] outline-none focus:border-[#F3E5AB]"
              required
              minLength={8}
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-[#F3E5AB] to-[#F7E792] text-[#050816] font-extrabold py-3.5 rounded-xl shadow-xl hover:opacity-90 transition mt-6 text-sm"
          >
            {isLoading ? 'Processing...' : isLoginMode ? 'Sign In' : 'Create Account'}
          </button>
        </form>

        <div className="mt-6 text-center text-xs text-[#A0A5C0]">
          {isLoginMode ? "Don't have an account? " : 'Already registered? '}
          <button
            type="button"
            onClick={() => {
              setIsLoginMode(!isLoginMode)
              setErrorMsg('')
            }}
            className="text-[#F3E5AB] font-bold underline ml-1"
          >
            {isLoginMode ? 'Register Now' : 'Sign In'}
          </button>
        </div>
      </div>
    </div>
  )
}
