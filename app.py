from flask import Flask, render_template, request
import os
import pandas as pd
import numpy as np
import smtplib
from email.message import EmailMessage
import re

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def topsis(df, weights, impacts):
    data = df.iloc[:, 1:].astype(float)

    norm = np.sqrt((data**2).sum(axis=0))
    normalized = data / norm

    weighted = normalized * weights

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

    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = dist_worst / (dist_best + dist_worst)
    df["Topsis Score"] = score
    df["Rank"] = df["Topsis Score"].rank(ascending=False, method="dense").astype(int)
    return df

def send_email(to_email, filepath):
    sender_email = "kmittal_be23@thapar.edu"
    sender_password = "kashvi0208"

    msg = EmailMessage()
    msg["Subject"] = "TOPSIS Result File"
    msg["From"] = sender_email
    msg["To"] = to_email
    msg.set_content("Hello, please find attached TOPSIS result file.")

    with open(filepath, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="octet-stream", filename=os.path.basename(filepath))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    file = request.files["file"]
    weights = request.form["weights"]
    impacts = request.form["impacts"]
    email = request.form["email"]

    if not validate_email(email):
        return "Invalid Email Format"

    weights_list = weights.split(",")
    impacts_list = impacts.split(",")

    if len(weights_list) != len(impacts_list):
        return "Number of weights must equal number of impacts"

    for i in impacts_list:
        if i.strip() not in ["+", "-"]:
            return "Impacts must be + or - only"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    df = pd.read_csv(filepath)

    if df.shape[1] < 3:
        return "Input file must contain 3 or more columns"

    for col in df.columns[1:]:
        if not pd.to_numeric(df[col], errors="coerce").notnull().all():
            return "All columns except first must be numeric"

    if len(weights_list) != len(df.columns) - 1:
        return "Weights & impacts count must match numeric columns"

    weights_array = np.array([float(x) for x in weights_list])
    impacts_list = [x.strip() for x in impacts_list]

    result_df = topsis(df, weights_array, impacts_list)

    output_file = os.path.join(OUTPUT_FOLDER, "result.csv")
    result_df.to_csv(output_file, index=False)

    send_email(email, output_file)

    return "Result sent to your email successfully!"

if __name__ == "__main__":
    app.run(debug=True)
