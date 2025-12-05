"""
Oliver Baccay
sankey.py
Utility functions for generating Sankey diagram data from word-frequency dictionaries.
"""

import pandas as pd
from collections import Counter

def _words_for_sankey(data, word_list=None, k=5):
    """ Returns a set of words to put in Sankey diagram. """
    if word_list is not None:
        return set(word_list)

    tot_counts = Counter()

    for counts in data.values():
        tot_counts.update(counts) # combine word freq from all txts

    sankey_words = [word for word, _ in tot_counts.most_common(k)]
    return set(sankey_words)

def _build_sankey_df(data, word_list=None, k=5):
    """ Build a dataframe of source-target-value for Sankey. """
    sankey_words = _words_for_sankey(data, word_list, k)

    df = []
    for label, counts in data.items():
        for word in sankey_words:
            if word in counts: #checks if word exists in current txt
                df.append({'src': label, 'targ': word, 'val': counts[word]})

    return pd.DataFrame(df)

def _prep_sankey_data(data, word_list=None, k=5):
    """ Prepare data for Sankey by mapping text labels to most frequent words. """

    df = _build_sankey_df(data, word_list, k)
    labels = pd.concat([df['src'], df['targ']]).unique().tolist()

    label_as_int = {label: num for num, label in enumerate(labels)} # map to an int

    source = [label_as_int[label] for label in df['src']]
    target = [label_as_int[label] for label in df['targ']]
    value = df['val'].tolist()

    link = {'source': source, 'target': target, 'value': value}
    node = {'label': labels}

    return link, node