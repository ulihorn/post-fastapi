#from random import randrange
#from typing import Optional
from typing import List, Optional
#from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
#from pydantic import BaseModel
#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(prefix='/posts', tags=['Posts'])

#@router.get('/', response_model=List[schemas.Post])
@router.get('/', response_model=List[schemas.PostOut])
#@router.get('/')
def test_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
	# print(f'limit: {limit}')
	#posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
	# posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
	posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
	#print(results)
	#return posts
	return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
	# print(current_user.email)
	# print(current_user.id)
	new_post = models.Post(user_id=current_user.id, **post.dict())
	db.add(new_post)
	db.commit()
	db.refresh(new_post)
	return new_post
	
@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
	#post = db.query(models.Post).filter(models.Post.id == id).first()
	post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
	# if post.user_id != current_user.id:
	# 	raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to perform requested action')
	return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
	post_query = db.query(models.Post).filter(models.Post.id == id)
	post = post_query.first()
	if post == None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
	if post.user_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to perform requested action')
	post_query.delete(synchronize_session=False)
	db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
	post_query = db.query(models.Post).filter(models.Post.id == id)
	first_post = post_query.first()
	if first_post == None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
	if first_post.user_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to perform requested action')
	post_query.update(post.dict(), synchronize_session=False)
	db.commit()
	return post_query.first()