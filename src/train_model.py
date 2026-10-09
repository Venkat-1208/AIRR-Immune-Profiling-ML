
from pathlib import Path
import json
import time

import joblib
import numpy as np
import pandas as pd

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from feature_extraction import extract_repertoire_features


ROOT = Path(__file__).resolve().parents[1]
TRAIN_ROOT = ROOT / "train_datasets" / "train_datasets"
RESULTS_DIR = ROOT / "results"

RANDOM_STATE = 42
TEST_SIZE = 0.20


def main():
    start = time.time()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    feature_rows = []
    labels = []
    dataset_names = []
    skipped = []

    dataset_dirs = sorted(TRAIN_ROOT.glob("train_dataset_*"))

    if not dataset_dirs:
        raise FileNotFoundError(
            f"No training dataset folders found under {TRAIN_ROOT}"
        )

    print(f"Found {len(dataset_dirs)} dataset folders.")

    for dataset_dir in dataset_dirs:
        metadata_path = dataset_dir / "metadata.csv"

        if not metadata_path.exists():
            print(f"Skipping {dataset_dir.name}: metadata.csv missing")
            continue

        metadata = pd.read_csv(metadata_path)

        required = {"filename", "label_positive"}
        if not required.issubset(metadata.columns):
            raise ValueError(
                f"{metadata_path} must contain {sorted(required)}"
            )

        print(
            f"\nProcessing {dataset_dir.name}: "
            f"{len(metadata)} metadata records"
        )

        for _, row in metadata.iterrows():
            filename = str(row["filename"])
            tsv_path = dataset_dir / filename

            label_text = str(row["label_positive"]).strip().lower()
            if label_text not in {"true", "false"}:
                skipped.append(
                    {"file": str(tsv_path), "reason": "invalid label"}
                )
                continue

            if not tsv_path.is_file():
                skipped.append(
                    {"file": str(tsv_path), "reason": "file missing"}
                )
                continue

            try:
                features = extract_repertoire_features(tsv_path, k=3)

                if not features:
                    skipped.append(
                        {"file": str(tsv_path), "reason": "empty features"}
                    )
                    continue

                feature_rows.append(features)
                labels.append(1 if label_text == "true" else 0)
                dataset_names.append(dataset_dir.name)

            except Exception as exc:
                skipped.append(
                    {
                        "file": str(tsv_path),
                        "reason": f"{type(exc).__name__}: {exc}",
                    }
                )

        print(f"Successfully processed: {len(feature_rows)} total")

    if len(feature_rows) < 10 or len(set(labels)) < 2:
        raise RuntimeError(
            "Insufficient valid samples or only one class was found."
        )

    print(f"\nTotal valid repertoires: {len(labels)}")
    print(f"Positive labels: {sum(labels)}")
    print(f"Negative labels: {len(labels) - sum(labels)}")
    print(f"Skipped files: {len(skipped)}")

    # Split at repertoire level, not at individual TCR-sequence level.
    indices = np.arange(len(labels))
    train_idx, test_idx = train_test_split(
        indices,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=labels,
    )

    X_train = [feature_rows[i] for i in train_idx]
    X_test = [feature_rows[i] for i in test_idx]
    y_train = np.asarray(labels)[train_idx]
    y_test = np.asarray(labels)[test_idx]

    model = Pipeline(
        steps=[
            ("vectorizer", DictVectorizer(sparse=True)),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )

    print("\nTraining Logistic Regression...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = {
        "model": "Logistic Regression",
        "random_state": RANDOM_STATE,
        "test_size": TEST_SIZE,
        "n_samples": int(len(labels)),
        "n_train": int(len(train_idx)),
        "n_test": int(len(test_idx)),
        "n_features": int(
            len(model.named_steps["vectorizer"].get_feature_names_out())
        ),
        "accuracy": float(accuracy_score(y_test, predictions)),
        "balanced_accuracy": float(
            balanced_accuracy_score(y_test, predictions)
        ),
        "precision": float(
            precision_score(y_test, predictions, zero_division=0)
        ),
        "recall": float(
            recall_score(y_test, predictions, zero_division=0)
        ),
        "f1": float(f1_score(y_test, predictions, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, probabilities)),
        "confusion_matrix": confusion_matrix(
            y_test, predictions, labels=[0, 1]
        ).tolist(),
        "label_definition": "metadata.csv: label_positive",
    }

    model_path = RESULTS_DIR / "airr_logistic_regression.joblib"
    metrics_path = RESULTS_DIR / "baseline_metrics.json"
    report_path = RESULTS_DIR / "classification_report.txt"
    skipped_path = RESULTS_DIR / "skipped_files.json"

    joblib.dump(model, model_path)

    metrics_path.write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )

    report = classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["False", "True"],
        zero_division=0,
    )
    report_path.write_text(report, encoding="utf-8")

    skipped_path.write_text(
        json.dumps(skipped, indent=2), encoding="utf-8"
    )

    print("\n===== HELD-OUT BASELINE RESULTS =====")
    for key in [
        "n_samples",
        "n_train",
        "n_test",
        "n_features",
        "accuracy",
        "balanced_accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
    ]:
        print(f"{key}: {metrics[key]}")

    print("\nConfusion matrix (rows=actual, columns=predicted):")
    print(np.array(metrics["confusion_matrix"]))

    print("\nClassification report:")
    print(report)

    print(f"Model saved to: {model_path}")
    print(f"Metrics saved to: {metrics_path}")
    print(f"Skipped-file log: {skipped_path}")
    print(f"Elapsed time: {(time.time() - start) / 60:.1f} minutes")


if __name__ == "__main__":
    main()
