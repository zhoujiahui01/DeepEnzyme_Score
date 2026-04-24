import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path


def read_dccm(file_path):
    data = []
    with open(file_path) as f:
        for line in f:
            if line.strip():
                data.append([float(x) for x in line.split()])
    return np.array(data)


def plot_matrix(matrix, title, output_name, cmap, vmin, vmax):
    plt.figure(figsize=(6, 5))
    plt.imshow(matrix, cmap=cmap, origin="lower", vmin=vmin, vmax=vmax)
    plt.colorbar(label="Correlation")
    plt.title(title)
    plt.xlabel("Residue index")
    plt.ylabel("Residue index")
    plt.tight_layout()
    plt.savefig(output_name, dpi=300)
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="Plot WT, mutant, and ΔDCCM matrices."
    )
    parser.add_argument("--wt", required=True, help="WT DCCM .dat file")
    parser.add_argument("--mut", required=True, help="Mutant DCCM .dat file")
    parser.add_argument(
        "--outdir",
        default="results",
        help="Output directory (default: results)"
    )
    parser.add_argument(
        "--prefix",
        default="DCCM",
        help="Output file prefix"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.3,
        help="ΔDCCM threshold for visualization"
    )

    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    dccm_wt = read_dccm(args.wt)
    dccm_mut = read_dccm(args.mut)

    if dccm_wt.shape != dccm_mut.shape:
        raise ValueError("WT and mutant DCCM dimensions do not match")

    delta = np.abs(dccm_mut - dccm_wt)

    plot_matrix(
        dccm_wt,
        "DCCM (WT)",
        outdir / f"{args.prefix}_WT.png",
        cmap="coolwarm",
        vmin=-1,
        vmax=1
    )

    plot_matrix(
        dccm_mut,
        "DCCM (Mutant)",
        outdir / f"{args.prefix}_Mut.png",
        cmap="coolwarm",
        vmin=-1,
        vmax=1
    )

    plot_matrix(
        delta,
        f"|ΔDCCM| (>{args.threshold})",
        outdir / f"{args.prefix}_Delta.png",
        cmap="viridis",
        vmin=args.threshold,
        vmax=1
    )

    print("[INFO] DCCM plots generated:")
    print(f" - {args.prefix}_WT.png")
    print(f" - {args.prefix}_Mut.png")
    print(f" - {args.prefix}_Delta.png")


if __name__ == "__main__":
    main()