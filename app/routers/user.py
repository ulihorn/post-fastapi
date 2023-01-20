#from random import randrange
#from typing import Optional
#from typing import List
#from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
#from pydantic import BaseModel
#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time
from sqlalchemy.orm import Session
from ..import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix='/users', tags=['Users'])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

	# hash the password - user.password
	hashed_password = utils.hash(user.password)
	user.password = hashed_password

	new_user = models.User(**user.dict())
	db.add(new_user)
	db.commit()
	db.refresh(new_user)

	return new_user
	
@router.get('/{id}', response_model=schemas.User)
def get_post(id: int, db: Session = Depends(get_db)):
	user = db.query(models.User).filter(models.User.id == id).first()
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id: {id} was not found')
	return user