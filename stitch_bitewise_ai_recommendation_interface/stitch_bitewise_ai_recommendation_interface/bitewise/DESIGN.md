---
name: BiteWise
colors:
  surface: '#131315'
  surface-dim: '#131315'
  surface-bright: '#39393b'
  surface-container-lowest: '#0e0e10'
  surface-container-low: '#1b1b1d'
  surface-container: '#201f21'
  surface-container-high: '#2a2a2c'
  surface-container-highest: '#353437'
  on-surface: '#e5e1e4'
  on-surface-variant: '#e1bfb5'
  inverse-surface: '#e5e1e4'
  inverse-on-surface: '#313032'
  outline: '#a98a80'
  outline-variant: '#594139'
  surface-tint: '#ffb59d'
  primary: '#ffb59d'
  on-primary: '#5d1900'
  primary-container: '#ff6b35'
  on-primary-container: '#5f1900'
  inverse-primary: '#ab3500'
  secondary: '#ffc640'
  on-secondary: '#402d00'
  secondary-container: '#e3aa00'
  on-secondary-container: '#5a4100'
  tertiary: '#d0bcff'
  on-tertiary: '#3c0091'
  tertiary-container: '#a884ff'
  on-tertiary-container: '#3d0094'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdbd0'
  primary-fixed-dim: '#ffb59d'
  on-primary-fixed: '#390c00'
  on-primary-fixed-variant: '#832600'
  secondary-fixed: '#ffdf9f'
  secondary-fixed-dim: '#f9bd22'
  on-secondary-fixed: '#261a00'
  on-secondary-fixed-variant: '#5c4300'
  tertiary-fixed: '#e9ddff'
  tertiary-fixed-dim: '#d0bcff'
  on-tertiary-fixed: '#23005c'
  on-tertiary-fixed-variant: '#5516be'
  background: '#131315'
  on-background: '#e5e1e4'
  surface-variant: '#353437'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 48px
    fontWeight: '800'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
  title-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.05em
  rating-number:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '700'
    lineHeight: 24px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 32px
  xl: 48px
  gutter: 16px
  margin-mobile: 20px
  margin-desktop: 64px
---

## Brand & Style
The design system for this premium AI restaurant recommendation service is built on a foundation of **Sophisticated Modernism** with a heavy emphasis on **Tactile Dark-Mode** aesthetics. The experience should feel like an exclusive concierge—intelligent, appetizing, and high-end. 

The aesthetic leverages high-contrast accents against deep, layered dark surfaces. We utilize **Glassmorphism** for featured content to create a sense of depth and focus, paired with **Corporate Modern** structural precision. The goal is to evoke the feeling of a late-night, high-end dining environment where the interface recedes to let food imagery and AI insights shine.

## Colors
This design system utilizes a "Deep Tech" dark palette optimized for OLED displays and high-end mobile devices. 

- **Primary Accent (#FF6B35):** Used for primary actions, active states, and highlighting "Crave-able" elements. It provides the essential warmth associated with food.
- **Secondary Accent (#FBBF24):** Reserved exclusively for ratings, prestige rankings, and "Top Choice" designations.
- **AI Signature:** The Purple-to-Teal gradient is the hallmark of intelligence. Use this for AI-generated summaries, "Smart Matches," and magic-action buttons.
- **Surface Strategy:** Backgrounds remain near-black to ensure the orange primary pops. Surfaces use a subtle lifted grey with a precise #2A2A32 border to maintain structure without relying on heavy shadows.

## Typography
We use **Plus Jakarta Sans** for its modern, friendly, yet professional geometric construction. It strikes a balance between a high-end editorial feel and technical efficiency.

- **Tabular Figures:** For ratings and prices, ensure `tnum` (tabular figures) is enabled so numbers align perfectly in lists.
- **Hierarchy:** Use `display-lg` sparingly for hero AI insights. `label-caps` should be used for categories (e.g., "CUISINE," "DISTANCE").
- **Readability:** Body text should maintain a healthy line height (1.5x) to ensure descriptions are legible against the dark background.

## Layout & Spacing
The layout follows a **Fluid Grid** model with strict 8px incremental spacing (the "Base-4" system). 

- **Mobile:** 4-column grid with 20px outside margins. Cards typically span full width or 2 columns in a staggered layout.
- **Desktop:** 12-column grid centered at a max-width of 1280px. 
- **Rhythm:** Use `md` (24px) for vertical separation between distinct content sections and `sm` (16px) for internal card padding. 
- **Glassmorphism Layering:** When using glassmorphism (e.g., a sticky header or a search overlay), apply a `20px` backdrop blur and a `10%` white tint to the surface.

## Elevation & Depth
In this dark-themed environment, depth is communicated through **Tonal Layering** and **Subtle Glows** rather than traditional black shadows.

- **Level 0 (Background):** #0D0D0F.
- **Level 1 (Cards/Surface):** #1A1A1F with a 1px solid border of #2A2A32.
- **Level 2 (Popovers/Modals):** #24242B with a soft #000000 (40% opacity) shadow, 20px blur.
- **The "AI Glow":** For AI-driven cards, apply a very faint outer glow using the primary AI gradient (10% opacity) to make the element appear to emit light.
- **Glassmorphism:** Use for "floating" elements like bottom navigation bars or filter chips over content.

## Shapes
The shape language is **Rounded and Organic**, mimicking the soft edges of plates and natural forms found in dining. 

- **Standard Elements:** Buttons and input fields use `0.5rem` (rounded-md).
- **Cards & Containers:** Use `1rem` (rounded-lg) to create a premium, modern feel.
- **AI Elements:** Use `rounded-xl` (1.5rem) or full pills for AI-suggested chips and "Smart" buttons to distinguish them from standard UI.
- **Images:** Food photography should always have a minimum of `1rem` corner radius; never use sharp corners for food imagery.

## Components
- **Buttons:** 
  - *Primary:* Solid #FF6B35 with white text. High-gloss finish.
  - *AI Action:* Gradient background with a subtle "sparkle" icon.
  - *Secondary:* Ghost style with #2A2A32 border and #F5F5F7 text.
- **Cards:** 
  - Restaurant cards feature a large image header, a floating #FBBF24 rating badge in the top right, and metadata (Distance, Price) using `label-caps`.
- **Chips:**
  - Used for cuisine types and filters. Background: #2A2A32; Text: #A1A1AA. Active state: #FF6B35 background.
- **Input Fields:**
  - Dark background (#121217), 1px border (#2A2A32), and subtle inset shadow to create a "hollow" tactile feel.
- **Lists:**
  - Use thin #2A2A32 dividers. Every list item should have a trailing chevron or an action icon (Map Pin/Sparkles).
- **AI Sparkle:** 
  - A small, animated icon component used next to AI-generated text or insights, utilizing the teal/purple gradient.