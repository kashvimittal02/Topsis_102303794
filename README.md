# TOPSIS Implementation in Python

**Name:** Kashvi Mittal  
**Roll Number:** 102303794  

---

## 1. Introduction

This project implements **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)**, a multi-criteria decision-making (MCDM) technique used to rank alternatives based on their distance from an ideal solution.

The assignment is divided into three parts:
- **Part-I:** Command-line TOPSIS implementation
- **Part-II:** Python package creation and PyPI deployment
- **Part-III:** Web service for TOPSIS with email-based result delivery

---

## 2. TOPSIS Methodology

TOPSIS is based on the concept that the best alternative should have the **shortest distance from the ideal best solution** and the **farthest distance from the ideal worst solution**.

### Step 1: Decision Matrix
The input CSV file consists of:
- First column: Alternative/Fund name (non-numeric)
- Remaining columns: Numeric criteria values

### Step 2: Normalization
Each criterion value is normalized to remove scale differences using vector normalization:

\[
r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{i=1}^{m} x_{ij}^2}}
\]

### Step 3: Weighted Normalized Matrix
Each normalized value is multiplied by its respective weight:

\[
v_{ij} = r_{ij} \times w_j
\]

### Step 4: Ideal Best and Ideal Worst
For each criterion:
- If impact is **positive (+)**:
  - Ideal Best = maximum value
  - Ideal Worst = minimum value
- If impact is **negative (-)**:
  - Ideal Best = minimum value
  - Ideal Worst = maximum value

### Step 5: Separation Measures
Euclidean distance of each alternative from ideal best and ideal worst is calculated.

### Step 6: TOPSIS Score
\[
C_i = \frac{S_i^-}{S_i^+ + S_i^-}
\]

A higher score indicates a better alternative.

### Step 7: Ranking
Alternatives are ranked in descending order of TOPSIS score.

---

## 3. Input and Output Format

### Input File Format
- Minimum 3 columns required
- First column: Alternative name
- Remaining columns: Numeric values only

**Sample Input**

| Fund Name | P1 | P2 | P3 | P4 | P5 |
|----------|----|----|----|----|----|
| M1 | 0.67 | 0.45 | 6.5 | 42.6 | 12.56 |
| M2 | 0.60 | 0.36 | 3.6 | 53.3 | 14.47 |

### Output File Format
Two additional columns are appended:
- **Topsis Score**
- **Rank**

**Sample Output**

| Fund Name | P1 | P2 | P3 | P4 | P5 | Topsis Score | Rank |
|----------|----|----|----|----|----|--------------|------|
| M1 | 0.67 | 0.45 | 6.5 | 42.6 | 12.56 | 20.58 | 2 |
| M2 | 0.60 | 0.36 | 3.6 | 53.3 | 14.47 | 40.83 | 4 |

---

## 4. Result Analysis and Graph Explanation

- Alternatives with **higher TOPSIS scores** are closer to the ideal solution.
- Rank 1 represents the best-performing alternative.
- A bar graph of TOPSIS scores clearly visualizes relative performance.
- The ranking is consistent with changes in criteria values and weights.

---

## 5. Part-I: Command Line Implementation

### Usage
```bash
python topsis.py <InputDataFile> <Weights> <Impacts> <OutputFileName>
```
Example
```bash
python topsis.py data.csv "1,1,1,2" "+,+,-,+" output-result.csv
```
- Input Validations Implemented
- Correct number of command-line parameters
- File not found handling
- Minimum three columns in input file
- Numeric validation for all criteria columns
- Equal number of weights, impacts, and criteria
- Impacts must be either + or -
- Weights and impacts must be comma-separated

---

## 6. Part-II: Python Package (PyPI)

- The TOPSIS implementation is packaged and uploaded to PyPI.
- **Package Name:** `Topsis-Kashvi-102303794`
- Installation:
```bash
pip install Topsis-Kashvi-102303794
```
- **PyPI Link:** https://pypi.org/project/Topsis-Kashvi-102303794/1.0.0/

---

## 7. Part-III: Web Service for TOPSIS

A web-based TOPSIS service is developed where the user provides:
- Input CSV file
- Weights
- Impacts
- Email ID

Features
- Input validation for weights and impacts
- Impacts must be + or -
- Weights and impacts must be comma-separated
- Valid email format check
- Result CSV file is emailed to the user

The user receives the computed TOPSIS result directly via email.

Open terminal inside Task-3 folder:
```
cd Topsis-Kashvi-102303794-Part3
```
Install dependencies:
```
python -m pip install -r requirements.txt
```
Start Flask server:
```
python app.py
```

---

## 8. Conclusion

This project successfully implements the TOPSIS decision-making technique across command-line, package-based, and web-based platforms. It ensures robustness through comprehensive input validation and provides scalable usability via PyPI and web service deployment.

---
