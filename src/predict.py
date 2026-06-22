import pickle
from preprocessing import clean_text


# Load saved model
model = pickle.load(
    open("model/phishing_detector.pkl", "rb")
)

vectorizer = pickle.load(
    open("model/vectorizer.pkl", "rb")
)


def predict_email(email):

    # Clean email
    email = clean_text(email)

    # Convert text
    email_vector = vectorizer.transform([email])

    # Prediction
    prediction = model.predict(email_vector)

    if prediction[0] == 1:
        return "⚠️ Phishing Email"
    else:
        return "✅ Safe Email"


# Test email
email = input("Enter email text: ")

result = predict_email(email)

print("\nPrediction:", result)