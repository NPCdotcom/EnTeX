---
chem_doc_id: chem.meta.index
chem_doc_topic: chemistry
chem_doc_kind: meta
chem_doc_tags: [index, regex]
chem_doc_regex_file: ^chem\-doc\-meta\-INDEX\.md$
---

<!-- CHEM_DOC_ID: chem.meta.index -->
<!-- CHEM_DOC_KIND: meta -->
<!-- CHEM_DOC_TOPIC: chemistry -->

# 化学ドキュメント索引

`documents/` 直下のフラット配置。各ファイルは **単体完結** の化学文書（学習フェーズ・サイクル情報なし）。

## 正規表現

```text
全件:     ^chem-doc-.*\.(md|yaml)$
トピック: ^chem-doc-(?!meta-)[a-z0-9-]+\.md$
ID:       <!-- CHEM_DOC_ID: ([\w.]+) -->
トピック: chem_doc_topic: chemistry
```

## 一覧（20 件）

### 基礎・分野

- `chem-doc-chemistry-overview.md` — `chem.topic.overview`
- `chem-doc-elements-atoms.md` — `chem.topic.elements_atoms`
- `chem-doc-molecular-structure-bonding.md` — `chem.topic.molecules_bonding`
- `chem-doc-chemical-reactions-stoichiometry.md` — `chem.topic.chemical_reactions`
- `chem-doc-physical-chemistry.md` — `chem.topic.physical_chemistry`
- `chem-doc-inorganic-coordination-chemistry.md` — `chem.topic.inorganic`
- `chem-doc-organic-chemistry.md` — `chem.topic.organic`
- `chem-doc-polymer-chemistry.md` — `chem.topic.polymer`
- `chem-doc-biochemistry.md` — `chem.topic.biochemistry`
- `chem-doc-analytical-chemistry.md` — `chem.topic.analytical`
- `chem-doc-applied-environmental-chemistry.md` — `chem.topic.applied_environmental`

### 深化（計算・反応・エネルギー移動）

- `chem-doc-catalysis-reaction-kinetics.md` — `chem.topic.catalysis_kinetics`
- `chem-doc-electrochemistry-photochemistry.md` — `chem.topic.electrochemistry_photochemistry`
- `chem-doc-computational-quantum-chemistry.md` — `chem.topic.computational_quantum`
- `chem-doc-molecular-dynamics.md` — `chem.topic.molecular_dynamics`
- `chem-doc-free-energy-calculations.md` — `chem.topic.free_energy`
- `chem-doc-pmf-enhanced-sampling.md` — `chem.topic.pmf_sampling`
- `chem-doc-marcus-electron-transfer.md` — `chem.topic.marcus_et`
- `chem-doc-machine-learning-potentials.md` — `chem.topic.ml_potentials`
- `chem-doc-photochemical-energy-transfer.md` — `chem.topic.photochemical_et`

- `chem-doc-meta-REGISTRY.yaml`
