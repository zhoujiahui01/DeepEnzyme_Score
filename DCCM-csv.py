import numpy as np
import pandas as pd
import argparse


def read_dccm(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return np.array([[float(x) for x in line.split()] for line in lines])


def main():
    parser = argparse.ArgumentParser(description="Compute ΔDCCM and export CSV for SPM analysis")

    parser.add_argument("--wt", required=True, help="WT DCCM file")
    parser.add_argument("--mut", required=True, help="Mutant DCCM file")
    parser.add_argument("--ref-res", type=int, required=True, help="Reference residue index (1-based)")
    parser.add_argument("--threshold", type=float, default=0.3, help="Threshold for |ΔCij|")
    parser.add_argument("--out", required=True, help="Output CSV file")

    args = parser.parse_args()

    C_wt = read_dccm(args.wt)
    C_mut = read_dccm(args.mut)

    if C_wt.shape != C_mut.shape:
        raise ValueError(f"Size mismatch: WT={C_wt.shape}, Mut={C_mut.shape}")

    n = C_wt.shape[0]

    if not (1 <= args.ref_res <= n):
        raise ValueError(f"Residue {args.ref_res} out of range (1-{n})")

    delta_C = C_mut - C_wt

    diff_row = delta_C[args.ref_res - 1, :]

    indices = np.where(np.abs(diff_row) > args.threshold)[0]
    values = diff_row[indices]

    df = pd.DataFrame({
        "Residue_index": indices + 1,
        "Delta_Cij": values
    }).sort_values(by="Delta_Cij", ascending=False)

    df.to_csv(args.out, index=False)

    print(f"Saved: {args.out}")
    print(f"Number of residues above threshold: {len(df)}")


if __name__ == "__main__":
    main()