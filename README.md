\# Machine Learning-Based Adaptive Immune Profiling Using AIRR Data



\## 📌 Project Overview



This project explores the use of Machine Learning (ML) techniques to analyze Adaptive Immune Receptor Repertoire (AIRR) sequencing data. It focuses on extracting meaningful patterns from T-cell receptor (TCR) sequences and developing a machine learning pipeline for immune repertoire analysis.



AIRR datasets contain large numbers of immune receptor sequences. Machine learning can help transform these sequences into numerical features and identify patterns that may support future immune-state classification research.



\## 🎯 Objectives



\- Process T-cell receptor repertoire data stored in TSV files.

\- Extract numerical features from amino acid sequences using k-mer frequency encoding.

\- Develop a baseline scoring mechanism for repertoire-level analysis.

\- Explore pseudo-labeling to construct provisional training labels when ground-truth labels are unavailable.

\- Train and compare machine learning models.

\- Build a pipeline that can process a new repertoire file for prediction.



\## 🧬 Dataset



The project uses AIRR-style repertoire data organized into training and testing directories.



The sequence data includes fields such as:



\- `junction\_aa` — amino acid sequence of the receptor junction.

\- `v\_call` — variable gene assignment.

\- `j\_call` — joining gene assignment.



The local datasets are excluded from this repository to avoid uploading large data files. Please ensure that you have permission to access and use the original dataset before using it.



\## ⚙️ Methodology



1\. \*\*Data loading:\*\* Read repertoire samples from TSV files.

2\. \*\*Sequence preprocessing:\*\* Extract and process amino acid sequences from `junction\_aa`.

3\. \*\*Feature extraction:\*\* Use overlapping k-mer frequency encoding to convert sequences into numerical feature vectors.

4\. \*\*Baseline scoring:\*\* Calculate a repertoire-level score using a distance-based approach.

5\. \*\*Pseudo-labeling:\*\* Generate provisional labels using predefined score thresholds, where applicable.

6\. \*\*Model training:\*\* Train and compare selected machine learning classifiers.

7\. \*\*Evaluation:\*\* Examine model performance using suitable evaluation metrics.

8\. \*\*Prediction:\*\* Apply the trained pipeline to a new repertoire file.



\## 🤖 Machine Learning Models



The project explores traditional machine learning methods, including:



\- Logistic Regression

\- Random Forest

\- XGBoost

\- LightGBM



The final model selection should be based on reproducible evaluation results rather than accuracy alone.



\## 🛠️ Technologies Used



\- Python

\- Pandas and NumPy

\- Scikit-learn

\- XGBoost

\- LightGBM

\- Git and GitHub

\- AIRR-style TSV data processing



\## 📁 Repository Structure



```text

AIRR-Immune-Profiling-ML/

├── README.md

├── .gitignore

├── sample\_submissions.csv

├── requirements.txt

├── src/

│   ├── feature\_extraction.py

│   ├── train\_model.py

│   └── predict\_tsv.py

├── notebooks/

│   └── model\_training.ipynb

└── docs/

&#x20;   └── project\_report.pdf

```



\*The `src/`, `notebooks/`, and `docs/` files are planned structure examples; add them only when the corresponding files exist.\*



\## 🚀 Getting Started



\### 1. Clone the repository



```bash

git clone https://github.com/Venkat-1208/AIRR-Immune-Profiling-ML.git

cd AIRR-Immune-Profiling-ML

```



\### 2. Create a virtual environment



```bash

python -m venv .venv

```



Activate it on Windows PowerShell:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



\### 3. Install dependencies



Once `requirements.txt` has been created:



```bash

pip install -r requirements.txt

```



\### 4. Run the pipeline



Run the training or prediction scripts after they have been added to the repository. Refer to their instructions and required data paths.



\## 📊 Evaluation



Model evaluation should include metrics such as:



\- Accuracy

\- Precision

\- Recall

\- F1-score

\- ROC-AUC, when appropriate

\- Confusion matrix



\*\*Important:\*\* If pseudo-labels are generated from a distance-based heuristic, performance measured against those labels reflects agreement with the heuristic. It does not establish real-world clinical diagnostic accuracy. Clinical claims require independently verified labels and appropriate validation.



\## 🔬 Future Work



\- Incorporate additional repertoire and gene-level features.

\- Investigate alternative sequence representations and deep learning models.

\- Improve pseudo-labeling through semi-supervised learning.

\- Evaluate using independently labeled datasets.

\- Develop a reproducible interface for analyzing new repertoire samples.



\## 👨‍💻 Author



\*\*Tarun Venkat Movva\*\*



GitHub: \[Venkat-1208](https://github.com/Venkat-1208)



\## 📄 Disclaimer



This project is intended for research and educational purposes. It is not a clinically validated diagnostic system.



## Baseline Results

The initial baseline uses Logistic Regression with repertoire-level features extracted from adaptive immune receptor repertoire (AIRR) TSV files.

### Dataset Summary

| Metric | Value |
|---|---:|
| Total repertoires | 3,610 |
| Training split | 2,888 |
| Test split | 722 |
| Extracted features | 8,190 |
| Skipped files | 0 |

### Evaluation Metrics

| Metric | Score |
|---|---:|
| Accuracy | 59.42% |
| Balanced Accuracy | 61.49% |
| Precision | 51.87% |
| Recall | 76.13% |
| F1-score | 61.70% |
| ROC-AUC | 0.6135 |

### Confusion Matrix

Rows represent actual labels and columns represent predicted labels.

| | Predicted Negative | Predicted Positive |
|---|---:|---:|
| Actual Negative | 193 | 219 |
| Actual Positive | 74 | 236 |

These are initial baseline results from a stratified random train/test split. Because repertoires from different dataset groups may appear in both splits, these results do not establish generalization to an entirely unseen dataset. Group-aware or leave-one-dataset-out validation is a necessary next step.

The current model is an experimental research baseline, not a clinically validated diagnostic system.

## Setup

Use Python 3.10 or another compatible Python version.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Dataset Organization

Place the training data locally in the following structure:

```text
train_datasets/
└── train_datasets/
    ├── train_dataset_1/
    │   ├── metadata.csv
    │   └── *.tsv
    ├── train_dataset_2/
    ├── train_dataset_3/
    ├── train_dataset_4/
    ├── train_dataset_5/
    ├── train_dataset_6/
    ├── train_dataset_7/
    └── train_dataset_8/
```

Each dataset directory must contain its metadata file and the corresponding repertoire TSV files. The dataset files are excluded from Git by `.gitignore`.

## Train the Model

From the project root:

```powershell
python .\src\train_model.py
```

The script extracts repertoire features, trains the Logistic Regression baseline, evaluates it, and saves the model and evaluation reports locally in the `results/` directory.

## Predict a Repertoire

Train the model first. Then provide the path to a repertoire TSV file:

```powershell
python .\src\predict_tsv.py "path\to\repertoire.tsv"
```

The script prints the predicted label and positive-class score.

To save the prediction to a CSV file:

```powershell
python .\src\predict_tsv.py "path\to\repertoire.tsv" --output "results\prediction.csv"
```

The trained model and generated results are local artifacts and are not included in the GitHub repository by the current ignore rules.

