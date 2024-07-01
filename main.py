from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import joblib
import json
import uvicorn

from fastapi.middleware.cors import CORSMiddleware

class model_input(BaseModel):
  step:int
  amount:float
  oldbalanceOrg:float
  newbalanceOrig:float
  oldbalanceDest:float
  newbalanceDest:float
  isFlaggedFraud:int
  type_1:int
  type_2:int
  type_3:int
  type_4:int
  type_5:int

app=FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("decision_tree_model.pkl")

@app.get("/")
def check():
    return "It's working"

@app.post('/prediction')
def fraud_predd(input_parameters : model_input):

    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)

    step = input_dictionary['step']
    Amount= input_dictionary['amount']
    sender_oldBalance = input_dictionary['oldbalanceOrg']
    sender_newbalance = input_dictionary['newbalanceOrig']
    receiver_oldbalance = input_dictionary['oldbalanceDest']
    receiver_newbalance = input_dictionary['newbalanceDest']
    dpf = input_dictionary['isFlaggedFraud']
    CASH_OUT = input_dictionary['type_1']
    PAYMENT=input_dictionary['type_2']
    CASH_IN=input_dictionary['type_3']
    TRANSFER= input_dictionary['type_4']
    DEBIT= input_dictionary['type_5']

    input_list = [step,Amount,sender_oldBalance,sender_newbalance,receiver_oldbalance,receiver_newbalance,dpf,CASH_OUT,PAYMENT,CASH_IN,TRANSFER, DEBIT]

    prediction = model.predict([input_list])

    if (prediction[0] == 0):
        return 'Payment is not Fraud'
    else:
        return 'Payment is Fraud'
    

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)