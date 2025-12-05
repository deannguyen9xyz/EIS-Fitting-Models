import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.optimize import least_squares

#======================
# 1. LOAD YOUR EIS DATA
#======================
base_dir = os.path.dirname((os.path.abspath(__file__)))
data_path = os.path.join(base_dir, "data", "EIS_data.csv")
df = pd.read_csv(data_path, header=0, skiprows=[1])
df_selected = df[["Freq", "Zreal", "Zimag"]]

f = df_selected["Freq"].values
Z_real = df_selected["Zreal"].values
Z_imag = df_selected["Zimag"].values

omega = 2 * np.pi * f
Z_meas = Z_real + 1j * Z_imag

#==========================
#2. WARMBURG + RANDLE MODEL
#==========================
def warburg_infinite(omega, Aw):
    """
    Infinite Warburg impedance:
    Zw = Aw * (1 - j) / sqrt(omega)
    """
    return Aw * (1 - 1j) / np.sqrt(omega)

def randles_impedance_model(params, omega):
    """
    Randles Circuit:
    Rs + ( Cdl || (Rct + Zw) )
    """
    Rs, Rct, Cdl, Aw = params

    j = 1j
    Zw = warburg_infinite(omega, Aw)
    Z_Rct_Zw = Rct + Zw

    # Admittances
    Y_Cdl = j * omega * Cdl
    Y_Rct_Zw = 1 / Z_Rct_Zw

    # Parallel combination
    Z_parallel = 1 / (Y_Cdl + Y_Rct_Zw)

    # Total impedance
    Z_total = Rs + Z_parallel
    return Z_total

#===================================
# 3. RESIDUAL FUNCTION (REAL + IMAG)
#===================================
def residuals(params, omega, Z_meas):
    Z_fit = randles_impedance_model(params, omega)
    res_real = np.real(Z_fit - Z_meas)
    res_imag = np.imag(Z_fit - Z_meas)
    return np.concatenate([res_real, res_imag])

#===================
# 4. INITIAL GUESSES
#===================
Rs0 = np.min(Z_real) * 0.8
Rct0 = (np.max(Z_real) - Rs0) * 0.8
Cdl0 = 1e-9
Aw0 = 100

x0 = [Rs0, Rct0, Cdl0, Aw0]

#Physical bounds
lower_bounds = [0, 0, 1e-12, 0]
upper_bounds = [np.inf, np.inf, 1, np.inf]

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
    max_nfev=20000
)

Rs_fit, Rct_fit, Cdl_fit, Aw_fit = result.x

#=================
# 6. PRINT RESULTS
#=================
print("\n========== FITTED RANDLE PARAMETERS ==========")
print(f"Rs  (Solution Resistance)   = {Rs_fit:.4g}  Ω")
print(f"Rct (Charge Transfer Res.) = {Rct_fit:.4g}  Ω")
print(f"Cdl (Double Layer Cap.)    = {Cdl_fit:.4e}  F")
print(f"Cdl                        = {Cdl_fit*1e9:.4g}  nF")
print(f"Aw  (Warburg Coefficient)  = {Aw_fit:.4g}")
print("==============================================")

#================
# 7. NYQUIST PLOT
#================
Z_fit = randles_impedance_model(result.x, omega)

plt.figure(figsize=(8,6))
plt.scatter(Z_real, -Z_imag, color='blue', label='Experimental Data', s=40)
plt.plot(Z_fit.real, -Z_fit.imag, color='red', lw=2, label='Randles Fit')
plt.xlabel('$Z_{real}$ / $\\Omega$', fontsize=14)
plt.ylabel('$-Z_{imag}$ / $\\Omega$', fontsize=14)
plt.title('Nyquist Plot: Randles Circuit (least_squares)', fontsize=16)
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()