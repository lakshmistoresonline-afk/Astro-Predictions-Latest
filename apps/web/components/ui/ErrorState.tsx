import React from 'react'

interface ErrorStateProps {
  title?: string
  message: string
  onRetry?: () => void
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = 'Calculation Error',
  message,
  onRetry
}) => {
  return (
    <div className="bg-rose-950/80 border border-rose-500/50 p-6 rounded-2xl text-rose-200 space-y-3 max-w-2xl mx-auto shadow-2xl">
      <h4 className="font-bold text-lg text-rose-100 flex items-center gap-2">
        <span>⚠</span> {title}
      </h4>
      <p className="text-sm leading-relaxed">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-2 bg-rose-500/30 hover:bg-rose-500/40 text-rose-100 font-bold px-4 py-2 rounded-xl text-xs transition"
        >
          Retry Request →
        </button>
      )}
    </div>
  )
}
