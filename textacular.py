"""
Oliver Baccay
textacular.py
An extensible framework for comparative text analysis.
"""

import plotly.graph_objects as go
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
import sankey as sk
import re
import math

class Textacular:
    def __init__(self, stopwords=None):
        """ Constructor to initialize state """

        # Where all the data extracted from the loaded documents is stored
        self.data = defaultdict(dict)

        if stopwords is not None:
            self.stopwords = set(self.load_stop_words(stopwords)) # around O(1) lookup bc of set()
        else:
            self.stopwords = set()

    @staticmethod
    def default_parser(text, stopwords):
        """ For processing plain text files (.txt)"""

        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text) # keep only alphabetical
        words = text.split()

        words = [w for w in words if w not in stopwords]

        wordcount = Counter(words)
        numwords = len(words)
        # print({'wordcount': dict(wordcount), 'numwords': numwords})
        return {'wordcount': dict(wordcount), 'numwords': numwords}

    def load_stop_words(self, stopfile):
        """ List of common or stop words that get filtered from each file automatically"""
        stopwords = []
        with open (stopfile, 'r') as txtfile:
            lines = txtfile.readlines()
            for line in lines:
                stopwords += line.split()
        return stopwords

    def load_text(self, filename, label=None, parser=None):
        """ Register a text file with the library. Optional "label" used in visualizations to identify the text. """
        if label is None:
            label = filename

        with open(filename, 'r') as f: #open file
            text = f.read()

        if parser is None:
            results = self.default_parser(text, stopwords=self.stopwords)
            word_freq = results['wordcount']
        else:
            word_freq = parser(text)

        self.data[label] = dict(word_freq)


    def wordcount_sankey(self, word_list=None, k=5):
        """ Sankey diagram that maps each file's text to words. word_list to specify a particular set of words,
        or the words can be the union of the k most common words across each text file. """
        link, node = sk._prep_sankey_data(self.data, word_list, k)

        num_txts = len(self.data)
        labels = node['label']

        node_col = (["lightblue"] * num_txts) + (["lightgreen"] * (len(labels) - num_txts))
        node['color'] = node_col

        fig = go.Figure(go.Sankey(link=link, node=node))
        fig.update_layout(font=dict(size=15)) #make font smaller
        fig.show()


    def top_words_hist_subplot(self, word_list=None, k=5):
        """ Subplots of histograms, one subplot for each text file. Shows the top words in each document. """
        docs = list(self.data.keys())
        counts = list(self.data.values())
        num_docs = len(docs)

        cols = math.ceil(math.sqrt(num_docs)) + 1 # sometimes there will be more than 8 docs
        rows = math.ceil(num_docs/cols)

        fig, axes = plt.subplots(rows, cols, figsize=(cols*5, rows*5))
        axes = axes.flatten()

        for i, (label, wordc) in enumerate(zip(docs, counts)):
            wordc = Counter(wordc) #most common words

            if word_list is None:
                top = wordc.most_common(k)

                words = [w for w, f in top] #seperate words and their freqs
                freqs = [f for w, f in top]

            else:
                words = word_list
                freqs = [wordc.get(w, 0) for w in words] #0 if the word isnt in txt

            ax = axes[i]
            ax.bar(words, freqs, color="lightgreen")
            ax.set_title(label, fontsize=16)
            ax.set_ylabel("Frequency", fontsize=15)
            ax.tick_params(axis='x', rotation=45, labelsize=14)
            ax.tick_params(axis='y', labelsize=12)

        for ax in axes[num_docs:]: #selects unused plots to be hidden
            ax.set_visible(False)

        plt.tight_layout()
        #plt.savefig('topwords_sub.png', dpi=300)
        plt.show()

    def calc_tfidf(self):
        """ Calculate TF-IDF score for words in the docs. """
        N = len(self.data)
        tfidf_data = defaultdict(dict)

        docs_containing = Counter() # count amount of docs that contain each word
        for doc_words in self.data.values():
            for word in doc_words.keys():
                docs_containing[word] += 1

        for label, word_counts in self.data.items():
            total_words = sum(word_counts.values())
            tfidf_doc = {}
            for word, count in word_counts.items():
                tf = count/total_words #formula for tf
                idf = math.log(N/(1 + docs_containing[word])) #formula for idf
                tfidf_doc[word] = tf * idf
            tfidf_data[label] = tfidf_doc

        self.data_tfidf = tfidf_data

    def tfidf_lineplot(self, k=5, title=None):
        """ Plot highest k TF-IDF words in each doc. """
        plt.figure(figsize=(12, 6))

        for label, tfidf_scores in self.data_tfidf.items():
            top = Counter(tfidf_scores).most_common(k)
            words = [w for w, s in top] # seperate word and their scores
            scores = [s for w, s in top]
            plt.plot(words, scores, marker='o', label=label)

        plt.xlabel('Words')
        plt.ylabel('TF-IDF Score')
        plt.xticks(rotation=-90)
        plt.title(title if title is not None else 'TF-IDF Scores Across Documents')
        plt.legend(prop={'size': 10})
        plt.tight_layout()
        #plt.savefig('lineplot.png', dpi=300)
        plt.show()
