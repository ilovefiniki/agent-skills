---
name: youtube-action-planner
description: Autonomous deep topic researcher and action plan generator from YouTube video corpora. Selects top fresh videos on a topic, extracts multi-video transcripts simultaneously, and synthesizes an executive implementation plan in Markdown.
---

# YouTube Action Planner & Topic Researcher

Researches top fresh videos on any technical or business topic, extracts full transcripts in batch, synthesizes multi-expert insights, and compiles an actionable step-by-step implementation plan.

---

## 🚀 Workflow

### Step 1: Discover High-Authority Videos
When given a topic (e.g. "building autonomous AI agents 2026"):
- Identify 5 to 10 top-ranking, fresh, high-authority YouTube video URLs.

### Step 2: Batch Extract Transcripts
Run the batch transcript extractor passing all video URLs:

```bash
python3 scripts/get_transcript.py <URL_1> <URL_2> <URL_3> ... <URL_10>
```

Outputs a consolidated JSON mapping each video URL to its full text transcript without downloading video or audio streams.

### Step 3: Cross-Expert Synthesis
Synthesize the extracted transcripts across all videos:
- Identify consensus practices vs divergent viewpoints.
- Filter out sponsor segments, channel promos, and generic fluff.
- Extract concrete tools, libraries, architectural decisions, and failure modes.

### Step 4: Generate Action Plan Report
Format into a clean, structured implementation document saved to `./plans/YYYY-MM-DD_topic-slug.md`:

```markdown
# 📋 Master Action Plan: [Topic Name]

**Synthesized Sources:** {count} videos analyzed  
**Generated:** YYYY-MM-DD  

## 🎯 Executive Summary
[High-level synthesis of current state of the art and key takeaways across all reviewed sources]

## 🛠️ Synthesized Multi-Step Action Plan
- [ ] **Phase 1: Foundation & Setup**
  - Concrete step 1 with rationale from video citations
  - Concrete step 2
- [ ] **Phase 2: Execution & Implementation**
  - Concrete step 3
- [ ] **Phase 3: Hardening & Testing**
  - Concrete step 4

## 💎 Golden Nuggets & Non-Obvious Insights
- Crucial architecture tip from [Creator/Channel] (URL)
- Common pitfall warned by [Creator/Channel] (URL)

## 🔗 Analyzed Sources & Citations
1. [Video Title 1](URL) — Key contribution
2. [Video Title 2](URL) — Key contribution
```
