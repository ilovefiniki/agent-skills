---
name: init-project
description: Initialize a new or existing project according to the Modern Multi-Agent Standard. Sets up AGENTS.md, GEMINI.md, CLAUDE.md, ARCHITECTURE.md, README.md, session scratchpads, fast zero-cost security rules, and runtime browser verification.
---

# init-project

Initialize any software project or repository according to the **Production Multi-Agent Governance Standard**.

Sets up universal agent governance (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`), dynamic architecture specifications (`ARCHITECTURE.md`), context scratchpads (`.vault-notes.md`), lightweight pre-commit security gates, zero-pollution analytics isolation, and browser runtime verification protocols.

## Trigger

Run whenever the user or agent initiates project setup:
- `init project`, `init-project`, `initialize project`, `setup project`
- `создать проект`, `настроить правила проекта`, `добавить агентов`, `инициализировать репозиторий`
- When opening a new repo or workspace and establishing AI agent governance rules.

---

## What this skill does

1. **Scans target workspace:** detects language and framework (Node/Astro/Next/React/Python/FastAPI/Docker), existing files, and Git status.
2. **Classifies project profile:**
   - **Public Web / SaaS / Client Site:** full SEO, security headers, cookie/consent gating, and contact intake validation.
   - **Internal App / CLI Tool / Microservice:** streamlined auth, focuses on API contracts and performance, skips consumer cookie banners.
3. **Generates Universal Multi-Agent Instructions:**
   - `AGENTS.md` (Master operational blueprint for Claude Code, Antigravity, Gemini, Cursor, and Windsurf).
   - `GEMINI.md` (Reference linking to `AGENTS.md`).
   - `CLAUDE.md` (Reference linking to `AGENTS.md`).
4. **Generates Spec-Driven Documentation:**
   - `ARCHITECTURE.md` (Living technical spec: directory tree, component contracts, schema, endpoints).
   - `README.md` (Quickstart, verification commands, and high-level architecture overview).
   - Enforces the **Spec-Driven Rule**: code changes must update `ARCHITECTURE.md`.
5. **Configures Context Scratchpad & Memory:**
   - Initializes `.vault-notes.md` for intra-session continuity.
   - Updates `.gitignore` to prevent committing local scratchpads and secrets.
   - (Optional) Connects Second Brain / Obsidian knowledge base synchronization.
6. **Injects Lightweight Quality & Security Gates:**
   - Automated syntax & build validation commands.
   - Fast pre-deploy secret leak check (detecting `.env` leaks, private tokens, honeypots).
   - Analytics zero-pollution guardrail (preventing local/test traffic from contaminating production analytics).
   - Browser runtime verification protocol via Chrome DevTools or Playwright.

---

## Execution Steps

### Step 1 — Project Discovery & Profile

Inspect the workspace:
- Check root files:
  - `package.json` -> inspect dependencies (`astro`, `next`, `react`, `vue`, `express`, `fastify`).
  - `requirements.txt` / `pyproject.toml` -> Python environment.
  - `Dockerfile` / `docker-compose.yml` -> Containerized service.
  - Verify if Git is initialized (`git rev-parse --is-inside-work-tree`).

Determine variables:
- `PROJECT_NAME`: directory basename.
- `PROJECT_TYPE`:
  - `Public Web Platform / Client Site`
  - `Internal Tool / Microservice / API`
- `BUILD_COMMAND`: e.g. `npm run build`, `npm test`, or `pytest`.

---

### Step 2 — Generate AGENTS.md

Create `AGENTS.md` in the project root:

```markdown
# AI Agent Instructions — PROJECT_NAME

> Project name: `PROJECT_NAME`
> Target environment: [Production URL / Staging URL / Localhost]

---

## 🎯 Project Overview & Core Focus

[Brief 2-3 sentence summary of what this project is, its core capabilities, and tech stack.]

---

## 🚨 Mandatory Project Documentation Rule (Spec-Driven)

**Whenever making ANY changes to the codebase, API routes, data models, or client forms:**
1. **Always update [`ARCHITECTURE.md`](ARCHITECTURE.md)** detailing modified/new components, endpoints, schema changes, security mechanisms, and data flows.
2. **Always update [`README.md`](README.md)** with user-facing summaries, API tables, and operational guides.
3. Keep documentation strictly synchronized with reality. Never leave stale architecture descriptions.

---

## 🧪 Verification & Runtime Testing Protocol (Mandatory)

**Never claim work is complete without rigorous verification.**

Before finishing any task or asking for review:
1. **Syntax & Build Validation:**
   - [SPECIFIC_BUILD_COMMAND, e.g. `npm run build` or `python3 -m py_compile ...`] (must pass with 0 errors).
2. **Automated Test Suite:**
   - [SPECIFIC_TEST_COMMAND, e.g. `npm test` or `pytest`] (must pass 100% of all tests).
3. **Browser Runtime Verification (Chrome DevTools / Playwright):**
   - Open the local dev/preview URL.
   - Check console messages: **0 unhandled JavaScript errors** (`TypeError`, `ReferenceError`).
   - Verify layout responsiveness (mobile < 480px and desktop > 1200px).
   - Verify dynamic element rendering.
4. **Analytics Zero-Pollution Guardrail:**
   - All tests, agents, and local development MUST suppress analytics tracking.
   - Ensure `localhost`, `127.0.0.1`, `navigator.webdriver === true`, `?admin=1`, or `localStorage.getItem('admin_ga_disabled')` prevents sending pageviews/events to GA4/Clarity.

---

## 🔒 Pre-Deploy Security Checklist (Fast & Low-Cost)

Before committing or pushing to production:
1. **Zero Leaked Secrets:** Check `git status` to ensure `.env` and local secrets are NOT tracked. Scan for hardcoded keys (`sk-`, `AIza`, `ghp_`, bearer tokens).
2. **Form Sanitization & Honeypots:** Ensure all customer-facing forms have active bot honeypots and input sanitization.
3. **Clean Style & Content:** In copywriting and docs, do NOT use em dashes `—` or AI buzzwords ("game-changer", "dive in", "delve", "tapestry").

> **Note on Major Launches:** For full production milestones or public releases, run the comprehensive audit skill: `prod-readiness-audit`.

---

## 🔄 Session Protocol (Context Continuity)

Follow this 3-phase protocol on every work session:

### Phase 1 — Session Start
1. Check if `.vault-notes.md` exists in this folder.
   - If yes: read it to absorb previous context.
   - If no: create it with today's date and a brief note about the current task.

### Phase 2 — During Session
Keep `.vault-notes.md` updated after each meaningful change:
- What was built or changed, in plain language.
- The decision or reason behind it.
- What is incomplete or next.

### Phase 3 — Before Commit / End of Session
Do this BEFORE committing:
1. Summarize key achievements and write a clean, structured commit message.
2. Clear `.vault-notes.md` (or let the post-commit hook archive it automatically).
```

---

### Step 3 — Generate GEMINI.md and CLAUDE.md

Create `GEMINI.md`:
```markdown
# Gemini & Antigravity Instructions

See [AGENTS.md](AGENTS.md) — all core instructions, testing rules, and session protocols apply here.

Mandatory rules:
1. Always maintain and update `ARCHITECTURE.md` and `README.md` with all technical specifications.
2. Run syntax/build and test commands before claiming work is complete.
3. Verify visual UI runtime with 0 unhandled console errors.
```

Create `CLAUDE.md`:
```markdown
# Claude Code Instructions

See [AGENTS.md](AGENTS.md) — master instructions apply to all sessions.

Follow the 3-phase session protocol (`.vault-notes.md` context continuity).
Always update `ARCHITECTURE.md` and verify 0 console errors before completing tasks.
```

---

### Step 4 — Generate ARCHITECTURE.md Blueprint

Create `ARCHITECTURE.md`:

```markdown
# Architecture Specification: PROJECT_NAME

> **Status:** Active Development  
> **Environment:** [URL / Localhost]  
> **Repository:** [Git repository URL]  

---

## 1. Concept & Scope

High-level summary of the system, business problems solved, and primary personas.

---

## 2. Directory Structure

```
PROJECT_NAME/
├── ARCHITECTURE.md          # Complete technical blueprint
├── README.md                # User guide & quickstart
├── AGENTS.md                # Universal multi-agent governance
├── GEMINI.md                # Reference to AGENTS.md
├── CLAUDE.md                # Reference to AGENTS.md
├── .vault-notes.md          # Session context scratchpad
│
├── [src/ / app/ / core/]    # Application source code
└── tests/                   # Automated test suite
```

---

## 3. Core Components & API Endpoints

| Route / Component | Purpose | Access |
|---|---|---|
| `/` | Main UI / Entry point | Public |
| `/api/health` | Service health check | Public |

---

## 4. Data Models & State Management

Database schema, migrations, tables, or client state handling.

---

## 5. Integrations & External Services

- **Webhooks & APIs:** Downstream event pipelines.
- **Observability:** Logging, analytics, and error tracking.

---

## 6. Security & Environment Configuration

- Secrets managed via `.env` (never committed).
- Bot honeypots on intake forms.
- Rate-limiting and input sanitization.
```

---

### Step 5 — Generate README.md

Create or update `README.md`:
```markdown
# PROJECT_NAME

[One-line elevator pitch for the project]

## Quickstart

```bash
# Install dependencies
npm install  # or pip install -r requirements.txt

# Run development server
npm run dev

# Run verification and build
npm test
npm run build
```

## Documentation & Architecture

- Technical specification and architecture: [`ARCHITECTURE.md`](ARCHITECTURE.md)
- Multi-agent instructions and testing protocols: [`AGENTS.md`](AGENTS.md)

## Development Rules

1. Any changes in code, schema, or routes must be reflected in `ARCHITECTURE.md`.
2. Ensure 0 unhandled console errors and clean test runs before committing.
3. Pre-deploy security checks are mandatory before production releases.
```

---

### Step 6 — Context Scratchpad & Git Configuration

1. **Create `.vault-notes.md`:**
```markdown
# Context Notes — PROJECT_NAME

Initialized: YYYY-MM-DD

[Active session context will be maintained here.]
```

2. **Update `.gitignore`:**
Ensure the following entries are ignored:
```gitignore
.vault-notes.md
.vault-notes-archive/
.env
.env.*
!.env.example
```

3. **(Optional) Install Post-Commit Archival Hook:**
To automatically archive `.vault-notes.md` on every commit, copy the provided hook:
```bash
mkdir -p .git/hooks
cp templates/post-commit.sh .git/hooks/post-commit
chmod +x .git/hooks/post-commit
```
