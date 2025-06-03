/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}"
  ],
  theme: {
    extend: {
      keyframes: {
        "bg-pan": {
          "0%": { "background-position": "0% 50%" },
          "50%": { "background-position": "100% 50%" },
          "100%": { "background-position": "0% 50%" }
        }
      },
      animation: {
        "bg-pan": "bg-pan 20s ease infinite"
      }
    }
  },
  plugins: []
};
