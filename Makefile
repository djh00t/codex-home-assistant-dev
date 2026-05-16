.PHONY: check quality-gates install clean build publish validate-json validate-skills validate-scripts

PYTHON ?= python3
SKILL_VALIDATOR ?= /Users/djh/.codex/skills/.system/skill-creator/scripts/quick_validate.py

check: validate-json validate-skills validate-scripts

quality-gates: check

install:
	$(PYTHON) -m venv .venv
	.venv/bin/python -m pip install --upgrade pip

clean:
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
	find . -name '*.pyc' -delete
	rm -rf .pytest_cache .mypy_cache .ruff_cache build dist

build: check
	@echo "Plugin content is source-distributed; no build artifact required."

publish:
	@echo "Publish by tagging a GitHub release from the repository."

validate-json:
	$(PYTHON) -m json.tool .codex-plugin/plugin.json >/dev/null

validate-skills:
	@for skill in skills/*; do \
		$(PYTHON) $(SKILL_VALIDATOR) "$$skill"; \
	done

validate-scripts:
	$(PYTHON) -m py_compile scripts/*.py
	$(PYTHON) scripts/classify_ha_repo.py . >/tmp/codex-ha-dev-classify.json
	$(PYTHON) scripts/generate_deploy_plan.py . --host root@example-ha >/tmp/codex-ha-dev-deploy-plan.md
	$(PYTHON) scripts/cache_bust_checklist.py . >/tmp/codex-ha-dev-cache-checklist.md
	$(PYTHON) scripts/check_release_readiness.py . >/tmp/codex-ha-dev-release-readiness.md
