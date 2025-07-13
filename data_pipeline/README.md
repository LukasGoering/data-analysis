# 🧹 Data Preprocessing Pipeline

This Python project implements a complete **data preprocessing pipeline** for structured datasets using **pandas**, **NumPy**, and **scikit-learn**. It includes dummy data generation, handling missing values, outlier removal, feature scaling, and categorical encoding.

---

## ⚙️ Features

- ✅ Dummy dataset generation with numeric and categorical columns  
- ✅ Missing value imputation (mean for numerics, 'Unknown' for categories)  
- ✅ Outlier removal using Z-score (threshold: ±3)  
- ✅ Feature scaling with `StandardScaler`  
- ✅ One-hot encoding for categorical columns  
- ✅ CSV export of raw and processed data  
- ✅ Toggleable verbosity via `VERBOSE` flag

---

## 🔄 Pipeline Overview

### 1. Generate Dummy Data
    generate_data(load_path)
Creates a dataset with:
- Normally distributed values (`Feature1`)
- Random integers (`Feature2`)
- Categorical values (`Category`)
- Binary classification target (`Target`)

---

### 2. Load Data
    df = load_data(filepath)

---

### 3. Handle Missing Values
    df[col] = df[col].fillna(df[col].mean())

---

### 4. Remove Outliers
Removes rows where any numeric feature has a Z-score > 3.

---

### 5. Scale Numeric Features
Standardizes numeric columns to zero mean and unit variance.

---

### 6. Encode Categorical Variables
Missing categories are labeled "Unknown" before one-hot encoding.

---

### 7. Save Processed Data
Output saved as:
    Data/data_preprocessing_pipeline.csv

---

## 🛠 Requirements

Install dependencies with:

    pip install pandas numpy matplotlib missingno scikit-learn scipy

---

## ▶️ How to Run

    python data_preprocessing_pipeline.py

Output:
    Preprocessing complete. Preprocessed data saved as Data/data_preprocessing_pipeline.csv

---

## 📌 Notes

- Modify the `VERBOSE = True` flag to inspect intermediate results.
- This template can be easily extended to real datasets by replacing the dummy data generation and `load_path`.

---

## 📜 License

MIT License. Feel free to use, adapt, and share.
