# OSMI 2016 — Unsupervised Learning zur Mitarbeitersegmentierung

Reproduzierbare Python-Pipeline zur unüberwachten Segmentierung von Beschäftigten
technologiebezogener Berufe auf Basis der Umfrage **OSMI „Mental Health in Tech 2016"**.
Der Code begleitet eine IU-Fallstudie (Modul DLBDSMLUSL01) und identifiziert über
Feature Engineering, Dimensionsreduktion und Clustering interpretierbare
Mitarbeitersegmente als Ansatzpunkte für ein betriebliches Präventionsprogramm.

> Dieses Repository enthält **ausschließlich den Code**. Der Rohdatensatz wird
> bewusst **nicht** mitveröffentlicht (personenbezogene Gesundheitsdaten, CC-BY-SA 4.0).

## Datenquelle

| | |
|---|---|
| Datensatz | OSMI Mental Health in Tech Survey 2016 |
| Bezug | Kaggle: `osmi/mental-health-in-tech-2016` |
| Lizenz | CC-BY-SA 4.0 |
| Umfang | 1.433 Befragte, 63 Fragen |

Lade die CSV von Kaggle und lege sie unter `archive/mental-heath-in-tech-2016_20161114.csv`
ab (Pfad relativ zum Projektwurzelverzeichnis, siehe `DATA_PATH` in `analyse.py`).

## Pipeline

1. **Explorative Analyse** — Dimensionalität, fehlende Werte je Spalte, Verteilungen.
2. **Feature Engineering**
   - Einschränkung auf Angestellte (Selbstständige überspringen die Arbeitgeberfragen).
   - Vereinheitlichung der freien Geschlechts-Texteingabe zu vier Kategorien.
   - Bereinigung unplausibler Altersangaben.
   - Auswahl modifizierbarer Arbeitsplatz-, Offenheits- und Wissensmerkmale als
     Clustering-Basis; Erkrankungs- und Behandlungsstatus dienen nur der Beschreibung.
   - Imputation (häufigster Wert bzw. Median), One-Hot-Encoding, Standardisierung,
     gebündelt in einer `scikit-learn`-Pipeline.
3. **Dimensionsreduktion** — PCA (Komponentenzahl über ≥ 80 % erklärte Varianz),
   t-SNE und UMAP zur zweidimensionalen Visualisierung.
4. **Clustering** — k-Means mit Auswahl der Clusteranzahl über Silhouettenkoeffizient
   und Elbow-Methode; hierarchisches Clustering und DBSCAN zur Robustheitsprüfung.
5. **Segmentinterpretation** — Größe, Durchschnittsalter und prägende Merkmale je
   Cluster über Lift-Analyse gegenüber der Gesamtverteilung.

## Reproduktion

```bash
git clone https://github.com/vvcrypt/osmi-mental-health-clustering.git
cd osmi-mental-health-clustering
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# CSV von Kaggle nach ./archive/ ablegen (siehe Abschnitt „Datenquelle")
python analyse.py
```

Sämtliche Zufallsprozesse sind über `RANDOM_STATE = 42` fixiert; der Lauf liefert
deterministisch dieselben Kennzahlen. Getestet mit Python 3.14.

### Ausgaben

- `output/r-results/results.json` und `results.md` — alle Kennzahlen.
- `assets/img/abb1…abb5*.png` — Abbildungen (PCA-Varianz, k-Auswahl, t-SNE, UMAP,
  Profil-Heatmap); identische Kopien unter `output/r-results/`.

## Ergebnisse des Referenzlaufs

- Analysepopulation: 1.146 Angestellte; 15 Cluster-Merkmale, nach One-Hot-Encoding
  51 Dimensionen.
- PCA: 18 Komponenten erklären 81,5 % der Varianz.
- k-Means: bestes **k = 2** (Silhouettenkoeffizient 0,118), Clustergrößen 439 und 707.
- Robustheit: adjustierter Rand-Index zwischen k-Means und hierarchischem Clustering
  0,56; DBSCAN findet einen dichten Kern mit 30 Rauschpunkten.
- Segment A (offenes, unterstützendes Arbeitsumfeld) gegenüber Segment B (von Stigma
  und Unsicherheit geprägtes Umfeld); beide Segmente weisen ähnliche Erkrankungs- und
  Behandlungsraten auf, unterscheiden sich also im wahrgenommenen Klima, nicht in der
  Belastung.

## Dateien

| Datei | Zweck |
|---|---|
| `analyse.py` | Vollständige Analyse-Pipeline |
| `requirements.txt` | Exakte Paketversionen des Referenzlaufs |
| `DATA_DICTIONARY.md` | Datenwörterbuch (Spaltentypen, fehlende Werte, Auffälligkeiten) |
| `results.example.json` | Erwartete Kennzahlen zur Verifikation |

## Lizenz

Der Code steht unter der MIT-Lizenz. Der zugrunde liegende Datensatz unterliegt der
CC-BY-SA 4.0 von Open Sourcing Mental Illness (OSMI) und ist nicht Teil dieses Repositories.
