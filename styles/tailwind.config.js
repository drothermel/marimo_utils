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
  // Literal classes under content paths (src/, nbs/) are compiled automatically.
  // Safelist common runtime klass= overrides documented for notebook users.
  safelist: ["ring-2", "ring-ring", "ring-offset-2", "text-lg"],
  plugins: [],
};
