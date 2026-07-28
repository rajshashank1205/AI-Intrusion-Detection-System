from joblib import dump

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

from data_loader import DataLoader
from preprocessor import DataPreprocessor


print("Loading dataset...")
loader = DataLoader()
df = loader.load()

print("Preprocessing dataset...")
processor = DataPreprocessor()
df, encoder = processor.preprocess(df)

# Separate features and labels
X = df.drop(columns=["Label"])
y = df["Label"]

# Keep only numeric columns
X = X.select_dtypes(include=["number"])

print(f"Training Features : {X.shape}")
print(f"Training Labels   : {y.shape}")

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, predictions))
print("\nClassification Report:")
print(classification_report(y_test, predictions))

dump(model, "models/anomaly_detector.pkl")
dump(encoder, "models/label_encoder.pkl")

print("\n✅ Real AI model trained successfully!")