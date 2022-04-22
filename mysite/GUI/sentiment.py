from keras.models import model_from_json
import pickle
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
from pandas.plotting import parallel_coordinates
from matplotlib import pyplot as plt
import json
import os
from mysite.settings import BASE_DIR

class AiSentiment:
    def __init__(self):
        with open(os.path.join(BASE_DIR, 'static', 'model.json'), "r") as json_file:
            model_json = json_file.read()
        self.model = model_from_json(model_json)
        self.model.load_weights("model-weights.h5")
        # serialize weights to HDF5
        self.model.load_weights("model-weights.h5")

        # saving tokenizer
        with open('GUI/tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)

    def result(self, query):
        sentiment = ['Neutral', 'Negative', 'Positive']

        sequence = self.tokenizer.texts_to_sequences([query])
        test = pad_sequences(sequence, maxlen=200)
        return self.model.predict(test)

    def collectResults(self, results):
        sentiment = ['Neutral', 'Negative', 'Positive']
        sentiments = {'Neutral': 0, 'Negative': 0, 'Positive': 0}
        for i in results:
            sentiments[sentiment[np.round(self.result(i.text), decimals=0).argmax(axis=1)[0]]] += 1
        return sentiments

    def excactResults(self, results):
        i = i['text']
        sentiments = {'Neutral': 0, 'Negative': 0, 'Positive': 0}
        sentiment = ['Neutral', 'Negative', 'Positive']
        self.Neutral = []
        self.Negative = []
        self.Positive = []
        for i in results:
            res = self.result(i)
            val = sentiment[np.round(self.result(i), decimals=0).argmax(axis=1)[0]]
            if val == 'Neutral':
                self.Neutral.append(res)
            elif val == 'Negative':
                self.Negative.append(res)
            elif val == 'Positive':
                self.Positive.append(res)

        self.data = {'Neutral': self.Neutral, 'Negative': self.Negative, 'Positive': self.Positive}

    def save(self):
        with open("static/savedResults.pkl", "wb") as file:
            pickle.dump(self.data, file)

    def load(self):
        with open("static/savedResults.pkl", "rb") as file:
            self.data = pickle.load(file)

    def pie(self):
        Neutral = self.data['Neutral']
        Negative = self.data['Negative']
        Positive = self.data['Positive']
        y = np.array([len(Neutral), len(Negative), len(Positive)])
        labels = ['Neutral', 'Negative', 'Positive']
        plt.pie(y, labels=labels)
        plt.show()

    def Curve(self):
        for i in self.data['Neutral']:
            plt.plot(['Neutral','Negative','Positive'], i.T, '.r-', linewidth=0.01, markersize=0.05)
        for i in self.data['Negative']:
            plt.plot(['Neutral','Negative','Positive'], i.T, '.b-', linewidth=0.01, markersize=0.05)
        for i in self.data['Positive']:
            plt.plot(['Neutral','Negative','Positive'], i.T, '.g-', linewidth=0.01, markersize=0.05)
        plt.show()

    def getGraphs(self):
        train = pd.read_csv('static/test.csv')
        self.load()
        self.Curve()





if __name__ == '__main__':
    NN = AiSentiment()
    NN.getGraphs()
