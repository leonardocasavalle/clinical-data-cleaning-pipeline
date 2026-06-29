Python
import numpy as np
import pandas as pd


def load_dirty_dataset():
    """Generates a dummy clinical/pharmaceutical dataset with structural anomalies

    to simulate real-world data cleansing operations.
    """
    raw_data = {
        "batch_id": [
            "B_101",
            "B_102",
            "B_103",
            "B_104",
            "B_101",
            "B_105",
            "B_106",
            "B_107",
        ],
        "assay_date": [
            "2026-05-12",
            "12/05/2026",
            "2026/05/13",
            None,
            "2026-05-12",
            "2026-05-14",
            "14-05-2026",
            "2026-05-15",
        ],
        "active_substance": [
            "Lidocaine HCl Monohydrate",
            "Lidocaine HCl Monohydrate",
            "Lidocaine HCl Monohydrate",
            "Lidocaine HCl Monohydrate",
            "Lidocaine HCl Monohydrate",
            "Lidocaine HCl Monohydrate",
            "Lidocaine HCl Monohydrate",
            "Lidocaine HCl Monohydrate",
        ],
        "concentration_mg_ml": [
            19.85,
            20.05,
            153.20,
            19.90,
            19.85,
            None,
            20.10,
            19.78,
        ],  # 153.20 is an outlier from manual typing error
        "ph_level": [6.45, 6.52, 6.38, 6.41, 6.45, 6.48, 14.20, 6.50],
    }  # 14.20 is an impossible pH reading for this stable acid solution
    return pd.DataFrame(raw_data)


def run_cleansing_pipeline(df):
    """Executes an automated validation and cleansing pipeline on the dataset."""
    print("--- Starting Data Cleansing Pipeline ---")
    cleaned_df = df.copy()

    # 1. Handle Duplicated Records
    initial_rows = len(cleaned_df)
    cleaned_df.drop_duplicates(keep="first", inplace=True)
    print(f"[INFO] Removed {initial_rows - len(cleaned_df)} duplicate rows.")

    # 2. Standardize Inconsistent Date Formats into ISO 8601
    print("[INFO] Standardizing datetime formats...")
    cleaned_df["assay_date"] = pd.to_datetime(
        cleaned_df["assay_date"], errors="coerce"
    )
    cleaned_df["assay_date"] = cleaned_df["assay_date"].ffill()

    # 3. Handle Missing Values in Critical Quantitative Measurements
    if cleaned_df["concentration_mg_ml"].isnull().any():
        median_concentration = cleaned_df["concentration_mg_ml"].median()
        cleaned_df["concentration_mg_ml"] = cleaned_df[
            "concentration_mg_ml"
        ].fillna(median_concentration)
        print(
            f"[INFO] Imputed missing concentration values using median: {median_concentration}"
        )

    # 4. Statistical Outlier Detection & Mitigation (Using IQR Method)
    q1 = cleaned_df["concentration_mg_ml"].quantile(0.25)
    q3 = cleaned_df["concentration_mg_ml"].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    cleaned_df["concentration_mg_ml"] = np.where(
        cleaned_df["concentration_mg_ml"] > upper_bound,
        upper_bound,
        np.where(
            cleaned_df["concentration_mg_ml"] < lower_bound,
            lower_bound,
            cleaned_df["concentration_mg_ml"],
        ),
    )
    print("[INFO] Analytical outliers handled using the IQR boundary capping.")

    # 5. Domain-Specific Logical Hard Boundaries
    cleaned_df["ph_level"] = np.where(
        cleaned_df["ph_level"] > 7.0, 6.5, cleaned_df["ph_level"]
    )
    print(
        "[INFO] Validated pH limits against strict physicochemical boundaries."
    )

    print("--- Pipeline Execution Completed Successfully ---")
    return cleaned_df


if __name__ == "__main__":
    dirty_data = load_dirty_dataset()
    print("\nInitial Raw (Dirty) Dataset:")
    print(dirty_data)

    clean_data = run_cleansing_pipeline(dirty_data)
    print("\nFinal Cleansed & Validated Dataset:")
    print(clean_data)
