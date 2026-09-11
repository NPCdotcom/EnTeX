# Generic implementation standards

Stack-specific: **AGENTS.md** and **rules/local/**.

## Scope

- Smallest change that satisfies the criterion
- One logical concern per commit-sized batch

## Quality

- Readable names; English identifiers unless AGENTS.md says otherwise
- Fail loudly at boundaries; avoid silent nil access
- Reuse project utilities before adding parallel helpers

## Architecture

- Separate decision logic from bulk computation where the project already does
- State changes only at documented simulation boundaries

## Verification

- State how to verify each acceptance criterion（editor steps, test command, or manual scenario）

## Anti-patterns

| Pattern | Avoid |
|---------|--------|
| Implementing undiscussed rules | Spec gap |
| Large refactor while adding feature | Out of plan Scope |
| Copy-paste plan text into comments | Link paths instead |
