import numpy as np
import os
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

def CPE(omega, Q, n):
    """Constant Phase Element (admittance form)"""
    return Q * (1j * omega) ** n

def warburg_infinite(omega, Aw):
    """Infinite Warburg impedance"""
    return Aw * (1 - 1j) / np.sqrt(omega)

def battery_eis_model(params, omega):
    """
    params = [Rs, Rsei, Qsei, nsei, Rct, Qdl, ndl, Aw]
    """

    Rs, Rsei, Qsei, nsei, Rct, Qdl, ndl, Aw = params

    # --- SEI parallel block ---
    Y_sei = (1 / Rsei) + CPE(omega, Qsei, nsei)
    Z_sei = 1 / Y_sei

    # --- Charge transfer parallel block ---
    Y_ct = (1 / Rct) + CPE(omega, Qdl, ndl)
    Z_ct = 1 / Y_ct

    # --- Warburg diffusion ---
    Z_w = warburg_infinite(omega, Aw)

    # --- Total impedance (series sum) ---
    Z_total = Rs + Z_sei + Z_ct + Z_w

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

Rs0   = np.min(Z_real) * 0.8
Rsei0 = 10
Qsei0 = 1e-5
nsei0 = 0.8
Rct0  = (np.max(Z_real) - Rs0) * 0.8
Qdl0  = 1e-4
ndl0  = 0.9
Aw0   = 50

x0 = [Rs0, Rsei0, Qsei0, nsei0, Rct0, Qdl0, ndl0, Aw0]

#Physical bounds
lower_bounds = [0, 0, 1e-12, 0.3, 0, 1e-12, 0.3, 0]
upper_bounds = [np.inf, np.inf, 1,  1.0, np.inf, 1,  1.0, np.inf]

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

Rs, Rsei, Qsei, nsei, Rct, Qdl, ndl, Aw = result.x

#==================
# 6. PRINT RESSULTS
#==================

print("\n========== FIT MODIFIED RANDLES PARAMETERS ==========")
print(f"Rs   (Electrolyte Resistance)   = {Rs:.4g} Ω")
print(f"Rsei (SEI Resistance)           = {Rsei:.4g} Ω")
print(f"Qsei (SEI CPE)                  = {Qsei:.4e}")
print(f"nsei (SEI Exponent)             = {nsei:.4f}")
print(f"Rct  (Charge Transfer Res.)    = {Rct:.4g} Ω")
print(f"Qdl  (Double Layer CPE)        = {Qdl:.4e}")
print(f"ndl  (DL Exponent)             = {ndl:.4f}")
print(f"Aw   (Warburg Coefficient)     = {Aw:.4g}")
print("=====================================================\n")

Z_fit = battery_eis_model(result.x, omega)

#================
# 7. NYQUIST PLOT
#================

Z_fit = battery_eis_model(result.x, omega)

plt.figure(figsize=(8,6))
plt.scatter(Z_real, -Z_imag, color='blue', label='Experimental Data', s=40)
plt.plot(Z_fit.real, -Z_fit.imag, color='red', lw=2, label='Modified Randles Fit')
plt.xlabel('$Z_{real}$ / $\\Omega$', fontsize=14)
plt.ylabel('$-Z_{imag}$ / $\\Omega$', fontsize=14)
plt.title('Nyquist Plot: Battery Modified Randles', fontsize=16)
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()