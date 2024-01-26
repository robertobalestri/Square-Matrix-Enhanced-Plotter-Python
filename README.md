# Square Matrix Enhanced Plotter

Square Matrix Enhanced Plotter is a Python package for interactive and enhanced visualization of square matrices. It leverages Matplotlib and mplcursors to provide zoom and interaction capabilities.

## Features

- Zoom in/out functionality for matrix visualization.
- Interactive cursors for detailed examination of matrix elements.
- Enhanced plotting capabilities for square matrices.

## Installation

You can install Square Matrix Enhanced Plotter using pip:

```bash
pip install SquareMatrixEnhancedPlotter
```

## Usage

Here is a simple example of how to use the Square Matrix Enhanced Plotter:

# Example square matrix
```bash
import numpy as np
import squarematrixenhancedplotter as smep

# Example Matrices
matrix = np.random.rand(9, 9)
matrix1 = np.random.rand(9, 9)

# Plot matrices side by side
smep.plot_matrices_side_by_side(*[matrix, matrix1], titles=["Example Matrix", "Example Matrix 1"])
```

# Contributing

Contributions to the Square Matrix Enhanced Plotter are welcome!
License

This project is licensed under the MIT License - see the LICENSE file for details.