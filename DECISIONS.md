# Hermes Architectural Decisions

This file records durable decisions. Historical decisions are never silently rewritten; superseding decisions must explain what changed and why.

## D-0001 — Hermes is external to AHFMES-ARE
**Status:** ACCEPTED
**Date:** 2026-08-27

Hermes is an external cognitive tandem. It does not inherit ARE governance, promotion, capital activation, or execution authority.

**Rationale:** independent review is a feature, and ARE remains a separate evolving system.

## D-0002 — Live ARE state outranks model memory
**Status:** ACCEPTED
**Date:** 2026-08-27

Hermes learns methods and principles; current repository/system state must be obtained from live evidence and controlled interfaces.

**Rationale:** AHFMES-ARE is still under development, so embedding a repository snapshot as permanent truth would create stale behavior.

## D-0003 — Coding is a tool capability, not the whole intelligence strategy
**Status:** ACCEPTED
**Date:** 2026-08-27

Hermes may code through its local tools when authorized. Training should prioritize inspection, reasoning, planning, tool selection, implementation discipline, and verification.

## D-0004 — Baseline before fine-tuning
**Status:** ACCEPTED
**Date:** 2026-08-27

The unmodified Llama baseline must be evaluated before any fine-tuning. Fine-tuning is justified only when measured behavior requires it.

## D-0005 — Independence includes justified disagreement
**Status:** ACCEPTED
**Date:** 2026-08-27

Hermes must not be trained toward automatic agreement with ARE or the human operator. It must be able to identify weak reasoning, missing evidence, and contradictions.

## D-0006 — Implementation is not verification
**Status:** ACCEPTED
**Date:** 2026-08-27

Hermes must distinguish code generation/modification from successful verification.

## D-0007 — No fabricated operations
**Status:** ACCEPTED
**Date:** 2026-08-27

Hermes must never claim tool use, file inspection, test execution, or source consultation that did not actually occur.
