# EIS-Fitting-Models
Different model for fitting Electrochemical Impedance Spectroscopy (EIS) data

# EIS Model Fitting Toolkit

This repository contains three standalone Python scripts for fitting **Electrochemical Impedance Spectroscopy (EIS)** data using:

* ✅ Randles Equivalent Circuit (for sensors)
* ✅ Modified Randles Model (for Li-ion batteries)
* ✅ Thevenin Multi-RC Equivalent Circuit Model (for battery ECM modeling)

Each script:

* Loads EIS data from a CSV file
* Defines the impedance model
* Fits the model to experimental data
* Plots the Nyquist diagram

---

## 📁 Project Files

| File Name                       | Description                                                       |
| ------------------------------- | ----------------------------------------------------------------- |
| `fit_randles.py`                | Fits EIS data using the classical Randles circuit                 |
| `fit_modified_randles_liion.py` | Fits EIS data using a Modified Randles model for Li-ion batteries |
| `fit_thevenin_multi_rc.py`      | Fits EIS data using a Multi-RC Thevenin ECM                       |

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

## ⚙️ Requirements

Install required libraries using:

```
pip install numpy scipy pandas matplotlib
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

Developed by: Vu Bao Chau Nguyen
Field: Electrochemical Impedance Spectroscopy (EIS), Battery Modeling, Sensors

---
