from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi import Depends, HTTPException, Response,status
from jose import JWTError as jwt
from requests import Session    #new
from apps.utils import OAuth2PasswordBearerWithCookie
from core.config import settings
from db.session import get_db    #new
from db.models.attendance import AttendanceUser
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")

# Get user from database
def get_user(username:str,db: Session):
    user = db.query(AttendanceUser).filter(AttendanceUser.phone == username).first()
    return user



# Get uesr from token
def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
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
