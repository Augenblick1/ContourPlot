# ContourPlot

## Project Overview
ContourPlot is a contour mapping tool for geoscience and engineering data visualization. It enables efficient generation of contour plots from spatial datasets, supporting interpolation and visualization of geological, geophysical, and environmental variables such as temperature, pressure, elevation, and subsurface properties.

---

## Key Features
- Supports multiple 2D spatial interpolation methods (e.g., IDW, Kriging, depending on implementation)
- Generates contour maps and filled contour plots
- Supports geoscientific data import (Excel / CSV)
- Exports visualization results (PNG / JPG)
- Allows customization of grid resolution and contour intervals
- Applicable to hydrogeology, engineering geology, and environmental geology data analysis

---

## Requirements
- Conda
- Python 3.8+
- NumPy
- Pandas
- Matplotlib
- SciPy
- pyvista
- PySide6
- pyvistaqt

---

## Installation

This project uses a Conda environment file for dependency management.

```bash
# Clone repository
git clone https://github.com/Augenblick1/ContourPlot.git
cd ContourPlot

# Create environment from file
conda env create -f environment.yml

# Activate environment
conda activate contourplot