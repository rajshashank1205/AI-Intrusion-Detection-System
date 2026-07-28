import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder


class DataPreprocessor:
    """
    Cleans and prepares the CIC-IDS2017 dataset for AI training.
    """

    def preprocess(self, df):

        print("Cleaning dataset...")

        # Remove duplicate rows
        df = df.drop_duplicates()

        # Remove leading/trailing spaces in column names
        df.columns = df.columns.str.strip()

        # Replace infinities with NaN
        df.replace([np.inf, -np.inf], np.nan, inplace=True)

        # Remove rows containing NaN
        df.dropna(inplace=True)

        # Encode labels
        encoder = LabelEncoder()
        df["Label"] = encoder.fit_transform(df["Label"])

        print(f"Remaining Rows : {len(df)}")

        return df, encoder