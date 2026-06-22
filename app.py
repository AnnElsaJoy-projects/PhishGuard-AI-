from flask import Flask, render_template, request
import pickle
import json
from datetime import datetime

from src.preprocessing import clean_text


app = Flask(__name__)


# Load model

model = pickle.load(
    open("model/phishing_detector.pkl", "rb")
)


# Load vectorizer

vectorizer = pickle.load(
    open("model/vectorizer.pkl", "rb")
)



# -----------------------------
# Detect suspicious keywords
# -----------------------------

def detect_keywords(email):

    words = [

        "urgent",
        "verify",
        "password",
        "account",
        "login",
        "click",
        "bank",
        "security",
        "suspended",
        "confirm",
        "winner",
        "free",
        "claim",
        "expire"

    ]


    found = []

    email = email.lower()


    for word in words:

        if word in email:

            found.append(word)


    return found




# -----------------------------
# Save history
# -----------------------------

def save_history(email,result):


    with open(
        "data/history.json",
        "r"
    ) as file:

        history=json.load(file)



    history.append({

        "email":email[:50],

        "risk":result["risk"],

        "confidence":result["confidence"],

        "time":
        datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        )

    })



    with open(
        "data/history.json",
        "w"
    ) as file:

        json.dump(
            history,
            file,
            indent=4
        )





# -----------------------------
# Statistics
# -----------------------------

def get_statistics():

    with open(
        "data/history.json",
        "r"
    ) as file:

        history=json.load(file)



    total=len(history)



    phishing=len(
        [
            x for x in history
            if x["risk"]=="HIGH"
        ]
    )



    safe=total-phishing



    return total,phishing,safe





# -----------------------------
# Home Dashboard
# -----------------------------

@app.route("/",methods=["GET","POST"])

def home():


    result=None



    if request.method=="POST":


        email=request.form["email"]



        cleaned=clean_text(email)



        vector=vectorizer.transform(
            [cleaned]
        )



        prediction=model.predict(
            vector
        )



        probability=model.predict_proba(
            vector
        )


        confidence=round(
            max(probability[0])*100,
            2
        )




        if prediction[0]==1:


            result={

                "risk":"HIGH",

                "confidence":confidence,

                "keywords":
                detect_keywords(cleaned)

            }



        else:


            result={

                "risk":"LOW",

                "confidence":confidence,

                "keywords":[]

            }



        save_history(
            email,
            result
        )





    total,phishing,safe=get_statistics()



    return render_template(

        "index.html",

        result=result,

        total=total,

        phishing=phishing,

        safe=safe

    )







# -----------------------------
# Analytics Page
# -----------------------------

@app.route("/analytics")

def analytics():


    with open(
        "data/history.json",
        "r"
    ) as file:


        history=json.load(file)



    total=len(history)



    phishing=len(

        [

        x for x in history

        if x["risk"]=="HIGH"

        ]

    )


    safe=total-phishing



    return render_template(

        "analytics.html",

        total=total,

        phishing=phishing,

        safe=safe,

        history=history[::-1]

    )





if __name__=="__main__":

    app.run(debug=True)