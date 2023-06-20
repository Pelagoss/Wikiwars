/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        squadaOne: ['Squada One', 'cursive'],
        work: ['Work Sans', 'sans-serif']
      },
      colors: {
        'accent': '#008b2a',
        'grey0': '#9dabb4'
      }
    },
  },
  plugins: [],
}
