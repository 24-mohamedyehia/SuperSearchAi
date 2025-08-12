import type { Config } from 'tailwindcss'
import lineClamp from '@tailwindcss/line-clamp'

const config: Config = {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // Standard Tailwind aliases that map to your custom colors
        background: '#ffffff',  // surface-50
        foreground: '#171717',  // neutral-900
        card: '#ffffff',        // surface-50
        'card-foreground': '#171717', // neutral-900
        popover: '#ffffff',     // surface-50
        'popover-foreground': '#171717', // neutral-900
        'muted': '#f4f4f5',     // surface-200
        'muted-foreground': '#737373', // neutral-500
        accent: '#f4f4f5',      // surface-200
        'accent-foreground': '#171717', // neutral-900
        destructive: '#ef4444', // error-500
        border: '#e5e5e5',      // neutral-200
        input: '#e5e5e5',       // neutral-200
        ring: '#0084ff',        // primary-500

        // Primary - Modern Blue (AI Assistant)
        primary: {
          50: '#f0f7ff',
          100: '#e0efff',
          200: '#b8deff',
          300: '#7cc4ff',
          400: '#36a7ff',
          500: '#0084ff',
          600: '#0066cc',
          700: '#004d99',
          800: '#003366',
          900: '#001a33',
          950: '#000d1a',
          DEFAULT: '#0084ff',
        },
        
        // Secondary - Soft Purple (User Messages)
        secondary: {
          50: '#faf8ff',
          100: '#f3f0ff',
          200: '#e6deff',
          300: '#d1c4ff',
          400: '#b399ff',
          500: '#9366ff',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
          950: '#2e1065',
          DEFAULT: '#9366ff',
        },
        
        // Success - Clean Green
        success: {
          50: '#f0fff4',
          100: '#dcffe4',
          200: '#bbffc9',
          300: '#86ff9e',
          400: '#4bff6b',
          500: '#22ff47',
          600: '#16cc38',
          700: '#15993d',
          800: '#166635',
          900: '#14532d',
          950: '#052e16',
          DEFAULT: '#22ff47',
        },
        
        // Warning - Warm Orange
        warning: {
          50: '#fff8f0',
          100: '#ffedd5',
          200: '#fed7aa',
          300: '#fdba74',
          400: '#fb923c',
          500: '#f97316',
          600: '#ea580c',
          700: '#c2410c',
          800: '#9a3412',
          900: '#7c2d12',
          950: '#431407',
          DEFAULT: '#f97316',
        },
        
        // Error - Modern Red
        error: {
          50: '#fef2f2',
          100: '#fee2e2',
          200: '#fecaca',
          300: '#fca5a5',
          400: '#f87171',
          500: '#ef4444',
          600: '#dc2626',
          700: '#b91c1c',
          800: '#991b1b',
          900: '#7f1d1d',
          950: '#450a0a',
          DEFAULT: '#ef4444',
        },
        
        // Neutral - Sophisticated Gray Scale
        neutral: {
          50: '#fafafa',
          100: '#f5f5f5',
          200: '#e5e5e5',
          300: '#d4d4d4',
          400: '#a3a3a3',
          500: '#737373',
          600: '#525252',
          700: '#404040',
          800: '#262626',
          900: '#171717',
          950: '#0a0a0a',
          DEFAULT: '#737373',
        },
        
        // Surface - Clean Background Colors
        surface: {
          50: '#ffffff',
          100: '#fafafa',
          200: '#f4f4f5',
          300: '#e4e4e7',
          400: '#d4d4d8',
          500: '#a1a1aa',
          600: '#71717a',
          700: '#52525b',
          800: '#27272a',
          900: '#18181b',
          950: '#09090b',
          DEFAULT: '#f4f4f5',
        },
        
        // Chat specific colors
        chat: {
          user: '#9366ff',      // Secondary default
          assistant: '#0084ff', // Primary default
          system: '#737373',    // Neutral default
          background: '#ffffff',
          sidebar: '#fafafa',
          border: '#e5e5e5',
          hover: '#f4f4f5',
          focus: '#e0efff',
        }
      },
      
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['SF Mono', 'Monaco', 'Cascadia Code', 'Roboto Mono', 'Courier New', 'monospace'],
      },
      
      borderRadius: {
        'none': '0',
        'sm': '0.25rem',
        'md': '0.375rem',
        'lg': '0.5rem',
        'xl': '0.75rem',
        '2xl': '1rem',
        '3xl': '1.5rem',
        'full': '9999px',
      },
      
      boxShadow: {
        'xs': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
        'sm': '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
        'md': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
        'lg': '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
        'xl': '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
        '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
        'chat': '0 2px 8px 0 rgb(0 0 0 / 0.1)',
        'message': '0 1px 3px 0 rgb(0 0 0 / 0.1)',
        'sidebar': 'inset -1px 0 0 rgb(0 0 0 / 0.1)',
      },
      
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'typing': 'typing 1.5s infinite',
      },
      
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        typing: {
          '0%, 60%': { opacity: '1' },
          '30%': { opacity: '0' },
        },
      },
      
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem',
        '88': '22rem',
        '100': '25rem',
      },
      
      maxWidth: {
        'chat': '65ch',
        'sidebar': '16rem',
      },
      
      typography: {
        'chat': {
          css: {
            '--tw-prose-body': '#404040',
            '--tw-prose-headings': '#171717',
            '--tw-prose-lead': '#525252',
            '--tw-prose-links': '#0084ff',
            '--tw-prose-bold': '#171717',
            '--tw-prose-counters': '#737373',
            '--tw-prose-bullets': '#d4d4d4',
            '--tw-prose-hr': '#e5e5e5',
            '--tw-prose-quotes': '#525252',
            '--tw-prose-quote-borders': '#e5e5e5',
            '--tw-prose-captions': '#737373',
            '--tw-prose-code': '#171717',
            '--tw-prose-pre-code': '#e5e5e5',
            '--tw-prose-pre-bg': '#18181b',
            '--tw-prose-th-borders': '#d4d4d4',
            '--tw-prose-td-borders': '#e5e5e5',
          },
        },
      },
    },
  },
  plugins: [
    lineClamp,
  ],
}

export default config