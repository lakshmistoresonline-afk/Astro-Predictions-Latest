import React from 'react'

interface UnavailableStateProps {
  title?: string
  description?: string
}

export const UnavailableState: React.FC<UnavailableStateProps> = ({
  title = 'Evidence Unavailable',
  description = 'Deterministic server-side evidence is not available for this component.'
}) => {
  return (
    <div className="bg-[#17163A]/60 border border-[#F3E5AB]/20 p-8 rounded-2xl text-center space-y-3 max-w-lg mx-auto">
      <span className="text-2xl text-[#A0A5C0]">✦</span>
      <h4 className="font-bold text-base text-[#F3E5AB]">{title}</h4>
      <p className="text-xs text-[#A0A5C0] leading-relaxed">{description}</p>
    </div>
  )
}
