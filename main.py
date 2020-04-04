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

@app.post('/patient/{patients}')
def return_patient(patients: str):
	global N
	output_str = {"id": f'{N}', "patient" :  f'{patients}'}
	N += 1
	return output_str