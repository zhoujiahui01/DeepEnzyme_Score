import argparse
import pandas as pd


def read_fasta(file_path):
    seq = []
    with open(file_path, "r") as f:
        for line in f:
            if line.startswith(">"):
                continue
            seq.append(line.strip())
    return "".join(seq)


def read_mutations(file_path):
    mutations = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                mutations.append(line)
    return mutations


def apply_mutation(seq, mutation):
    """
    mutation format: A42V
    """
    wt_aa = mutation[0]
    mut_aa = mutation[-1]
    pos = int(mutation[1:-1])

    if pos > len(seq):
        raise ValueError(f"Position {pos} out of range")

    if seq[pos - 1] != wt_aa:
        raise ValueError(f"WT mismatch at {pos}: expected {wt_aa}, found {seq[pos - 1]}")

    new_seq = list(seq)
    new_seq[pos - 1] = mut_aa

    return "".join(new_seq)


def main():
    parser = argparse.ArgumentParser(description="Generate single mutant sequence library")

    parser.add_argument("--wt-seq", required=True, help="WT FASTA")
    parser.add_argument("--mutations", required=True, help="Mutation list (e.g., A42V)")
    parser.add_argument("--out", required=True, help="Output CSV")

    args = parser.parse_args()

    wt_seq = read_fasta(args.wt_seq)
    mutations = read_mutations(args.mutations)

    records = []

    for mut in mutations:
        try:
            mut_seq = apply_mutation(wt_seq, mut)
            records.append({
                "Mutation": mut,
                "Sequence": mut_seq
            })
        except Exception as e:
            print(f"Skipping {mut}: {e}")

    df = pd.DataFrame(records)
    df.to_csv(args.out, index=False)

    print(f"Saved: {args.out}")
    print(f"Total mutants: {len(df)}")


if __name__ == "__main__":
    main()