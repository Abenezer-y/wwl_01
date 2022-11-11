from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import pandas as pd
from dataclasses import dataclass, asdict

wwl_db = {'cluster': "WWL", 
'uri': 'https://data.mongodb-api.com/app/data-qvnrx/endpoint/data/v1' ,
'db': "wwl" ,
'key': "5d9sGO28viSiX1HnJlOLN6QMqPqxYz6NIKVUMvEU8wXvAS0CPHMMHs2jF0UHKSCF"}

app = FastAPI()

origins = ['*']


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@dataclass
class Activity:
    id: str
    status: str
    activity: str


def update_data(collection, condition, doc,  credential):
    headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*','api-key': credential['key']}
    updateOne_url = f"{credential['uri']}/action/updateOne"
    Payload = json.dumps({"collection": collection, "database": credential['db'], "dataSource": credential['cluster'], "filter": condition, "update":{"$set": doc}})
    response = requests.request("POST", updateOne_url, headers=headers, data=Payload)
    return response

def get_data(collection, credential):
    headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*','api-key': credential['key']}
    findAll_url =  f"{credential['uri']}/action/find"
    Payload = json.dumps({"collection": collection, "database":credential['db'], "dataSource": credential['cluster'], "filter": {}, "limit":5000})
    response = requests.request("POST", findAll_url, headers=headers, data=Payload)
    response_json = response.json()['documents']
    status = [_['status'] for _ in response_json]
    # df = pd.read_json(json.dumps(response_json))
    return status

def get__data(collection, credential):
    headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*','api-key': credential['key']}
    findAll_url =  f"{credential['uri']}/action/find"
    Payload = json.dumps({"collection": collection, "database":credential['db'], "dataSource": credential['cluster'], "filter": {}, "limit":5000})
    response = requests.request("POST", findAll_url, headers=headers, data=Payload)
    response_json = response.json()['documents']
    # status = [_['status'] for _ in response_json]
    df = pd.read_json(json.dumps(response_json))
    return df



@app.get("/", tags=["root"])
async def read_root() -> dict:
    data = 'hello'
    return data

@app.get("/status", tags=["root"])
async def read_root() -> dict:
    data = get_data(collection='status', credential=wwl_db)
    return data



@app.post("/saveStatus", tags=["root"])
async def add_staus(status: dict) -> dict:
    update_data('status', {'_id': int(status['_id'])}, {'status': status['status']}, wwl_db)
    print(status)
    return 'Updated'


@app.get("/allData", tags=["root"])
def get_all():
    df = get__data(collection='activity_01', credential=wwl_db)
    df.head(3)
    lt = ['1530', '1530-1630', '1630', '1630-1730', '1700', '1730', '2350/0050 (After close of final session)', '0015/0115 ', '(After last guest leave skate exchange)', '0130/0230']
    segemented_activity = []
    for t in lt:
        data = df[df['time']==t]
        act_lt = data['activity'].values.tolist()
        st_lt = data['status'].values.tolist()
        id_lt = data['_id'].values.tolist()
        temp_lt = []
        row_count = data.shape[0]
        for i in range(row_count):
            record = Activity(status=st_lt[i], id=str(id_lt[i]), activity=act_lt[i])
            temp_lt.append(asdict(record))
        segemented_activity.append(temp_lt)
    return segemented_activity