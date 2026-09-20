---
name: youtube-summary-extractor
description: "Extract transcripts and generate structured summaries, executive takeaways, or actionable plans from YouTube videos directly without downloading video files. Use whenever the user shares a YouTube URL (video, short, podcast) and asks for a summary, key takeaways, transcript, or structured notes."
---

# YouTube Summary Extractor

Extracts complete transcripts and official chapters from YouTube videos in 1–2 seconds **without downloading any video or audio files**, and formats structured executive summaries tailored for technical, educational, and business content.

---

## 🛡️ Safety & Rate Limiting Guards

* **Zero Video Download:** Pulls subtitles directly from YouTube's transcript API, saving bandwidth and disk space.
* **Rate Guard:**
  * Maximum **20 requests per hour** (rolling 60-minute window).
  * **5-second cooldown** between successive requests.
  * State tracked in `~/.cache/youtube_rate_limit.json`.
* **Zero Account Risk:** Operates anonymously with no Google cookies or logins.

---

## 🚀 Execution Workflow

### Step 1: Extract Transcript & Chapters
Run the extractor script with the video URL (or 11-char ID):

```bash
python3 scripts/extract_transcript.py "<YOUTUBE_URL>"
```

Returns JSON with:
* `title`: Video title
* `channel`: Creator / channel name
* `duration_formatted`: e.g. `14:20`
* `chapters`: Official chapter marks (if provided)
* `chunks`: Grouped transcript segments with timestamps
* `full_text`: Complete transcript text

### Step 2: Format Structured Summary

Format into a clean markdown document:

```markdown
# 📺 [Video Title]
**Channel / Speaker:** {channel} | **Duration:** {duration_formatted} | [Watch on YouTube]({url})

---

### 📌 Core Takeaway (TL;DR / BLUF)
{2-3 concise sentences: core thesis, problem addressed, and final conclusion}

---

### 🧭 Timestamped Breakdown

#### ⏱️ 00:00 – {Chapter Title}
* {Key thesis}
* {Technical context / examples}

#### ⏱️ 04:30 – {Chapter Title}
* {Key thesis}
* {Actionable advice}

---

### 💡 Golden Nuggets & Key Quotes
* "{Direct quote or crucial insight}"

### 🛠️ Actionable Recommendations
- [ ] Task 1
- [ ] Task 2
```
