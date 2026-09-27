# Source of Truth Audit ("Astrovision")

## 1. Repository & Git Status
- **Local Repository Path**: `D:/Astro Predictions`
- **Remote URL**: `https://github.com/lakshmistoresonline-afk/Astro-Predictions-Latest.git`
- **Local Branch**: `main`
- **Local HEAD**: `5aa3e8c78970f92b2ecdce7b0ac5e004571a0491`
- **Origin/Main SHA**: `5aa3e8c78970f92b2ecdce7b0ac5e004571a0491`
- **Status**: Up to date with origin/main.

## 2. Runtime Identity
- **Frontend Entrypoint**: `apps/web/app/page.tsx` & `apps/web/app/layout.tsx`
- **Start Command**: `npm run dev -p 3000` (in `apps/web`)
- **Root Cause of Mismatch**: Stale Next.js compilation cache in `.next/` serving pre-compiled server pages from previous test iterations. Resolved by clearing `.next/` and restarting the dev process.
