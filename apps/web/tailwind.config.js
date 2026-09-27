/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        midnight: "#050816",
        deepnavy: "#080D1F",
        cosmicnavy: "#0B1026",
        indigo: "#17163A",
        purple: "#29204F",
        champagne: "#D6B36A",
        lightgold: "#F0D898",
        ivory: "#F7F3EA",
        mutedtext: "#A7A9B7",
        success: "#5BC98A",
        warning: "#E7B95E",
        error: "#D86C78",
      },
    },
  },
  plugins: [],
}
