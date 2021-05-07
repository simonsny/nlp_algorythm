from flask import Flask, request, jsonify, render_template
from utils.nlp import Summarizer
from utils.scraper import scrape_url
#from utils.sentiment import sentiment
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import matplotlib.pyplot as plt


app = Flask(__name__)
URL_80 = 'https://www.gutenberg.org/files/103/103-h/103-h.htm'

pic_folder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = pic_folder

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict_text", methods=["POST"])
def predict_text():
    text = [str(x) for x in request.form.values()]
    text = text[0]
    if len(text) > 50:
        summarizer.book = text
    summarizer.chunk_book()
    output = summarizer.summarize_chunks()
    sentences = summarizer.text_to_sentences(output)
    sentiment(sentences)
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'figure.png')
    return render_template(
        "result.html", summarization=output, user_image=pic1
    )

@app.route("/predict_url", methods=["POST"])
def predict_url():
    url = text = [str(x) for x in request.form.values()][0]
    book = scrape_url(url)
    summarizer.set_book(book)
    summarizer.chunk_book()
    output = summarizer.summarize_chunks()

    sentences = summarizer.text_to_sentences(output)
    sentiment(sentences)
    pic = os.path.join(app.config['UPLOAD_FOLDER'], 'figure.png')
    print(pic)
    return render_template(
        "result.html", summarization=output, user_image=pic
    )

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')


def sentiment(sentences: list):
    """
    Takes a list of sentences and creates an image with sentiment analysis.
    """
    analyzer = SentimentIntensityAnalyzer()
    sentiments = {'compound': [0.0], 'neg': [0.0], 'neu': [0.0], 'pos': [0.0]}
    for s in sentences:
        vs = analyzer.polarity_scores(s)
        sentiments['compound'].append(vs['compound'])
        sentiments['neg'].append(vs['neg'])
        sentiments['neu'].append(vs['neu'])
        sentiments['pos'].append(vs['pos'])

    for key in sentiments.keys():
        print(len(sentiments[key]))
        sentiments[key] = moving_average(np.array(sentiments[key]), 5)
        print(len(sentiments[key]))
        plt.plot(sentiments[key], label=key)
    plt.savefig('figure.png')
    plt.savefig('static/images/figure.png')


if __name__ == "__main__":
    summarizer = Summarizer()
    app.run(debug=True)
