import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# 1. Load Data
print("Loading dataset...")
try:
    data = pd.read_csv("phishing_data.csv")
except FileNotFoundError:
    print("Error: 'phishing_data.csv' not found. Please put it in this folder.")
    exit()

# 2. Preprocessing
# We drop 'index' (it's just row numbers) and 'Result' (what we want to predict)
# The rest are our features.
X = data.drop(['index', 'Result'], axis=1)
y = data['Result']

# 3. Training
print("Training Random Forest model (this might take a moment)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest is excellent for this specific dataset
model = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# 4. Save the Model
print("Saving model...")
pickle.dump(model, open("model.pkl", "wb"))
print("SUCCESS: model.pkl created!")