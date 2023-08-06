from ast import List
import enum
from typing import Any, Type
from fastapi import APIRouter, Body,Depends, File, Form, Query, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from apps.rps_remit.fireabse_bucket import upload_file
from apps.rps_remit.gs_cloud_storage import upload_to_gcs

from db.models.user import Banners, Users, all_permissons
from db.session import get_db
from other_apps.upload_file import firebase_upload
from schemas.users import AcPayBankListRequest,  CancelTransactionRequest, CashPayoutLocationRequest, CreateCSPRequest, CreateCustomer, ForeignExchangeCharge, KycTypeBase, Receiver, SearchCsp, SearchTransactionRequest, SendTransasctionRequest, StaticDataList
from xml_request.rps_creation_requests.request_method import RequestMethods


router=APIRouter(tags=['Complaince'])

@router.get('/static_data')
def static_datalist(type:StaticDataList):
   return RequestMethods.get_static_data(type.value)



@router.get('/acpayBankList')
def acPayBankList(acPayBankList:AcPayBankListRequest= Depends(),):
   return RequestMethods.acpay_bank_branchlist(acPayBankList)   
@router.post('/cancel-transasction')
def cancelTransaction(cancelRequest:CancelTransactionRequest):
    return RequestMethods.cancel_transaction(cancelRequest)   

@router.get('/cash-payout-location-list',)
def cashPayoutLocationList(cashPayoutLocationRequest:CashPayoutLocationRequest= Depends(),):
   return RequestMethods.cash_payout_locationlist(cashPayoutLocationRequest)   

@router.get('/compliance-transactions',)
def complianceTransactions( ):
   return RequestMethods.compliance_transactions( )   

@router.post('/create-csp')
def createCsp(cspRequest:CreateCSPRequest):
    return RequestMethods.create_csp(cspRequest)

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
@router.post('/send-transactions')
async def sendTransaction(sendTransaction:SendTransasctionRequest):
   return RequestMethods.send_transaction(sendTransaction)

@router.get('/unverified-customer')
async def unverified_customers():
    return RequestMethods.unverified_customer()
# @router.post('/uploadcspDocument')
# async def uploadCSPDocument(document:Any):
#       return RequestMethods.uploadCSPDocument(document)

# @router.post('/upload-customer-document')
# async def upload_customer_document():
#     return RequestMethods.search_transaction(searchTransactions)
