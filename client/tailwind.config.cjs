/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    minHeight: {
      '1/2': '50%',
    },
    extend: {
      fontFamily: {
        squadaOne: ['Squada One', 'cursive'],
        work: ['Work Sans', 'sans-serif']
      },
      colors: {
        'error': '#ec155e',
        'error50': '#c02b5a',
        'accent': '#008b2a',
        'primary': '#f2f2f2',
        'accent50': '#74a183',
        'grey0': '#9dabb4'
      }
    },
  },
  plugins: [],
  safelist: [
    'list-decimal',
    'w-1',
    'w-2',
    'w-3',
    '!bg-transparent',
    'flipped-x',
    'flipped-x-y',
    'flipped-y',
  ]
}
