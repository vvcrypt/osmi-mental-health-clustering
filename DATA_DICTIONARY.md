# Datenwörterbuch - OSMI Mental Health in Tech 2016

Dateiversion: 20161114 | Analysedatum: 09.06.2026

## 1. Überblick

**Datensatz**: Mental Health in Tech Survey 2016 (OSMI)
**Quelle**: Open Sourcing Mental Illness
**Format**: CSV

### Shape
| Metrik | Wert |
|--------|------|
| Zeilen (Respondenten) | 1433 |
| Spalten (Features) | 63 |

## 2. Alle Spalten - Übersichtstabelle

| # | Spalte | dtype | Missing | % | Unique | Bemerkungen |
|---|--------|-------|---------|---|--------|-------------|
| 1 | `Are you self-employed?` | int64 | 0 | 0.0% | 2 |  |
| 2 | `How many employees does your company or organiz...` | str | 287 | 20.0% | 6 |  |
| 3 | `Is your employer primarily a tech company/organ...` | float64 | 287 | 20.0% | 2 |  |
| 4 | `Is your primary role within your company relate...` | float64 | 1170 | 81.6% | 2 | ⚠️ >70% Missing |
| 5 | `Does your employer provide mental health benefi...` | str | 287 | 20.0% | 4 |  |
| 6 | `Do you know the options for mental health care ...` | str | 420 | 29.3% | 3 |  |
| 7 | `Has your employer ever formally discussed menta...` | str | 287 | 20.0% | 3 |  |
| 8 | `Does your employer offer resources to learn mor...` | str | 287 | 20.0% | 3 |  |
| 9 | `Is your anonymity protected if you choose to ta...` | str | 287 | 20.0% | 3 |  |
| 10 | `If a mental health issue prompted you to reques...` | str | 287 | 20.0% | 6 |  |
| 11 | `Do you think that discussing a mental health di...` | str | 287 | 20.0% | 3 |  |
| 12 | `Do you think that discussing a physical health ...` | str | 287 | 20.0% | 3 |  |
| 13 | `Would you feel comfortable discussing a mental ...` | str | 287 | 20.0% | 3 |  |
| 14 | `Would you feel comfortable discussing a mental ...` | str | 287 | 20.0% | 3 |  |
| 15 | `Do you feel that your employer takes mental hea...` | str | 287 | 20.0% | 3 |  |
| 16 | `Have you heard of or observed negative conseque...` | str | 287 | 20.0% | 2 |  |
| 17 | `Do you have medical coverage (private insurance...` | float64 | 1146 | 80.0% | 2 | ⚠️ >70% Missing |
| 18 | `Do you know local or online resources to seek h...` | str | 1146 | 80.0% | 3 | ⚠️ >70% Missing |
| 19 | `If you have been diagnosed or treated for a men...` | str | 1146 | 80.0% | 5 | ⚠️ >70% Missing |
| 20 | `If you have revealed a mental health issue to a...` | str | 1289 | 90.0% | 3 | ⚠️ >70% Missing |
| 21 | `If you have been diagnosed or treated for a men...` | str | 1146 | 80.0% | 5 | ⚠️ >70% Missing |
| 22 | `If you have revealed a mental health issue to a...` | str | 1146 | 80.0% | 4 | ⚠️ >70% Missing |
| 23 | `Do you believe your productivity is ever affect...` | str | 1146 | 80.0% | 4 | ⚠️ >70% Missing |
| 24 | `If yes, what percentage of your work time (time...` | str | 1229 | 85.8% | 4 | ⚠️ >70% Missing |
| 25 | `Do you have previous employers?` | int64 | 0 | 0.0% | 2 |  |
| 26 | `Have your previous employers provided mental he...` | str | 169 | 11.8% | 4 |  |
| 27 | `Were you aware of the options for mental health...` | str | 169 | 11.8% | 4 |  |
| 28 | `Did your previous employers ever formally discu...` | str | 169 | 11.8% | 4 |  |
| 29 | `Did your previous employers provide resources t...` | str | 169 | 11.8% | 3 |  |
| 30 | `Was your anonymity protected if you chose to ta...` | str | 169 | 11.8% | 4 |  |
| 31 | `Do you think that discussing a mental health di...` | str | 169 | 11.8% | 4 |  |
| 32 | `Do you think that discussing a physical health ...` | str | 169 | 11.8% | 3 |  |
| 33 | `Would you have been willing to discuss a mental...` | str | 169 | 11.8% | 3 |  |
| 34 | `Would you have been willing to discuss a mental...` | str | 169 | 11.8% | 4 |  |
| 35 | `Did you feel that your previous employers took ...` | str | 169 | 11.8% | 4 |  |
| 36 | `Did you hear of or observe negative consequence...` | str | 169 | 11.8% | 3 |  |
| 37 | `Would you be willing to bring up a physical hea...` | str | 0 | 0.0% | 3 |  |
| 38 | `Why or why not?` | str | 338 | 23.6% | 1085 |  |
| 39 | `Would you bring up a mental health issue with a...` | str | 0 | 0.0% | 3 |  |
| 40 | `Why or why not?.1` | str | 307 | 21.4% | 1080 |  |
| 41 | `Do you feel that being identified as a person w...` | str | 0 | 0.0% | 5 |  |
| 42 | `Do you think that team members/co-workers would...` | str | 0 | 0.0% | 5 |  |
| 43 | `How willing would you be to share with friends ...` | str | 0 | 0.0% | 6 |  |
| 44 | `Have you observed or experienced an unsupportiv...` | str | 89 | 6.2% | 4 |  |
| 45 | `Have your observations of how another individua...` | str | 776 | 54.2% | 3 | ~30-70% Missing |
| 46 | `Do you have a family history of mental illness?` | str | 0 | 0.0% | 3 |  |
| 47 | `Have you had a mental health disorder in the past?` | str | 0 | 0.0% | 3 |  |
| 48 | `Do you currently have a mental health disorder?` | str | 0 | 0.0% | 3 |  |
| 49 | `If yes, what condition(s) have you been diagnos...` | str | 865 | 60.4% | 128 | ~30-70% Missing |
| 50 | `If maybe, what condition(s) do you believe you ...` | str | 1111 | 77.5% | 99 | ⚠️ >70% Missing |
| 51 | `Have you been diagnosed with a mental health co...` | str | 0 | 0.0% | 2 |  |
| 52 | `If so, what condition(s) were you diagnosed with?` | str | 722 | 50.4% | 116 | ~30-70% Missing |
| 53 | `Have you ever sought treatment for a mental hea...` | int64 | 0 | 0.0% | 2 |  |
| 54 | `If you have a mental health issue, do you feel ...` | str | 0 | 0.0% | 5 |  |
| 55 | `If you have a mental health issue, do you feel ...` | str | 0 | 0.0% | 5 |  |
| 56 | `What is your age?` | int64 | 0 | 0.0% | 53 |  |
| 57 | `What is your gender?` | str | 3 | 0.2% | 70 |  |
| 58 | `What country do you live in?` | str | 0 | 0.0% | 53 |  |
| 59 | `What US state or territory do you live in?` | str | 593 | 41.4% | 47 | ~30-70% Missing |
| 60 | `What country do you work in?` | str | 0 | 0.0% | 53 |  |
| 61 | `What US state or territory do you work in?` | str | 582 | 40.6% | 48 | ~30-70% Missing |
| 62 | `Which of the following best describes your work...` | str | 0 | 0.0% | 264 |  |
| 63 | `Do you work remotely?` | str | 0 | 0.0% | 3 |  |

## 3. Detailergebnisse zu Spezialspalten

### 3.1 Self-Employed Status

**Spalte**: 'Are you self-employed?' (Spalte 1)
**Wichtigkeit**: Kritisch - steuert Skip-Logik der gesamten Umfrage

| Status | Anzahl | Prozent |
|--------|--------|---------|
| Nicht selbstständig (0) | 1146 | 80.0% |
| Selbstständig (1) | 287 | 20.0% |

**Implikation**: Die 287 selbstständigen Respondenten (20%) skip viele Arbeitgeber-bezogene Fragen, was zu den 80% Missing-Werten bei Employer-Fragen führt. Employer-Fragen sollten nur für die 1146 Angestellten (80%) analysiert werden.

### 3.2 Alter

**Spalte**: 'What is your age?' (Spalte 56)
**dtype**: int64 | **Missing**: 0 | **Unique**: 53

| Metrik | Wert |
|--------|------|
| Minimum | 3 |
| Maximum | 323 |
| Median | 33 |
| Mittelwert | 34.3 |

**Datenqualitätsprobleme**:
- Minimum = 3: unplausibel (Respondent wahrscheinlich <5 Jahre alt?)
- Maximum = 323: offensichlich Fehleingabe (evtl. '23' mit Präfix)
- **Insgesamt**: 2 unplausible Werte (<15 oder >100)

**Empfehlung**: Vor Analyse filtern oder z-score-Normalisierung mit robustem Median/IQR anwenden.

### 3.3 Geschlecht

**Spalte**: 'What is your gender?' (Spalte 57)
**dtype**: str | **Missing**: 3 (0.2%) | **Unique**: 70

**Rohheit der Freitexteingabe**: EXTREM chaotisch

| Wert | Häufigkeit | Prozent |
|------|-----------|---------|
| 'Male' | 610 | 42.6% |
| 'male' | 249 | 17.4% |
| 'Female' | 153 | 10.7% |
| 'female' | 95 | 6.6% |
| 'M' | 86 | 6.0% |
| 'm' | 79 | 5.5% |
| 'F' | 38 | 2.7% |
| 'f' | 23 | 1.6% |
| [weitere 62 Rohwerte] | 52 | 3.6% |

**Beispiele aus den Top-40-Rohwerten:**
- Case-Variationen: 'Male', 'male', 'M', 'm'
- Spaces: 'Male ', 'Female '
- Normaltext-Varianten: 'man', 'woman', 'Woman'
- Non-binary (4): 'non-binary', 'Nonbinary', 'Androgynous', 'genderqueer'
- Spezifikationen: 'Male (cis)', 'Cisgender Female', 'Transitioned, M2F'
- Sonstige: 'none of your business', 'fm', 'male 9:1 female, roughly'

**Implikation**: Dringend Daten-Cleaning notwendig!
- **Normalisierungsstrategie**: Auf 3-4 Kategorien reduzieren: 'Male', 'Female', 'Non-binary', 'Other'
- Groß/Kleinschreibung einheitlich machen
- Whitespace trimmen
- Komplexe Aussagen ('male 9:1 female') → 'Non-binary' oder 'Other'

### 3.4 Wohnort - Land

**Spalte**: 'What country do you live in?' (Spalte 58)
**dtype**: str | **Missing**: 0 | **Unique**: 53

| Rang | Land | Anzahl | Prozent |
|------|------|--------|---------|
| 1 | USA | 840 | 58.6% |
| 2 | UK | 180 | 12.6% |
| 3 | Kanada | 78 | 5.4% |
| 4 | Deutschland | 58 | 4.0% |
| 5 | Niederlande | 48 | 3.4% |
| 6 | Australien | 35 | 2.4% |
| 7-20 | [14 weitere Länder] | ~132 | ~9.2% |
| 21-53 | [33 weitere Länder] | ~62 | ~4.3% |

**Implikation**: Stark USA-zentriert (58.6%). Nicht-anglophon: 24% (DE, NL, RU, etc.), daher sprachliche Variabilität in Freitexten wahrscheinlich.

### 3.5 Wohnort - US State

**Spalte**: 'What US state or territory do you live in?' (Spalte 59)
**dtype**: str | **Missing**: 593 (41.4%) | **Unique**: 47

| Rang | State | Anzahl | Prozent (von 840 US-Respondenten) |
|------|-------|--------|----------------------------------|
| 1 | California | 130 | 15.5% |
| 2 | Illinois | 56 | 6.7% |
| 3 | Michigan | 48 | 5.7% |
| 4 | New York | 45 | 5.4% |
| 5 | Washington | 43 | 5.1% |
| 6 | Texas | 43 | 5.1% |
| 7 | Minnesota | 42 | 5.0% |
| 8-15 | [8 weitere States] | ~192 | ~22.9% |

**Implikation**: Tech-Hub-Konzentrierung (CA 15.5%, IL+NY+WA+TX 21.5%). Die 593 Missing sind primär Non-US-Respondenten.

## 4. Spalten mit >70% Missing (Kandidaten für Ausschluss)

| # | Spalte (gekürzt) | Missing % | Grund | Empfehlung |
|---|---|----------|-------|-------------|
| 1 | 'If you have revealed...impact negatively' | 90.0% | Skip-Logik: nur wenn ja/nein zu Punkt davor | EXCLUDE |
| 2 | 'If yes, what percentage...affected' | 85.8% | Skip: nur wenn 'ja' zu Produktivität | EXCLUDE |
| 3 | 'Is your primary role...tech/IT' | 81.6% | Skip: nur wenn nicht selbstständig + relevant | EXCLUDE |
| 4 | 'Do you have medical coverage...issues' | 80.0% | Skip-Logik | EXCLUDE |
| 5 | 'Do you know local/online resources...' | 80.0% | Skip-Logik | EXCLUDE |
| 6 | 'If you have been diagnosed...reveal...clients' | 80.0% | Skip: nur wenn diagnostiziert | EXCLUDE |
| 7 | 'If revealed...coworkers...negatively' | 80.0% | Skip-Logik | EXCLUDE |
| 8 | 'Do you believe productivity...affected' | 80.0% | Skip-Logik | EXCLUDE |
| 9 | 'If maybe, what conditions do you believe' | 77.5% | Skip: nur wenn 'maybe' zu mentaler Erkrankung | EXCLUDE |

**Strategie**: Diese Spalten sind fast vollständig für 20% der Population (Selbstständige) leer. Entweder:
1. Nach `Are you self-employed?` stratifizieren und separate Analysen machen
2. Oder diese Spalten komplett ausschließen und nur auf Selbstständige filtern

## 5. Kern-Einstellungsfragen (Clustering-geeignet)

**Kriterium**: <10% Missing + <20 eindeutige Werte → vollständig, kategorisch

### 5.1 Career/Stigma-Dimensionen

| Spalte | Missing | Unique | Kategorien |
|--------|---------|--------|-----------|
| 'Do you feel that being identified...hurt career' | 0% | 5 | Yes/No/Maybe/Yes,it has/No,it has not |
| 'Do you think team members...view negatively' | 0% | 5 | Yes/No/Maybe + variations |
| 'How willing...share friends/family' | 0% | 6 | Very open/Somewhat/Neutral/Somewhat not/Not/N/A |

### 5.2 Kommunikationsfähigkeit

| Spalte | Missing | Unique | Kategorien |
|--------|---------|--------|-----------|
| 'Would you be willing...physical...interview' | 0% | 3 | Yes/No/Maybe |
| 'Would you bring up...mental health...interview' | 0% | 3 | Yes/No/Maybe |

### 5.3 Persönlicher Hintergrund

| Spalte | Missing | Unique | Kategorien |
|--------|---------|--------|-----------|
| 'Do you have a family history...' | 0% | 3 | Yes/No/I don't know |
| 'Have you had...mental disorder...past' | 0% | 3 | Yes/No/Maybe |
| 'Do you currently have...' | 0% | 3 | Yes/No/Maybe |
| 'Have you been diagnosed...by professional' | 0% | 2 | Yes/No |
| 'Have you ever sought treatment...' | 0% | 2 | Yes (=1) / No (=0) |

### 5.4 Work Impact

| Spalte | Missing | Unique | Kategorien |
|--------|---------|--------|-----------|
| 'Interferes...when TREATED effectively' | 0% | 5 | Never/Rarely/Sometimes/Often/N/A |
| 'Interferes...when NOT treated effectively' | 0% | 5 | Never/Rarely/Sometimes/Often/N/A |

### 5.5 Arbeitsplatz/Demografie

| Spalte | Missing | Unique | Kategorien |
|--------|---------|--------|-----------|
| 'Are you self-employed' | 0% | 2 | 0/1 |
| 'Do you have previous employers' | 0% | 2 | 0/1 |
| 'Do you work remotely' | 0% | 3 | Always/Sometimes/Never |

### 5.6 Negativ-Erfahrungen

| Spalte | Missing | Unique | Kategorien |
|--------|---------|--------|-----------|
| 'Unsupported response in workplace' | 6.2% | 4 | No/Maybe/Yes-observed/Yes-experienced |

## 6. Freitextspalten (Qualitative Daten)

| Spalte | Missing | Unique | Typ | Verwendung |
|--------|---------|--------|-----|-----------|
| 'Why or why not?' (physical) | 23.6% | 1085 | Freitext | Sentiment/Themen-Analyse |
| 'Why or why not?.1' (mental) | 21.4% | 1080 | Freitext | Sentiment/Themen-Analyse |
| 'If yes, what condition(s)...' (diagnosed) | 60.4% | 128 | Freitext | Diagnose-Kategorisierung |
| 'If so, conditions diagnosed with' | 50.4% | 116 | Freitext | Diagnose-Kategorisierung |
| 'Which describes...work position' | 0% | 264 | Freitext | Job-Titel-Clustering |

## 7. Empfehlungen für Clustering

### 7.1 Empfohlenes Feature-Set (ohne Daten-Cleaning)

**14-16 Spalten für stabiles Clustering:**

```
Kerngruppe (vollständig, low-variance):
  1. Are you self-employed? (0/1)
  2. Do you have previous employers? (0/1)
  3. Do you work remotely? (3 Kategorien)
  4. Do you currently have a mental health disorder? (3)
  5. Have you been diagnosed by professional? (2)
  6. Have you ever sought treatment? (2)
  7. Do you have family history? (3)
  8. Have you had...disorder in past? (3)

Stigma/Perception (0% Missing):
  9. Would bring up mental health in interview? (3)
 10. Would bring up physical health in interview? (3)
 11. Feel identified would hurt career? (5)
 12. Team would view negatively? (5)
 13. Willing to share w/ friends/family? (6)

Work Impact (0% Missing):
 14. Interferes when treated effectively? (5)
 15. Interferes when NOT treated effectively? (5)

Demographie (mit Vorsicht):
 16. Age (numerisch, aber outlier-bereinigen)
 17. Gender (nach Cleaning: M/F/Non-binary/Other)
```

### 7.2 Daten-Vorverarbeitung

1. **Alter bereinigen:**
   - Outlier (<15, >100) entfernen oder als NaN markieren
   - Z-score-Normalisierung oder IQR-Methode anwenden

2. **Geschlecht normalisieren:**
   - Case-insensitive matching ('male'/'MALE' → 'Male')
   - Whitespace trimmen (strip)
   - Kategorie-Mapping:
     * 'Male', 'M', 'man', 'Cis male', etc. → 'Male'
     * 'Female', 'F', 'woman', 'Cis female', etc. → 'Female'
     * 'Non-binary', 'Nonbinary', 'Genderfluid', 'Agender', etc. → 'Non-binary'
     * Rest → 'Other'

3. **Kategoriale Fragen standardisieren:**
   - JA/NEIN → 1/0
   - 'Yes'/'No'/'Maybe' → numerisch ordinal (2/0/1) oder OrdinalEncoder
   - Likert-Skalen → numerisch oder preserve kategorisch

4. **Missing-Handling für Self-Employed=1:**
   - OPTION A: Filtern auf Self-Employed=0 (n=1146)
   - OPTION B: Forward-fill mit Group-Median pro Feature
   - OPTION C: Separate Clusters für SE vs. Non-SE

### 7.3 Empfohlene Clustering-Algorithmen

1. **K-Means** (nach Normalisierung):
   - Alle Features standard-skalieren
   - Elbow-Method / Silhouette-Score für k (erwarte 3-5 Cluster)

2. **Hierarchical Clustering** (dendrogramm):
   - Ward-Linkage oder Complete-Linkage
   - Gut für Interpretation

3. **DBSCAN** (falls Dichte-Cluster vermutet):
   - eps / min_samples tunen

### 7.4 Interpretierbare Cluster-Labels (erwartet)

Basierend auf Stigma + mentale Gesundheit:

- **Cluster A: "Vulnerable"** (hochstigmatisiert, aktuell diagnositziert)
  * High: Career-Angst, Stigma, aktuelle mentale Erkrankung
  * Low: Offenheit, Kommunikation in Interviews

- **Cluster B: "Informed/Managed"** (diagnositziert aber in Behandlung)
  * High: Frühere oder aktuelle Diagnose, aber Low interference when treated
  * Medium: Stigma

- **Cluster C: "Healthy/Non-Affected"** (kein MH-Hintergrund)
  * High: Offenheit, Low: Interference, Low: Familien-Historie
  * Low: Stigma (da nicht betroffen)

## 8. Datenqualitätszusammenfassung

| Aspekt | Status | Details |
|--------|--------|---------|
| Vollständigkeit | 🟡 AKZEPTABEL | 63 Spalten, 14 davon >70% Missing (Skip-Logik) |
| Konsistenz | 🔴 SCHLECHT | Geschlecht: 70 Rohwerte (sehr uneinheitlich) |
| Validität | 🟡 MIXED | Alter: 2 extreme Outlier (3, 323) |
| Repräsentativität | 🟢 GUT | n=1433, USA-lastig (58%) aber international |

