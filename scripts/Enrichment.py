import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("results.csv")

df = df.sort_values(by="DeepEnzyme_score", ascending=False).reset_index(drop=True)

df["cum_active"] = df["active"].cumsum()

total_active = df["active"].sum()

df["recall"] = df["cum_active"] / total_active

df["fraction"] = (df.index + 1) / len(df)

plt.figure()

plt.plot(df["fraction"], df["recall"], label="DeepEnzyme_score")

plt.plot([0,1], [0,1], linestyle="--", label="Random")

plt.xlabel("Fraction of variants screened")
plt.ylabel("Fraction of actives recovered")
plt.title("Enrichment Curve")
plt.legend()

plt.tight_layout()
plt.show()