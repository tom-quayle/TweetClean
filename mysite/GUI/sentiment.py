from keras.models import model_from_json
import pickle
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
from pandas.plotting import parallel_coordinates
from matplotlib import pyplot as plt
import os

class AiSentiment:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = BASE_DIR + '/GUI/static/model.json'
        with open(filepath, "r") as handle:
            self.model = handle.read()
        self.model = model_from_json(self.model)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = BASE_DIR + '/GUI/static/best_model.hdf5'
        self.model.load_weights(filepath)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = BASE_DIR + '/GUI/static/Tokenizer.pickle'
        with open(filepath, "rb") as handle:
            self.tokenizer = pickle.load(handle)

    def result(self, query):

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
        sentiments = {'Neutral': 0, 'Negative': 0, 'Positive': 0}
        sentiments = ['Neutral', 'Negative', 'Positive']
        self.Neutral = []
        self.Negative = []
        self.Positive = []
        for i in results:
            i=i['text']
            sequence = self.tokenizer.texts_to_sequences([i])
            input = pad_sequences(sequence, maxlen=200)
            print(i)
            sentiment = self.model.predict(input)
            val = sentiments[np.around(sentiment, decimals=0).argmax(axis=1)[0]]
            if val == 'Neutral':
                self.Neutral.append(sentiment)
            elif val == 'Negative':
                self.Negative.append(sentiment)
            elif val == 'Positive':
                self.Positive.append(sentiment)

        self.data = {'Neutral': self.Neutral, 'Negative': self.Negative, 'Positive': self.Positive}

    def save(self):
        with open("savedResults.pkl", "wb") as file:
            pickle.dump(self.data, file)

    def load(self):
        with open("savedResults.pkl", "rb") as file:
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
        from matplotlib.lines import Line2D

        fig, ax = plt.subplots(dpi=100)
        ax.plot(['Neutral','Negative','Positive'], [0,0,0], '.r-', label="Neutral statement")
        ax.plot(['Neutral', 'Negative', 'Positive'], [0, 0, 0], '.b-', label="Negative statement")
        ax.plot(['Neutral', 'Negative', 'Positive'], [0, 0, 0], '.g-', label="Positive statement")
        for i in self.data['Neutral']:
            ax.plot(['Neutral','Negative','Positive'], i.T, '.r-', linewidth=0.01, markersize=0.05)
        for i in self.data['Negative']:
            ax.plot(['Neutral','Negative','Positive'], i.T, '.b-', linewidth=0.01, markersize=0.05)
        for i in self.data['Positive']:
            ax.plot(['Neutral','Negative','Positive'], i.T, '.g-', linewidth=0.01, markersize=0.05)

        plt.rcParams["font.size"] = 7
        plt.legend(loc='upper left')
        plt.ylim(0, 1.3)
        plt.tight_layout()
        plt.title("Confidence distribution")
        plt.ylabel("Confidence")
        plt.savefig("GUI/static/GUI/images/distChart.jpg")

    def getGraphs(self):
        train = pd.read_csv('test.csv')
        #self.load()
        self.Curve()





if __name__ == '__main__':
    NN = AiSentiment()
    NN.getGraphs()
