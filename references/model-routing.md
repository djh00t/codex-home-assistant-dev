# Model and Thinking Routing

Use this reference when a Home Assistant task can be decomposed across agents or models.

## OpenAI Defaults

- Repo classification, release readiness, and checklist generation: fast/small model, low reasoning.
- Code edits, tests, and packaging fixes: coding-capable model, medium reasoning.
- Live deploy diagnosis, HA log interpretation, and subtle cache/runtime issues: stronger model, high reasoning.
- Architecture redesign or cross-repo release/deploy planning: strongest available model, high or extra-high reasoning.

## Anthropic Defaults

- Simple repo inspection and checklist generation: Haiku-class model, low thinking.
- Code edits and skill updates: Sonnet-class model, medium thinking.
- Live deploy diagnosis and production guardrails: Sonnet or Opus-class model, high thinking.
- Cross-repo release strategy and self-improvement design: strongest available model, high thinking.

## Other Providers

If the provider is neither OpenAI nor Anthropic, adjust thinking/reasoning level only:
- Low for classification and rote checklist work.
- Medium for scoped implementation.
- High for live system diagnosis, releases, and ambiguous failures.

## Subagent Guidance

Use subagents for independent validation, not for hidden policy decisions:
- Repo classifier pass.
- Skill forward-test pass.
- Release-readiness pass.
- Cache-busting/deploy-plan review.

Do not delegate the immediate blocking task if the main agent needs the result before taking the next local action.
