# clinical-data-cleaning-pipeline
Automated data validation and cleansing workflows for clinical datasets using Python and Pandas.
# Pharmaceutical Data Integrity & Cleansing Pipeline

## Project Overview
This repository implements an automated data validation and cleansing pipeline designed to audit, clean, and standardize high-stakes analytical laboratory logs. Built using **Python**, **Pandas**, and **NumPy**, the project simulates an industrial setting processing stability and quality metrics for an active pharmaceutical ingredient (API)—specifically focusing on batch parameters for **Lidocaine Hydrochloride Monohydrate** matrices.

The main objective is to showcase an ironclad approach to data quality, ensuring that raw, human-input data is systematically transformed into a production-ready dataset suitable for biostatistical analysis or downstream predictive modeling.

## Data Quality Anomalies Handled
The pipeline automatically identifies and resolves five distinct categories of data corruption:
* **Duplicated Records:** Detects and drops redundant multi-entry tracking logs without data loss.
* **Inconsistent Datetime Structural Strings:** Parses heterogeneous string formats (e.g., ISO, fallback slash notation) into standard datetime objects.
* **Missing Quantitative Values:** Imputes null values in critical metrics using localized historical statistical medians to prevent sample-size degradation.
* **Statistical Outliers (Fat-Finger Inputs):** Isolate and mitigate measurement extremes utilizing Interquartile Range (IQR) boundary capping techniques.
* **Physicochemical Domain Boundary Violations:** Implements logical validation checks on non-negotiable chemical fields (e.g., flags and corrections on impossible pH readings).

## Technical Architecture & Tools
* **Language:** Python 3.x
* **Core Libraries:** Pandas (Data manipulation & indexing), NumPy (Vectorized data boundary mapping).
* **Methodology:** Object-oriented workflow with parametric mathematical bounds.

## How It Works
The execution logic can be tracked via the core module `clean_pipeline.py`. To run the script locally and inspect the pipeline transformation, use:
```bash
python clean_pipeline.py
