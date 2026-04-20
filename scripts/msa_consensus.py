import argparse
from collections import Counter


def read_alignment(file_path):
    sequences = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(">"):
                continue
            sequences.append(line)
    return sequences


def compute_consensus(sequences):
    n_seq = len(sequences)
    length = len(sequences[0])

    consensus = []
    conservation_scores = []

    for i in range(length):
        column = [seq[i] for seq in sequences if seq[i] != "-"]

        if not column:
            consensus.append("-")
            conservation_scores.append(0.0)
            continue

        counts = Counter(column)
        most_common_res, count = counts.most_common(1)[0]

        freq = count / len(column)

        consensus.append(most_common_res)
        conservation_scores.append(freq)

    return consensus, conservation_scores


def main():
    parser = argparse.ArgumentParser(description="Compute consensus and identify non-conserved positions from MSA")

    parser.add_argument("--aln", required=True, help="Input alignment file (FASTA or CLUSTAL-like)")
    parser.add_argument("--out", required=True, help="Output file")
    parser.add_argument("--threshold", type=float, default=0.7,
                        help="Conservation threshold (default=0.7). Below this = non-conserved")

    args = parser.parse_args()

    sequences = read_alignment(args.aln)

    if len(sequences) == 0:
        raise ValueError("No sequences found in alignment file")

    length = len(sequences[0])
    if not all(len(seq) == length for seq in sequences):
        raise ValueError("Alignment sequences must have equal length")

    consensus, scores = compute_consensus(sequences)

    non_conserved_positions = [
        i + 1 for i, s in enumerate(scores) if s < args.threshold
    ]

    with open(args.out, "w") as f:
        f.write("# Position\tConsensus\tConservation\n")
        for i, (res, score) in enumerate(zip(consensus, scores), start=1):
            f.write(f"{i}\t{res}\t{score:.3f}\n")

        f.write("\n# Non-conserved positions (threshold={}):\n".format(args.threshold))
        f.write(",".join(map(str, non_conserved_positions)) + "\n")

    print(f"Saved: {args.out}")
    print(f"Total positions: {length}")
    print(f"Non-conserved positions (<{args.threshold}): {len(non_conserved_positions)}")


if __name__ == "__main__":
    main()
