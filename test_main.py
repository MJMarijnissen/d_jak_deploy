from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_hello_world():
	response = client.get('/')
	assert response.status_code == 200
	assert response.json() == {"message": "Hello World during the coronavirus pandemic!"}

@pytest.mark.parametrize("name", ["Ala", "Zażółź Gęślą jaźń"])
def test_hello_name(name):
	response = client.get(f'/hello/{name}')
	assert response.status_code == 200
	assert response.json() == {"message": f"Hello {name}"}

def test_method_return():
	response = client.get('/method')
	assert response.status_code == 200
	assert response.json() == {"method": "GET"}
	
	response = client.post('/method')
	assert response.status_code == 200
	assert response.json() == {"method": "POST"}
	
	response = client.put('/method')
	assert response.status_code == 200
	assert response.json() == {"method": "PUT"}

	response = client.delete('/method')
	assert response.status_code == 200
	assert response.json() == {"method": "DELETE"}

@pytest.mark.parametrize("patients", {"name": "IMIE", "surename": "NAZWISKO"})
def test_return_patient(patients):
	enter = client.post(f'/patient/{patients})
	assert enter.json() == {"patient": {"name": "IMIE", "surename": "NAZWISKO"}}}
	#assert enter.json() == {"id": N, "patient": {"name": "IMIE", "surename": "NAZWISKO"}}