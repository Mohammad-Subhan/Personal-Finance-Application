/** @type {import('tailwindcss').Config} */
module.exports = {
	darkMode: ["class"],
	content: ["./index.html", "./src/**/*.{ts,tsx,js,jsx}"],
	theme: {
		extend: {
			borderRadius: {
				lg: 'var(--radius)',
				md: 'calc(var(--radius) - 2px)',
				sm: 'calc(var(--radius) - 4px)'
			},
			colors: {
				background: "var(--background)",
				text: "var(--text)",
				primary: "var(--primary)",
				primaryAccent: "var(--primary-accent)",
				primaryHover: "var(--primary-hover)",
			}
		}
	},
	plugins: [require("tailwindcss-animate")],
}
