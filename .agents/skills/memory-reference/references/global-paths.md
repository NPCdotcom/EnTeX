# Global memory paths

**Cursor user home** — OS 共通 convention:

| OS | Path |
|----|------|
| Windows | `%USERPROFILE%\.agents\memory\global\` |
| macOS / Linux | `~/.agents/memory/global/` |

## Resolve at runtime

1. If workspace env or shell exposes `USERPROFILE` / `HOME`, use above
2. Else infer from known user profile (Windows: `C:\Users\<user>\.agents\memory\global\`)
3. If global `index.yaml` missing → skip global recall; note in recall report `global_index: missing`

## Bootstrap

Copy kit template:

```text
skills/memory-reference/assets/global/index.yaml.example
  → %USERPROFILE%\.agents\memory\global\index.yaml
```

Create dirs: `knowledge/{philosophy,lessons,preferences}/`

## project_id（任意）

When linking global entry to a specific repo:

```yaml
project_id: "github.com/org/repo"   # preferred: git remote origin URL
# or
project_id: "my-game-client"        # workspace folder basename
```

Resolve: `git remote get-url origin` when available; else workspace root folder name.

## Read/write

| Skill | Global access |
|-------|---------------|
| memory-reference | Read index + budgeted files |
| memory-reason | Propose scope global vs project |
| memory-flush | Route content by scope |
| memory-record | Write global paths when scope=global |

Do not write project episodes/threads to global paths.
