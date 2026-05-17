import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# ============================================================
# Figure 3.2: Point Doubling on an Elliptic Curve
# Curve: E: y^2 = x^3 - x + 1
# Example point:
# P = (1, 1)
# Then 2P = (-1, 1)
# ============================================================

# Curve parameters: y^2 = x^3 + ax + b
a = -1
b = 1

def curve_function(x, y):
    return y**2 - (x**3 + a*x + b)

def f(x):
    return x**3 + a*x + b

# Point on the curve
P = np.array([1.0, 1.0])

# Check that P is on the curve
assert abs(P[1]**2 - f(P[0])) < 1e-9

# Tangent slope at P
# lambda = (3x1^2 + a) / (2y1)
m = (3 * P[0]**2 + a) / (2 * P[1])
c = P[1] - m * P[0]

# For doubling:
# x3 = lambda^2 - 2x1
# y3 = lambda(x1 - x3) - y1
x3 = m**2 - 2 * P[0]
y3 = m * (P[0] - x3) - P[1]

# R = 2P
R = np.array([x3, y3])

# R' is the point before reflection
R_prime = np.array([x3, -y3])

# Create grid for implicit plotting
x_min, x_max = -2.0, 2.4
y_min, y_max = -2.4, 2.4

x = np.linspace(x_min, x_max, 800)
y = np.linspace(y_min, y_max, 800)

X, Y = np.meshgrid(x, y)
Z = curve_function(X, Y)

plt.figure(figsize=(7, 6))

# Plot elliptic curve using implicit equation
plt.contour(
    X, Y, Z,
    levels=[0],
    colors="green",
    linewidths=2
)

# Plot tangent line at P
x_tangent = np.linspace(-1.5, 1.7, 300)
y_tangent = m * x_tangent + c

plt.plot(
    x_tangent,
    y_tangent,
    color="seagreen",
    linewidth=1.8
)

# Reflection line from R' to R
plt.plot(
    [R_prime[0], R[0]],
    [R_prime[1], R[1]],
    color="gray",
    linestyle="--",
    linewidth=1.2
)

# Plot points
plt.scatter(P[0], P[1], color="black", s=45, zorder=5)
plt.scatter(R_prime[0], R_prime[1], color="black", s=45, zorder=5)
plt.scatter(R[0], R[1], color="red", s=45, zorder=5)

# Labels
plt.text(P[0] + 0.08, P[1] + 0.15, r"$P(1,1)$", fontsize=11)
plt.text(R_prime[0] - 0.75, R_prime[1] - 0.2, r"$R'(-1,-1)$", fontsize=11)
plt.text(R[0] - 0.75, R[1] + 0.15, r"$R(-1,1)=2P$", color="red", fontsize=11)

# Axes
plt.axhline(0, color="black", linewidth=0.8)
plt.axvline(0, color="black", linewidth=0.8)

plt.text(x_max - 0.15, -0.18, r"$x$", fontsize=12)
plt.text(0.08, y_max - 0.2, r"$y$", fontsize=12)

# Legend
legend_elements = [
    Line2D([0], [0], color="green", linewidth=2, label=r"Curve $E$"),
    Line2D([0], [0], color="seagreen", linewidth=1.8, label=r"Tangent line at $P$"),
    Line2D([0], [0], marker="o", color="black", linestyle="None", label=r"Other intersection $R'$"),
    Line2D([0], [0], marker="o", color="red", linestyle="None", label=r"$R=2P$")
]

plt.legend(handles=legend_elements, loc="lower left")

# Formatting
plt.title(r"Figure 2: Point Doubling on an Elliptic Curve")
plt.grid(alpha=0.25)
plt.axis("equal")
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

# Save image for LaTeX
plt.savefig("Figure2.png", dpi=300, bbox_inches="tight")

plt.show()