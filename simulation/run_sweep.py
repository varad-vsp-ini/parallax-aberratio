"""
run_sweep.py

Executable script. Imports the core simulation from newcomb_core.py and:
  1. Runs a 1D sweep over p (alpha=0, i.e. the original blind-only model)
     and plots mean payoff vs. accuracy for CDT and EDT — this is the
     "first milestone" plot, with the theoretical crossover (p=0.5005)
     marked for comparison against the empirical result.
  2. Runs the full 2D sweep over (p, alpha) and produces the phase
     diagram — the headline Review 1 visual.

Both figures are saved into ./figures/ (created if it doesn't exist),
relative to wherever this script is run from — no hardcoded absolute
paths, so this runs the same on any machine.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from newcomb_core import Simulate

# ------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------
FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

n = int(input("How many trials per data point? (e.g. 2000): "))

THEORETICAL_CROSSOVER = 0.5005  # from the hand-derived EDT vs CDT crossover


# ------------------------------------------------------------------
# 1. First milestone plot: mean payoff vs. accuracy (alpha = 0)
# ------------------------------------------------------------------
print("\nRunning 1D sweep (alpha=0)...")

p_values_1d = np.linspace(0.01, 0.99, 100)
CDT_means_1d = []
EDT_means_1d = []

for p in p_values_1d:
    cdt_mean, edt_mean, _, _ = Simulate(p, alpha=0.0, n=n)
    CDT_means_1d.append(cdt_mean)
    EDT_means_1d.append(edt_mean)

plt.figure(figsize=(8, 6))
plt.plot(p_values_1d, CDT_means_1d, label="CDT (always two-box)")
plt.plot(p_values_1d, EDT_means_1d, label="EDT (expected utility)")
plt.axvline(THEORETICAL_CROSSOVER, color="black", linestyle="--",
            linewidth=1, label=f"theoretical crossover (p={THEORETICAL_CROSSOVER})")
plt.xlabel("Predictor Accuracy (p)")
plt.ylabel("Mean Payoff")
plt.title("Newcomb's Problem: Mean Payoff vs Predictor Accuracy (alpha=0)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
path_1d = os.path.join(FIGURES_DIR, "payoff_vs_accuracy.png")
plt.savefig(path_1d, dpi=140)
plt.close()
print(f"Saved: {path_1d}")


# ------------------------------------------------------------------
# 2. Headline plot: 2D phase diagram over (p, alpha)
# ------------------------------------------------------------------
print("\nRunning 2D sweep (p x alpha)... this takes longer.")

grid_size = 50
p_values_2d = np.linspace(0.01, 0.99, grid_size)
alpha_values_2d = np.linspace(0.0, 1.0, grid_size)

CDT_grid = np.zeros((grid_size, grid_size))
EDT_grid = np.zeros((grid_size, grid_size))

for i, alpha in enumerate(alpha_values_2d):
    for j, p in enumerate(p_values_2d):
        cdt_mean, edt_mean, _, _ = Simulate(p, alpha, n)
        CDT_grid[i, j] = cdt_mean
        EDT_grid[i, j] = edt_mean

winner_grid = np.where(EDT_grid > CDT_grid, 1, 0)  # 1 = EDT wins, 0 = CDT wins

plt.figure(figsize=(8, 6))
plt.imshow(
    winner_grid,
    extent=[p_values_2d.min(), p_values_2d.max(), alpha_values_2d.min(), alpha_values_2d.max()],
    origin="lower",
    aspect="auto",
    cmap="coolwarm"
)
plt.colorbar(label="0 = CDT wins, 1 = EDT wins")
plt.axvline(THEORETICAL_CROSSOVER, color="black", linestyle="--",
            linewidth=1, label=f"theoretical crossover (alpha=0)")
plt.xlabel("Predictor Accuracy (p_base)")
plt.ylabel("Predictor Adaptiveness (alpha)")
plt.title("Phase Diagram: CDT vs EDT")
plt.legend()
plt.tight_layout()
path_2d = os.path.join(FIGURES_DIR, "phase_diagram.png")
plt.savefig(path_2d, dpi=140)
plt.close()
print(f"Saved: {path_2d}")

print("\nDone. Note: below p=0.5005, CDT and EDT prescribe the SAME action,\n"
      "so the checkerboard pattern there is sampling noise around a tie,\n"
      "not a meaningful boundary — this is expected, see theory notes.")
