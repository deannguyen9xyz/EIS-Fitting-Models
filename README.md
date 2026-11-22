# EIS-Fitting-Models
Different model for fitting Electrochemical Impedance Spectroscopy (EIS) data

# EIS Model Fitting Toolkit

This repository contains three standalone Python scripts for fitting **Electrochemical Impedance Spectroscopy (EIS)** data using:

* ✅ Randles Equivalent Circuit (can be used for sensors)

      Rs + ( Cdl || (Rct + Zw) )
* ✅ Modified Randles Model (can be used for Li-ion batteries)

      Rs – (Rsei||CPEsei) – (Rct||CPEdl) – W
* ✅ Thevenin Multi-RC Equivalent Circuit Model (2 RC Thevenin battery model)

      Rs – (R1||C1) – (R2||C2)

Each script:

* Loads EIS data from a CSV file
* Defines the impedance model
* Fits the model using least_square
* Plots the Nyquist diagram

---

## 📁 Project Files

| File Name                       | Description                                                       |
| ------------------------------- | ----------------------------------------------------------------- |
| `fit_Randles.py`                | Fits EIS data using the classical Randles circuit                 |
| `fit_modified_Randles` | Fits EIS data using a Modified Randles model for Li-ion batteries |
| `fit_Thevenin_Multi_RC.py`      | Fits EIS data using a Multi-RC Thevenin ECM                       |

---

## 📊 Input Data Format

Each script expects a **CSV file** with the following columns:

```
Freq, Zreal, Zimag
Hz, ohm, ohm
100000, 123.456, -234.567
50000, 345.678, -456.789
...
```

* `Freq` → Frequency in Hz
* `Zreal` → Real part of impedance (Ω)
* `Zimag` → Imaginary part of impedance (Ω)

---

### Sample data

`data/EIS_data.csv` is an impedance spectrum from an electrochemical sensor, so it suits `fit_Randles.py`. The modified Randles and Thevenin scripts are battery models: they run on this file, but the fitted values have no physical meaning there (for example, Rs ≈ 465 Ω from the Randles fit vs. 0.12 Ω from the modified Randles fit). Use battery EIS data for those two scripts.

---

## ⚙️ Requirements
Place the input CSV data file named "EIS_data.csv" in the `data/` folder at the top of the repository (next to `scripts/`).

Install required libraries using:

```
pip install -r requirements.txt
```
---

## ▶️ How to Run

Run each model separately, depends on the purpose:

### 1️⃣ Randles Model

```
python fit_randles.py
```

### 2️⃣ Modified Randles for Li-ion Battery

```
python fit_modified_randles_liion.py
```

### 3️⃣ Thevenin Multi-RC ECM

```
python fit_thevenin_multi_rc.py
```

Each script will:

* Print fitted parameter values
* Display the Nyquist plot

---

## 📈 Output

Each script generates:

* ✅ Nyquist plot (Z′ vs −Z″)
* ✅ Extracted circuit parameters (Rs, Rct, Cdl, RC values, etc.)

---

## 🎯 Purpose of This Project

This project is designed for:

* Electrochemical sensor modeling
* Battery EIS analysis
* Learning equivalent circuit modeling
* GitHub portfolio demonstration

---

## 📌 Future Improvements

* Add Bode plots
* Add more model for EIS fitting
* Add Jupyter notebook examples

---

## 🧑‍💻 Author

Developed by: Vu Bao Chau Nguyen, Ph.D.

Keywords: Electrochemical Impedance Spectroscopy (EIS), Battery Modeling, Sensors

---
