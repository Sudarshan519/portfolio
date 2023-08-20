 
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException,status
from sqlmodel import Session
from apps.rps_remit.otp.main import OTPService
from apps.rps_remit.recipient.schema import RecipientRead, RecipientResponse
from apps.rps_remit.transaction.schema import TransactionRead
# from apps.rps_remit.otp.schema import OTP
 
from apps.rps_remit.user.schema import *
from apps.rps_remit.user.user_from_token import get_remit_user_from_bearer
from core.hashing import Hasher
from core.config import settings
from core.security import Authorize, create_access_token

from db.session_sqlmodel import get_session
from schemas.base import GenericResponse, PageResponse, create_data_model
from schemas.users import LoginResponse, UserBaseSchema, UserLoginRequest
 
from apps.rps_remit.kyc.schema import Kyc
app=APIRouter(prefix="/user",tags=[]) 
@app.post('/register',tags=['RPS REMIT:REGISTER'],response_model=LoginResponse )#response_model=RemitUserRead)#
async def register(payload:RemitUserCreate,db: Session = Depends(get_session)):
    # Check if user already exist
    try:
        user = db.query(RemitUser).filter(
            RemitUser.email == str(payload.email.lower()),
            # RemitUserBase.verified==False
            ).first() 
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=e)
    if user:
 
        if user.verified:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail='Account already exist')

    else:
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
        user = RemitUser(hashed_password=hashed_password,**payload_dict)
        db.add(user)
        db.commit()
        db.refresh(user)
        print(user)
        otp=OTPService.create_otp(phoneOrEmail=payload.email,db=db)
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
            data={'id':str(user.id)}, expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_IN))

    # Store refresh and access tokens in cookie
   #  response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
   #                      ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
   #  response.set_cookie('refresh_token', refresh_token,
   #                      REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
   #  response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
   #                      ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    # Send both access
    print(user)
    return {'status': 'success', 'data':{'access_token': access_token,'refresh_token':refresh_token,
            "user":    user}
            # 'email_verified':user.verified,
            # 'phone_verified':user.phone_verified,
            # 'password_expired':False,
            # 'ekyc_verified':False,
            # 'ekyc_status':False
                }
        # return {"otp":otp}#new_user


class ResponseSchema(BaseModel):
    status:str="success"
    data:Any


@app.get('/user',tags=['Home'],response_model=UserBaseSchema)
async def get_user(current_user:RemitUser=Depends(get_remit_user_from_bearer), db: Session = Depends(get_session),):
    # RemitUserResponse=create_data_model(RemitUser)
    # BaseResponse=create_data_model(PageResponse[RemitUserResponse ])
    #   
    kyc=Kyc.filter_by(db,{"id":current_user.id})
    # print((kyc))
    # profile:List[UserProfile]=[]
    # # recipients:List[Recipient]=[]
    # transactions:List[TransactionRead]=[]
    # quick_send: List[RecipientResponse]=None
    return  current_user #GenericResponse(data=current_user)

@app.post('/login',tags=['Login'],response_model=LoginResponse )
async def login(payload: UserLoginRequest, db: Session = Depends(get_session),):
                #Authorize: AuthJWT = Depends()):
    # Check if the user exist
    user = db.query(RemitUser).filter(
        RemitUser.email == (payload.email.lower())).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
  
    # Check if user verified his email
    # if not user.verified:
    #     otp=OTPService.create_otp(phoneOrEmail=payload.email,db=db)
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail={"otp":otp,"error":'Please verify your email address'})

    # Check if the password is valid
    if not Hasher.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect Email or Password')
    # Set Fcm token 
    if user.fcm_token!=payload.fcm_token:
        user.fcm_token=payload.fcm_token
        db.commit()

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
        data={'id':str(user.id)}, expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_IN))

    # Store refresh and access tokens in cookie
   #  response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
   #                      ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
   #  response.set_cookie('refresh_token', refresh_token,
   #                      REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
   #  response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
   #                      ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    # Send both access
    # print(user.kyc)
    return {'status': 'success', 'data':{'access_token': access_token,'refresh_token':refresh_token,
        "user":    user}
        # 'email_verified':user.verified,
        # 'phone_verified':user.phone_verified,
        # 'password_expired':False,
        # 'ekyc_verified':False,
        # 'ekyc_status':False
            }


@app.get('/transactions',response_model=List[TransactionRead],tags=["Transactions"])
async def get_users_transactions(db:Session=Depends(get_session),current_user:RemitUser=Depends(get_remit_user_from_bearer),limit:int=10,offset:int=0):
  return db.query(Transaction).where(Transaction.sender_id==current_user.id).order_by(Transaction.id.desc()).offset(offset*limit).limit(limit).all()

@app.get('/recipients',response_model=List[RecipientResponse],tags=["Recipients"])
async def get_users_transactions(db:Session=Depends(get_session),current_user:RemitUser=Depends(get_remit_user_from_bearer),limit:int=10,offset:int=0):
  return db.query(Recipient).where(Recipient.user_id==current_user.id).order_by(Recipient.id.desc()).offset(offset*limit).limit(limit).all()