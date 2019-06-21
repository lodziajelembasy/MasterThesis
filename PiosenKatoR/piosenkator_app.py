import pandas as pd
from representation import Representation
from sklearn.metrics.pairwise import cosine_similarity
      
k=5 
R = Representation()
df_bigram, df2_bigram = R.bigram_count()

sim = cosine_similarity(df_bigram, df2_bigram)
df_sim = pd.DataFrame(sim, index=df_bigram.index, columns = df2_bigram.index)
best = df_sim[0].nlargest(k)

print(R.reading.iloc[0,-1])
print()
for each in best.index:
    print(R.df_songs.iloc[each,0])
