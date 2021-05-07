from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import matplotlib.pyplot as plt
import os

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')


def sentiment(sentences):
    analyzer = SentimentIntensityAnalyzer()
    sentiments = {'compound': [0.0], 'neg': [0.0], 'neu': [0.0], 'pos': [0.0]}
    for s in sentences:
        vs = analyzer.polarity_scores(s)
        sentiments['compound'].append(vs['compound'])
        sentiments['neg'].append(vs['neg'])
        sentiments['neu'].append(vs['neu'])
        sentiments['pos'].append(vs['pos'])

    for key in sentiments.keys():
        sentiments[key] = moving_average(np.array(sentiments[key]), 5)
        plt.plot(sentiments[key], label=key)
    print('lala')
    #plt.show()
    print(os.getcwd())
    plt.savefig('figure.png')

    plt.show()
    print(sentiments)
