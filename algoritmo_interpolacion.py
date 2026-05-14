#!/usr/bin/env python3
"""
Analisis Numerico — Proyecto Final
Interpolacion Polinomial: Lagrange y Neville
Pais 16 | Derek Sarmiento Loeber

Ejecutar: python algoritmo_interpolacion.py
"""

import sys
import os
import subprocess

# ---------------------------------------------------------------------------
# Auto-instalacion de dependencias (con venv automatico si es necesario)
# ---------------------------------------------------------------------------
def ensure_dependencies():
    missing = []
    for pkg in ["numpy", "pandas"]:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if not missing:
        return

    print(f"[INFO] Dependencias faltantes: {', '.join(missing)}")
    
    # Intentar instalar en user site primero
    try:
        print("[INFO] Intentando instalar con --user ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", *missing])
        print("[INFO] Instalacion exitosa. Reiniciando ...\n")
        # No reiniciamos, solo reintentamos importar en la siguiente ejecucion si es necesario
        # Pero para evitar problemas de PATH, es mejor reiniciar
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception:
        pass

    # Si falla, crear venv automatico
    venv_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".interp_venv")
    if not os.path.exists(venv_dir):
        print(f"[INFO] Creando entorno virtual en: {venv_dir}")
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
    
    pip_exe = os.path.join(venv_dir, "bin", "pip")
    python_exe = os.path.join(venv_dir, "bin", "python")
    if sys.platform == "win32":
        pip_exe = os.path.join(venv_dir, "Scripts", "pip.exe")
        python_exe = os.path.join(venv_dir, "Scripts", "python.exe")
    
    print(f"[INFO] Instalando dependencias en entorno virtual ...")
    subprocess.check_call([pip_exe, "install", *missing])
    print("[INFO] Dependencias instaladas. Reiniciando script con entorno virtual ...\n")
    os.execl(python_exe, python_exe, *sys.argv)

ensure_dependencies()

import numpy as np
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP

# ---------------------------------------------------------------------------
# Datos conocidos (hardcodeados)
# ---------------------------------------------------------------------------
YEARS_KNOWN = np.array([
    1994, 1996, 1997, 1998, 1999, 2001, 2002, 2003, 2004, 2005,
    2006, 2007, 2008, 2010, 2012, 2013, 2014, 2015, 2017, 2018,
    2019, 2020, 2021, 2022, 2023
], dtype=float)

PCT_KNOWN = np.array([
    0.319, 0.783, 1.17, 2.69, 5.44, 12.5283, 40.14, 43.04, 52.89, 55.19,
    56.08, 61.8, 66.05, 75.71, 76.71, 77.8826, 79.9843, 77.6347, 81.6257, 80.4489,
    82.8537, 89.9209, 88.9256, 89.0677, 87.2131
], dtype=float)

MISSING_YEARS = [1995, 2000, 2009, 2011, 2016]

# ---------------------------------------------------------------------------
# Redondeo custom a 5 decimales
# ---------------------------------------------------------------------------
def custom_round(val):
    """Redondea al quinto decimal usando ROUND_HALF_UP."""
    d = Decimal(str(val))
    return d.quantize(Decimal('1.00000'), rounding=ROUND_HALF_UP)

# ---------------------------------------------------------------------------
# Lagrange
# ---------------------------------------------------------------------------
def lagrange_interpolate(x, x_nodes, y_nodes):
    n = len(x_nodes)
    result = 0.0
    for i in range(n):
        term = float(y_nodes[i])
        for j in range(n):
            if i != j:
                term *= (x - x_nodes[j]) / (x_nodes[i] - x_nodes[j])
        result += term
    return result

# ---------------------------------------------------------------------------
# Neville
# ---------------------------------------------------------------------------
def neville_interpolate(x, x_nodes, y_nodes):
    n = len(x_nodes)
    Q = np.zeros((n, n), dtype=float)
    Q[:, 0] = y_nodes
    for j in range(1, n):
        for i in range(n - j):
            Q[i, j] = (
                (x - x_nodes[i+j]) * Q[i, j-1] - (x - x_nodes[i]) * Q[i+1, j-1]
            ) / (x_nodes[i] - x_nodes[i+j])
    return Q[0, n-1], Q

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    print("=" * 80)
    print(" ANALISIS NUMERICO — PROYECTO FINAL ")
    print(" Interpolacion Polinomial: Lagrange y Neville ")
    print(" Pais 16 | Derek Sarmiento Loeber ")
    print("=" * 80)

    # Seccion 1
    print("\n" + "-" * 40)
    print("SECCION 1 — Datos Conocidos")
    print("-" * 40)
    print(f"Total de puntos conocidos: {len(YEARS_KNOWN)}")
    print(f"Periodo: {int(YEARS_KNOWN[0])}–{int(YEARS_KNOWN[-1])}")
    print("\nYear    | Percentage (%)")
    print("-" * 25)
    for yr, pct in zip(YEARS_KNOWN, PCT_KNOWN):
        print(f"{int(yr)}  | {pct}")

    # Seccion 2
    print("\n" + "-" * 40)
    print("SECCION 2 — Lagrange Interpolation")
    print("-" * 40)
    lagrange_results = []
    for year in MISSING_YEARS:
        val = lagrange_interpolate(year, YEARS_KNOWN, PCT_KNOWN)
        rounded = custom_round(val)
        lagrange_results.append((year, val, rounded))
        print(f"Year {year}: {val:.10f}  ->  {rounded}")

    # Seccion 3
    print("\n" + "-" * 40)
    print("SECCION 3 — Neville's Algorithm")
    print("-" * 40)
    neville_results = []
    for year in MISSING_YEARS:
        val, Q = neville_interpolate(year, YEARS_KNOWN, PCT_KNOWN)
        rounded = custom_round(val)
        neville_results.append((year, val, rounded, Q))
        print(f"Year {year}: {val:.10f}  ->  {rounded}")

    # Seccion 4
    print("\n" + "-" * 40)
    print("SECCION 4 — Comparacion")
    print("-" * 40)
    print(f"{'Year':<8} {'Lagrange (5 dec)':<18} {'Neville (5 dec)':<18} {'Diff':<18} {'Match?'}")
    print("-" * 70)
    for (yl, vl, rl), (yn, vn, rn, _) in zip(lagrange_results, neville_results):
        diff = abs(float(rl) - float(rn))
        match = "SI" if diff == 0 else f"{diff:.2e}"
        print(f"{yl:<8} {rl:<18} {rn:<18} {diff:<18.5f} {match}")

    # Seccion 5 — Tabla Completa
    print("\n" + "-" * 40)
    print("SECCION 5 — Tabla Completa 1994-2023")
    print("-" * 40)
    print(f"{'Year':<8} {'Percentage (%)':<18} {'Nota'}")
    print("-" * 45)
    
    known_dict = {int(y): v for y, v in zip(YEARS_KNOWN, PCT_KNOWN)}
    est_dict = {y: float(r) for y, _, r in lagrange_results}
    
    for year in range(1994, 2024):
        if year in est_dict:
            print(f"{year:<8} {est_dict[year]:<18.5f} *Estimado")
        else:
            print(f"{year:<8} {known_dict[year]:<18} Conocido")

    # Seccion 6 — Q-Table de Neville para 1995 (muestra)
    print("\n" + "-" * 40)
    print("SECCION 6 — Q-Table (Neville) para año 1995 (muestra reducida)")
    print("-" * 40)
    _, Q_1995 = neville_interpolate(1995, YEARS_KNOWN, PCT_KNOWN)
    df_q = pd.DataFrame(Q_1995[:6, :6])  # Mostrar solo 6x6 como muestra
    print(df_q.to_string())

    # Seccion 7 — Analisis
    print("\n" + "=" * 80)
    print("SECCION 7 — Analisis de Estabilidad y Error")
    print("=" * 80)
    print(f"""
Grado del polinomio interpolador: {len(YEARS_KNOWN)-1}
Numero de nodos: {len(YEARS_KNOWN)}

FENOMENO DE RUNGE:
El resultado para 1995 ({lagrange_results[0][1]:.2f}%) demuestra oscilaciones 
masivas propias del fenomeno de Runge. Interpolacion polinomial global de 
alto grado sobre nodos casi equiespaciados produce inestabilidad severa, 
especialmente cerca de los extremos del intervalo (1995, 2000).

Los valores centrales (2009, 2011, 2016) son mas estables y realistas.

Termino de error teorico:
    f^(n+1)(xi) / (n+1)! * Prod(x - x_i)

Este termino crece exponencialmente cerca de los extremos cuando los nodos
estan uniformemente distribuidos (como los años).

Estrategias de mitigacion (conceptual):
- Interpolacion por tramos (splines cubicas): mantiene grado bajo (3) entre
  nodos adyacentes en lugar de un polinomio global de grado 24.
- Nodos de Chebyshev: agrupados cerca de los extremos del intervalo para
  suprimir oscilaciones. No aplicables aqui porque los años son fijos.
""")
    print("=" * 80)
    print("FIN DEL REPORTE")
    print("=" * 80)

if __name__ == "__main__":
    main()
