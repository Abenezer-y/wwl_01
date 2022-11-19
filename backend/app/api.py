from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import dataclass, asdict
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import requests
import json
import pandas as pd

tdy = datetime.today()
date = f'Nov {tdy.day}, 2022'

wwl_db = {'cluster': "WWL", 
'uri': 'https://data.mongodb-api.com/app/data-qvnrx/endpoint/data/v1' ,
'db': "wwl" ,
'key': "5d9sGO28viSiX1HnJlOLN6QMqPqxYz6NIKVUMvEU8wXvAS0CPHMMHs2jF0UHKSCF"}


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
    # status = [_['status'] for _ in response_json]
    # df = pd.read_json(json.dumps(response_json))
    return response_json

def get__data(collection, credential):
    headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*','api-key': credential['key']}
    findAll_url =  f"{credential['uri']}/action/find"
    Payload = json.dumps({"collection": collection, "database":credential['db'], "dataSource": credential['cluster'], "filter": {}, "limit":5000})
    response = requests.request("POST", findAll_url, headers=headers, data=Payload)
    response_json = response.json()['documents']
    # status = [_['status'] for _ in response_json]
    df = pd.read_json(json.dumps(response_json))
    return df

def file_edittor():
    filename = "duty.xlsx"
    xl_df = pd.read_excel(filename)
    df = get__data(collection='activity_02', credential=wwl_db)
    status = df['status'].values.tolist()
    new_st = []
    for s in status:
        if s == True: 
            new_st.append('complete')
        else:
            new_st.append('Incomplete')
    df[f'Status_{date}'] = new_st
    xl_df[f'Status_{date}'] = new_st
    xl_df[['Time', 'Activity', f'Status_{date}']].to_excel(filename, index=False)

def send_email(filename=None):
    sender_email ='dohawwlreports@gmail.com'
    pw = 'iloudhwueynlnsqg'
    receiver_email = 'Daniel.Noake-Contractor@img.com'
    message = MIMEMultipart()
    message["Subject"] = f"Duty Manager Check list as of {date}"
    message["From"] = sender_email
    message["To"] = sender_email
    body = f"Submission of Duty Check list on {date}"
    message.attach(MIMEText(body, "plain"))

    if filename is not None:

        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header( "Content-Disposition", f"attachment; filename= {filename}",)
        message.attach(part)


    # Add attachment to message and convert message to string
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, pw)
            server.sendmail(sender_email, receiver_email, text)
    except:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, pw)
            server.sendmail(sender_email, receiver_email, text)

app = FastAPI()
origins = ["*"]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
    expose_headers = ['*']
)

@dataclass
class Activity:
    id: str
    status: str
    activity: str


df_db = get__data(collection='activity_02', credential=wwl_db)

@app.get("/", tags=["root"])
async def read_root() -> dict:
    data = 'hello'
    return data

@app.get("/allData", tags=["root"])
async def get_all():
    df = get__data(collection='activity_02', credential=wwl_db)
    print(df.head(3))
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

@app.get("/attendance", tags=["root"])
async def read_attendance() -> dict:
    data = get_data(collection='attendance', credential=wwl_db)
    return data

@app.post("/saveStatus", tags=["root"])
async def add_staus(status: dict) -> dict:
    update_data('status', {'_id': status['_id']}, {'status': status['status'], }, wwl_db)
    print(status)
    return 'Updated'

@app.post("/editStatus", tags=["root"])
async def edit_staus(status: dict) -> dict:
    print(status)
    data = df_db[df_db['_id']==status['_id']]
    print(data['activity'].values.tolist()[0])
    print(update_data('activity_02', {'activity': data['activity'].values.tolist()[0]}, {'status': status['status'], 'activity': data['activity'].values.tolist()[0], 'time':data['time'].values.tolist()[0]}, wwl_db))
    # print({'status': status['status'], 'activity': data['activity'][0], 'time':data['time'][0]})
    return 'Updated'

@app.get("/submit", tags=["root"])
async def send_mail():
    print('here')
    file_edittor()
    print('here')
    send_email(filename = "duty.xlsx")
    return 'Email Sent'





    