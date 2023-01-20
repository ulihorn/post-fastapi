from datetime import datetime
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from typing import Optional

class UserCreate(BaseModel):
	email: EmailStr
	password: str

class User(BaseModel):
	email: EmailStr
	id: int
	created_at: datetime
	class Config:
		orm_mode = True

class PostBase(BaseModel):
	title: str
	content: str
	published: bool = True

class PostCreate(PostBase):
	pass

class Post(PostBase):
	id: int
	user_id: int
	created_at: datetime
	owner: User
	class Config:
		orm_mode = True

class PostOut(BaseModel):
	Post: Post
	votes: int

	class Config:
		orm_mode = True

class UserLogin(BaseModel):
	email: EmailStr
	password: str

class Token(BaseModel):
	access_token: str
	token_type: str

class TokenData(BaseModel):
	id: Optional[str] = None

class Vote(BaseModel):
	post_id: int
	dir: int #conint(le=1) 