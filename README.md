# TESS Earth Similarity Analysis

## Overview

This project investigates the question:

**Which rocky exoplanets discovered by NASA's Transiting Exoplanet Survey Satellite (TESS) have the greatest physical and environmental similarity to Earth?**

Using data from the NASA Exoplanet Archive, I developed a Python-based computational model to compare rocky exoplanets with Earth across four primary characteristics:

- Planetary radius
- Planetary density
- Equilibrium temperature
- Stellar insolation

Each measurement is converted into an Earth-similarity percentage and combined into a Composite Earth Similarity Value (ESV). I also performed a sensitivity analysis using different weighting systems to determine how dependent the results were on the assumptions of the model.

This project measures **similarity to Earth, not planetary habitability or the probability of life**.

---

## Data

The planetary data comes from the **NASA Exoplanet Archive Planetary Systems table**.

The dataset was filtered to include:

- Confirmed exoplanets
- Planets discovered by TESS
- Planetary radius ≤ 1.8 Earth radii

The radius threshold was used as an initial screening criterion for potentially rocky planets rather than as proof of rocky composition.

The final dataset contains **12 exoplanets**.

---

## Earth Reference Values

Each exoplanet was compared with the following Earth reference values:

| Characteristic | Earth Reference |
|---|---:|
| Radius | 1 R⊕ |
| Density | 5.51 g/cm³ |
| Equilibrium Temperature | 255 K |
| Insolation | 1 S⊕ |

Orbital period and planetary mass were analyzed as supplemental characteristics but were not included in the Composite ESV.

---

## Similarity Model

For each available measurement, similarity to Earth was calculated using the proportional difference from the corresponding Earth value.

A measurement identical to Earth's receives a similarity score of **100%**. Similarity decreases as the measurement deviates from the Earth reference value, with a lower bound of **0%**.

The model treats deviations above and below Earth's value equally.

### Composite Earth Similarity Value

The primary model gives equal weight to the four criteria:

| Criterion | Weight |
|---|---:|
| Radius | 25% |
| Density | 25% |
| Equilibrium Temperature | 25% |
| Insolation | 25% |

Because measurements are unavailable for some exoplanets, a planet must have data for at least **three of the four criteria** to receive a composite score. When one measurement is unavailable, the remaining weights are proportionally normalized.

Missing measurements are never treated as zero.

---

## Sensitivity Analysis

To test whether the final rankings depended heavily on the selected weights, three models were compared.

### Equal Weighting

- Radius: 25%
- Density: 25%
- Equilibrium Temperature: 25%
- Insolation: 25%

### Environmental Emphasis

- Radius: 15%
- Density: 15%
- Equilibrium Temperature: 35%
- Insolation: 35%

### Physical Emphasis

- Radius: 35%
- Density: 35%
- Equilibrium Temperature: 15%
- Insolation: 15%

---

## Results

**TOI-700 d was the strongest candidate based on the available physical and environmental evidence.**

Its approximate scores across the three models were:

| Model | TOI-700 d ESV |
|---|---:|
| Equal Weighting | 90.8% |
| Environmental Emphasis | 90.3% |
| Physical Emphasis | 91.4% |

TOI-700 d remained the highest-ranked candidate under all three weighting systems. The difference between its highest and lowest scores was only about **1.1 percentage points**.

The analysis also demonstrated why planetary radius alone is insufficient for identifying Earth-like planets. Several relatively Earth-sized planets in the dataset experienced equilibrium temperatures or stellar insolation substantially different from Earth's.

---

## Why Orbital Period Is Not Included

Orbital period was excluded from the Composite ESV because its significance depends strongly on the host star.

A planet orbiting a smaller, cooler star can receive Earth-like levels of stellar radiation while orbiting much closer to its star than Earth does to the Sun. Such a planet can therefore have a much shorter orbital period while still experiencing relatively Earth-like insolation.

Equilibrium temperature and stellar insolation were used as more direct environmental comparisons.

---

## Limitations

The Composite ESV is a custom comparison model and should not be interpreted as a scientifically validated habitability index.

Important limitations include:

- Missing measurements for several planets
- Uncertainty in measured exoplanet properties
- Linear similarity calculation
- Assumptions involved in weighting different characteristics
- Correlation between equilibrium temperature and insolation
- TESS observational selection effects
- Earth-centered definition of similarity
- Limited information about exoplanet atmospheres

The model also does not account for atmospheric composition, atmospheric pressure, liquid water, greenhouse effects, stellar activity, magnetic fields, geological activity, tidal locking, or long-term climate stability.

A high ESV therefore does **not** demonstrate that a planet is habitable or capable of supporting life.

---

## Repository Structure

```text
tess-earth-similarity-analysis/
│
├── README.md
├── analysis.py
├── requirements.txt
│
├── data/
│   └── tess_rocky_planets.xlsx
│
├── figures/
│   └── [generated figures]
│
└── paper/
    └── NASA_Exoplanet_Paper.pdf
