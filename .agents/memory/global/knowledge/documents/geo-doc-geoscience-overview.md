---
geo_doc_id: geo.topic.overview
geo_doc_topic: geoscience
geo_doc_kind: topic
geo_doc_tags: [overview]
geo_doc_regex_file: ^geo\-doc\-geoscience\-overview\.md$
---

<!-- GEO_DOC_ID: geo.topic.overview -->
<!-- GEO_DOC_KIND: topic -->
<!-- GEO_DOC_TOPIC: geoscience -->


# 地球科学の全体像

**出典**: [地球科学（Wikipedia）](https://ja.wikipedia.org/wiki/%E5%9C%B0%E7%90%83%E7%A7%91%E5%AD%A6) · [Portal:地球科学](https://ja.wikipedia.org/wiki/Portal:%E5%9C%B0%E7%90%83%E7%A7%91%E5%AD%A6)

---

## 地球科学とは

**地球科学**（earth science / geoscience）は、地球磁気圏から内核に至る地球現象を研究する学問の総称。**地学**はその日本語略称。惑星科学を含め **地球惑星科学** と呼ぶ場合もある。

| 研究スケール | 例 |
|--------------|-----|
| 全球 · 内部 | マントル対流 · 地磁気 · 核 |
| 岩石圏 | 地層 · 断層 · 火山 |
| 流体圏 | 大気 · 海洋 · 河川 |
| 表面 | 地形 · 土壌 · 氷河 |
| 宇宙 | 太陽系 · 比較惑星学 |

## 学問分野の地図

Portal:地球科学 は学問を **関連学問** · **関連トピック** · **研究対象** の三層で整理する。本ドキュメント群は主要学問ごとに **単体完結** の文書として格納する（`geo-doc-*`）。

### 固体地球

- **地質学** — `geo-doc-geology.md`
- **層序学** — `geo-doc-stratigraphy.md`
- **堆積学** — `geo-doc-sedimentology.md`
- **構造地質学** — `geo-doc-structural-geology.md`
- **地史学** — `geo-doc-historical-geology.md`
- **古生物学** — `geo-doc-paleontology.md`
- **岩石学** — `geo-doc-petrology.md`
- **鉱物学** — `geo-doc-mineralogy.md`
- **鉱床学** — `geo-doc-ore-deposits.md`
- **火山学** — `geo-doc-volcanology.md`

### 物理・化学地球

- **地球化学** — `geo-doc-geochemistry.md`
- **地球物理学** — `geo-doc-geophysics.md`
- **地震学** — `geo-doc-seismology.md`

### 流体地球

- **海洋学** — `geo-doc-oceanography.md`
- **大気科学** — `geo-doc-atmospheric-science.md`
- **気象学** — `geo-doc-meteorology.md`
- **気候学** — `geo-doc-climatology.md`

### 表面・水圏

- **雪氷学** — `geo-doc-cryosphere.md`
- **土壌学** — `geo-doc-soil-science.md`
- **自然地理学** — `geo-doc-physical-geography.md`
- **測地学** — `geo-doc-geodesy.md`
- **地形学** — `geo-doc-geomorphology.md`
- **水文学** — `geo-doc-hydrology.md`
- **陸水学** — `geo-doc-limnology.md`

### 惑星

- **惑星科学** — `geo-doc-planetary-science.md`

### 横断統合

- **地球の構造** — `geo-doc-earth-structure.md`

## 三つの柱

```text
  地質学（物質と歴史）
  地球物理学（物理場と内部）
  地球化学（組成と循環）
        |
  流体・表面・惑星科学が外側を包む
```

## エージェント識別

```text
全件:     ^geo-doc-.*\.(md|yaml)$
トピック: ^geo-doc-(?!meta-)[a-z0-9-]+\.md$
ID:       <!-- GEO_DOC_ID: ([\w.]+) -->
トピック: geo_doc_topic: geoscience
```

索引: `geo-doc-meta-INDEX.md` · レジストリ: `geo-doc-meta-REGISTRY.yaml`
