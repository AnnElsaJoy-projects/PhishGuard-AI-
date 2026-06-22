from preprocessing import load_and_process_data
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os


# Load processed data
X_train, X_test, y_train, y_test, vectorizer = load_and_process_data()


# Create model
model = LogisticRegression()


# Train model
model.fit(X_train, y_train)


# Test model
prediction = model.predict(X_test)


# Accuracy
accuracy = accuracy_score(y_test, prediction)

print("Model Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, prediction))


# Create model folder
os.makedirs("model", exist_ok=True)


# Save model
pickle.dump(model, open("model/phishing_detector.pkl", "wb"))

pickle.dump(
    vectorizer,
    open("model/vectorizer.pkl", "wb")
)

print("Model saved successfully!")