import pandas as pd
from pathlib import Path


class DataLoader:
    """
    Loads every CSV file from data/raw
    and combines them into one dataset.
    """

    def __init__(self, data_folder="data/raw"):
        self.data_folder = Path(data_folder)

    def load(self):

        csv_files = list(self.data_folder.glob("*.csv"))

        if not csv_files:
            raise FileNotFoundError("No CSV files found in data/raw")

        dataframes = []

        for file in csv_files:

            print(f"Loading {file.name}")

            df = pd.read_csv(file, low_memory=False)

            dataframes.append(df)

        dataset = pd.concat(dataframes, ignore_index=True)

        print("\nDataset Loaded Successfully")
        print(f"Total Rows    : {len(dataset)}")
        print(f"Total Columns : {len(dataset.columns)}")

        return dataset


if __name__ == "__main__":

    loader = DataLoader()

    data = loader.load()

    print(data.head())