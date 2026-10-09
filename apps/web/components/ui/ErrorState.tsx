import React from 'react'

interface ErrorStateProps {
  title?: string
  message: string
  onRetry?: () => void
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = 'Calculation Exception',
  message,
  onRetry
}) => {
  return (
    <div className="bg-rose-950/40 border border-rose-500/40 p-6 rounded-2xl text-rose-200 space-y-3 max-w-2xl mx-auto backdrop-blur-md shadow-2xl">
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-rose-500/20 border border-rose-500/40 flex items-center justify-center text-rose-400 font-bold shrink-0">
          !
        </div>
        <div>
          <h4 className="font-bold text-base text-rose-100">{title}</h4>
          <p className="text-xs font-mono text-rose-300/80 leading-relaxed mt-1">{message}</p>
        </div>
      </div>
      {onRetry && (
        <div className="pt-2 flex justify-end">
          <button
            onClick={onRetry}
            className="bg-rose-500/20 hover:bg-rose-500/30 border border-rose-500/40 text-rose-100 font-semibold px-4 py-2 rounded-xl text-xs transition duration-150 flex items-center gap-2"
          >
            <span>↻</span> Retry Operation
          </button>
        </div>
      )}
    </div>
  )
}
