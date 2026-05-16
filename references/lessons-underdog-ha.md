# Lessons from UnderDog HA

Use this reference when the task touches live Home Assistant deployment, source automation, cache invalidation, backfill, or release handoff.

## Merge Means Deploy Handoff

When the user says a Home Assistant PR is merged, treat it as a signal to prepare the live deploy handoff if the project has a known HA target. Do not stop at GitHub state.

## Validate the Right Tree

If local checkout state is stale, dirty, detached, or otherwise not the merged tree, use a clean worktree or snapshot and state exactly what was validated.

If a GitHub tarball snapshot is used, `git diff --check` can fail because the snapshot has no `.git` directory. Report substantive checks separately instead of mislabeling that as a code regression.

## Backup and Restart Interpretation

Always take and record a Home Assistant backup before live writes. After restarting Core, an active `home_assistant_core_restart` Supervisor job can be a normal restart artifact. Wait and re-poll before calling the deploy unhealthy.

## Daily Collection vs Backfill

Answer live ingestion status by source. Separate:
- daily rolling catch-up
- compaction
- one-time historical backfill
- impossible-to-reconstruct forecast snapshots

Forecast snapshots cannot be recreated for dates before they were captured. Only observed or actual history can be backfilled from retained local data or external archives.

## Concrete UnderDog HA Paths

- Repo mirror: `/config/underdog_ha_shadow/repo`
- Custom component: `/config/custom_components/underdog_ha`
- AEMO actuals marker: `/config/underdog_ha_shadow/weather/aemo-rooftop-pv-actual.jsonl.maintenance.json`
- Compacted sources seen in prior runs: `weather-forecasts.jsonl`, `aemo-rooftop-pv-forecast.jsonl`, `aemo-rooftop-pv-actual.jsonl`
