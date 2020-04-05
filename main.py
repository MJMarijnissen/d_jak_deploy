from fastapi import FastAPI, HTTPException
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
patients_list = []

class Patients(BaseModel):
    name: str
    surename: str

@app.post('/patient/')
def post_patient(patients: Patients):
	global N
	global patients_list
	output_str = {"id": N, "patient" :  patients}
	patients_list.append(patients)
	N += 1
	return output_str

@app.get('/patient/{pk}')
def return_patient(pk: int):
	global patients_list
	if pk > len(patients_list) -1:
		raise HTTPException(status_code = 204)
		return None
	return patients_list[pk]
