from fastapi import FastAPI

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