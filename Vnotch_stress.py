import numpy as np

# Loading setup 
l1 = 4.36 * 0.0254
la = 2.198 * 0.0254
F = 125.0

# Beam / notch geometry (meters)
D = 0.02534     # full beam height (m)
t = 0.00546     # thickness (out-of-plane) (m)
h = 0.250 * 0.0254     # notch depth (m)  
r = 0.00025     # notch tip radius (m) 
alpha = 40.426   # notch angle in degrees 

a = (l1 - la) / 2.0
M = (F / 2.0) * a

d = D - h
sigma_nom = 6.0 * M / (t * d**2)   # Pa

hr = h / r
hD = h / D

# First compute Ktu using the U-notch table form


# Now apply the V-notch correction 
if alpha <= 90.0:
    
    if 0.5 <= hr <= 2.0:
        C1 = 1.795 + 1.481*hr - 0.211*hr**2
        C2 = -3.544 - 3.677*hr + 0.578*hr**2
        C3 = 5.459 + 3.691*hr - 0.565*hr**2
        C4 = -2.678 - 1.531*hr + 0.205*hr**2
    else:
        C1 = 2.966 + 0.502*hr - 0.009*hr**2
        C2 = -6.475 - 1.126*hr + 0.019*hr**2
        C3 = 8.023 + 1.253*hr - 0.020*hr**2
        C4 = -3.572 - 0.634*hr + 0.010*hr**2

    Ktu = C1 + C2*hD + C3*hD**2 + C4*hD**3
    
    Kt = Ktu
else:
    if not (90.0 < alpha <= 150.0):
        raise ValueError("This formula is stated for alpha up to 150 deg.")
    if not (0.5 <= hr <= 4.0):
        raise ValueError("This V-notch correction is stated for 0.5 <= h/r <= 4.0.")

    x = alpha / 150.0
    Kt = 1.11*Ktu - ( -0.0159 + 0.2243*x - 0.4293*x**2 + 0.3609*x**3 ) * (Ktu**2)

sigma_max = Kt * sigma_nom

print("\n--- Analytical U-Notch Stress Calculation ---\n")

print(f"Moment arm, a = {a:.6f} m")
print(f"Bending moment, M = {M:.6f} N·m")

print(f"Beam height, D = {D:.6f} m")
print(f"Thickness, t = {t:.6f} m")
print(f"Notch depth, h = {h:.6f} m")
print(f"Notch radius, r = {r:.6f} m")
print(f"V angle, alpha = {alpha:.6f} degrees")

print(f"Reduced section height, d = {d:.6f} m")

print(f"Nominal bending stress, sigma_nom = {sigma_nom*1e-6:.3f} MPa")

print(f"Stress concentration factor, Kt = {Kt:.3f}")

print(f"\nMaximum notch-tip stress, sigma_max = {sigma_max*1e-6:.3f} MPa\n")