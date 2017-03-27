#typeform_api.py

import requests
import csv
import pandas as pd

def get_id(api_key):
    '''This function takes an argument- the api key, and return the typeform_uid 
    that will be used to access the document associated with that uid'''
    global u_id
    
    url1='https://api.typeform.com/v1/forms?&key='+api_key
    resp = requests.get(url1)
    if(resp.ok):
        for item in resp.json():
            print(resp.json())
            u_id = item['id']
    else:
        resp.raise_for_status()

def get_documents(uid, api_key):
    '''This function takes two arguments-uid and the api key, and produces a JSON document'''
    global respJSON
    url2='https://api.typeform.com/v1/form/'+uid+'?key='+api_key
    resp2 = requests.get(url2)
    if(resp2.ok):
        respJSON = resp2.json()
        return respJSON 
    else:
        resp2.raise_for_status()

#call both functions
key='ac83034cfa742c0f79c26e9a612b4ba7e2aa0d3d'
get_id(key)
get_documents(u_id,key)

#Get a header for csv
#I believe the useful header (column) will be the answers (response to the questions) 
#as well as the date submitted and network id

#Here we get the key of network_id and date_submit as strings
metadata_keys = list(respJSON['responses'][0]['metadata'].keys())

for i in metadata_keys:
    if i == 'network_id':
        header_1 = i
        
    if i == 'date_submit':
        header_2 = i
        
#Here, we get the id of each question and use it as a header
#I am only using the id to keep the header looking clean
#we will also use this variable later to make sure our responses matches the header
        
questions_id = []
for i in range(len(respJSON['questions'])):
    questions_id.append(respJSON['questions'][i]['id'])
        
#create the header
header = [str(header_1), str(header_2)]
for i in range(len(questions_id)):
    header.append(str(questions_id[i]))

#Get answers from responses matching the question id in the header
all_rows = [[] for _ in range(len(respJSON['responses']))]
for i in range(len(respJSON['responses'])):
    rows=[]
    
    try:
        rows.append(respJSON['responses'][i]['metadata']['network_id'])
    except:
        rows.append('NaN')
    try:
        rows.append(respJSON['responses'][i]['metadata']['date_submit'])
    except:
        rows.append('NaN')
    
    for j in range(len(questions_id)):
        try:
            rows.append(respJSON['responses'][i]['answers'][questions_id[j]].replace('\n', ' '))
        except:
            rows.append('NaN')
    
    all_rows[i].extend(rows)

#write to CSV
with open('documents.csv', 'w', newline='') as documents:
    csvwriter = csv.writer(documents)
    
    csvwriter.writerow(header)
    
    for row in all_rows:
        csvwriter.writerow(row) 
    
documents.close()
    
with open('documents.csv', 'r') as doc:
    for row in doc:
        print(row)

