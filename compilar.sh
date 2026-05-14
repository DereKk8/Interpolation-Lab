#!/bin/bash
pdflatex informe.tex
pdflatex informe.tex  # second pass for TOC and refs
echo "Compilación completa: informe.pdf"
