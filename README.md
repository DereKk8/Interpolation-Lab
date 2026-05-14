# Interpolation Lab

**Numerical Analysis Final Project**  
Polynomial Interpolation: Lagrange & Neville Methods  
Country Data: **País 16** (Internet Usage 1994–2023)  
Student: **Derek Sarmiento Loeber**

---

## 📁 Project Overview

This project implements and demonstrates polynomial interpolation techniques for reconstructing missing data points from a dataset of internet usage percentage over a 30-year period.

### Key Features
- **Two interpolation methods**: Lagrange and Neville's Algorithm
- **25 known data points** (1994–2023, excluding 5 missing years)
- **5 estimated values** for years: 1995, 2000, 2009, 2011, 2016
- **Complete stability analysis** including Runge's phenomenon assessment
- **Interactive HTML application** with Chart.js visualization

---

## 📊 Results Summary

| Year | Lagrange (5 dec) | Neville (5 dec) | Notes |
|------|-----------------|-----------------|-------|
| 1995 | -63601.83367 | -63601.83367 | ⚠️ Runge phenomenon (extreme) |
| 2000 | -61.19508 | -61.19508 | ⚠️ Runge phenomenon |
| 2009 | 69.75345 | 69.75345 | ✅ Stable |
| 2011 | 78.28847 | 78.28847 | ✅ Stable |
| 2016 | 77.55012 | 77.55012 | ✅ Stable |

**Key Insight**: The global polynomial of degree 24 exhibits severe oscillations at the interval edges (Runge's phenomenon), while values near the center (2009, 2011, 2016) remain realistic.

---

## 🖥️ HTML Application

**File**: `interpolacion.html`

A self-contained single-page application with 6 tabs:

1. **Known Data** — Table with 25 known points + 5 unknown highlighted
2. **Lagrange** — Formula, results, step-by-step accordion, live recalculation button
3. **Neville** — Full 25×25 Q-table with pagination, results
4. **Comparison** — Side-by-side table + Runge's phenomenon warning box + rounding rule
5. **Complete Table & Chart** — Full 1994–2023 table + Chart.js visualization (Y-axis limited to [0,100] to show instability)
6. **About** — Pseudocode, implementation decisions, Python execution instructions

### How to Use
1. Download `interpolacion.html`
2. Double-click to open in any browser (Chrome, Firefox, Edge, Safari)
3. No internet required — Chart.js fallback is embedded inline

---

## 🐍 Python Script

**File**: `algoritmo_interpolacion.py`

Executable script with automatic dependency installation.

### How to Run
```bash
python algoritmo_interpolacion.py
```

The script will:
1. Automatically detect if `numpy` and `pandas` are missing
2. Create a virtual environment (`.interp_venv/`) if needed
3. Install dependencies
4. Execute the full analysis and print results to console

### Output Includes
- Known data points
- Lagrange & Neville interpolation results (full precision + 5 decimals)
- Comparison table
- Complete 1994–2023 reconstructed table
- Sample Q-table for Neville's algorithm
- Stability analysis and Runge's phenomenon explanation

---

## 📚 Technical Details

### Polynomial Degree
- **Degree**: 24 (n-1 where n=25 data points)
- **Node Distribution**: Nearly uniform (years)

### Runge's Phenomenon Analysis
- **Error Term**: E(x) = f⁽ⁿ⁺¹⁾(ξ) / (n+1)! × ∏(x - xᵢ)
- **Observation**: Error grows exponentially near interval edges when nodes are uniformly distributed
- **Mitigation Strategies**:
  - Cubic splines (piecewise interpolation)
  - Chebyshev nodes (clustered near edges)

### Custom Rounding Rule
- Method: `ROUND_HALF_UP` to 5 decimal places
- Implementation uses string manipulation to avoid floating-point artifacts

---

## 📂 Repository Structure

```
Interpolation-Lab/
├── README.md                 # This file
├── interpolacion.html        # Self-contained HTML application
├── algoritmo_interpolacion.py # Python script with auto-install
└── .gitignore                # Excludes .interp_venv/
```

---

## 🎯 Learning Objectives Met

- ✅ Implement Lagrange interpolation formula
- ✅ Implement Neville's algorithm with divided difference table
- ✅ Analyze polynomial interpolation stability (Runge's phenomenon)
- ✅ Apply custom rounding rules (5 decimal places)
- ✅ Create interactive data visualization
- ✅ Build self-contained deliverable (single HTML file)
- ✅ Document algorithmic decisions

---

## 📬 Contact

For questions about this project, contact:  
**Derek Sarmiento Loeber**  
Student | Systems Engineering  
Pontificia Universidad Javeriana

---

*Project completed for Numerical Analysis course, 2026*