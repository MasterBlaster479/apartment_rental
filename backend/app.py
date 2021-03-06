from fastapi import FastAPI, UploadFile, File, Form, Body, Header, Depends, APIRouter, __version__ as fapi_version
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse, Response
from typing import List, Optional
from pydantic import BaseModel
from datetime import date
import uvicorn
import logging
import sys
import os
import crud, db
# to initialize AuthJWT correctly, first must be set environment variable AUTHJWT_SECRET_KEY
os.environ["AUTHJWT_SECRET_KEY"] = 'secret_key'
os.environ["AUTHJWT_ACCESS_TOKEN_EXPIRES"] = '3600'
from fastapi_jwt_auth import AuthJWT

def get_authorization_user(Authorization: str = Header(default='')):
    auth_jwt_token = AuthJWT(Authorization)
    auth_jwt_token.jwt_required()
    jwt_ident = auth_jwt_token.get_jwt_identity()
    return User(**crud.get_user_by_login(jwt_ident))

handler = logging.StreamHandler(sys.stdout)
logger = logging.getLogger('fastapi')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.debug(f'FastAPI v{fapi_version}')
app = FastAPI()
app.debug = True

class User(BaseModel):
    login: str
    password: str
    first_name: str
    last_name: str
    email: str

class UserLogin(BaseModel):
    login: str
    password: str

@app.post('/login')
def login(user: UserLogin):
    login = crud.login(user)
    if not login:
        return Response(content='Invalid login/password', status_code=404)
    access_token = AuthJWT.create_access_token(identity=user.login)
    return access_token

@app.put('/register')
def register(user: User):
    registered_user = crud.register_user(user)
    access_token = AuthJWT.create_access_token(identity=registered_user.login)
    return access_token

@app.post('/import-calendar')
def import_calendar(file: UploadFile = File(...), current_user: User = Depends(get_authorization_user)):
    crud.process_calendar_file_data([(file.filename, file.file.read())])

@app.post('/import-calendars')
def import_calendar(files: List[UploadFile] = File(...), current_user: User = Depends(get_authorization_user)):
    crud.process_calendar_file_data([(file.filename, file.file.read()) for file in files])

@app.get('/export-calendar{apartment_id}')
def export_calendar(id: int, current_user: User = Depends(get_authorization_user)):
    file_name, data = crud.export_calendar_by_apartment_id(id)
    response = StreamingResponse(data, media_type='text-plain')
    setattr(response, 'filename', file_name)
    return response

@app.get('/calendars')
def get_calendar(date_from: Optional[date] = None, date_to: Optional[date] = None,
                 current_user: User = Depends(get_authorization_user)):
    return crud.get_calendar(date_from=date_from, date_to=date_to)

if __name__ == '__main__':
    db.register_models(app)
    uvicorn.run(app, port=8000, host='127.0.0.1')
