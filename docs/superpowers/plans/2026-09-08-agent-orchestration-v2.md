# Agent orchestration v2 implementation plan

> For agentic workers: execute this approved plan task-by-task with test-driven development and verification before completion.

**Goal:** Implement the attached provider-neutral multi-agent architecture without weakening the existing release boundary.

**Architecture:** A strict registry and immutable DAG coordinate independently authored component instances. Repository adapters translate their evidence into existing schemas; the old release authority remains final.

**Tech stack:** Python 3.10+, unittest, jsonschema Draft 2020-12, referencing, existing python-pptx/PyMuPDF audits.

**Spec:** `docs/superpowers/specs/2026-09-08-agent-orchestration-v2-design.md`

## Global constraints

Context and component-record remain schema 2; content and manifest remain schema 3.
Keep v1 registry compatibility. Never fabricate independent review or release evidence.
No changes to calibrated year-profile or teaching contracts. Never merge main as part of implementation.

## 1. Registry, schema and source identity

Files: nine `schemas/*.schema.json`, `skills/registry.v2.json`,
`scripts/agent_protocol.py`, `scripts/agent_registry.py`, `scripts/build_execution_plan.py`.

- [x] Write failing unittest assertions for unique roles, local schema resolution,
  traversal rejection, frozen-source hashes and repeated-owner DAG nodes.
- [x] Run `python -m unittest discover -s tests -p 'test_agent*.py' -v` and confirm
  the missing implementation is the cause.
- [x] Implement `AgentRegistry.load()`, `validate_json(payload, schema)`,
  `freeze_context(context, registry, source_root)` and
  `build_execution_plan(context, registry)` with exact plan validation.
- [x] Verify the above tests and the existing runtime compatibility tests.

## 2. Handoffs, state, bounded parallel authoring

Files: `scripts/agent_adapter.py`, `scripts/agent_orchestrator.py`,
`scripts/agent_state.py`, `scripts/validate_agent_artifacts.py`,
`agents/maths-critic.md`, tests.

- [x] Test wrong owner/profile/run, missing checks, excessive time, shared actor,
  repeated instances, actual concurrency, immutable attempts and exhausted repairs.
- [x] Implement async provider-neutral invocations, trusted command envelopes,
  copied projections, host-receipt checks, persistent state and cumulative budgets.
- [x] Aggregate canonical records without rewriting content or evidence.
- [x] Verify tests including an executable local synthetic host adapter.

## 3. Assembly, independent QA, repairs and release bridge

Files: `scripts/agent_pipeline.py`, orchestrator, tests.

- [x] Test stale hashes, incomplete coverage, false PASS, wrong repair destination,
  missing renders, manifest path escapes and missing release evidence.
- [x] Stage through existing runtime, retain all declared assets, derive expected
  checks from pack_evidence, export actual host receipts and batch owner repairs.
- [x] Re-run all applicable QA after each repair and delegate release unchanged.
- [x] Test a real minimal PPTX/briefing staging boundary and real rejection paths;
  mark synthetic test-host releases explicitly as tests, not live acceptance.

## 4. Runtime, packaging and operating documentation

Files: `scripts/dlp_build_runtime.py`, package builders/auditor, `SKILL.md`,
`requirements.txt`, `.github/workflows/dlp-tests.yml`, docs and the documented host configuration contract.

- [x] Load generator ownership from the validated registry; reject mismatched run IDs.
- [x] Set pack QA to explicit-only invocation.
- [x] Include every new runtime dependency/schema/agent reference in complete packages.
- [x] Run full unittest suite, compilation, package creation and extracted-package
  audits.
- [ ] Publish an implementation PR and verify GitHub checks before reporting.
