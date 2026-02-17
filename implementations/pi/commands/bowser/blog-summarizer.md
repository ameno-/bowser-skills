---
description: Visit a blog, summarize the latest post, rate it
defaults:
  skill: playwright-bowser
  mode: headless
  vision: false
---

# Blog Summarizer

Visit a blog URL, find the latest post, summarize it, and give it a rating.

## Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `SKILL` | `playwright-bowser` | Headless browser |
| `MODE` | `headless` | No visible window |

## Workflow

1. Navigate to: {PROMPT} (the blog URL)
2. Verify the blog loads
3. Identify the latest blog post
4. Extract: title, author, date, and content
5. Create a concise summary (2-3 paragraphs)
6. Give it a rating out of 10 with brief justification
7. Report: title, author, summary, and rating

## Example Usage

```bash
pi "/bowser:hop-automate blog-summarizer 'https://simonwillison.net/'"
```

---

*Original implementation: [github.com/disler/bowser](https://github.com/disler/bowser)*
