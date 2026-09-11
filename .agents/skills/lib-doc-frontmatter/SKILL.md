---
name: lib-doc-frontmatter
description: Shared YAML frontmatter and Facts/Assumptions/Open section rules for design, plan, and ADR markdown. Use when writing or reviewing docs under docs/design, docs/requirements, docs/adr, or .agents/plans.
---

# Library — document frontmatter

**Cross-cutting** · linked from design-record · plan-record · doc-record

## Required frontmatter keys

```yaml
title: 
kind: design|plan|adr|requirement
phase: P0|P1|P2|P3|P4|P5|P6
scope_level: H0|H1|H2|H3|H4|H5
status: draft|agreed|superseded
```

## Body sections (when applicable)

| Section | Purpose |
|---------|---------|
| Facts | Verified |
| Assumptions | Unverified — do not treat as Fact |
| Open | Unresolved questions |
| User `>` blocks | User scratch — do not delete |

## Do not

Duplicate this text inside each `*-record` skill — link here.

Details: [`references/frontmatter-spec.md`](references/frontmatter-spec.md)
