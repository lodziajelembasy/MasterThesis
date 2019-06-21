import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, manhattan_distances
#from sklearn.metrics import jaccard_score

#songs_representation = 'piosenki_avg_w2v_nkjp-lemmas-all-300-skipg-ns_pl_lem.csv'
#readings_representation = 'czytania_avg_w2v_nkjp-lemmas-all-300-skipg-ns_pl_lem.csv'

songs_repr_list = ['piosenki_bow_bin_pl_lem.csv',
                  'piosenki_bow_count_pl_lem.csv',
                   'piosenki_bigram_bin_pl_lem.csv',
                   'piosenki_bigram_count_pl_lem.csv',
                   'piosenki_trigram_bin_pl_lem.csv',
                   'piosenki_trigram_count_pl_lem.csv',
                   'piosenki_tfidf_default_lem_pl',
                   'piosenki_tfidf_min05_lem_pl',
                   'piosenki_doc2vec_default_lem_pl',
                   'piosenki_doc2vec_default_dm1_lem_pl',
                   'piosenki_avg_w2v_nkjp+wiki-lemmas-all-100-cbow-hs_pl_lem.csv',
                   'piosenki_avg_w2v_nkjp-lemmas-all-100-cbow-hs_pl_lem.csv',
                   'piosenki_avg_w2v_nkjp-lemmas-all-100-cbow-ns_pl_lem.csv',
                   'piosenki_avg_w2v_nkjp-lemmas-all-100-skipg-hs_pl_lem.csv',
                   'piosenki_avg_w2v_nkjp-lemmas-all-100-skipg-ns_pl_lem.csv',
                   'piosenki_avg_w2v_nkjp-lemmas-all-300-cbow-hs_pl_lem.csv',
                   'piosenki_avg_w2v_nkjp-lemmas-all-300-cbow-ns_pl_lem.csv',
                   'piosenki_avg_w2v_nkjp-lemmas-all-300-skipg-hs_pl_lem.csv'
                   
                  ]
readings_repr_list = ['czytania_bow_bin_pl_lem.csv',
                     'czytania_bow_count_pl_lem.csv',
                      'czytania_bigram_bin_pl_lem.csv',
                      'czytania_bigram_count_pl_lem.csv',
                      'czytania_trigram_bin_pl_lem.csv',
                      'czytania_trigram_count_pl_lem.csv',
                      'czytania_tfidf_default_lem_pl',
                      'czytania_tfidf_min05_lem_pl',
                      'czytania_doc2vec_default_lem_pl',
                       'czytania_doc2vec_default_dm1_lem_pl',
                      'czytania_avg_w2v_nkjp+wiki-lemmas-all-100-cbow-hs_pl_lem.csv',
                      'czytania_avg_w2v_nkjp-lemmas-all-100-cbow-hs_pl_lem.csv',
                      'czytania_avg_w2v_nkjp-lemmas-all-100-cbow-ns_pl_lem.csv',
                      'czytania_avg_w2v_nkjp-lemmas-all-100-skipg-hs_pl_lem.csv',
                      'czytania_avg_w2v_nkjp-lemmas-all-100-skipg-ns_pl_lem.csv',
                      'czytania_avg_w2v_nkjp-lemmas-all-300-cbow-hs_pl_lem.csv',
                      'czytania_avg_w2v_nkjp-lemmas-all-300-cbow-ns_pl_lem.csv',
                      'czytania_avg_w2v_nkjp-lemmas-all-300-skipg-hs_pl_lem.csv'
                     ]

def evaluate(songs_representation, readings_representation):
    piosenki = pd.read_csv(songs_representation, 
                           header=0, 
                           index_col=0)

    czytania = pd.read_csv(readings_representation, 
                           header=0, 
                           index_col=0)

    sim = cosine_similarity(piosenki, czytania)
    #sim = jaccard_score(piosenki, czytania, average=None)
    #sim = 1 - euclidean_distances(piosenki, czytania)
    #sim = 1 - manhattan_distances(piosenki, czytania)
    df_sim = pd.DataFrame(sim, 
                          index=piosenki.index, 
                          columns = czytania.index)

    test = pd.read_csv('ewaluacja.csv',
                       header=0, 
                       index_col=0)

    k=[]
    for date in czytania.index:
        k.append(test[date].sum())

    x = []
    for i, date in enumerate(czytania.index):
        model_recommendation = df_sim[date].nlargest(k[i])
        human_recommendation = test[date].nlargest(k[i])
        counter = 0
        for each in model_recommendation.index:
            if each in human_recommendation.index:
                counter += 1
        x.append(counter)
    return np.sum(x), np.round(np.sum(x) / len(czytania), 3), np.round(np.sum(x) / np.sum(k),3), (np.array(x)/np.array(k))
#     print(x)
#     print("Suma wszystkich dopasowanych poprawnie:", np.sum(x))
#     print("Średnia liczba poprawnych dopasowań na liczbę czytań", np.round(np.sum(x) / len(czytania), 3))
#     print("Średnia liczba poprawnych dopasowań na liczbę rekomendowanych piosenek", np.round(np.sum(x) / np.sum(k),3))
    
#evaluate(songs_representation, readings_representation)
#print(len(songs_repr_list), len(readings_repr_list))
def statistics():
    suma = []
    pc = []
    pr = []
    perd = []
    for i in range(len(songs_repr_list)):
        s, c, r, d  = evaluate(songs_repr_list[i], readings_repr_list[i])
        suma.append(s)
        pc.append(c)
        pr.append(r)
        perd.append(d)
    return suma, pc, pr, perd