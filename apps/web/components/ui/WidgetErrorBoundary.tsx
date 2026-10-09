import React, { Component, ErrorInfo, ReactNode } from 'react'

interface Props {
  children: ReactNode
  title?: string
}

interface State {
  hasError: boolean
  error: Error | null
}

export class WidgetErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('WidgetErrorBoundary caught an error:', error, errorInfo)
  }

  public handleRetry = () => {
    this.setState({ hasError: false, error: null })
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="p-6 rounded-2xl bg-red-950/20 border border-red-500/30 backdrop-blur-md space-y-3 my-4">
          <div className="flex items-center gap-2 text-red-400 font-semibold text-sm">
            <svg className="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{this.props.title || 'Widget Component Error'}</span>
          </div>
          <p className="text-xs text-slate-400 font-mono">
            {this.state.error?.message || 'An unexpected rendering error occurred in this dashboard module.'}
          </p>
          <button
            onClick={this.handleRetry}
            className="px-3 py-1.5 rounded-lg bg-red-500/20 hover:bg-red-500/30 border border-red-500/40 text-red-300 text-xs font-medium transition duration-150"
          >
            Retry Component
          </button>
        </div>
      )
    }

    return this.props.children
  }
}
