from ast import List
from typing import Any
from fastapi import APIRouter, Body,Depends, File, Form, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from apps.rps_remit.fireabse_bucket import upload_file
from apps.rps_remit.gs_cloud_storage import upload_to_gcs

from db.models.user import Banners, Users
from db.session import get_db
from other_apps.upload_file import firebase_upload
from schemas.users import AcPayBankListRequest, CancelTransactionRequest, CashPayoutLocationRequest, CreateCSPRequest, CreateCustomer, Receiver, SearchCsp, SearchTransactionRequest, StaticDataList
from xml_request.rps_creation_requests.request_method import RequestMethods


router=APIRouter(tags=['Dashboard'])
class DataModel(BaseModel):
    Value:str
    Label:str
class ResponseModel(BaseModel):
    Code:str=None
    Message:str=None
    DataList:list[DataModel]=[]
   

@router.get('/acpayBankList')
def acPayBankList(acPayBankList:AcPayBankListRequest= Depends()):
   return RequestMethods.acpay_bank_branchlist(acPayBankList)   
@router.post('/cancel-transasction')
def cancelTransaction(cancelRequest:CancelTransactionRequest):
    return RequestMethods.cancel_transaction(cancelRequest)   

@router.get('/cash-payout-location-list')
def cashPayoutLocationList(cashPayoutLocationRequest:CashPayoutLocationRequest= Depends()):
   return RequestMethods.cash_payout_locationlist(cashPayoutLocationRequest)   

@router.get('/compliance-transactions')
def complianceTransactions( ):
   return RequestMethods.compliance_transactions( )   

@router.post('/create-csp')
def createCsp(cspRequest:CreateCSPRequest):
    return RequestMethods.create_csp(cspRequest)

@router.get('/static_data')
def static_datalist(type:StaticDataList):
   return RequestMethods.get_static_data(type.value)


@router.get('/get-state-district')
def state_district(country:str):
   return RequestMethods.get_state_district(country)

@router.post('/create-customer')
def create_customer(customer:CreateCustomer):
    return RequestMethods.create_customers(customer)

@router.post('/create-receiver')
def create_receiver(customer:Receiver):
    return RequestMethods.create_receivier(customer)

@router.get('/get-customer-by-mobile')
def get_customer_by_mobile(mobile:int=9823579775):
    return RequestMethods.get_cutomer_by_mobile(mobile)


@router.get('/get-customer-by-idno')
def get_customer_by_mobile(id:int):
    try:
      return RequestMethods.get_customer_by_id(id)
    except Exception as e:
        return e


@router.get('/service_charge')
def service_charge():
    return RequestMethods.get_service_charge()

@router.post('/search-csp')
async def searchCSP(cspsearchrequest:SearchCsp):
    return RequestMethods.search_csp(cspsearchrequest)


@router.post('/search-transactions')
async def searchCSP(searchTransactions:SearchTransactionRequest):
    return RequestMethods.search_transaction(searchTransactions)

# @router.post('/uploadcspDocument')
# async def uploadCSPDocument(document:Any):
#       return RequestMethods.uploadCSPDocument(document)

# @router.post('/upload-customer-document')
# async def upload_customer_document():
#     return RequestMethods.search_transaction(searchTransactions)

@router.get("/")
def index():
   return {"message": "Hello World from remit dashboard app"}
class UserSchema(BaseModel):
   id:int
   email:str
   verified:bool
   is_active:bool

   class Config:
      orm_mode=True

@router.post('/login')
async def login(username:str,password:str):
   pass
@router.get('/users',response_model=list[UserSchema])
def all_users(db:Session=Depends(get_db)):
   return db.query(Users).filter(Users.is_superuser==False).all()
class BannerSchema(BaseModel):
   url:str
   image:str 
   class Config:
      orm_mode=True

@router.post("/banners")
async def add_banner(url:str=Body( ),image:UploadFile =File(...),db:Session=Depends(get_db)):
   file_content=await image.read()
   filename=image.filename
   upload_to_gcs(filename,file_content ,image.content_type)
   if image:
      
      with open("images/"+filename, 'wb') as f:
            while contents := image.file.read(1024 * 1024):
                    f.write(contents)
      image_url='/images/'+filename
      # await upload_file(image)
      # print(image.filename)
      # ext= image.filename.split(".")[-1]
      # image_url=firebase_upload(image.file.read(),ext,image.filename)
      # print(image_url)
   banner=Banners(url=url,image=image_url)
   db.add(banner)
   db.commit()
   db.refresh(banner)
   return banner
