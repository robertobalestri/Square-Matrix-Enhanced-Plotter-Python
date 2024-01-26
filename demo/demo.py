import numpy as np
import squarematrixenhancedplotter as smep

# Example Matrices
matrix = np.random.rand(900, 900) * 10
matrix1 = np.random.rand(900, 900) * 10
matrix2 = np.random.rand(900, 900) * 10

smep.plot_matrix(matrix, title="Example Matrix")

# Plot matrices side by side
smep.plot_matrices_side_by_side(*[matrix, matrix1, matrix2], titles=["Example Matrix", "Example Matrix 1", "Example Matrix 2"])
