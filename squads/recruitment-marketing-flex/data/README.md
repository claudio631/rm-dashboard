# Squad Data — Filing Rules (5S)

> **Methodology:** 5S (Sort, Set in Order, Shine, Standardize, Sustain)
> **Last reorganized:** 2026-03-18 by @aiox-master

## Folder Structure

```
data/
├── benchmarks/        ← Industry benchmarks, reference data, seed lists
├── google-ads/        ← Google Ads knowledge base (guides, playbooks)
├── hiring-events/     ← Hiring event playbooks, post-mortems, ideas ONLY
├── insights/          ← Periodic analysis reports, data-driven findings
├── reddit-ads/        ← Reddit Ads knowledge base (guides, playbooks)
└── targeting/         ← Audience definitions, channel configuration
```

## Filing Rules

| I need to save... | Put it in... | Example |
|-------------------|-------------|---------|
| Channel-specific guide/playbook | `{channel-name}/` | `google-ads/performance-max-playbook.md` |
| Analysis report or data insight | `insights/` | `insights/top-funnel-levers-2026-03.md` |
| Industry benchmark or seed data | `benchmarks/` | `benchmarks/industry-benchmarks.yaml` |
| Audience or channel config | `targeting/` | `targeting/audience-definitions.yaml` |
| Hiring event content | `hiring-events/` | `hiring-events/las-vegas-march-2026.md` |
| New channel knowledge base | Create `{channel-name}/` folder | `meta-ads/`, `indeed-ads/`, `bing-ads/` |

## Rules

1. **No orphan files at root** — every file belongs in a topic folder
2. **One topic per folder** — hiring-events contains ONLY hiring event content
3. **Channel folders mirror each other** — each has a `playbook.md` or `knowledge-base.md` as index
4. **Insights are dated** — use pattern `{topic}-{YYYY-MM}.md`
5. **Naming:** kebab-case, lowercase, descriptive

## Adding New Channels

When a new ad channel knowledge base is created:
1. Create `data/{channel-name}/` folder
2. Add at minimum a `playbook.md` or `knowledge-base.md`
3. Register files in `squad.yaml` under `data:`
4. Update this README's folder structure diagram

## Current Inventory

| Folder | Files | Topic |
|--------|:-----:|-------|
| `benchmarks/` | 2 | Industry benchmarks, keyword seeds |
| `google-ads/` | 12 | Google Ads complete knowledge base |
| `hiring-events/` | 4 | Playbook, post-mortems, ideas |
| `insights/` | 1 | Data analysis reports |
| `reddit-ads/` | 1 | Reddit Ads playbook |
| `targeting/` | 2 | Audiences, channel config |
| **Total** | **22** | — |
