import sys
import os
import pandas as pd
import numpy as np

def error(msg):
    print("Error:", msg)
    sys.exit(1)

def validate_email(email):
    import re
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def topsis(input_file, weights, impacts, output_file):
    # ---------- Read file ----------
    if not os.path.exists(input_file):
        error("File not Found")

    try:
        df = pd.read_csv(input_file)
    except Exception:
        error("Unable to read CSV file")

    if df.shape[1] < 3:
        error("Input file must contain three or more columns")

    # ---------- Check numeric columns (2nd to last) ----------
    data = df.iloc[:, 1:].copy()
    for col in data.columns:
        if not pd.to_numeric(data[col], errors='coerce').notnull().all():
            error("From 2nd column to last column must contain numeric values only")

    data = data.astype(float)

    # ---------- Parse weights and impacts ----------
    weights = weights.split(",")
    impacts = impacts.split(",")

    if len(weights) != len(impacts):
        error("Number of weights must be equal to number of impacts")

    if len(weights) != data.shape[1]:
        error("Number of weights, impacts, and number of columns (from 2nd to last) must be same")

    try:
        weights = np.array([float(w) for w in weights])
    except:
        error("Weights must be numeric and separated by commas")

    impacts = [i.strip() for i in impacts]
    for i in impacts:
        if i not in ["+", "-"]:
            error("Impacts must be either +ve or -ve")

    # ---------- TOPSIS Steps ----------
    # Step 1: Normalize
    norm = np.sqrt((data**2).sum(axis=0))
    normalized = data / norm

    # Step 2: Apply weights
    weighted = normalized * weights

    # Step 3: Ideal best & worst
    ideal_best = []
    ideal_worst = []

    for j in range(weighted.shape[1]):
        if impacts[j] == "+":
            ideal_best.append(weighted.iloc[:, j].max())
            ideal_worst.append(weighted.iloc[:, j].min())
        else:
            ideal_best.append(weighted.iloc[:, j].min())
            ideal_worst.append(weighted.iloc[:, j].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # Step 4: Distance measures
    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    # Step 5: Score
    score = dist_worst / (dist_best + dist_worst)

    # Step 6: Rank
    df["Topsis Score"] = score
    df["Rank"] = df["Topsis Score"].rank(ascending=False, method="dense").astype(int)

    # ---------- Save output ----------
    df.to_csv(output_file, index=False)
    print("✅ TOPSIS completed successfully!")
    print("✅ Output saved to:", output_file)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        error("Usage: python topsis.py <InputDataFile> <Weights> <Impacts> <OutputFileName>")

    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file = sys.argv[4]

    topsis(input_file, weights, impacts, output_file)
