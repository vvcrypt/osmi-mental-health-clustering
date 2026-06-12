#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unsupervised-Learning-Pipeline fuer den OSMI-Datensatz "Mental Health in Tech 2016".

Reproduzierbare Segmentierung von Beschaeftigten technologiebezogener Berufe ueber
Feature Engineering, Dimensionsreduktion (PCA, t-SNE, optional UMAP) und Clustering
(k-Means mit Silhouetten-/Elbow-Auswahl, hierarchisch und DBSCAN zur Robustheitspruefung).

Datenquelle: Kaggle "osmi/mental-health-in-tech-2016" (CC-BY-SA 4.0).
Der Rohdatensatz wird NICHT mitveroeffentlicht; lokaler Pfad siehe DATA_PATH.

Aufruf:
    python analyse.py

Alle Zufallsprozesse sind ueber RANDOM_STATE fixiert, der Lauf ist damit reproduzierbar.
"""
from __future__ import annotations

import json
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.manifold import TSNE
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

warnings.filterwarnings("ignore")

# ----------------------------------------------------------------------------
# Konfiguration
# ----------------------------------------------------------------------------
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

HERE = Path(__file__).resolve().parent


def _find_base() -> Path:
    """Projektwurzel robust bestimmen: funktioniert, wenn analyse.py im
    Wurzelverzeichnis des heruntergeladenen Repositorys liegt ebenso wie
    eingebettet unter scripts/ml/ im Gesamtprojekt. Gesucht wird das erste
    Verzeichnis (von hier aufwaerts), das einen Ordner "archive" enthaelt."""
    for cand in (HERE, HERE.parent, HERE.parent.parent):
        if (cand / "archive").is_dir():
            return cand
    return HERE


PROJECT = _find_base()
DATA_PATH = PROJECT / "archive" / "mental-heath-in-tech-2016_20161114.csv"

# Ausgaben: Abbildungen fuer die Einbettung + Rohausgaben fuer die Dokumentation.
ASSETS_IMG = PROJECT / "assets" / "img"
RAW_OUT = PROJECT / "output" / "r-results"
ASSETS_IMG.mkdir(parents=True, exist_ok=True)
RAW_OUT.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", context="paper")
PALETTE = "tab10"


def find_col(df: pd.DataFrame, needle: str) -> str | None:
    """Findet eine Spalte ueber einen eindeutigen Teilstring (Spaltennamen sind sehr lang)."""
    needle = needle.lower()
    matches = [c for c in df.columns if needle in c.lower()]
    if not matches:
        return None
    # kuerzeste passende Spalte bevorzugen, um Teilstring-Mehrdeutigkeit zu vermeiden
    return min(matches, key=len)


# Kuratiertes, inhaltlich begruendetes Feature-Set. Rolle "cluster": modifizierbare
# Arbeitsplatz-, Offenheits- und Wissensmerkmale, an denen ein Praeventionsprogramm
# ansetzt; diese bilden die Merkmalsmatrix. Rolle "profile": persoenlicher
# Erkrankungs-/Behandlungsstatus, der die gefundenen Segmente nachtraeglich
# charakterisiert, aber nicht in die Gruppierung eingeht (er ist Ergebnis, nicht
# modifizierbarer Ansatzpunkt). Schluessel = (Kurzname, Teilstring, Rolle).
CORE_FEATURES = [
    ("benefits", "mental health benefits as part of healthcare coverage", "cluster"),
    ("know_options", "know the options for mental health care available under your employer", "cluster"),
    ("formal_discussion", "formally discussed mental health", "cluster"),
    ("resources", "offer resources to learn more about mental health concerns", "cluster"),
    ("anonymity", "anonymity protected if you choose to take advantage", "cluster"),
    ("leave", "medical leave from work", "cluster"),
    ("neg_cons_employer", "discussing a mental health disorder with your employer would have negative", "cluster"),
    ("comfort_coworkers", "comfortable discussing a mental health disorder with your coworkers", "cluster"),
    ("comfort_supervisor", "comfortable discussing a mental health disorder with your direct supervisor", "cluster"),
    ("seriousness", "takes mental health as seriously as physical health", "cluster"),
    ("observed_neg", "heard of or observed negative consequences for co-workers who have been open", "cluster"),
    ("hurt_career", "being identified as a person with a mental health issue would hurt your career", "cluster"),
    ("coworkers_negative", "team members/co-workers would view you more negatively", "cluster"),
    ("gender", "what is your gender", "cluster"),
    ("age", "what is your age", "cluster"),
    ("family_history", "family history of mental illness", "profile"),
    ("past_disorder", "had a mental health disorder in the past", "profile"),
    ("current_disorder", "do you currently have a mental health disorder", "profile"),
    ("sought_treatment", "sought treatment for a mental health issue from a mental health professional", "profile"),
]


def clean_gender(value) -> str:
    """Vereinheitlicht die freie Geschlechts-Texteingabe zu vier Kategorien."""
    if pd.isna(value):
        return "k. A."
    v = str(value).strip().lower()
    male = {"male", "m", "man", "cis male", "cis man", "male.", "mail", "malr",
            "male (cis)", "cisdude", "dude", "sex is male", "i'm a man why didn't you make this a drop down question. you should of asked sex? and i would of answered yes please. seriously how much text can this take?",
            "male 9:1 female, roughly", "m|", "male/genderqueer"}
    female = {"female", "f", "woman", "cis female", "cis-woman", "cis woman", "fem",
              "female assigned at birth", "female (props for making this a freeform field, though)",
              "i identify as female.", "female or multi-gender femme", "female/woman", "fm"}
    v_norm = v.replace(".", "").replace("(", "").replace(")", "").strip()
    if v_norm in {"male", "m", "man", "cis male", "cis man", "mail", "malr", "dude", "cisdude", "sex is male"}:
        return "maennlich"
    if v_norm in {"female", "f", "woman", "cis female", "cis woman", "cis-woman", "fem", "femake", "female assigned at birth", "fm"}:
        return "weiblich"
    # Heuristik fuer die zahlreichen Freitextvarianten
    if v_norm.startswith("male") or v_norm.startswith("m ") or v == "m" or "man" in v_norm.split() or v_norm in male:
        return "maennlich"
    if v_norm.startswith("female") or v_norm.startswith("f ") or v == "f" or "woman" in v_norm.split() or v_norm in female:
        return "weiblich"
    if any(t in v_norm for t in ["trans", "non-binary", "nonbinary", "non binary", "genderqueer",
                                 "fluid", "queer", "androgyn", "enby", "agender", "nb", "neutral",
                                 "bigender", "all", "other", "human", "unicorn"]):
        return "divers/nichtbinaer"
    return "divers/nichtbinaer"


def main() -> dict:
    print(f"Lade Datensatz: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    n_rows, n_cols = df.shape
    print(f"Rohdaten: {n_rows} Zeilen x {n_cols} Spalten")

    results: dict = {
        "random_state": RANDOM_STATE,
        "raw_shape": [int(n_rows), int(n_cols)],
    }

    # ------------------------------------------------------------------
    # 1) Explorative Analyse: fehlende Werte
    # ------------------------------------------------------------------
    miss = df.isna().mean().sort_values(ascending=False)
    results["columns_over_70pct_missing"] = int((miss > 0.70).sum())
    print(f"Spalten mit >70% fehlenden Werten: {results['columns_over_70pct_missing']}")

    # Selbststaendige ueberspringen viele Arbeitgeberfragen (Skip-Logik). Fuer ein
    # betriebliches Praeventionsprogramm sind Angestellte die relevante Population.
    self_emp = find_col(df, "are you self-employed")
    if self_emp is not None:
        before = len(df)
        df = df[df[self_emp] == 0].copy()
        print(f"Einschraenkung auf Angestellte: {before} -> {len(df)} Zeilen")
    results["n_employees"] = int(len(df))

    # ------------------------------------------------------------------
    # 2) Feature Engineering: Auswahl, Bereinigung, Encoding, Skalierung
    # ------------------------------------------------------------------
    col_map: dict[str, str] = {}
    roles: dict[str, str] = {}
    for short, needle, role in CORE_FEATURES:
        col = find_col(df, needle)
        if col is None:
            print(f"  ! Spalte nicht gefunden: {short} ({needle})")
            continue
        col_map[short] = col
        roles[short] = role
    cluster_short = [s for s in col_map if roles[s] == "cluster"]
    profile_short = [s for s in col_map if roles[s] == "profile"]
    print(f"Cluster-Merkmale: {len(cluster_short)}, Profil-Merkmale: {len(profile_short)}")

    work = pd.DataFrame(index=df.index)
    for short, col in col_map.items():
        work[short] = df[col]

    # Geschlecht vereinheitlichen
    if "gender" in work:
        work["gender"] = work["gender"].apply(clean_gender)
        results["gender_distribution"] = {k: int(v) for k, v in work["gender"].value_counts().items()}

    # Alter bereinigen: unplausible Werte als fehlend markieren
    if "age" in work:
        work["age"] = pd.to_numeric(work["age"], errors="coerce")
        implausible = ((work["age"] < 15) | (work["age"] > 100)).sum()
        work.loc[(work["age"] < 15) | (work["age"] > 100), "age"] = np.nan
        results["age_implausible_set_nan"] = int(implausible)
        results["age_median"] = float(work["age"].median())

    # numerische vs. kategoriale Merkmale (nur Cluster-Merkmale gehen in die Matrix)
    num_features = [c for c in ["age"] if c in cluster_short]
    cat_features = [c for c in cluster_short if c not in num_features]   # Encoding/Clustering
    profile_cat = [c for c in profile_short]                             # nur Beschreibung
    all_cat_features = cat_features + profile_cat                        # vollstaendige Profilierung

    # alle kategorialen Merkmale als String (NaN -> der Imputation/Profilierung ueberlassen)
    for c in all_cat_features:
        work[c] = work[c].astype("object")

    results["n_cluster_features"] = len(cluster_short)
    results["n_profile_features"] = len(profile_short)
    results["n_categorical_cluster_features"] = len(cat_features)
    results["n_numeric_cluster_features"] = len(num_features)

    # Vorverarbeitungs-Pipeline: Imputation -> Encoding/Skalierung
    cat_pipe = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    num_pipe = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    pre = ColumnTransformer([
        ("cat", cat_pipe, cat_features),
        ("num", num_pipe, num_features),
    ])
    X = pre.fit_transform(work)
    results["encoded_dimensions"] = int(X.shape[1])
    print(f"Merkmalsmatrix nach Encoding: {X.shape[0]} x {X.shape[1]}")

    # ------------------------------------------------------------------
    # 3) Dimensionsreduktion: PCA (Komponentenzahl ueber erklaerte Varianz)
    # ------------------------------------------------------------------
    pca_full = PCA(random_state=RANDOM_STATE).fit(X)
    cum_var = np.cumsum(pca_full.explained_variance_ratio_)
    n_comp = int(np.argmax(cum_var >= 0.80) + 1)  # >= 80% erklaerte Varianz
    results["pca_components_80pct"] = n_comp
    results["pca_cum_var_at_n"] = float(cum_var[n_comp - 1])
    print(f"PCA: {n_comp} Komponenten erklaeren {cum_var[n_comp - 1]:.1%} der Varianz")

    pca = PCA(n_components=n_comp, random_state=RANDOM_STATE)
    X_pca = pca.fit_transform(X)

    # Abbildung 1: kumulierte erklaerte Varianz
    plt.figure(figsize=(6, 4))
    plt.plot(range(1, len(cum_var) + 1), cum_var, marker="o", ms=3)
    plt.axhline(0.80, color="gray", ls="--", lw=1)
    plt.axvline(n_comp, color="crimson", ls="--", lw=1)
    plt.xlabel("Anzahl Hauptkomponenten")
    plt.ylabel("Kumulierte erklärte Varianz")
    plt.title("PCA: erklärte Varianz nach Komponentenzahl")
    plt.tight_layout()
    for d in (ASSETS_IMG, RAW_OUT):
        plt.savefig(d / "abb1_pca_varianz.png", dpi=150)
    plt.close()

    # ------------------------------------------------------------------
    # 4) Clustering: k-Means, Auswahl ueber Silhouette + Elbow
    # ------------------------------------------------------------------
    k_range = list(range(2, 9))
    inertias, silhouettes = [], []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        labels = km.fit_predict(X_pca)
        inertias.append(float(km.inertia_))
        silhouettes.append(float(silhouette_score(X_pca, labels)))
    best_idx = int(np.argmax(silhouettes))
    best_k = k_range[best_idx]
    results["k_candidates"] = k_range
    results["silhouettes"] = {str(k): round(s, 4) for k, s in zip(k_range, silhouettes)}
    results["inertias"] = {str(k): round(i, 2) for k, i in zip(k_range, inertias)}
    results["best_k"] = best_k
    results["best_silhouette"] = round(silhouettes[best_idx], 4)
    print(f"k-Means: bestes k={best_k} (Silhouette={silhouettes[best_idx]:.4f})")

    # Abbildung 2: Elbow + Silhouette
    fig, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(k_range, inertias, marker="o", color="steelblue", label="Trägheit (Inertia)")
    ax1.set_xlabel("Anzahl Cluster k")
    ax1.set_ylabel("Trägheit", color="steelblue")
    ax1.tick_params(axis="y", labelcolor="steelblue")
    ax2 = ax1.twinx()
    ax2.plot(k_range, silhouettes, marker="s", color="crimson", label="Silhouette")
    ax2.set_ylabel("Silhouettenkoeffizient", color="crimson")
    ax2.tick_params(axis="y", labelcolor="crimson")
    ax2.axvline(best_k, color="gray", ls="--", lw=1)
    ax1.grid(False)
    ax2.grid(False)
    plt.title("Bestimmung der Clusteranzahl (Elbow und Silhouette)")
    fig.tight_layout()
    for d in (ASSETS_IMG, RAW_OUT):
        fig.savefig(d / "abb2_k_auswahl.png", dpi=150)
    plt.close(fig)

    km = KMeans(n_clusters=best_k, random_state=RANDOM_STATE, n_init=10)
    cluster_labels = km.fit_predict(X_pca)
    work = work.copy()
    work["cluster"] = cluster_labels

    sizes = pd.Series(cluster_labels).value_counts().sort_index()
    results["cluster_sizes"] = {str(k): int(v) for k, v in sizes.items()}
    print(f"Clustergroessen: {results['cluster_sizes']}")

    # ------------------------------------------------------------------
    # 5) Robustheitspruefung: hierarchisch + DBSCAN
    # ------------------------------------------------------------------
    agglo = AgglomerativeClustering(n_clusters=best_k)
    agglo_labels = agglo.fit_predict(X_pca)
    results["ari_kmeans_vs_agglo"] = round(float(adjusted_rand_score(cluster_labels, agglo_labels)), 4)
    results["agglo_silhouette"] = round(float(silhouette_score(X_pca, agglo_labels)), 4)

    # DBSCAN: eps ueber typische Nachbardistanz grob kalibriert
    from sklearn.neighbors import NearestNeighbors
    nn = NearestNeighbors(n_neighbors=5).fit(X_pca)
    dists, _ = nn.kneighbors(X_pca)
    eps = float(np.percentile(dists[:, -1], 90))
    db = DBSCAN(eps=eps, min_samples=5)
    db_labels = db.fit_predict(X_pca)
    n_db_clusters = len(set(db_labels)) - (1 if -1 in db_labels else 0)
    results["dbscan_eps"] = round(eps, 3)
    results["dbscan_n_clusters"] = int(n_db_clusters)
    results["dbscan_noise_points"] = int((db_labels == -1).sum())
    print(f"Robustheit: ARI(kMeans,Agglo)={results['ari_kmeans_vs_agglo']}, "
          f"DBSCAN-Cluster={n_db_clusters}, Rauschpunkte={results['dbscan_noise_points']}")

    # ------------------------------------------------------------------
    # 6) 2D-Visualisierung: t-SNE (+ UMAP falls verfuegbar)
    # ------------------------------------------------------------------
    tsne = TSNE(n_components=2, random_state=RANDOM_STATE, init="pca",
                perplexity=30, learning_rate="auto")
    X_tsne = tsne.fit_transform(X_pca)
    _scatter(X_tsne, cluster_labels, "t-SNE-Projektion der Mitarbeitersegmente",
             ASSETS_IMG / "abb3_cluster_tsne.png", RAW_OUT / "abb3_cluster_tsne.png")

    umap_done = False
    try:
        import umap
        reducer = umap.UMAP(n_components=2, random_state=RANDOM_STATE)
        X_umap = reducer.fit_transform(X_pca)
        _scatter(X_umap, cluster_labels, "UMAP-Projektion der Mitarbeitersegmente",
                 ASSETS_IMG / "abb4_cluster_umap.png", RAW_OUT / "abb4_cluster_umap.png")
        umap_done = True
    except Exception as exc:  # pragma: no cover
        print(f"UMAP uebersprungen: {exc}")
    results["umap_available"] = umap_done

    # ------------------------------------------------------------------
    # 7) Segmentprofile: praegende Merkmale je Cluster
    # ------------------------------------------------------------------
    profiles = describe_clusters(work, all_cat_features, num_features, best_k, profile_cat)
    results["cluster_profiles"] = profiles

    # Abbildung 5: Heatmap ausgewaehlter Merkmalsanteile je Cluster
    _profile_heatmap(work, all_cat_features, best_k, ASSETS_IMG / "abb5_profile_heatmap.png",
                     RAW_OUT / "abb5_profile_heatmap.png")

    # ------------------------------------------------------------------
    # Ergebnisse persistieren
    # ------------------------------------------------------------------
    (RAW_OUT / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))
    write_results_markdown(results, col_map, RAW_OUT / "results.md")
    print(f"\nErgebnisse gespeichert: {RAW_OUT / 'results.json'}")
    return results


def _scatter(coords, labels, title, *paths):
    plt.figure(figsize=(6, 5))
    sns.scatterplot(x=coords[:, 0], y=coords[:, 1], hue=labels.astype(str),
                    palette=PALETTE, s=18, linewidth=0, alpha=0.8)
    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")
    plt.title(title)
    plt.legend(title="Cluster", fontsize=8, title_fontsize=9, loc="best")
    plt.tight_layout()
    for p in paths:
        plt.savefig(p, dpi=150)
    plt.close()


def describe_clusters(work, cat_features, num_features, k, profile_cat=None) -> dict:
    """Ermittelt pro Cluster Groesse, Alter und die am staerksten ueberrepraesentierten Auspraegungen."""
    profile_cat = profile_cat or []
    profiles: dict = {}
    n_total = len(work)
    # globale Anteile je (Merkmal, Auspraegung)
    global_share = {}
    for c in cat_features:
        global_share[c] = work[c].value_counts(normalize=True, dropna=False)
    for cl in range(k):
        sub = work[work["cluster"] == cl]
        entry = {
            "size": int(len(sub)),
            "share_of_total": round(len(sub) / n_total, 3),
        }
        if "age" in num_features:
            entry["age_mean"] = round(float(sub["age"].mean()), 1)
        # Beschreibende Aufschluesselung der nicht geclusterten Status-Merkmale
        breakdown = {}
        for c in profile_cat:
            local = sub[c].value_counts(normalize=True, dropna=False)
            glob = work[c].value_counts(normalize=True, dropna=False)
            top = str(local.index[0])
            breakdown[c] = {
                "top_level": top,
                "cluster_share": round(float(local.iloc[0]), 3),
                "global_share": round(float(glob.get(local.index[0], 0.0)), 3),
            }
        entry["profile_breakdown"] = breakdown
        lifts = []
        for c in cat_features:
            local = sub[c].value_counts(normalize=True, dropna=False)
            for level, loc_share in local.items():
                if loc_share < 0.5:  # nur dominante Auspraegungen
                    continue
                glob = float(global_share[c].get(level, 0.0))
                lift = loc_share - glob
                lifts.append({
                    "feature": c,
                    "level": str(level),
                    "cluster_share": round(float(loc_share), 3),
                    "global_share": round(glob, 3),
                    "lift": round(float(lift), 3),
                })
        lifts.sort(key=lambda d: d["lift"], reverse=True)
        entry["defining_features"] = lifts[:5]
        profiles[str(cl)] = entry
    return profiles


def _profile_heatmap(work, cat_features, k, *paths):
    """Heatmap: Anteil der jeweils haeufigsten globalen Auspraegung je Merkmal und Cluster."""
    rows = []
    feats = [c for c in cat_features if c != "gender"][:12]
    for c in feats:
        top_level = work[c].value_counts(dropna=False).index[0]
        row = []
        for cl in range(k):
            sub = work[work["cluster"] == cl]
            row.append((sub[c] == top_level).mean())
        rows.append(row)
    mat = pd.DataFrame(rows, index=feats, columns=[f"C{cl}" for cl in range(k)])
    plt.figure(figsize=(7, 6))
    sns.heatmap(mat, annot=True, fmt=".2f", cmap="RdYlBu_r", cbar_kws={"label": "Anteil"})
    plt.title("Merkmalsprofile der Cluster (Anteil dominanter Ausprägung)")
    plt.tight_layout()
    for p in paths:
        plt.savefig(p, dpi=150)
    plt.close()


def write_results_markdown(results: dict, col_map: dict, path: Path) -> None:
    lines = ["# Reproduzierbare Ergebnisse der OSMI-Clustering-Analyse", ""]
    lines.append(f"- random_state: {results['random_state']}")
    lines.append(f"- Rohdaten: {results['raw_shape'][0]} Zeilen x {results['raw_shape'][1]} Spalten")
    lines.append(f"- Angestellte (Analysepopulation): {results['n_employees']}")
    lines.append(f"- Cluster-Merkmale: {results['n_cluster_features']} "
                 f"({results['n_categorical_cluster_features']} kategorial, "
                 f"{results['n_numeric_cluster_features']} numerisch); "
                 f"Profil-Merkmale (nur Beschreibung): {results['n_profile_features']}")
    lines.append(f"- Merkmalsmatrix nach One-Hot-Encoding: {results['encoded_dimensions']} Dimensionen")
    lines.append(f"- PCA: {results['pca_components_80pct']} Komponenten = "
                 f"{results['pca_cum_var_at_n']:.1%} erklaerte Varianz")
    lines.append(f"- k-Means: bestes k = {results['best_k']}, "
                 f"Silhouette = {results['best_silhouette']}")
    lines.append(f"- Clustergroessen: {results['cluster_sizes']}")
    lines.append(f"- Robustheit ARI(k-Means, hierarchisch) = {results['ari_kmeans_vs_agglo']}")
    lines.append(f"- DBSCAN: {results['dbscan_n_clusters']} Cluster, "
                 f"{results['dbscan_noise_points']} Rauschpunkte")
    lines.append("")
    lines.append("## Silhouettenwerte je k")
    lines.append("")
    lines.append("| k | Silhouette | Traegheit |")
    lines.append("|---|---|---|")
    for k in results["k_candidates"]:
        lines.append(f"| {k} | {results['silhouettes'][str(k)]} | {results['inertias'][str(k)]} |")
    lines.append("")
    lines.append("## Segmentprofile")
    for cl, prof in results["cluster_profiles"].items():
        lines.append("")
        lines.append(f"### Cluster {cl} (n={prof['size']}, {prof['share_of_total']:.0%})")
        if "age_mean" in prof:
            lines.append(f"- Durchschnittsalter: {prof['age_mean']}")
        lines.append("- Praegende Merkmale (ueberrepraesentierte Auspraegung):")
        for d in prof["defining_features"]:
            lines.append(f"  - {d['feature']} = \"{d['level']}\" "
                         f"({d['cluster_share']:.0%} vs. {d['global_share']:.0%} gesamt, "
                         f"Lift {d['lift']:+.0%})")
        if prof.get("profile_breakdown"):
            lines.append("- Status-Merkmale (nur Beschreibung, nicht geclustert):")
            for feat, b in prof["profile_breakdown"].items():
                lines.append(f"  - {feat}: haeufigste Auspraegung \"{b['top_level']}\" "
                             f"({b['cluster_share']:.0%} vs. {b['global_share']:.0%} gesamt)")
    path.write_text("\n".join(lines))


if __name__ == "__main__":
    main()
