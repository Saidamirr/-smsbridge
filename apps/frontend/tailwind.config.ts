import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#111827",
        line: "#dbe3ef",
        panel: "#f6f8fb",
        accent: "#2563eb",
        violet: "#6d5dfc",
        cyan: "#0891b2"
      }
    }
  },
  plugins: []
};

export default config;
