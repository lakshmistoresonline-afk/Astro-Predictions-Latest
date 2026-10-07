import React from 'react'

interface KundaliAstrolabeProps {
  svgChart: string | null
}

export const KundaliAstrolabe: React.FC<KundaliAstrolabeProps> = ({ svgChart }) => {
  return (
    <div className="bg-[#17163A]/90 p-8 md:p-12 rounded-3xl border border-[#F3E5AB]/30 shadow-2xl space-y-6 w-full max-w-2xl mx-auto">
      <h2 className="text-2xl md:text-3xl font-extrabold text-[#F3E5AB] text-center">
        North Indian Kundali Astrolabe
      </h2>
      {svgChart ? (
        <div
          dangerouslySetInnerHTML={{ __html: svgChart }}
          className="p-4 bg-black/40 rounded-2xl border border-[#F3E5AB]/20 flex justify-center items-center overflow-hidden"
        />
      ) : (
        <div className="bg-[#050816] p-12 rounded-2xl border border-[#F3E5AB]/20 text-center">
          <p className="text-sm text-[#A0A5C0]">Kundali SVG Chart Unavailable</p>
        </div>
      )}
    </div>
  )
}
