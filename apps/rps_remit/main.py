# import base64
# from datetime import date, timedelta ,datetime
# import json
# from fastapi import APIRouter, FastAPI, HTTPException, Header, Request, Response,Depends,status 
# # from fastapi_sqlalchemy import db
# import iso3166
# from jose import JWTError
# from mysqlx import get_session
# from pydantic import BaseModel 
# from apps.rps_remit.schema import *
 
# # from pydantic import EmailStr
# from core.config import  settings#jwtSettings,
# from core.hashing import Hasher
# from core.security import create_access_token,Authorize
# from db.repository.role_permission import RoleService
# from db.session import get_db
# from requests import Session
# from other_apps.get_rates import get_rates  
# from db.models.user import Banners, ExchangeRate, Permissions, Rates, Users as User, all_permissons
# from schemas.users import IndividualBusiness, LoginResponse, UserBaseSchema, UserCreate, UserLoginRequest, UserResponse
# from apps.rps_remit.dashboard import router
# import jwt




# remit_app = FastAPI()

from fastapi import APIRouter, BackgroundTasks, UploadFile

from other_apps.fcm_send import NotificationService
from utils.send_mail import EmailService


app=APIRouter(include_in_schema=True,prefix="") #remit_app
# remitapp=FastAPI()
# remit_app=app
# app=remitapp
# ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRE_MINUTES
# REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN

from apps.rps_remit.remit_deposit_locations.main import app as depositlocations
app.include_router(depositlocations,prefix='')


from apps.rps_remit.remit_deposit_banks.main import app as bankdeposit
app.include_router(bankdeposit,prefix='')


from apps.rps_remit.remit_pickup_locations.main import app as pickuplocations
app.include_router(pickuplocations,prefix='')


from apps.rps_remit.kyc_state.main import app as kycstateapp
app.include_router(kycstateapp,prefix='')


@app.post('/notification',tags=["RPS REMTI NOTIFICATION"])
async def send_notification(title:str,msg:str,to:str,file:UploadFile=None):
    try:
        NotificationService.send_notification(title,msg,to)
        # data:dict=None,
        return {"status":"sucess"}
    except Exception as e:
        return e
        

@app.post("/send-email",tags=["RPS REMIT EMAIL SEND"])
async def send_email(title:str,msg:str,background_tasks: BackgroundTasks):
    EmailService.send_mail_from_background( background_tasks,email=['sudarshan@mailinator.com',],subject=title, body=msg)#["sudarshan@mailinator.com"],title,msg)
    return "sucess"

from apps.rps_remit.transaction.main import app as transactionapp
app.include_router(transactionapp,prefix='')



from apps.rps_remit.receiving_methods.main import app as recivingmethodapp
app.include_router(recivingmethodapp,prefix='')

from apps.rps_remit.recipient.main import app as recipientapp
app.include_router(recipientapp,prefix='')




from apps.rps_remit.user_profile.main import app as userProfile
app.include_router(userProfile,prefix='')


from apps.rps_remit.kyc.main import app as ekycapp
app.include_router(ekycapp,prefix='')



from apps.rps_remit.otp.main import app as otpmain
app.include_router(otpmain,prefix="") 

from apps.rps_remit.user.main import app as usermain
app.include_router(usermain,prefix="")


from apps.rps_remit.compliance_service import router as compliance
app.include_router(compliance,prefix='')




from apps.rps_remit.hero.main import app as heroapp
from apps.rps_remit.banners.main import app as banners
from apps.rps_remit.transactions_state.main import app as transactionstate

from apps.rps_remit.forex_exchange.main import app as forex
from apps.rps_remit.user.main import app as userapp
app.include_router(forex,prefix='')
app.include_router(banners,prefix='')
app.include_router(transactionstate,prefix='')
app.include_router(heroapp,prefix='')



# from apps.rps_remit.currency.main import app as currencyapp
# app.include_router(currencyapp,prefix='/currency')



# from apps.rps_remit.dashboard import router
# app.include_router(router,prefix='/dashboard')


# def create_otp(email,db):
#         otp=OTP(phoneOrEmail=email)
#         otp.setrand()
#         db.add(otp)
#         db.commit()
#         db.refresh(otp)
#         return otp

# from core.jwt_bearer import JWTBearer
# async def get_current_user( jwtb: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#     )
#     try:
#         payload = jwt.decode(
#             jwtb, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
#         ) 
 
        
#         id: str = payload.get("sub")
#         user = db.query(User).filter(User.id == id).first()
#         return user
 
#     except JWTError as e:
#         return credentials_exception

# @app.post('/create-permission')
# async def create_permission(name:str,db: Session = Depends(get_db)):

#     role=Permissions(name)
#     return RoleService.createPermission(role,db)
# # @app.post('/create-role')
# # async def create_role(name:str,permission:list[str]):
# #     print(name)
# #     print(permission)
# #     pass
#     # role=Role(name,permission)
#     # return RoleService.createRole(role)
# @app.get('/all-permissions')
# async def all():
    
#     return all_permissons()

# @app.get("/")
# async def index():
#    return {"message": "Hello World from remit app"}


# async def flag_emoji(name):
#     alpha = iso3166.countries.get(name).alpha2
#     box = lambda ch: chr( ord(ch) + 0x1f1a5 )
#     return box(alpha[0]) + box(alpha[1])

# from countryinfo import CountryInfo
# @app.get('/exchange-rates/',tags=['ExchangeRate'])
# async def get_exchanges_rates(db: Session = Depends(get_db)):

#     dbrates=db.query(ExchangeRate).filter(ExchangeRate.date==date.today()).order_by(ExchangeRate.id.desc()).first()
#     if dbrates:
#         dbrates.rates
#         flag=[]
#         # f = open("myfile.json", "w")
#         # f.write("[")
#         # f.close()

#         # for country_name in iso3166.countries_by_name:
           
#         #     # if country_name != 'åland islands':
#         #         try:
#         #             countryi = CountryInfo(country_name)
#         #             # print(country_name)
                    
             
                
#         #             flag=flag_emoji(country_name)
#         #             currency=str(countryi.currencies())
#         #             result=createNewCurrency(currency=CountryCurrencyCreate(name=country_name,currency=currency,flag=flag))

#         #             print(result)
#         #         except:
#         #             ''
#         #         else:
#                     # ''
#         f = open("myfile.json", "a")
#         f.write("]")
#         f.close()

#             # 
#                 # print(countryi.currencies())
#             # print(iso3166.countries.get(country).currencies())
#         # print(iso3166.countries)
#         # for rate in dbrates.rates:
#         #     print(rate.iso3)
            
#             # print(iso3166.countries_by_alpha3.get("NPR"))
#             # print(flag_emoji(("NP")))
#             # flag.append(await flag_emoji(rate.iso3))
#         # print(dbrates.rates)
#         return {
#             "flag":flag,
#             "rates":dbrates}
#     rates=  get_rates()
#     exchangeRate=ExchangeRate(published_on=datetime.datetime.strptime(rates['published_on'],'%Y-%m-%d %H:%M:%S'),modified_on=datetime.datetime.strptime(rates['modified_on'],'%Y-%m-%d %H:%M:%S'),date=datetime.datetime.strptime(rates['date'],'%Y-%m-%d'))
#     print(exchangeRate)
#     db.add(exchangeRate)
#     db.commit( )
#     db.refresh(exchangeRate)
#     print(rates['rates'])
#     allrates=[]
#     for data in rates['rates']:
 
#         rate=Rates(iso3=data['currency']['iso3'],name=data['currency']['name'],unit=data['currency']['unit'],buy=data ['buy'],sell=data ['sell'],rate=exchangeRate.id)
#         allrates.append(rate)

#     # print(exchangeRate)
#     db.bulk_save_objects(allrates)
#     db.commit()
#     return rates

# @app.post('/register',response_model=UserResponse,tags=['RPS REMIT:Register'])
# async def register(payload:UserCreate,db: Session = Depends(get_db)):
#     # Check if user already exist
#     user = db.query(User).filter(
#         User.email == str(payload.email.lower())).first()
#     if user:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT,
#                             detail='Account already exist')
#    # Compare password and passwordConfirm
#    #  if payload.password != payload.passwordConfirm:
#    #      raise HTTPException(
#    #          status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
#    #  Hash the password
#     hashed_password = Hasher.get_password_hash(payload.password)
#    #  del payload.passwordConfirm
#    #  payload.role = 'user'
#    #  payload.verified = True
#     payload.email = str(payload.email.lower())
#     payload_dict=payload.dict()
#     del payload_dict['password']
#     new_user = User(hashed_password=hashed_password,**payload_dict)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @app.post('verify-email')
# async def verify_email(otp,phone):
#     pass


# class BannerResponse(BaseModel):
#     url:str=None
#     get_image:str=None
#     class Config:
#         orm_mode=True
# @app.get('/banners',tags=['Banners'],response_model=list[BannerResponse])
# async def banners( db: Session = Depends(get_db),):
#     return db.query(Banners).all() 
# @app.post('/login',tags=['Login'],response_model=LoginResponse)
# async def login(payload: UserLoginRequest,response: Response, db: Session = Depends(get_db),):
#                 #Authorize: AuthJWT = Depends()):
#     # Check if the user exist
#     user = db.query(User).filter(
#         User.email == (payload.email.lower())).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail='Incorrect Email or Password')

#     # Check if user verified his email
#     if not user.verified:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail='Please verify your email address')

#     # Check if the password is valid
#     if not Hasher.verify_password(payload.password, user.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail='Incorrect Email or Password')

#     # Create access token
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#             data={"sub": str(user.id)}, expires_delta=access_token_expires
#         )
#    #  access_token = 
#    #  Authorize.create_access_token(
#    #      subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

#     # Create refresh token
#     refresh_token = Authorize.create_refresh_token(
#         data={'id':str(user.id)}, expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_IN))

#     # Store refresh and access tokens in cookie
#    #  response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
#    #                      ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
#    #  response.set_cookie('refresh_token', refresh_token,
#    #                      REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
#    #  response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
#    #                      ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

#     # Send both access
#     return {'status': 'success', 'data':{'access_token': access_token,'refresh_token':refresh_token,
#         "user":    user}
#         # 'email_verified':user.verified,
#         # 'phone_verified':user.phone_verified,
#         # 'password_expired':False,
#         # 'ekyc_verified':False,
#         # 'ekyc_status':False
#             }
# # import jwt
# # # Refresh access token
# @app.get('/refresh',tags=['Refresh Token'])
# async def refresh_token(refresh_token: str = Header(...), db: Session = Depends(get_db)):#,Authorize: AuthJWT = Depends()
#     try:
#         key=base64.b64decode(
#         settings.JWT_PUBLIC_KEY).decode('utf-8')
#         decoded=jwt.decode(refresh_token, settings.SECRET_KEY , algorithms=[settings.ALGORITHM])#"RS256"])#(refresh_token)
#         print(decoded)
#         start=datetime.datetime.fromtimestamp(decoded['exp'])
#         stop = datetime.datetime.now()

#         elapsed =start-stop 
#         print(elapsed)
#         print(elapsed.total_seconds() )
#         if elapsed.total_seconds()>0:
#          user_id = decoded['id']
#          if not user_id:
#                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                  detail='Could not refresh access token')
#          user = db.query(User).filter(User.id == user_id).first()
#          if not user:
#                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                  detail='The user belonging to this token no logger exist')
 
#          access_token = create_access_token(
#                 data={"sub": str(user.id)}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
#         else:
#             raise HTTPException(status_code=401,detail='Token invalid/expired.')
#     except Exception as e:
        
#         print(e)
#         error = e.__class__.__name__
#         if error == 'MissingTokenError':
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
#         raise HTTPException(status_code=401,detail='Token invalid/expired.')
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail=error)

#    #  response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
#    #                      ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
#    #  response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
#    #                      ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
#     return {'access_token': access_token}

# # @app.get('/logout', status_code=status.HTTP_200_OK,tags=['Logout'])
# # def logout(response: Response, user_id: str = Depends(oauth2.require_user)):#Authorize: AuthJWT = Depends(), 
# #    #  Authorize.unset_jwt_cookies()
# #    #  response.set_cookie('logged_in', '', -1)

# #     return {'status': 'success'}
# @app.post('/register',tags=['RPS REMIT:Register'],)#response_model=RemitUserRead)#
# async def register(payload:RemitUserCreate,db: Session = Depends(get_session)):
#     # Check if user already exist
#     try:
#         user = db.query(RemitUser).filter(
#             RemitUser.email == str(payload.email.lower()),
#             # RemitUserBase.verified==False
#             ).first()

#     except Exception as e:
#         return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=e)
#     if user:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT,
#                                 detail='Account already exist')

#     else:
#     # Compare password and passwordConfirm
#     #  if payload.password != payload.passwordConfirm:
#     #      raise HTTPException(
#     #          status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
#     #  Hash the password
#         hashed_password = Hasher.get_password_hash(payload.password)
#     #  del payload.passwordConfirm
#     #  payload.role = 'user'
#     #  payload.verified = True
#         payload.email = str(payload.email.lower())
#         payload_dict=payload.dict()
#         del payload_dict['password']
#         new_user = RemitUser(hashed_password=hashed_password,**payload_dict)
#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)
        
#         return {"otp":"2023"}#new_user



# @app.post('/login',tags=['Login'],response_model=LoginResponse)
# async def login(payload: UserLoginRequest, db: Session = Depends(get_session),):
#                 #Authorize: AuthJWT = Depends()):
#     # Check if the user exist
#     user = db.query(RemitUser).filter(
#         RemitUser.email == (payload.email.lower())).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail='Incorrect Email or Password')

#     # Check if user verified his email
#     if not user.verified:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail='Please verify your email address')

#     # Check if the password is valid
#     if not Hasher.verify_password(payload.password, user.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail='Incorrect Email or Password')

#     # Create access token
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#             data={"sub": str(user.id)}, expires_delta=access_token_expires
#         )
#    #  access_token = 
#    #  Authorize.create_access_token(
#    #      subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

#     # Create refresh token
#     refresh_token = Authorize.create_refresh_token(
#         data={'id':str(user.id)}, expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_IN))

#     # Store refresh and access tokens in cookie
#    #  response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
#    #                      ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
#    #  response.set_cookie('refresh_token', refresh_token,
#    #                      REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
#    #  response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
#    #                      ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

#     # Send both access
#     return {'status': 'success', 'data':{'access_token': access_token,'refresh_token':refresh_token,
#         "user":    user}
#         # 'email_verified':user.verified,
#         # 'phone_verified':user.phone_verified,
#         # 'password_expired':False,
#         # 'ekyc_verified':False,
#         # 'ekyc_status':False
#             }
    

# @app.post('/forgot-password')
# async def forgot_password():
#     pass
# @app.post('/reset-password')
# async def reset_password(email:str):
#     pass

# @app.post('/verify-otp',tags=['VerifyOtp'])
# def verify_otp(otp,email):
#     pass

# @app.post('/tpin-setup')
# async def setupTransactionPin(otp,user:User=Depends(get_current_user)):
#     pass


# app.post('/change-password')
# async def change_password(newpassword:str):
#     pass

# @app.post('/mobile-setup',tags=['REMIT MOBILE SETUP'])
# async def phone_setup(mobile:str):
#     pass
# @app.post('/verify-mobile',tags=['REMIT MOBILE VERIFY'])
# def verify_mobile(otp,mobile):
#     pass
# @app.post('/signup-individual-business',tags=['SignupIndividualBusiness'])
# def signup_individual(signupIndividualBusiness:IndividualBusiness):
#     pass
# @app.post('/documents')
# async def user_documents():
#     pass
# @app.get('/home-api',tags=['HomePage'],response_model=UserBaseSchema)
# async def home_data(user:User=Depends(get_current_user)):#current_user:AttendanceUser=Depends(get_current_user_from_bearer),):
#    return user

# @app.post('/add-recipients')
# async def add_recipients(recipient):
#     pass

# @app.get('/cash-deposit-locations')
# async def cash_deposit_location():
#     pass

# @app.get('/cash-pickup-locations')
# async def cash_deposit_location():
#     pass

# @app.post('/bank-deposit')
# async def bank_deposit():
#     pass

# @app.post('/recipients')
# async def all_recipients():
#     pass
# @app.get('/transactions',tags=['Transactions History'])
# async def all_transactions():
#     pass

# @app.post('/transactions-submit',tags=['Send Money'])
# async def cash_deposit_location():
#     pass 


# def createNewCurrency(currency:CountryCurrencyCreate,db:Session=Depends(get_session)):
#     print(currency.dict())
#     f = open("myfile.json", "a")
    
#     f.write(json.dumps(currency.dict())+"\n,")
#     f.close()
#     # CountryCurrency.create(currency,CountryCurrencyBase, db)
# @app.get('/',response_model=list[CountryRead])
# async def all(db:Session=Depends(get_session)):
#     # f=open('myfile.json')
#     # data=json.load(f)
#     # for d in data:
#     #     CountryCurrency.create(CountryCurrencyCreate(name=d['name'],currency=d['currency'],flag=d['flag']),CountryCurrencyBase,db)
#     return CountryCurrency.all(session=db)

# @app.post('/')
# async def create(currency:CountryCurrencyCreate,db:Session=Depends(get_session)):
#     return CountryCurrency.create(currency,CountryCurrencyBase, db)

# @app.get('/{id}',response_model=CountryCurrencyRead)
# async def get_currency(id:int,db:Session=Depends(get_session)):
#     return CountryCurrency.by_id(id,session=db)


# @app.patch('/{id}',response_model=CountryCurrencyRead)
# async def update(id:int,hero:CountryCurrencyUpdate,db:Session=Depends(get_session)):
#     return CountryCurrency.update(CountryCurrency.by_id(id,session=db),hero,db)
 
# @app.delete('/')
# async def delete(id:int,db:Session=Depends(get_session)):
#     return CountryCurrency.delete(CountryCurrency.by_id(id,session=db))