from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import dataclass, asdict
from .functions import wwl_db, get__data, update_data, get_data, file_edittor, send_email

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

@app.get("/status", tags=["root"])
async def read_status() -> dict:
    data = get_data(collection='status', credential=wwl_db)
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

@app.get("/submit")
async def send_mail():
    print('here')
    file_edittor()
    print('here')
    send_email(filename = "duty.xlsx")
    return 'Email Sent'





    