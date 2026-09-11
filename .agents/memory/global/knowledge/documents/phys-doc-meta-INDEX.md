---
phys_doc_id: phys.meta.index
phys_doc_topic: physics
phys_doc_kind: meta
phys_doc_tags: [index, regex]
phys_doc_regex_file: ^phys\-doc\-meta\-INDEX\.md$
---

<!-- PHYS_DOC_ID: phys.meta.index -->
<!-- PHYS_DOC_KIND: meta -->
<!-- PHYS_DOC_TOPIC: physics -->

# 物理学ドキュメント索引

`documents/` 直下のフラット配置。各ファイルは **単体完結** の物理学文書。

## 正規表現

```text
全件:     ^phys-doc-.*\.(md|yaml)$
トピック: ^phys-doc-(?!meta-)[a-z0-9-]+\.md$
ID:       <!-- PHYS_DOC_ID: ([\w.]+) -->
トピック: phys_doc_topic: physics
PACS:     phys_doc_pacs: (任意)
```

## 一覧（25 件）

### 基礎

- `phys-doc-physics-overview.md` — `phys.topic.overview`
- `phys-doc-classical-mechanics.md` — `phys.topic.classical_mechanics`
- `phys-doc-waves-oscillations.md` — `phys.topic.waves_oscillations`
- `phys-doc-thermodynamics-statistical-mechanics.md` — `phys.topic.thermo_stat_mech`
- `phys-doc-electromagnetism.md` — `phys.topic.electromagnetism`
- `phys-doc-optics.md` — `phys.topic.optics`
- `phys-doc-quantum-mechanics.md` — `phys.topic.quantum_mechanics`
- `phys-doc-relativity-gravitation.md` — `phys.topic.relativity_gravitation`
- `phys-doc-computational-physics.md` — `phys.topic.computational_physics`
- `phys-doc-applied-mathematical-physics.md` — `phys.topic.applied_math_physics`

### 観測宇宙論 · 重力波 · 天体

- `phys-doc-gravitational-wave-astronomy.md` — `phys.topic.gw_astronomy`
- `phys-doc-pulsar-timing-arrays.md` — `phys.topic.pulsar_timing`
- `phys-doc-cosmological-observations.md` — `phys.topic.cosmological_observations`
- `phys-doc-mhd-black-hole-imaging.md` — `phys.topic.mhd_eht`
- `phys-doc-astrophysics-neutron-stars.md` — `phys.topic.neutron_stars`
- `phys-doc-radiative-transfer-astrophysics.md` — `phys.topic.radiative_transfer`
- `phys-doc-cosmic-rays-acceleration.md` — `phys.topic.cosmic_rays`

### プラズマ · 核融合 · 惑星

- `phys-doc-fusion-plasma-heating.md` — `phys.topic.fusion_heating`
- `phys-doc-plasma-physics-diagnostics.md` — `phys.topic.plasma_diagnostics`
- `phys-doc-exoplanet-atmospheres.md` — `phys.topic.exoplanet_atmospheres`

### 量子 · 物性 · 高エネ

- `phys-doc-quantum-optomechanics.md` — `phys.topic.optomechanics`
- `phys-doc-quantum-information-metrology.md` — `phys.topic.quantum_metrology`
- `phys-doc-condensed-matter-quantum-transport.md` — `phys.topic.condensed_matter`
- `phys-doc-particle-nuclear-physics.md` — `phys.topic.particle_nuclear`
- `phys-doc-lattice-qcd-gauge-theory.md` — `phys.topic.lattice_qcd`

- `phys-doc-meta-REGISTRY.yaml`
