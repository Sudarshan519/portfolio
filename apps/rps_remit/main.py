import base64
from datetime import timedelta
import datetime
from typing import Annotated
from fastapi import FastAPI, HTTPException, Header, Request, Response
from fastapi_sqlalchemy import db
from jose import JWTError
from pydantic import BaseModel
# from pydantic import EmailStr
from core.config import  settings#jwtSettings,
from core.hashing import Hasher
from core.security import create_access_token,Authorize
from db.session import get_db
from requests import Session
from other_apps.get_rates import get_rates
# from fastapi_jwt_auth import AuthJWT
from fastapi import Depends,status
from core import oauth2

from db.models.user import Banners, Users as User
from schemas.users import UserBaseSchema, UserCreate, UserResponse
from apps.rps_remit.dashboard import router


from fastapi.staticfiles import StaticFiles
remit_app = FastAPI()
import jwt
app=remit_app

ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN
app.include_router(router,prefix='/dashboard')

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




@remit_app.get("/")
def index():
   return {"message": "Hello World from remit app"}
@app.get('/exchange-rates/',tags=['ExchangeRate'])
async def get_exchanges_rates():
    rates=  get_rates()
    return rates

@app.post('/register',response_model=UserResponse,tags=['Register'])
async def register(payload:UserCreate,db: Session = Depends(get_db)):
    # Check if user already exist
    user = db.query(User).filter(
        User.email == str(payload.email.lower())).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')
   # Compare password and passwordConfirm
   #  if payload.password != payload.passwordConfirm:
   #      raise HTTPException(
   #          status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
   #  Hash the password
    hashed_password = Hasher.get_password_hash(payload.password)
   #  del payload.passwordConfirm
   #  payload.role = 'user'
   #  payload.verified = True
    payload.email = str(payload.email.lower())
    payload_dict=payload.dict()
    del payload_dict['password']
    new_user = User(hashed_password=hashed_password,**payload_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
class BannerResponse(BaseModel):
    url:str=None
    image_url:str=None
    class Config:
        orm_mode=True
@app.get('/banners',tags=['Banners'],response_model=list[BannerResponse])
async def banners( db: Session = Depends(get_db),):
    return db.query(Banners).all() 
@app.post('/login',tags=['Login'])
async def login(payload: UserCreate,response: Response, db: Session = Depends(get_db),):
                #Authorize: AuthJWT = Depends()):
    # Check if the user exist
    user = db.query(User).filter(
        User.email == (payload.email.lower())).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    # Check if user verified his email
    if not user.verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Please verify your email address')

    # Check if the password is valid
    if not Hasher.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
   #  access_token = 
   #  Authorize.create_access_token(
   #      subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    # Create refresh token
    refresh_token = Authorize.create_refresh_token(
        data={'id':str(user.id)}, expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    # Store refresh and access tokens in cookie
   #  response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
   #                      ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
   #  response.set_cookie('refresh_token', refresh_token,
   #                      REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
   #  response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
   #                      ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    # Send both access
    return {'status': 'success', 'access_token': access_token,'refresh_token':refresh_token
            }
# import jwt
# # Refresh access token
@app.get('/refresh',tags=['Refresh Token'])
def refresh_token(refresh_token: str = Header(...), db: Session = Depends(get_db)):#,Authorize: AuthJWT = Depends()
    try:
        key=base64.b64decode(
        settings.JWT_PUBLIC_KEY).decode('utf-8')
        decoded=jwt.decode(refresh_token, key , algorithms=["RS256"])#(refresh_token)
        print(decoded)
        start=datetime.datetime.fromtimestamp(decoded['exp'])
        stop = datetime.datetime.now()

        elapsed =start-stop 
        print(elapsed.total_seconds() )
        if elapsed.total_seconds()>0:
         user_id = decoded['sub']
         if not user_id:
               raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail='Could not refresh access token')
         user = db.query(User).filter(User.id == user_id).first()
         if not user:
               raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail='The user belonging to this token no logger exist')
         access_token = create_access_token(
               subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
        else:
            raise HTTPException(status_code=401,detail='Token invalid/expired.')
    except Exception as e:
        
        print(e)
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(status_code=401,detail='Token invalid/expired.')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

   #  response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
   #                      ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
   #  response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
   #                      ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
    return {'access_token': access_token}

# @app.get('/logout', status_code=status.HTTP_200_OK,tags=['Logout'])
# def logout(response: Response, user_id: str = Depends(oauth2.require_user)):#Authorize: AuthJWT = Depends(), 
#    #  Authorize.unset_jwt_cookies()
#    #  response.set_cookie('logged_in', '', -1)

#     return {'status': 'success'}


@app.post('/verify-otp',tags=['VerifyOtp'])
def verify_otp(otp,email):
    pass
@app.post('/verify-otp',tags=['VerifyOtp'])
def signup_individual(otp,email):
    pass
@app.post('/documents')
async def user_documents():
    pass
@app.get('/home-api',tags=['HomePage'],response_model=UserBaseSchema)
async def home_data(user:User=Depends(get_current_user)):#current_user:AttendanceUser=Depends(get_current_user_from_bearer),):
   return user

@app.post('/add-benificary')
async def benificary():
    pass

@app.post('/cash-deposit-locations')
async def cash_deposit_location():
    pass

@app.post('/cash-pickup-locations')
async def cash_deposit_location():
    pass

@app.post('/bank-deposit')
async def bank_deposit():
    pass

@app.post('/recipients')
async def all_recipients():
    pass
@app.get('/transactions')
async def all_transactions():
    pass

@app.post('/transactions-submit')
async def cash_deposit_location():
    pass 