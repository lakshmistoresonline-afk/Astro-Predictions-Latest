export type SupportedLanguage = 'en' | 'hi' | 'sa'

export interface TranslationDictionary {
  planets: Record<string, string>
  rashis: Record<string, string>
  ui: Record<string, string>
}

export const TRANSLATIONS: Record<SupportedLanguage, TranslationDictionary> = {
  en: {
    planets: {
      Sun: "Sun", Moon: "Moon", Mars: "Mars", Mercury: "Mercury",
      Jupiter: "Jupiter", Venus: "Venus", Saturn: "Saturn", Rahu: "Rahu", Ketu: "Ketu", Ascendant: "Ascendant"
    },
    rashis: {
      Aries: "Aries", Taurus: "Taurus", Gemini: "Gemini", Cancer: "Cancer",
      Leo: "Leo", Virgo: "Virgo", Libra: "Libra", Scorpio: "Scorpio",
      Sagittarius: "Sagittarius", Capricorn: "Capricorn", Aquarius: "Aquarius", Pisces: "Pisces"
    },
    ui: {
      app_title: "Astrovision",
      dashboard: "Dashboard Overview",
      birth_profile: "Birth Profile Form",
      kundli: "Kundli & Astrology",
      planets: "Planetary Positions",
      vargas: "16 Vargas Atlas",
      dashas: "Vimshottari Dashas",
      yogas: "Yogas & Doshas",
      strength: "Shadbala & SAV",
      jaimini: "Jaimini Sutras",
      panchanga: "Panchanga & Muhurta",
      compatibility: "36-Pt Compatibility",
      rectification: "Birth Time Rectification",
      digest: "Weekly Transit Digest",
      predictions: "14 Domain Predictions",
      ai: "AI Evidence Synthesis",
      export_pdf: "Export PDF Treatise",
      export_json: "Gold Standard JSON",
      new_profile: "New Birth Profile"
    }
  },
  hi: {
    planets: {
      Sun: "सूर्य (Surya)", Moon: "चन्द्र (Chandra)", Mars: "मंगल (Mangala)", Mercury: "बुध (Budha)",
      Jupiter: "गुरु (Guru)", Venus: "शुक्र (Shukra)", Saturn: "शनि (Shani)", Rahu: "राहु (Rahu)", Ketu: "केतु (Ketu)", Ascendant: "लग्न (Lagna)"
    },
    rashis: {
      Aries: "मेष (Mesha)", Taurus: "वृषभ (Vrishabha)", Gemini: "मिथुन (Mithuna)", Cancer: "कर्क (Karka)",
      Leo: "सिंह (Simha)", Virgo: "कन्या (Kanya)", Libra: "तुला (Tula)", Scorpio: "वृश्चिक (Vrishchika)",
      Sagittarius: "धनु (Dhanu)", Capricorn: "मकर (Makara)", Aquarius: "कुंभ (Kumbha)", Pisces: "मीन (Meena)"
    },
    ui: {
      app_title: "एस्ट्रोविज़न (Astrovision)",
      dashboard: "डैशबोर्ड विवरण",
      birth_profile: "जन्म विवरण फॉर्म",
      kundli: "कुंडली एवं ज्योतिष",
      planets: "ग्रहों की स्थितियां",
      vargas: "16 वर्ग चार्ट",
      dashas: "विंशोत्तरी दशा",
      yogas: "योग एवं दोष",
      strength: "षडबल एवं सर्वाष्टकवर्ग",
      jaimini: "जैमिनी सूत्र",
      panchanga: "पंचांग एवं मुहूर्त",
      compatibility: "36-गुण मिलान",
      rectification: "जन्म समय संशोधन",
      digest: "साप्ताहिक गोचर सार",
      predictions: "14 क्षेत्र भविष्यवाणियां",
      ai: "एआई साक्ष्य विश्लेषण",
      export_pdf: "पीडीएफ रिपोर्ट डाउनलोड",
      export_json: "गोल्ड मानक जेसन",
      new_profile: "नवीन जन्म विवरण"
    }
  },
  sa: {
    planets: {
      Sun: "सूर्यः (Sūryaḥ)", Moon: "चन्द्रः (Candraḥ)", Mars: "मङ्गलः (Maṅgalaḥ)", Mercury: "बुधः (Budhaḥ)",
      Jupiter: "गुरुः (Guruḥ)", Venus: "शुक्रः (Śukraḥ)", Saturn: "शनिः (Śaniḥ)", Rahu: "राहुः (Rāhuḥ)", Ketu: "केतुः (Ketuḥ)", Ascendant: "लग्नम् (Lagnam)"
    },
    rashis: {
      Aries: "मेषः (Meṣaḥ)", Taurus: "वृषभः (Vṛṣabhaḥ)", Gemini: "मिथुनम् (Mithunam)", Cancer: "कर्कः (Karkaḥ)",
      Leo: "सिंहः (Siṁhaḥ)", Virgo: "कन्या (Kanyā)", Libra: "तुला (Tulā)", Scorpio: "वृश्चिकः (Vṛścikaḥ)",
      Sagittarius: "धनुः (Dhanuḥ)", Capricorn: "मकरः (Makaraḥ)", Aquarius: "कुम्भः (Kumbhaḥ)", Pisces: "मीनः (Mīnaḥ)"
    },
    ui: {
      app_title: "एस्ट्रोविज़नम् (Astrovisionam)",
      dashboard: "मुख्यपीठम्",
      birth_profile: "जन्मपत्रम्",
      kundli: "कुण्डली ज्योतिषम्",
      planets: "ग्रहस्थितयः",
      vargas: "षोडशवर्गाः",
      dashas: "विंशोत्तरी दशा",
      yogas: "योगाः दोषाश्च",
      strength: "षड्बलम् अष्टकवर्गश्च",
      jaimini: "जैमिनी सूत्राणि",
      panchanga: "पञ्चाङ्गम् मुहूर्तम",
      compatibility: "अष्टकूट मेलपकम्",
      rectification: "समय संशोधनम्",
      digest: "गोचर विवरणम्",
      predictions: "भविष्यवाणी सङ्ग्रहः",
      ai: "एआई विश्लेषणम्",
      export_pdf: "पीडीएफ निर्यातम्",
      export_json: "जेसन निर्यातम्",
      new_profile: "नवीन पत्रम्"
    }
  }
}
