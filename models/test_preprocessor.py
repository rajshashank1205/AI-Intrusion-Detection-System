from data_loader import DataLoader
from preprocessor import DataPreprocessor

loader = DataLoader()
df = loader.load()

processor = DataPreprocessor()
clean_df, encoder = processor.preprocess(df)

print(clean_df.head())
print(clean_df.shape)