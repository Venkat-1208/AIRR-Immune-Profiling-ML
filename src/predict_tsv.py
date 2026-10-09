
from pathlib import Path
import argparse

import joblib
import pandas as pd

from feature_extraction import extract_repertoire_features


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = ROOT / "results" / "airr_logistic_regression.joblib"


def predict_tsv(tsv_path, model_path):
    tsv_path = Path(tsv_path)
    model_path = Path(model_path)

    if not tsv_path.is_file():
        raise FileNotFoundError(f"Input TSV not found: {tsv_path}")

    if not model_path.is_file():
        raise FileNotFoundError(
            f"Model not found: {model_path}. Train the model first."
        )

    features = extract_repertoire_features(tsv_path, k=3)
    model = joblib.load(model_path)

    # DictVectorizer ignores unknown features and fills missing training
    # features with zero, preserving the training feature schema.
    probability = model.predict_proba([features])[0, 1]
    predicted_label = int(probability >= 0.5)

    return {
        "input_file": str(tsv_path),
        "predicted_label": predicted_label,
        "positive_class_score": float(probability),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Score a TCR repertoire TSV with the trained AIRR model."
    )
    parser.add_argument("tsv_path", help="Path to the input repertoire TSV")
    parser.add_argument(
        "--model",
        default=str(DEFAULT_MODEL),
        help="Path to the trained .joblib model",
    )
    parser.add_argument(
        "--output",
        help="Optional path to save the prediction as a CSV",
    )
    args = parser.parse_args()

    result = predict_tsv(args.tsv_path, args.model)

    print(f"Input file: {result['input_file']}")
    print(f"Predicted label: {result['predicted_label']}")
    print(f"Positive-class score: {result['positive_class_score']:.6f}")

    if args.output:
        pd.DataFrame([result]).to_csv(args.output, index=False)
        print(f"Prediction saved to: {args.output}")


if __name__ == "__main__":
    main()
