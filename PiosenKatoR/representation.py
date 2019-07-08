import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from reading import Reading

class Representation(object):
        
    R = Reading()
    reading_cleaned = R.cleaned_and_tokenized()
    reading = R.get_readable()
    
    def __init__(self):
        self.df_songs = pd.read_csv('../CSV/prep_songs_pl_lem_stop_wcrft2.csv', header=0, index_col=None)
        
    def bigram_count(self):
        bigram_vect = CountVectorizer(ngram_range=(2,2), binary=False)
        bigram_sparse = bigram_vect.fit_transform(self.df_songs.iloc[:,-1])
        df_bigram = pd.DataFrame(bigram_sparse.toarray())
        df_bigram.columns = bigram_vect.get_feature_names()
        
        bigram_sparse2 = bigram_vect.transform(self.reading_cleaned)
        df2_bigram = pd.DataFrame(bigram_sparse2.toarray())
        df2_bigram.columns = bigram_vect.get_feature_names()
        return df_bigram, df2_bigram