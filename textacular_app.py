"""
Oliver Baccay
textacular_app.py
Run textacular.py framework on 8 Insurance Court Cases
"""

from textacular import Textacular

def main():
    tt = Textacular(stopwords='data/my_stopwords.txt')

    #Load my 8 Insurance Coverage Litigation Court Cases
    tt.load_text("data/progressive_appeal.txt", label="Progressive")
    tt.load_text("data/maryland_ins_admin_appeal.txt", label="Maryland Insurance")
    tt.load_text("data/travelers_ins_appeal.txt", label="Travelers")
    tt.load_text("data/amfam_ins_appeal.txt", label="American Family")
    tt.load_text("data/liberty_mutual_appeal.txt", label="Liberty Mutual")
    tt.load_text("data/geico_appeal.txt", label="Geico")
    tt.load_text("data/state_farm_appeal.txt", label="State Farm")
    tt.load_text("data/farmers_ins_appeal.txt", label="Farmers Insurance")

    # Sankey Diagram
    tt.wordcount_sankey(k=10)

    # Histogram Subplots
    tt.top_words_hist_subplot(k=5)

    # TF-IDF Diagram
    tt.calc_tfidf()
    tt.tfidf_lineplot(k=5, title='Term Importance Scores Across Insurance Coverage Cases')

if __name__ == "__main__":
    main()