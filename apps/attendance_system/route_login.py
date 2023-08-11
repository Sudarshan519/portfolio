from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from fastapi import Depends, HTTPException, Response,status
 
from requests import Session    #new
from apps.utils import OAuth2PasswordBearerWithCookie
from core.config import settings
from db.models.user import Users
from db.session import get_db    #new
from db.models.attendance import AttendanceUser
oauth2_scheme = oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Get user from database
def get_user(username:str,db: Session):
    user = db.query(AttendanceUser).filter(AttendanceUser.phone == username).first()
    return user


from core.jwt_bearer import JWTBearer
def get_current_user_from_bearer( jwtb: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            jwtb, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        ) 
 
        
        username: str = payload.get("sub")

        return get_user(username=username, db=db)
 
    except JWTError as e:
        return credentials_exception



# Get uesr from token
def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    print(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        ) 
        
        username: str = payload.get("sub")
 
        if username is None:
            raise credentials_exception
    except jwt:
        raise credentials_exception
    user = get_user(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user

from core.jwt_bearer import JWTBearer
def get_current_user( jwtb: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            jwtb, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        ) 
 
        
        id: str = payload.get("sub")
        user = db.query(User).filter(User.id == id).first()
        return user
 
    except JWTError as e:
        return credentials_exception

