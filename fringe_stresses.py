import numpy as np
import matplotlib.pyplot as plt

# Fringe constant (MPa per fringe)
C = 1.645

# Beam height (meters)
h = 0.02534 # for unnotched and V-notch
#h = 0.02536 # for U-notch

# Fringe locations from top surface 
z_in_un = np.array([0.075, 0.313, 0.545, 0.770, 0.973])
z_in_u = np.array([0.292, 0.323, 0.360, 0.488, 0.720, 0.908])
z_in_v = np.array([0.302, 0.365, 0.498, 0.613, 0.718, 0.924])

#z = z_in_un * 0.0254 
#z = z_in_u * 0.0254 
z = z_in_v * 0.0254 

# Signed distance from neutral axis
y = (h / 2) - z

# Fringe orders
#N = np.array([2, 1, 0, 1, 2]) # for unnotched
N = np.array([3, 2, 1, 0, 1, 2]) # for u-notch and v-notch

# Stress (MPa)
sigma = C * N

# Print table
print("Fringe location y (mm) | Stress (MPa) | N")
print("----------------------------------------")
for yi, si, ni in zip(y * 1e3, sigma, N):
    print(f"{yi:>20.3f} | {si:>10.3f} | {ni}")

# Plot
plt.figure()
plt.plot(y * 1e3, sigma, 'o-')

# Label each point with fringe order
for yi, si, ni in zip(y * 1e3, sigma, N):
    plt.text(yi, si, f"N={ni}", fontsize=12,
             ha='left', va='bottom')

plt.xlabel('Signed distance from neutral axis (mm)', fontsize=12)
plt.ylabel('Stress |σ| (MPa)', fontsize=12)
plt.axvline(0, color='k', linewidth=1)
plt.grid(True)
plt.show()