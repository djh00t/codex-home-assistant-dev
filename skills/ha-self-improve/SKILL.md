---
name: ha-self-improve
description: Use when capturing recurring Home Assistant development lessons, proposing updates to this plugin's skills, references, or scripts, validating those updates with subagents, and keeping the plugin self-improving without silently changing live guardrails.
---

# Home Assistant Self Improvement

Self-improvement is draft-patch by default. Capture evidence, propose a change, validate it, and leave behavior changes reviewable.

## Workflow

1. Capture the exact symptom, command, log line, path, and resolution.
2. Classify the lesson as workflow, guardrail, artifact validation, cache busting, release, or model/subagent routing.
3. Propose a concrete patch to one skill, one reference, or one script.
4. Forward-test with a subagent when practical using a realistic prompt and minimal leaked context.
5. Run `quick_validate.py` for changed skills and script smoke tests for changed scripts.
6. Report the evidence and the proposed plugin update. Do not silently rewrite guardrails after one noisy run.

## Good Lesson Criteria

- Reproducible or likely to recur.
- Specific enough to change behavior.
- Backed by command output, logs, or a live artifact.
- Not just a stale one-off site state.
