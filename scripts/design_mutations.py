import argparse
import pandas as pd


def read_consensus(file_path):
    consensus = {}
    with open(file_path, "r") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            pos = int(parts[0])
            aa = parts[1]
            consensus[pos] = aa
    return consensus


def read_fasta(file_path):
    seq = []
    with open(file_path, "r") as f:
        for line in f:
            if line.startswith(">"):
                continue
            seq.append(line.strip())
    return "".join(seq)


def main():
    parser = argparse.ArgumentParser(description="Design mutations based on DCCM + MSA consensus")

    parser.add_argument("--positions", required=True,
                        help="CSV from DCCM-csv.py (Residue_index column required)")
    parser.add_argument("--consensus", required=True,
                        help="Consensus file from msa_consensus.py")
    parser.add_argument("--wt-seq", required=True,
                        help="WT sequence in FASTA format")
    parser.add_argument("--out", required=True,
                        help="Output mutation list")

    args = parser.parse_args()

    df = pd.read_csv(args.positions)
    consensus = read_consensus(args.consensus)
    wt_seq = read_fasta(args.wt_seq)

    mutations = []

    for pos in df["Residue_index"]:
        if pos > len(wt_seq):
            continue

        wt_aa = wt_seq[pos - 1]
        cons_aa = consensus.get(pos, "-")

        if cons_aa == "-" or cons_aa == wt_aa:
            continue

        mutation = f"{wt_aa}{pos}{cons_aa}"
        mutations.append(mutation)

    with open(args.out, "w") as f:
        for m in mutations:
            f.write(m + "\n")

    print(f"Saved: {args.out}")
    print(f"Total mutations: {len(mutations)}")


if __name__ == "__main__":
    main()
