import React, { useState, useEffect } from 'react'
import { BirthProfileRequest } from '../../types/api'
import { fetchGemstoneMatrix } from '../../services/apiClient'

interface GemstonePariharaViewProps {
  birthInput?: BirthProfileRequest | null
}

export const GemstonePariharaView: React.FC<GemstonePariharaViewProps> = ({ birthInput }) => {
  const [loading, setLoading] = useState(false)
  const [gemstoneData, setGemstoneData] = useState<any>(null)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)
  const [filterClass, setFilterClass] = useState<string>('ALL')

  const handleLoadGemstones = async () => {
    if (!birthInput) return
    setLoading(true)
    setErrorMsg(null)
    try {
      const data = await fetchGemstoneMatrix(birthInput)
      setGemstoneData(data)
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to calculate Gemstone Dignity Matrix.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (birthInput) {
      handleLoadGemstones()
    }
  }, [birthInput])

  if (!birthInput) {
    return (
      <div className="bg-slate-900/80 backdrop-blur-xl p-8 rounded-3xl border border-slate-800 text-center space-y-4 font-mono select-none">
        <span className="text-3xl text-amber-300">💎</span>
        <h3 className="text-xl font-bold text-amber-300">Gemstone Safety & Dignity Matrix</h3>
        <p className="text-slate-400 text-xs">Please calculate a birth profile first to view gemstone suitabilities.</p>
      </div>
    )
  }

  const recommendations = gemstoneData?.recommendations || []
  const filteredRecs = recommendations.filter((r: any) => {
    if (filterClass === 'ALL') return true
    return r.suitability_class === filterClass
  })

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl p-6 md:p-8 rounded-3xl border border-slate-800/80 shadow-2xl space-y-6 w-full select-none font-mono">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-xl font-extrabold text-amber-300 flex items-center gap-2 font-serif-heading">
            <span>💎</span> Gemstone Safety & Dignity Matrix (Anukuul Protocol)
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Parashari Lagna Lord vs. Maraka/Badhaka Lord Gemstone Suitability Checks
          </p>
        </div>

        {/* Filter Buttons */}
        <div className="flex bg-slate-950 p-1 rounded-xl border border-slate-800 text-xs">
          <button
            onClick={() => setFilterClass('ALL')}
            className={`px-3 py-1.5 rounded-lg transition cursor-pointer ${filterClass === 'ALL' ? 'bg-amber-500/20 text-amber-300 font-bold border border-amber-500/40' : 'text-slate-400 hover:text-white'}`}
          >
            All Planets ({recommendations.length})
          </button>
          <button
            onClick={() => setFilterClass('RECOMMENDED')}
            className={`px-3 py-1.5 rounded-lg transition cursor-pointer ${filterClass === 'RECOMMENDED' ? 'bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/40' : 'text-slate-400 hover:text-white'}`}
          >
            Recommended
          </button>
          <button
            onClick={() => setFilterClass('STRICTLY_FORBIDDEN')}
            className={`px-3 py-1.5 rounded-lg transition cursor-pointer ${filterClass === 'STRICTLY_FORBIDDEN' ? 'bg-rose-500/20 text-rose-300 font-bold border border-rose-500/40' : 'text-slate-400 hover:text-white'}`}
          >
            Forbidden
          </button>
        </div>
      </div>

      {loading ? (
        <div className="p-8 text-center bg-slate-950/40 rounded-2xl border border-slate-800 text-xs text-amber-300 animate-pulse">
          Evaluating Lagna Lord and Maraka/Badhaka Gemstone Suitabilities...
        </div>
      ) : errorMsg ? (
        <div className="p-4 bg-rose-500/10 border border-rose-500/30 text-rose-300 rounded-2xl text-xs">
          {errorMsg}
        </div>
      ) : gemstoneData ? (
        <div className="space-y-6">
          <div className="p-4 rounded-2xl bg-slate-950/60 border border-amber-500/30 flex flex-wrap justify-between items-center gap-4 text-xs">
            <div>
              <span className="text-slate-400 block text-[10px] uppercase">Natal Ascendant (Lagna)</span>
              <strong className="text-amber-300 text-base">{gemstoneData.lagna_sign} Lagna</strong>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase">Lagna Lord (1st House)</span>
              <strong className="text-cyan-300 text-base">{gemstoneData.lagna_lord}</strong>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase">Safety Protocol</span>
              <strong className="text-emerald-300 text-xs font-bold">100% Non-Malefic Enforcement</strong>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredRecs.map((r: any) => {
              const isRec = r.suitability_class === 'RECOMMENDED'
              const isForb = r.suitability_class === 'STRICTLY_FORBIDDEN'

              return (
                <div
                  key={r.planet}
                  className={`p-5 rounded-2xl bg-slate-950/60 border space-y-3 shadow-lg transition ${
                    isRec
                      ? 'border-emerald-500/40 hover:border-emerald-500/80'
                      : isForb
                      ? 'border-rose-500/40 hover:border-rose-500/80'
                      : 'border-amber-500/30 hover:border-amber-500/60'
                  }`}
                >
                  <div className="flex items-center justify-between gap-2 border-b border-slate-800 pb-3">
                    <div>
                      <h4 className="font-bold text-slate-100 text-base flex items-center gap-2">
                        <span>{r.planet}</span>
                        <span className="text-xs text-slate-400 font-normal">({r.lordship_role})</span>
                      </h4>
                      <p className="text-xs font-bold text-amber-300 mt-0.5">{r.gemstone_name}</p>
                    </div>
                    <span className={`text-[10px] px-2.5 py-1 rounded-full font-bold border shrink-0 ${
                      isRec
                        ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                        : isForb
                        ? 'bg-rose-500/20 text-rose-300 border-rose-500/40'
                        : 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                    }`}>
                      {r.suitability_class}
                    </span>
                  </div>

                  <p className="text-xs text-slate-300 font-sans leading-relaxed">
                    {r.rationale}
                  </p>

                  <div className="pt-2 grid grid-cols-3 gap-2 text-[11px] text-slate-400 border-t border-slate-800/60">
                    <div>
                      <span className="text-slate-500 block text-[10px]">Substitute</span>
                      <span className="text-slate-200">{r.substitute}</span>
                    </div>
                    <div>
                      <span className="text-slate-500 block text-[10px]">Metal</span>
                      <span className="text-cyan-300">{r.suitable_metal}</span>
                    </div>
                    <div>
                      <span className="text-slate-500 block text-[10px]">Finger</span>
                      <span className="text-amber-200">{r.wearing_finger}</span>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      ) : null}
    </div>
  )
}
