---
name: design-director
description: "Master frontend design orchestrator. Enforces elite design taste, bans AI-slop, and routes UI tasks to the right specialized design engine (taste-skill for landing pages & redesigns, ui-ux-pro-max for web apps & complex SaaS components, superdesign for multi-concept exploration). Use whenever building, styling, redesigning, or reviewing any frontend UI, landing page, web application, dashboard, or component."
---

# Design Director — Master Web UI Orchestrator

The Design Director coordinates frontend design to ensure that AI coding agents produce human-grade, visually striking, and functionally robust interfaces instead of generic "AI slop".

---

## 🚨 Non-Negotiable Core Directives (All UI Work)

1. **NO DEFAULT AI-SLOP:**
   - NEVER use the generic purple-blue mesh gradient on dark backgrounds.
   - NEVER use the 3-identical-cards layout with icons in rounded colored squares.
   - NEVER use emojis in place of real SVG icons (use Lucide, Heroicons, or Phosphor).
   - NEVER invent fake traction metrics ("99.9% customer satisfaction", "10,000+ happy clients") unless provided by the user.
   - NEVER default to plain Inter + Slate-900 without a deliberate reason.

2. **MANDATORY DESIGN READ:**
   Before writing a single line of CSS or HTML, output a one-line declaration:
   > **Design Read:** [Page/Component type] for [Target Audience] with [Aesthetic/Vibe], using [Design Stack / System].

---

## 🧭 The 3-Way Engine Routing

Whenever tasked with UI creation, styling, or redesign, the Design Director delegates to the appropriate specialized engine:

```
                                  UI Task
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
   [Branch 1: Taste]           [Branch 2: Pro Max]         [Branch 3: Canvas]
  Landings, Brand, Redesign     SaaS, Dashboards, Forms    Visual Variant Exploration
         │                           │                           │
  taste-skill                 ui-ux-pro-max               superdesign
```

### Branch 1: Landing Pages, Portfolios & Brand Redesigns
**Engine:** `taste-skill` (`~/.agents/skills/taste-skill/SKILL.md`)

Use this for: Marketing sites, landing pages, agency portfolios, single-purpose conversion pages, and homepage redesigns.

**Execution Protocol:**
1. **Set The Three Dials (1 to 10):**
   - `DESIGN_VARIANCE` (1 = strict symmetric grid; 10 = editorial asymmetric magazine layout).
   - `VISUAL_DENSITY` (1 = spacious Apple-style luxury; 10 = compact high-information density).
   - `MOTION_INTENSITY` (1 = static/minimal; 10 = cinematic scroll-driven storytelling).
2. **Hero 2-Line Rule:**
   The `<h1>` must never wrap into an ugly 4–6 line text clump. Use wide containers (`max-w-5xl`+) and fluid typography (`clamp(2.5rem, 5vw, 4.5rem)`).
3. **Pacing & Generous Spacing:**
   Separate distinct narrative chapters with generous vertical breathing room (`py-24 md:py-36`).

---

### Branch 2: Web Apps, Dashboards, Complex Forms & Data Tables
**Engine:** `ui-ux-pro-max` (`~/.agents/skills/ui-ux-pro-max/SKILL.md`)

Use this for: SaaS dashboards, CRM interfaces, quote calculators, multi-step booking wizards, data tables, and settings pages.

**Execution Protocol:**
1. **Query Local Design Database:**
   Run the search tool to extract tested palettes, font pairings, and UX rules:
   ```bash
   python3 ~/.gemini/config/skills/ui-ux-pro-max/scripts/search.py "<niche-keyword>" --domain color
   python3 ~/.gemini/config/skills/ui-ux-pro-max/scripts/search.py "<style-keyword>" --domain style
   python3 ~/.gemini/config/skills/ui-ux-pro-max/scripts/search.py "<ux-topic>" --domain ux
   ```
2. **State Completeness Checklist:**
   Every interactive component MUST explicitly handle:
   - Default, Hover, Active, Focus-visible (keyboard a11y), Disabled.
   - Empty states (with clear CTA).
   - Loading states (skeletons with layout stability, no CLS jump).
   - Error states (inline validation text next to the field, not just top-level banners).
3. **Accessibility (WCAG AA Minimum):**
   - Text contrast >= 4.5:1 against background.
   - Tap targets >= 44x44px on mobile.
   - Visible outline on `:focus-visible`.

---

### Branch 3: Exploratory Concept Generation
**Engine:** `superdesign` (`~/.gemini/config/skills/superdesign/SKILL.md`)

Use this when: The user explicitly asks for 2-4 visual options, wireframes, or wants to explore aesthetic directions before committing to code.

---

## 🛠️ Technical Foundation (Modern Web Standard)

Regardless of the selected branch, always apply modern web standards:
- **CSS Architecture:** Semantic design tokens (CSS Custom Properties) for colors, radiuses, and typography.
- **Modern Selectors:** Use `:has()` for parent-state styling, CSS Subgrid for aligned nested items, Container Queries for modular components.
- **Micro-Animations:** Use CSS transitions with tailored cubic-bezier timing (`transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1)`).
- **Responsive Resilience:** Mobile-first; test at `<400px`, `768px`, and `>1280px`. Zero horizontal scrollbar.

---

## ✅ Pre-Flight Delivery Checklist

Before marking any UI code complete, run this mental audit:
- [ ] Stated the **Design Read** upfront?
- [ ] Cleaned of all **AI clichés** (no purple neons, no fake ratings, no emoji-icons)?
- [ ] Typography rhythm is balanced (headings don't wrap awkwardly into 5+ lines)?
- [ ] All interactive states (hover, focus, active, loading, error) are accounted for?
- [ ] Mobile view is clean with touch targets >= 44px?
