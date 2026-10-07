import React from 'react'

interface LoadingStateProps {
  stepMessage?: string
}

export const LoadingState: React.FC<LoadingStateProps> = ({ stepMessage }) => {
  return (
    <div className="fixed inset-0 bg-[#050816]/95 backdrop-blur-2xl z-50 flex flex-col items-center justify-center p-8 space-y-8">
      <div className="relative w-32 h-32 flex items-center justify-center">
        <div className="absolute inset-0 rounded-full border-4 border-[#F3E5AB]/20 border-t-[#F3E5AB] animate-spin"></div>
        <div className="text-4xl text-[#F3E5AB] animate-pulse">✦</div>
      </div>
      <div className="text-center space-y-3 max-w-md">
        <h3 className="text-2xl font-extrabold text-[#F3E5AB]">Calculating Ephemeris State</h3>
        {stepMessage && (
          <p className="text-sm text-[#A0A5C0]">{stepMessage}</p>
        )}
      </div>
    </div>
  )
}
