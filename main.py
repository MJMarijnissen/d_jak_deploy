from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def hello_world():
	return {"message": "Hello World during the coronavirus pandemic!"}

@app.get('/hello/{name}')
def hello_name(name: str):
	return {"message": f"Hello {name}"}

@app.get('/method')
def method_return():
	return {"method": "GET"}

@app.post('/method')
def method_return():
	return {"method": "POST"}

@app.put('/method')
def method_return():
	return {"method": "PUT"}

@app.delete('/method')
def method_return():
	return {"method": "DELETE"}

N = 0

class Patients(BaseModel):
    name: str
    surename: str

@app.post('/patient/')
def return_patient(patients: Patients):
	global N
	output_str = {"id": N, "patient" :  patients}
	N += 1
	return output_str