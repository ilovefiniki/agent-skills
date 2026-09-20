---
name: infographic-engine
description: "AI-native engineering infographic and interactive diagram generator. Builds code-first, responsive, accessible, zero-dependency HTML/CSS/SVG infographics across 5 core archetypes (CAD Architecture Blueprint, Dynamic ROI Calculator & Split-Slider, Execution Trace Replay, Metric Delta Grid with Sparklines, and Multi-Agent DAG Topology). Automatically adapts to the host site's design tokens and brand palette (ilf-studio.com, ilovefiniki.com, LocalAnyDay, Finiki CRM, etc.). Use whenever creating or updating diagrams, architecture charts, comparison tables, performance visualizers, or infographics in blog posts, landing pages, and case studies."
---

# 📐 Infographic Engine — Code-First Architecture Visualizer

This skill generates human-grade, interactive, accessible, and high-performance technical infographics directly in code (HTML + CSS + SVG). It banishes static blurry PNGs and generic "AI-slop" in favor of living, lightweight, semantic components that rank #1 in search engines and get cited by AI Overviews (Perplexity, SearchGPT).

---

## 🚨 Non-Negotiable Engineering Directives

1. **Zero Heavy Raster Images:**
   - NEVER embed PNG/JPG/WebP for technical schemas, workflows, or comparisons.
   - All infographics MUST be 100% Code-First (HTML + CSS + inline SVG).
   - Payload budget: Under 6 KB total per infographic. 0 external JS libraries (no heavy React bundles, D3, or Canvas needed for core presentation).
2. **Strict Anti-AI-Slop:**
   - ❌ NO generic purple-blue mesh gradients on dark slate.
   - ❌ NO emojis as architectural or node icons (use clean vector SVGs or monospaced technical badges).
   - ❌ NO vague fake numbers ("99.9% customer happiness"). Always use concrete engineering deltas (`−98.5% TTFB`, `$48/mo vs $2,450/mo`, `420ms end-to-end`).
3. **AEO & LLM Machine-Readability:**
   - All content in nodes and metrics MUST be semantic text in the DOM so that AI scrapers (SearchGPT, Claude, Perplexity) can parse, understand, and cite the data directly in answer snapshots.
4. **Mobile & Fluid Responsiveness:**
   - All grids MUST collapse gracefully on mobile screens (`max-width: 768px`) without horizontal overflow or micro-text clipping.

---

## 🎨 Automatic Design Token Adaptor (Multi-Site Theming)

Before generating any infographic, inspect the host project's stylesheet or `AGENTS.md` to bind the CSS variables:

| Token | Purpose | `ilf-studio.com` | `LocalAnyDay.com` | `ilovefiniki.com` / CRM |
|---|---|---|---|---|
| `--info-bg-page` | Page background | `#EFE8DC` (Cream) | `#fbf9f6` (Limestone) | `#0B0F17` / `#141210` |
| `--info-surface` | Diagram card container | `#141210` (Dark) / `#FAF5EB` (Light) | `#1e3a2b` (Slate) / `#FFFFFF` | `#161F30` / `#1F1C18` |
| `--info-accent` | Primary brand accent | `#CC7A3E` (Terracotta) | `#c2531a` (British Terracotta) | `#38BDF8` (Cyan) / `#22C55E` |
| `--info-accent-soft` | Soft badge background | `rgba(204, 122, 62, 0.15)` | `rgba(194, 83, 26, 0.15)` | `rgba(56, 189, 248, 0.15)` |
| `--info-border` | Subtle structural borders | `#2E2720` (Dark) / `#D4C8B8` (Light) | `#2d4f3b` / `#e2ded6` | `#2B3548` / `#332B22` |
| `--info-text-main` | Primary reading text | `#EDE6DC` (Dark) / `#2A241B` (Light) | `#FFFFFF` / `#1A202C` | `#F8FAFC` |
| `--info-text-muted` | Secondary technical text | `#9E9080` (Dark) / `#6B5B4A` (Light) | `#9fb5a7` / `#718096` | `#94A3B8` |
| `--info-font-display`| Headings & big metrics | `Geist`, `Plus Jakarta Sans` | `Outfit`, `Plus Jakarta Sans` | `Inter`, `Geist` |
| `--info-font-mono`   | Timestamps, ports & code | `JetBrains Mono` | `JetBrains Mono` | `JetBrains Mono` |

---

## 🏛️ The 5 Master Infographic Archetypes

### 1. CAD Architecture Blueprint (`.cad-container`)
* **Best for:** Deep system architectures, microservices, Docker/VPS deployments, database persistence, and API gateways.
* **Aesthetic:** High-precision hardware schematic with millimetric grid lines, technical corner brackets, and copper pulse data buses.
* **Markup Template:**

```html
<div class="cad-container">
  <div class="cad-corner-mark c-tl"></div>
  <div class="cad-corner-mark c-tr"></div>
  <div class="cad-corner-mark c-bl"></div>
  <div class="cad-corner-mark c-br"></div>
  <div class="cad-canvas">
    <div class="cad-top-bar">
      <span>SCHEMATIC: [MODULE_NAME]</span>
      <span>ENV: DOCKER_CONTAINER_V2</span>
      <span>STATUS: ACTIVE</span>
    </div>
    <div class="cad-grid">
      <div class="cad-node-box">
        <span class="cad-node-tag">[PORT_8642] INTAKE</span>
        <div class="cad-node-title">Fastify Gateway</div>
        <div class="cad-node-desc">Latency: 4.2ms • Zero Overhead</div>
      </div>
      <div class="cad-wire">
        <div class="cad-wire-line"><div class="cad-wire-pulse"></div></div>
        <span class="cad-wire-label">JSON_BUS</span>
      </div>
      <div class="cad-node-box">
        <span class="cad-node-tag">[AI_EVAL] SCORER</span>
        <div class="cad-node-title">Gemini 2.0 Flash</div>
        <div class="cad-node-desc">Processing: 240ms • Intent Tagging</div>
      </div>
      <div class="cad-wire">
        <div class="cad-wire-line"><div class="cad-wire-pulse"></div></div>
        <span class="cad-wire-label">SQL_WAL</span>
      </div>
      <div class="cad-node-box">
        <span class="cad-node-tag">[PERSIST] STORAGE</span>
        <div class="cad-node-title">SQLite WAL Engine</div>
        <div class="cad-node-desc">Encrypted • Zero Network IO</div>
      </div>
    </div>
  </div>
</div>
```

---

### 2. Dynamic ROI Calculator & Split-Slider (`.calc-card-studio`)
* **Best for:** Cost comparisons (Custom Code vs SaaS, In-House vs Outsourced, Legacy vs Modernized), pricing tiers, and interactive ROI calculation.
* **Aesthetic:** Interactive range slider that dynamically recalculates costs, paired with a draggable Before/After reveal slider.
* **Markup Template:**

```html
<div class="calc-card-studio">
  <div class="calc-header">
    <div>
      <h3 class="calc-title">TCO Cost Simulator</h3>
      <p class="calc-subtitle">Drag slider to calculate savings for your volume:</p>
    </div>
    <span class="calc-badge">REAL-TIME ESTIMATE</span>
  </div>
  <div class="calc-slider-box">
    <div class="calc-slider-label">
      <span>Monthly Volume:</span>
      <strong id="calcVolumeDisplay">5,000 requests / mo</strong>
    </div>
    <input type="range" class="custom-range" id="volumeRange" min="500" max="50000" step="500" value="5000" oninput="updateCalculator(this.value)">
  </div>
  <div class="calc-results-grid">
    <div class="calc-res-item">
      <div class="calc-res-title">Legacy SaaS Cost</div>
      <div class="calc-res-val legacy-red" id="saasCostVal">$450/mo</div>
    </div>
    <div class="calc-res-item">
      <div class="calc-res-title">Sovereign Cloud Stack</div>
      <div class="calc-res-val accent" id="dockerCostVal">$13/mo</div>
    </div>
    <div class="calc-res-item">
      <div class="calc-res-title">Annual Net Savings</div>
      <div class="calc-res-val green" id="savingsVal">$5,244 / yr</div>
    </div>
  </div>

  <!-- Interactive Before/After Split -->
  <div class="split-slider-container" id="splitBox">
    <div class="split-panel split-legacy">
      <div>
        <div class="split-legacy-tag">Legacy Approach</div>
        <div class="split-legacy-title">Vendor SaaS Lock-in</div>
        <div class="split-legacy-desc">Recurring seat taxes, rate-limit throttles, and third-party data tracking.</div>
      </div>
    </div>
    <div class="split-panel split-modern" id="modernPanel">
      <div class="split-modern-inner">
        <div class="split-modern-tag">AI-Native Standard</div>
        <div class="split-modern-title">Sovereign Fastify Core</div>
        <div class="split-modern-desc">420ms latency, zero seat license fees, and complete data privacy.</div>
      </div>
    </div>
    <div class="split-handle" id="splitHandle"><div class="split-handle-btn">⇄</div></div>
  </div>
</div>
```

---

### 3. Execution Trace Replay (`.trace-replay`)
* **Best for:** Speed, latency analysis, API webhooks, AI agent thinking pipelines, and GEO/SearchGPT retrieval passes.
* **Aesthetic:** Millisecond timeline cascade showing exact execution bottlenecks and milestone events.
* **Markup Template:**

```html
<div class="infographic-wrapper">
  <div class="infographic-header">
    <div class="infographic-title-wrap">
      <span class="infographic-dot"></span>
      <span class="infographic-title">EXECUTION TRACE: INTAKE TO TELEGRAM ALERT</span>
    </div>
    <span class="infographic-tag">TOTAL RUNTIME: 418ms</span>
  </div>
  <div class="infographic-body">
    <div class="trace-replay" id="traceBox">
      <div class="trace-row">
        <span class="trace-time">00:00.000</span>
        <span class="trace-badge ok">POST 200</span>
        <span class="trace-node">Client Form Ingestion</span>
        <span class="trace-detail">Encrypted payload via Fastify API</span>
        <span class="trace-delta">+4ms</span>
      </div>
      <div class="trace-row">
        <span class="trace-time">00:00.012</span>
        <span class="trace-badge security">SHIELD</span>
        <span class="trace-node">Honeypot & Auth Check</span>
        <span class="trace-detail">Zero bot tokens, SQL sanitization passed</span>
        <span class="trace-delta">+8ms</span>
      </div>
      <div class="trace-row highlight">
        <span class="trace-time">00:00.120</span>
        <span class="trace-badge ai">AI SCORER</span>
        <span class="trace-node">Intent & Budget Score</span>
        <span class="trace-detail">Gemini Flash: "High Commercial Intent", €8,500</span>
        <span class="trace-delta">+260ms</span>
      </div>
      <div class="trace-row final">
        <span class="trace-time">00:00.418</span>
        <span class="trace-badge notify">DISPATCH</span>
        <span class="trace-node">Telegram Alert Push</span>
        <span class="trace-detail">Delivered to operator's mobile app</span>
        <span class="trace-delta">DONE</span>
      </div>
    </div>
  </div>
</div>
```

---

### 4. Metric Delta Grid with Sparklines (`.metric-delta-grid`)
* **Best for:** Performance leaps, SEO Core Web Vitals comparisons (Drupal/WP vs Astro), and infrastructure migrations.
* **Aesthetic:** Grid of high-contrast cards with Before ➔ After deltas, percentage badges, and lightweight inline SVG sparklines.
* **Markup Template:**

```html
<div class="metric-delta-grid">
  <div class="metric-card">
    <div class="metric-label">Time to First Byte (TTFB)</div>
    <div class="metric-compare">
      <span class="metric-before">1,850ms</span>
      <span class="metric-arrow">➔</span>
      <span class="metric-after">28ms</span>
    </div>
    <div class="metric-badge win">−98.5% LATENCY</div>
    <svg class="metric-sparkline-svg" viewBox="0 0 100 30" preserveAspectRatio="none">
      <path d="M0 5 Q 30 5, 50 15 T 100 28" fill="none" stroke="currentColor" stroke-width="2.5" />
      <circle cx="100" cy="28" r="3.5" fill="currentColor" />
    </svg>
  </div>
  <div class="metric-card">
    <div class="metric-label">Monthly Cloud Hosting</div>
    <div class="metric-compare">
      <span class="metric-before">$180/mo</span>
      <span class="metric-arrow">➔</span>
      <span class="metric-after">$0/mo</span>
    </div>
    <div class="metric-badge win">100% SAVINGS</div>
    <svg class="metric-sparkline-svg" viewBox="0 0 100 30" preserveAspectRatio="none">
      <path d="M0 6 L 40 6 L 50 26 L 100 26" fill="none" stroke="currentColor" stroke-width="2.5" />
      <circle cx="100" cy="26" r="3.5" fill="currentColor" />
    </svg>
  </div>
</div>
```

---

### 5. Multi-Agent DAG Topology (`.dag-container`)
* **Best for:** Autonomous multi-agent systems, orchestrator-worker delegation, LangGraph/Hermes setups, and task dispatching.
* **Aesthetic:** Clean hierarchical tree with pulsing connection wires and security privilege chips.

---

## 🛠️ Step-by-Step Agent Workflow

When asked to create or add an infographic to an article or page:

1. **Design Read & Archetype Selection:**
   - What is the story? (Latency? Architecture? Cost ROI? Multi-agent?)
   - Pick the exact Archetype (1 to 5).
2. **Theme Binding:**
   - Detect project colors and map tokens (`var(--terracotta)` on ILF Studio, `var(--primary)` on Next.js, etc.).
3. **Embed HTML/SVG:**
   - Insert clean, accessible HTML blocks directly into Markdown, MDX, or Astro templates.
4. **Validation:**
   - Ensure `npm run build` passes with 0 errors.
   - Verify layout responsiveness on mobile.
