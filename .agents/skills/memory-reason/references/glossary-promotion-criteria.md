# Glossary promotion criteria

Used by **memory-reason** after **terminology-research** or when term appears in episodes/alignment.

| ID | Criterion | Effect |
|----|-----------|--------|
| G1 | Same term in **2+ turns** OR `knowledge/alignment/<term>.md` exists | **candidate** |
| G2 | Project-specific definition writable in **1 paragraph** | update alignment |
| G3 | External source URL from terminology-research | treat as Fact for alignment |
| G4 | User Go **OR** P2+ gate pass for requirements track | **doc-record → docs/glossary/** allowed |
| G5 | Definition still Assumption-only | **no promote** — episode/Open only |

## Agent output

For each term: `candidate | promote | hold | reject` + criteria ids + suggested path.

If `promote` and G4 met → add **role-execute** row: `spec_designer` + `doc-record`.

If G1-G3 but not G4 → brief **Conditional Go** + user confirm question.

## Link

- alignment file: `.agents/memory/knowledge/alignment/<slug>.md` (**scope: project**)
- canonical: `docs/glossary/<slug>.md` (**scope: team**)
- index: project + team entries with `linked: [each other]`
