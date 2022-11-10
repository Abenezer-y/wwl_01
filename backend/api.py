from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import json

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
    return status

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