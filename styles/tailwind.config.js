/** @type {import('tailwindcss').Config} */
export default {
  content: ["../src/marimo_utils/**/*.py", "../nbs/**/*.py"],
  corePlugins: {
    preflight: false,
  },
  theme: {
    extend: {
      width: {
        100: "25rem",
        160: "40rem",
      },
    },
  },
  // Classes must appear as literal strings under content paths (src/, nbs/).
  // Dynamic klass= overrides are not compiled unless added there or safelisted.
  plugins: [],
};
