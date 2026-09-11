---
geo_doc_id: geo.meta.index
geo_doc_topic: geoscience
geo_doc_kind: meta
geo_doc_tags: [index, regex]
geo_doc_regex_file: ^geo\-doc\-meta\-INDEX\.md$
---

<!-- GEO_DOC_ID: geo.meta.index -->
<!-- GEO_DOC_KIND: meta -->
<!-- GEO_DOC_TOPIC: geoscience -->

# 地学ドキュメント索引

`documents/` 直下のフラット配置。各ファイルは **単体完結** の地学文書（学習フェーズ・サイクル情報なし）。

## 正規表現

```text
全件:     ^geo-doc-.*\.(md|yaml)$
トピック: ^geo-doc-(?!meta-)[a-z0-9-]+\.md$
ID:       <!-- GEO_DOC_ID: ([\w.]+) -->
トピック: geo_doc_topic: geoscience
```

## 一覧（27 件）

### メタ

- `geo-doc-geoscience-overview.md` — `geo.topic.overview`

### 固体地球

- `geo-doc-geology.md` — `geo.topic.geology`
- `geo-doc-stratigraphy.md` — `geo.topic.stratigraphy`
- `geo-doc-sedimentology.md` — `geo.topic.sedimentology`
- `geo-doc-structural-geology.md` — `geo.topic.structural_geology`
- `geo-doc-historical-geology.md` — `geo.topic.historical_geology`
- `geo-doc-paleontology.md` — `geo.topic.paleontology`
- `geo-doc-petrology.md` — `geo.topic.petrology`
- `geo-doc-mineralogy.md` — `geo.topic.mineralogy`
- `geo-doc-ore-deposits.md` — `geo.topic.ore_deposits`
- `geo-doc-volcanology.md` — `geo.topic.volcanology`

### 物理・化学地球

- `geo-doc-geochemistry.md` — `geo.topic.geochemistry`
- `geo-doc-geophysics.md` — `geo.topic.geophysics`
- `geo-doc-seismology.md` — `geo.topic.seismology`

### 流体地球

- `geo-doc-oceanography.md` — `geo.topic.oceanography`
- `geo-doc-atmospheric-science.md` — `geo.topic.atmospheric_science`
- `geo-doc-meteorology.md` — `geo.topic.meteorology`
- `geo-doc-climatology.md` — `geo.topic.climatology`

### 表面・水圏

- `geo-doc-cryosphere.md` — `geo.topic.cryosphere`
- `geo-doc-soil-science.md` — `geo.topic.soil_science`
- `geo-doc-physical-geography.md` — `geo.topic.physical_geography`
- `geo-doc-geodesy.md` — `geo.topic.geodesy`
- `geo-doc-geomorphology.md` — `geo.topic.geomorphology`
- `geo-doc-hydrology.md` — `geo.topic.hydrology`
- `geo-doc-limnology.md` — `geo.topic.limnology`

### 惑星

- `geo-doc-planetary-science.md` — `geo.topic.planetary_science`

### 横断統合

- `geo-doc-earth-structure.md` — `geo.topic.earth_structure`

- `geo-doc-meta-REGISTRY.yaml`
