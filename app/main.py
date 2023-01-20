#from random import randrange
#from typing import Optional
#from typing import List
#from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
#from fastapi import FastAPI, Response, status, HTTPException, Depends
#from pydantic import BaseModel
#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time
#from sqlalchemy.orm import Session
#from . import models, schemas, utils
#from .database import engine, get_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
print(settings.database_hostname)
print(settings.database_port)
print(settings.database_password)
print(settings.database_name)
print(settings.database_username)
print(settings.secret_key)
print(settings.algorithm)
print(settings.access_token_expire_minutes)

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#origins = ['https://www.google.com']
origins = ['*']

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*'],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def root():
	return {'message': 'Hello World'}