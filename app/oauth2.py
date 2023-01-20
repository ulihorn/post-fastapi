from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
# Algorithm
# Expiration Time

#SECRET_KEY = "a8dd98796d213969a21edeef146026c6f0d1863fd50085f2efa45083ae774e6d"
SECRET_KEY = settings.secret_key
#ALGORITHM = 'HS256'
ALGORITHM = settings.algorithm
#ACCESS_TOKEN_EXPIRE_MINUTES = 90
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
	to_encode = data.copy()

	expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({'exp': expire})

	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

	return encoded_jwt

def verify_access_token(token: str, credentials_exception):
	# print("got to verify access token")
	try:
		# print("got to try")
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		# print(f'payload: {payload}')

		id: str = payload.get('user_id')
		# print(f'id: {id}')

		if id is None:
			raise credentials_exception
		token_data = schemas.TokenData(id=id)
	except JWTError:
		# print("got to exception")
		raise credentials_exception
	# except JWTError as e:
	# 	print(e)
	# 	raise credentials_exception
	# except AssertionError as e:
	# 	print(e)
	# print(f'token data: {token_data}')
	return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
	#print("got to get current user")
	#print(f'token: {token}')
	credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})

	token = verify_access_token(token, credentials_exception)
	user = db.query(models.User).filter(models.User.id == token.id).first()
	# print(user)
	return user
