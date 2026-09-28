# Phase 1C Licensing Analysis ("Astrovision")

| Provider | Library License | Ephemeris Data License | Commercial SaaS Implications | Binary Dependency | Source Disclosure |
|---|---|---|---|---|---|
| Swiss Ephemeris (`pyswisseph`) | GPL / AGPL | Free / Proprietary Dual | High (Requires commercial license for closed-source SaaS) | Yes (C Extension) | Required under GPL/AGPL unless commercial license purchased |
| Skyfield (`skyfield`) | MIT | JPL Public Domain | Low (Permissive) | No (Pure Python + Data file) | Not required |
| Candidate C (Meeus) | MIT / PSF | Public Domain | Low (Permissive) | No (Pure Python) | Not required |
