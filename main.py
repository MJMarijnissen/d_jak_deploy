import secrets
import hashlib

from fastapi import Depends, FastAPI, Cookie, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse

from pydantic import BaseModel

app = FastAPI()
app.users = {"trudnY": "PaC13Nt"}
app.sessions = {}

security = HTTPBasic()
KEY = "Silly key is silly, but not as silly as no key"

def create_token(username: str, password: str):
	token = hashlib.sha256(bytes(f"{username}{password}{KEY}", "utf-8"))
	token = token.hexdigest()
	return token


def authenticate(username: str, password: str):
	if username not in app.users or password != app.users[username]:
		raise HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user or password")
	token = create_token(username, password)
	app.sessions[token] = username
	return token

def check_token(ses_token: str=Cookie(None)):
	if ses_token not in app.sessions:
		raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "login required")
	return True

@app.get('/')
def hello_world():
	return {"message": "Hello World during the coronavirus pandemic!"}

@app.get('/welcome')
def hello_welcome(ses_token: str = Depends(check_token)):
	if ses_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "Unauthorized"
	return {"message": "Hello again, how do you do?"}

@app.post('/login')
def get_current_username(credentials: HTTPBasicCredentials = Depends(security), ):
	ses_token = authenticate(credentials.username, credentials.password)
	response = RedirectResponse(url='/welcome', status_code=status.HTTP_302_FOUND)
	response.set_cookie(key="ses_token", value=ses_token)
	return response

@app.post('/logout', dependencies=[Depends(check_token)])
def logout_user(ses_token: str = Cookie(None)):
	del app.sessions[ses_token]
	response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
	return response


N = 0
patients_list = []

class Patients(BaseModel):
	name: str
	surename: str

@app.post('/patient/')
def post_patient(patients: Patients,ses_token: str = Depends(check_token)):
	if ses_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "Unauthorized"
	global N
	global patients_list
	output_str = {"id": N, "patient" :  patients}
	patients_list.append(patients)
	N += 1
	return output_str

@app.get('/patient/{pk}')
def return_patient(pk: int, ses_token: str = Depends(check_token)):
	if ses_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "Unauthorized"
	global patients_list
	if pk > len(patients_list) -1:
		raise HTTPException(status_code = 204)
		return None
	return patients_list[pk]
