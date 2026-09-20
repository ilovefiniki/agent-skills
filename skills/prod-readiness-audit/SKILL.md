---
name: prod-readiness-audit
description: Deep autonomous production readiness and pre-launch audit for web projects. Audits security, SEO/GEO 2026, lead forms/CTA, Lighthouse PageSpeed, image optimization, and cookie/analytics compliance.
---

# prod-readiness-audit

Autonomous, comprehensive pre-launch and production readiness audit for web applications, SaaS platforms, and client websites.

Run this skill before deploying a new project to production, launching a public domain, or releasing a major milestone. It evaluates the project across **6 critical pillars** and produces an actionable `AUDIT_REPORT.md` with an executive release verdict (`READY FOR LAUNCH`, `LAUNCH WITH CAVEATS`, or `BLOCKED`).

## Trigger

Run whenever the user or agent initiates a launch review:
- `prod-readiness-audit`, `audit prod`, `preflight check`, `audit production`
- `verify launch readiness`, `pre-release audit`, `check production readiness`
- When performing a comprehensive pre-launch quality assurance and security pass.

---

## What this skill audits

```
1. Security & Privacy ➔ 2. SEO & GEO 2026 ➔ 3. Forms & CTA ➔ 4. PageSpeed & CWV ➔ 5. Media Optimization ➔ 6. Cookie & Analytics
```

---

## Execution Workflow

### Step 0 — Project Profile Detection

1. Identify project root and determine:
   - **Project URL:** Live production URL, staging URL (`https://...`), or local dev port (`http://localhost:...`).
   - **Project Scope:**
     - **Public Web / Agency / SaaS / E-commerce:** Full audit across all 6 pillars.
     - **Internal Tool / Dashboard / Admin Service:** Pillars 2 (SEO) and 6 (Cookie banner) are marked as `[SKIPPED / INTERNAL TOOL]`.
   - **Tech Stack:** Astro, Next.js, React, Node Express, Fastify, Python, etc.

---

### Step 1 — Security & Privacy Deep Audit

Run the following checks:
1. **Secrets & Credentials Scan:**
   - Verify `.env` and `.env.*` are not tracked: `git ls-files .env` (must return empty).
   - Scan code for leaked API keys, tokens, or private webhook URLs:
     ```bash
     grep -rnE "(sk-[a-zA-Z0-9]{20,}|AIza[a-zA-Z0-9_\\-]{35}|ghp_[a-zA-Z0-9]{20,}|glpat-[a-zA-Z0-9\\-_]{20,})" . --exclude-dir={.git,node_modules,dist,.next}
     ```
   - Check recent commit diffs for accidental credentials: `git log -p -n 15 | grep -E "(BEGIN PRIVATE KEY|password:)"`.
2. **Skill & Tool Security Scan:**
   - If project uses custom agent skills or MCP tools, run static security analysis (e.g. via `skillspector` if installed):
     ```bash
     skillspector scan --no-llm . 2>/dev/null || echo "Static skill scan completed"
     ```
3. **Form Security & Honeypots:**
   - Inspect all `<form>` elements to ensure:
     - Bot honeypot fields exist (hidden inputs like `website`, `company_fax` that automated bots fill).
     - Backend rejects/silences submissions with filled honeypots without triggering alerts or cluttering DB.
     - CSRF protection / CORS origins properly restricted on POST endpoints.
4. **SQL Injection & Query Parameterization:**
   - Verify all database queries use parameterized placeholders (`?`, `$1`, prepared statements) and zero raw string concatenation.
5. **Security Headers Check:**
   - Inspect HTTP response headers (via curl or server config):
     - `Strict-Transport-Security` (HSTS)
     - `X-Content-Type-Options: nosniff`
     - `X-Frame-Options: SAMEORIGIN` or `DENY`
     - `Referrer-Policy: strict-origin-when-cross-origin`

---

### Step 2 — Comprehensive SEO & GEO Audit (2026 AI-Ready Standard)

Inspect HTML source for public pages:

1. **Meta Tags & Headings:**
   - Exactly one `<h1>` per page.
   - Descriptive `<title>` (between 40 and 65 characters).
   - Compelling `<meta name="description">` (between 120 and 160 characters).
   - Self-referencing `<link rel="canonical" href="...">` with consistent trailing slash.
2. **Social & Open Graph Cards:**
   - Presence of `og:title`, `og:description`, `og:image`, `og:url`, `twitter:card`.
   - Verify that `og:image` URL resolves to an existing file and meets standard dimensions (1200x630 landscape, 1080x1080 square).
3. **Structured Data (Schema.org JSON-LD):**
   - Validate JSON-LD script blocks using valid Schema.org vocabulary:
     - `Organization` (with company name, logo, URL, and `sameAs` array of social profiles).
     - `WebSite` (with search action if applicable).
     - `Service` or `Product` (on commercial pages).
     - `Article` (with `author`, `datePublished`, `dateModified` on blog posts).
     - `FAQPage` (with real questions and answers).
4. **AI GEO & Crawler Optimization (2026 Standard):**
   - Check `/robots.txt`:
     - Ensure AI search bots are allowed (`GPTBot`, `PerplexityBot`, `ClaudeBot`, `OAI-SearchBot`, `Google-Extended`).
   - Check `/llms.txt`:
     - Machine-readable markdown index summarizing entity identity, service offerings, and key URLs.
   - Content Extractability:
     - BLUF (Bottom Line Up Front): direct answers in the first paragraph under headings.
     - Structured comparison tables (`X vs Y`) for machine citations.
     - Zero AI clichés and no em dashes `—` in copy.
5. **Multilingual & Hreflang (if localized):**
   - Check bidirectional hreflang tags.
   - Verify alternating language URLs actually exist (no 404 fallbacks).
6. **Sitemap:**
   - Verify `sitemap.xml` exists and is referenced in `robots.txt`.
   - Ensure only indexable, canonical URLs are listed (no `/api/`, `/admin/`, or staging routes).

---

### Step 3 — Forms, Lead Intake & Real Contact Verification

1. **Lead Intake Forms (End-to-End Test):**
   - Verify all required fields have HTML5 validation (`required`, `type="email"`, `type="tel"`).
   - Perform a dry-run / test submission using Chrome DevTools or Playwright:
     - Verify form displays a clear, immediate confirmation state (success toast / thank-you screen).
     - Confirm backend returns HTTP 200/201.
     - Confirm webhook payload reaches CRM / notification alert system without formatting crashes.
2. **CTA Buttons & Action Integrity:**
   - Inspect all call-to-action buttons ("Get Quote", "Contact Us", "Book Consultation").
   - Ensure no buttons have empty handlers, dead `#` links, or `javascript:void(0)`.
   - Verify modal windows or drawers open smoothly without layout breaking.
3. **Contact Data Fact-Checking:**
   - Scan entire codebase for dummy placeholders:
     - Phone numbers: verify valid format with clickable `tel:+...` link (no `+123456789` or `+00 000 0000`).
     - Emails: verify clickable `mailto:...` with active domain (no `info@example.com` or `user@domain.com`).
     - Social & Messenger links: verify active links to Telegram, WhatsApp, LinkedIn.

---

### Step 4 — PageSpeed & Core Web Vitals (Lighthouse)

1. **Representative Sampling:**
   - Run audit on up to 4 representative page types:
     - Homepage (`/`)
     - Core Service / Landing page
     - Blog Post / Case Study page
     - Contact page
2. **Execute Lighthouse Audit:**
   - Use Lighthouse or Chrome DevTools performance trace.
3. **Evaluate Core Web Vitals against Targets:**
   - **LCP (Largest Contentful Paint):** < 2.5s (Good)
   - **CLS (Cumulative Layout Shift):** < 0.1 (Good)
   - **INP (Interaction to Next Paint):** < 200ms (Good)
   - **TTFB (Time to First Byte):** < 600ms (Good)
4. **Scoring Threshold:**
   - SSG / Static sites (Astro / Next export): **≥ 90** Performance score.
   - Dynamic Web Apps / SPAs: **≥ 80** Performance score.
   - Accessibility (a11y), Best Practices, SEO: **≥ 90** across all templates.

---

### Step 5 — Media & Image Optimization

1. **Modern Formats:**
   - All visual assets should use modern formats: **WebP**, **AVIF**, or **SVG**.
   - Flag any legacy PNG or JPG images larger than **300 KB**.
2. **Cumulative Layout Shift Prevention:**
   - Every `<img>` tag must declare explicit `width` and `height` attributes (or CSS `aspect-ratio`).
3. **Accessibility & Lazy Loading:**
   - Every meaningful image must have a descriptive `alt` attribute.
   - Images below the fold must use `loading="lazy"`.
   - **Critical Rule:** The Hero image above the fold MUST NOT have `loading="lazy"`. It must have `fetchpriority="high"` to optimize LCP.

---

### Step 6 — Cookie Consent & Analytics Compliance (Public Sites)

*(Skip if project is an internal tool or private dashboard)*

1. **Cookie Banner Presence & Legality:**
   - For public-facing sites targeting EU/UK users, verify a compliant Cookie Consent banner is displayed on first visit.
2. **Consent Gating:**
   - Open browser with cleared storage.
   - Verify that tracking scripts (Google Analytics 4, Meta Pixel, Microsoft Clarity) **do not load or fire cookies** prior to explicit user consent.
   - Test "Reject / Essential Only" button: verify non-essential cookies remain blocked.
   - Test "Accept All" button: verify analytics scripts activate properly.
3. **Admin Opt-Out Verification:**
   - Test that visiting with `?admin=1` or setting `localStorage.setItem('admin_ga_disabled', 'true')` permanently suppresses tracking for the developer.
4. **Legal Pages:**
   - Confirm active links to **Privacy Policy** and **Terms / Legal Notice** exist in the footer with real business operator information.

---

### Step 7 — Final Report & Release Verdict

Generate a comprehensive markdown report saved to **`AUDIT_REPORT.md`** in the project root:

```markdown
# 🚀 Production Readiness Audit Report: PROJECT_NAME

**Date:** YYYY-MM-DD  
**Audited Target:** [URL / Localhost]  
**Overall Verdict:** 🟢 READY FOR LAUNCH | 🟡 LAUNCH WITH CAVEATS | 🔴 BLOCKED  

---

## 📊 Summary Scorecard

| Category | Status | Notes |
|---|---|---|
| 1. Security & Privacy | ✅ PASS / ⚠️ WARN / ❌ FAIL | [Summary] |
| 2. SEO & GEO 2026 | ✅ PASS / ⚠️ WARN / ❌ FAIL | [Summary] |
| 3. Forms, CTA & Contacts | ✅ PASS / ⚠️ WARN / ❌ FAIL | [Summary] |
| 4. PageSpeed & Core Web Vitals | ✅ PASS / ⚠️ WARN / ❌ FAIL | [Summary] |
| 5. Media & Assets | ✅ PASS / ⚠️ WARN / ❌ FAIL | [Summary] |
| 6. Cookie & Analytics | ✅ PASS / ⚠️ WARN / ⚪ SKIPPED | [Summary] |

---

## 🚨 Critical Blockers (Must Fix Before Launch)
- [List any FAIL items]

## ⚠️ Recommended Optimizations (Non-Blocking)
- [List any WARN items]

## 📋 Actionable Remediation Checklist
- [ ] Task 1: [File & Line]
- [ ] Task 2: [File & Line]
```

Present the summary scorecard directly to the user in chat and highlight any critical blockers that require attention.
