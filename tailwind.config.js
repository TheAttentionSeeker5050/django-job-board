// Path: tailwind.config.js
module.exports = {
  content: [ 
    './templates/*.html',
    './**/templates/**/*.html',
    './**/templates/**/**/*.html',
    './static/js/*.js',
    './**/views/*.py',
    './**/views.py',
   ],
  theme: {
    extend: {},
  },
  variants: {},
  plugins: [],
}