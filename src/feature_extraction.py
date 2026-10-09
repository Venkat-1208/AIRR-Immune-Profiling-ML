
from collections import Counter
from pathlib import Path
import pandas as pd


def extract_repertoire_features(tsv_path, k=3):
    """
    Extract repertoire-level features from a TCR repertoire TSV.

    Features:
    - Normalized overlapping amino-acid k-mer frequencies
    - V-gene frequencies
    - J-gene frequencies
    - Basic repertoire statistics
    """
    tsv_path = Path(tsv_path)
    df = pd.read_csv(tsv_path, sep="\t")

    required = {"junction_aa", "v_call", "j_call"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    sequences = (
        df["junction_aa"]
        .dropna()
        .astype(str)
        .str.upper()
        .tolist()
    )

    kmers = Counter()
    valid_sequences = []

    for sequence in sequences:
        sequence = sequence.strip()
        if len(sequence) < k:
            continue

        valid_sequences.append(sequence)

        for i in range(len(sequence) - k + 1):
            kmer = sequence[i:i + k]
            if all(aa in "ACDEFGHIKLMNPQRSTVWY" for aa in kmer):
                kmers[kmer] += 1

    total_kmers = sum(kmers.values())
    features = {
        f"kmer_{kmer}": count / total_kmers
        for kmer, count in kmers.items()
    } if total_kmers else {}

    for column, prefix in [("v_call", "v"), ("j_call", "j")]:
        genes = df[column].dropna().astype(str).str.strip()
        counts = genes.value_counts(normalize=True)

        for gene, frequency in counts.items():
            # Keep the feature name deterministic and readable.
            safe_gene = (
                gene.replace("/", "_")
                .replace("*", "_")
                .replace(" ", "_")
                .replace("-", "_")
            )
            features[f"{prefix}_{safe_gene}"] = float(frequency)

    features["repertoire_sequence_count"] = len(sequences)
    features["valid_sequence_count"] = len(valid_sequences)
    features["mean_sequence_length"] = (
        sum(map(len, valid_sequences)) / len(valid_sequences)
        if valid_sequences else 0.0
    )

    return features


if __name__ == "__main__":
    sample = (
        Path(__file__).resolve().parents[1]
        / "train_datasets"
        / "train_datasets"
        / "train_dataset_1"
        / "44967b361684556629a8b61288daf20c.tsv"
    )

    result = extract_repertoire_features(sample)
    print(f"Extracted {len(result)} features")
    print("Sample features:")

    for name, value in list(result.items())[:15]:
        print(f"{name}: {value}")
