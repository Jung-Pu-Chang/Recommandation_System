import configparser
from fastapi import FastAPI
from service.module import Model 
#from module import Model 
from pydantic import BaseModel
import uvicorn
config = configparser.ConfigParser()
config.read('./config/config.ini')
model_path = config['recommand']['model_path']
node_path = config['recommand']['data_path']+'node_df.csv'
edge_path = config['recommand']['data_path']+'edge_df.csv'

#config.read('config.ini')
#model_path = 'edge_model'
#node_path = 'node_df.csv'
#edge_path = 'edge_df.csv'
batch_size = int(config['recommand']['batch_size'])
num_samples = list(config['recommand']['num_samples'])
num_samples = [int(x) for x in num_samples]

app = FastAPI() # initiate API
model = Model(model_path, node_path, edge_path, batch_size, num_samples) 

class ModelParams(BaseModel):
    item: str

@app.post("/submit")
def submit(params: ModelParams): 
    pred_df = model.recommand(params.item)
    return pred_df

if __name__ == "__main__": 
     uvicorn.run("module_api:app", host="0.0.0.0") 
     # http://192.168.1.69:8000/submit