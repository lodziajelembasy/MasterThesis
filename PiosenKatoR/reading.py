import warnings
warnings.filterwarnings("ignore")
import datetime
from download_readings import download_readings
from clean_text import clean_text
import zipfile
import xml.etree.ElementTree as ET
from gensim.utils import tokenize
import codecs
import pandas as pd
import api_test 

class Reading(object):

    today = datetime.date.today()
    
    def __init__(self):
        self.prepare_for_lem()
        self.run_api()
        self.extract()
    
    def run_api(self):
        api_test.main()
        
    def get_cleaned_readings(self,n):
        df_raw = download_readings(n)
        df = df_raw.copy()
        for each in df_raw.columns:
            df[each] = df[each].apply(lambda x: clean_text(x))
        return df
    
    def get_readable(self):
        df = self.get_cleaned_readings(1)
        df['Tekst'] = df['Pierwsze czytanie'][0] + ' ' + df['Psalm_ref'][0] + ' ' + df['Psalm'][0] + ' ' + df['Werset przed Ewangelią'][0] + ' ' + df['Ewangelia'][0]
        return df
        
    def prepare_for_lem(self):
        df = self.get_readable()       
        df[['Tekst']].to_csv('czytania_do_lem\\'+str(self.today)+'.txt', 
                             header=False, 
                             index=False)
        zf = zipfile.ZipFile('czytania_do_lem\\czytanie.zip', mode='w')
        zf.write('czytania_do_lem\\' + str(self.today) + '.txt')
        zf.close()

    def extract(self):
        with zipfile.ZipFile('czytania_z_lem\out.zip', 'r') as zipObj:
            zipObj.extractall('czytania_z_lem')

    def get_txt(self):
        root = ET.parse('czytania_z_lem\czytania_do_lem%'
                        +str(self.today)+'.txt').getroot()
        r = root.findall('chunk/sentence/tok/lex/base')
        txt = ' '.join([child.text for child in r])
        return txt
    
    def cleaned_and_tokenized(self):
        x = self.get_txt()
        r = list(tokenize(x, to_lower=True))
        polish_stops = codecs.open("../polishStopWords",'r','utf-8')
        stopwords = polish_stops.read().split('\n')
        polish_stops.close()
        no_stops = [t for t in r if t not in stopwords]
        return pd.Series(str([no_stops]))