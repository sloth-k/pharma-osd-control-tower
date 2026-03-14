/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,jsx}",
    "./components/**/*.{js,jsx}",
    "./charts/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#0f172a",
        mist: "#e2e8f0",
        signal: {
          green: "#14b8a6",
          amber: "#f59e0b",
          red: "#ef4444",
          blue: "#0284c7"
        }
      },
      fontFamily: {
        sans: ["ui-sans-serif", "system-ui", "sans-serif"]
      },
      boxShadow: {
        panel: "0 18px 45px rgba(15, 23, 42, 0.10)"
      }
    },
  },
  plugins: [],
};
