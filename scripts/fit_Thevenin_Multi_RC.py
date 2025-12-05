import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

#=================
# 1. LOAD EIS DATA
#=================
base_dir = os.path.dirname((os.path.abspath(__file__)))
data_path = os.path.join(base_dir, "data", "EIS_data.csv")
df = pd.read_csv(data_path, header=0, skiprows=[1])
df_selected = df[["Freq", "Zreal", "Zimag"]]

f = df_selected["Freq"].values
Z_real = df_selected["Zreal"].values
Z_imag = df_selected["Zimag"].values

omega = 2 * np.pi * f
Z_meas = Z_real + 1j * Z_imag


#=========================================
# 2. CIRCUIT ELEMENT DEFINITIONS and MODEL
#=========================================

def RC_parallel(omega, R, C):
    """Parallel Resistor-Capacitor (RC) impedance block"""
    # Z_RC = R / (1 + j*omega*R*C)
    return R / (1 + 1j * omega * R * C)

def battery_eis_model(params, omega):
    """
    params = [Rs, R1, C1, R2, C2]
    """

    Rs, R1, C1, R2, C2 = params

    # --- RC Block 1 (High Frequency/Short Time Constant) ---
    Z_rc1 = RC_parallel(omega, R1, C1)

    # --- RC Block 2 (Low Frequency/Long Time Constant) ---
    Z_rc2 = RC_parallel(omega, R2, C2)

    # --- Total impedance (series sum) ---
    Z_total = Rs + Z_rc1 + Z_rc2

    return Z_total

#=====================
# 3. RESIDUAL FUNCTION
#=====================

def residuals(params, omega, Z_meas):
    Z_fit = battery_eis_model(params, omega)
    res_real = np.real(Z_fit - Z_meas)
    res_imag = np.imag(Z_fit - Z_meas)
    return np.concatenate([res_real, res_imag])

#===================
# 4. INITIAL GUESSES
#===================

# Initial guess for the high-frequency intercept
Rs0 = np.min(Z_real) * 0.9

# Initial guesses for RC pair 1 (faster dynamics)
R10 = 0.5 * (np.max(Z_real) - Rs0) * 0.5  # Arbitrary split of remaining resistance
C10 = 1e-4                               # Typical high-frequency capacitance (uF to mF range)

# Initial guesses for RC pair 2 (slower dynamics)
R20 = (np.max(Z_real) - Rs0) * 0.5        # Arbitrary split of remaining resistance
C20 = 1e-1                               # Typical low-frequency capacitance (mF to F range)

x0 = [Rs0, R10, C10, R20, C20]

# Physical bounds
lower_bounds = [0, 0, 1e-9, 0, 1e-9]
upper_bounds = [np.inf, np.inf, np.inf, np.inf, np.inf]

#===========
# 5. RUN FIT
#===========

result = least_squares(
    residuals,
    x0,
    args=(omega, Z_meas),
    bounds=(lower_bounds, upper_bounds),
    xtol=1e-12,
    ftol=1e-12,
    max_nfev=30000
)

Rs, R1, C1, R2, C2 = result.x

#===========================
# 6. PRINT FITTED PARAMETERS
#===========================

print("\n========== 2-RC THEVENIN ECM FIT ==========")
print(f"Rs (Series/Electrolyte Res.)  = {Rs:.4g} Ω")
print(f"R1 (RC1 Resistance)           = {R1:.4g} Ω")
print(f"C1 (RC1 Capacitance)          = {C1:.4e} F")
print(f"Tau1 (RC1 Time Constant)      = {R1 * C1:.4e} s")
print(f"R2 (RC2 Resistance)           = {R2:.4g} Ω")
print(f"C2 (RC2 Capacitance)          = {C2:.4e} F")
print(f"Tau2 (RC2 Time Constant)      = {R2 * C2:.4e} s")
print("===========================================\n")

#================
# 7. NYQUIST PLOT
#================

Z_fit = battery_eis_model(result.x, omega)

plt.figure(figsize=(8,6))
plt.scatter(Z_real, -Z_imag, color='blue', label='Experimental Data', s=40)
plt.plot(Z_fit.real, -Z_fit.imag, color='red', lw=2, label='2-RC Thevenin Fit')

plt.xlabel('$Z_{real}$ / $\\Omega$', fontsize=14)
plt.ylabel('$-Z_{imag}$ / $\\Omega$', fontsize=14)
plt.title('Nyquist Plot: Battery 2-RC Thevenin ECM', fontsize=16)
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()