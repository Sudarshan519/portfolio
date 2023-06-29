#core > security.py

from datetime import datetime,timedelta
from typing import Optional
from jose import JWTError, jwt

from core.config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"]=  (expire)
    print(to_encode)
    # encoded_jwt="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjk4NjM0NTAxMDcsImV4cCI6MTY4ODE1MTM4Nn0.EEAyQ4v1set4wx_9u6z_VkKVI5DezIzz_n1LMcIrqOA"
    token = jwt.encode(to_encode,  settings.SECRET_KEY, algorithm='HS256')
    # encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    # print(str(encoded_jwt))
    decoded=jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
    print(decoded)
    return token