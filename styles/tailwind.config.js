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
  safelist: ["ring-2", "ring-ring", "ring-offset-2", "container"],
  plugins: [],
};
