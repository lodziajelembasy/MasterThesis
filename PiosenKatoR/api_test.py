import json
import urllib
import glob
import os
import time
import requests

user="211497@student.pwr.edu.pl"
task="any2txt|wcrft2"
#"any2txt|wcrft2|wsd"

url="http://ws.clarin-pl.eu/nlprest2/base"
#url+'http://ws.clarin-pl.eu/nlprest2/base/download/requests/makezip/6b8c8427-83e4-42ed-ac06-a2d523b1faa5

def upload(file):
        with open (file, "rb") as myfile:
            doc=myfile.read()
        return requests.post(url=url+'/upload', data=doc, headers={'Content-Type': 'binary/octet-stream'}).text
        #urllib2.urlopen(urllib2.Request(url+'/upload/',doc,{'Content-Type': 'binary/octet-stream'})).read();

def process(data):
        doc=json.dumps(data)
        taskid = requests.post(url+'/startTask/', data=doc, headers={'Content-Type': 'application/json'}).text#urllib2.urlopen(urllib2.Request(url+'/startTask/',doc,{'Content-Type': 'application/json'})).read();
        time.sleep(0.2);
        resp = requests.get(url+'/getStatus/'+taskid).text#urllib2.urlopen(urllib2.Request(url+'/getStatus/'+taskid));
        #print(resp)
        data=json.loads(resp)
        #print(data, 'data')
        while data["status"] == "QUEUE" or data["status"] == "PROCESSING" :
            time.sleep(0.5);
            resp = requests.get(url+'/getStatus/'+taskid).text#urllib2.urlopen(urllib2.Request(url+'/getStatus/'+taskid));
            #print(resp)
            data=json.loads(resp)
        if data["status"]=="ERROR":
            print("Error "+data["value"]);
            return None;
        return data["value"]


def main():
    in_file = 'PiosenKator\czytania_do_lem\\czytanie.zip'
    #'czytania.zip'
    out_file= 'Piosenkator\czytania_z_lem\out.zip'
    global_time = time.time()
    fileid=upload(in_file)
    lpmn='filezip('+fileid+')|'+task+'|dir|makezip'
    data={'lpmn':lpmn,'user':user}
    data=process(data)
    #print(data)
    if data!=None:
        data=data[0]["fileID"];
        #print(data)
        content = requests.get(url=url+'/download'+data).content#urllib2.urlopen(urllib2.Request(url+'/download'+data)).read();
        #print(content)
        with open (out_file, "wb") as outfile:
            outfile.write(content)
    #print("GLOBAL %s seconds ---" % (time.time() - global_time))

#main();
