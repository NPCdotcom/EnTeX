# Generic review standards

Project-specific rules: **AGENTS.md** and **.agents/rules/local/**.

## Universal

- Public APIs typed and named clearly
- Errors handled at boundaries; no silent swallow
- No secrets in repo
- Comments explain why, not what
- Diff stays within stated scope

## Structure

- Separate presentation, domain logic, and infrastructure where applicable
- Avoid god objects and duplicated business rules

## Tests

- Flag missing tests for criteria marked testable in the plan

## Anti-patterns

| Pattern | Why flag |
|---------|----------|
| Spec behavior only in code | Drift; link `docs/design/` |
| Scope beyond plan | Needs plan_slicer |
| Hot path work without measurement note | Premature or risky optimization |
