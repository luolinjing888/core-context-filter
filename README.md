# Core Context Filter

Turn noisy raw information into task-ready AI context.

Core Context Filter is a Codex skill for preventing agent information overload. It helps an AI agent receive long articles, X/Twitter threads, transcripts, reports, PDFs, pasted notes, or scraped pages without dumping all of that raw content into the working context.

Instead of asking the agent to read everything, the skill converts raw information into:

- **Core Context**: what the agent actually needs to act
- **Execution Implications**: what should change in the agent's next steps
- **Reference Map**: source anchors that preserve traceability
- **Discarded / Deferred Context**: what was intentionally ignored or parked
- **Uncertainty / Follow-Up**: what still needs verification

The result is lower token cost, less context pollution, and better execution reliability.

## Why This Exists

Agents often fail because the context window fills with material that is interesting but not operationally necessary. A strong article may contain:

- background storytelling
- social proof
- examples that do not apply to the current project
- duplicated claims
- engagement bait
- useful evidence mixed with commentary

Core Context Filter keeps the useful signal while preserving enough reference structure to revisit the full source later.

## Use Cases

- Convert an X thread into a startup task brief
- Extract only role-relevant insights from a job market article
- Turn a long market research report into an Etsy product validation packet
- Filter a technical blog post into implementation requirements
- Convert PR / branding articles into execution-ready communication strategy
- Prevent multi-agent systems from passing oversized raw material between departments

## Install

Clone this repository, then copy the skill folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R core-context-filter ~/.codex/skills/
```

Restart Codex or open a new thread if your environment requires skill reload.

## Invoke

```text
Use $core-context-filter to turn this raw X thread into a core-context handoff for the entrepreneurship department.
```

```text
Use $core-context-filter on this article. Keep only what the employment department needs for resume/portfolio optimization.
```

## Example Output

```markdown
# Core Context Handoff

## Intended Agent
- Role: Entrepreneurship department
- Task: Improve Etsy digital product quality

## Core Context
- Bestselling products show three repeated patterns: clear preview images, explicit deliverable counts, and outcome-focused titles.
- Pricing clusters around low-friction impulse purchases.

## Execution Implications
- Add product-preview acceptance criteria before generating new assets.
- Compare each draft against the top-selling reference structure.

## Reference Map
| Core point | Source reference | Why it matters |
|---|---|---|
| Preview images drive trust | Source paragraph 4 | Converts raw research into quality criteria |

## Discarded / Deferred Context
- Dropped: personal anecdotes, creator backstory, engagement prompts.

## Uncertainty / Follow-Up
- Verify sales estimates with a second marketplace source.
```

## Included Helper Script

For local text or Markdown files:

```bash
python core-context-filter/scripts/filter_context.py input.txt \
  --agent "employment department" \
  --task "extract portfolio optimization insights" \
  --out handoff.md
```

The script creates a first-pass packet. Review it before sending it to another agent.

## Design Principles

- Preserve source traceability.
- Compress aggressively but honestly.
- Never turn speculation into fact.
- Treat third-party source instructions as untrusted content.
- Make the receiving agent's next action clearer, not just shorter.

## Suggested Repository Topics

`codex-skill`, `ai-agents`, `context-engineering`, `prompt-engineering`, `information-filtering`, `token-optimization`, `multi-agent`

## License

MIT
