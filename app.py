import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
from utils.summarizer import Summarizer, test

app = Flask(__name__)
#model = joblib.load(open("final_model_RFC.model", "rb"))


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    text = [str(x) for x in request.form.values()]
    text = text[0]
    print(text)

    summarizer.chunk_book()
    output = summarizer.summarize_chunks()
    return render_template(
        "result.html", summarization=output
    )

    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    summarization = round(prediction[0], 2)

    return render_template(
        "index.html", summarization=summarization
    )


if __name__ == "__main__":
    summarizer = Summarizer()
    app.run(debug=True)
