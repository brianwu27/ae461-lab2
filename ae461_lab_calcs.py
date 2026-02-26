import numpy as np
import matplotlib.pyplot as plt

# INPUTS
l1 = 4.36 * 0.0254 # distance from supports (m)
la = 2.198 * 0.0254 # distance from loads (m)

H = 0.02534 # beam height (m) 
t = 0.00546 # beam thickness (m) 

F = 155.0 # Applied force (N)
a = (l1 - la) / 2.0 # moment arm 

I = t * H**3 / 12.0 # moment of inertia
M = (F / 2.0) * a # Applied moment

# Fringe locations from top (in -> m)
z_in = np.array([0.075, 0.313, 0.545, 0.770, 0.973])
z = z_in * 0.0254


# BENDING STRESS
y = H/2.0 - z
sigma = np.abs(M * y / I)   # Stress in Pa

# Fringe order mapping
mid = np.argmin(np.abs(y))
N_all = np.abs(np.arange(len(z)) - mid)

# Remove neutral axis (N=0)
mask = N_all > 0
N_raw = N_all[mask]
sigma_raw = sigma[mask]

# Average symmetric pairs
N_unique = np.unique(N_raw)
sigma_avg = np.array([sigma_raw[N_raw == n].mean() for n in N_unique])

print("Averaged stresses:")
for n, s in zip(N_unique, sigma_avg):
    print(f"N = {n}:  sigma = {s/1e6:.3f} MPa")

slope = np.dot(N_unique, sigma_avg) / np.dot(N_unique, N_unique)  # Pa per fringe
f_sigma = slope * t                                               # Pa·m

print(f"\n(f_sigma / t) = {slope/1e6:.3f} MPa/fringe")
print(f"f_sigma = {f_sigma:.1f} Pa·m")

# PLOT
plt.figure()

# Raw points
plt.plot(N_raw, sigma_raw/1e6, 'o', label='Raw |σ|')

# Averaged points
plt.plot(N_unique, sigma_avg/1e6, 's', markersize=8,
         label='Averaged per N')

# Final fit (through origin)
N_fit = np.linspace(0, N_unique.max(), 200)
plt.plot(N_fit, (slope * N_fit)/1e6, '-', 
         label='σ = (fσ/t)·N (through origin)')

plt.xlabel('Fringe order N (dark fringes)')
plt.ylabel('|σ| (MPa)')
plt.grid(True)
plt.legend()
plt.xticks(np.arange(0, N_unique.max() + 1, 1))
plt.show()