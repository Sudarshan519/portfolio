 
from fastapi import APIRouter,  Depends    
from apps.rps_remit.compliance_schema import AcPayBankListRequest,  CancelTransactionRequest, CashPayoutLocationRequest, CreateCSPRequest, CreateCustomer, GetServiceCharge, Receiver, SearchCsp, SearchTransactionRequest, SendTransasctionRequest, StaticDataList
from schemas.users import UploadPaymentSlipRequest, ValidateTransactionRequest
from xml_request.request_method import RequestMethods


router=APIRouter(tags=['Compliance'])
@router.get('/static_data')

def static_datalist(type:StaticDataList):
    
    return RequestMethods.get_static_data(type.value)
 



@router.get('/acpayBankList')
def acPayBankList(acPayBankList:AcPayBankListRequest= Depends(),):
   return RequestMethods.acpay_bank_branchlist(acPayBankList)   

@router.post('/cancel-transasction')
def cancelTransaction(cancelRequest:CancelTransactionRequest):
    return RequestMethods.cancel_transaction(cancelRequest)   


@router.post('/upload-transasction-slip')
def upload_payment_slip(uploadPaymentSlipRequest:UploadPaymentSlipRequest):
    return RequestMethods.upload_payment_slip(uploadPaymentSlipRequest)   

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
@router.get('/get-customer-by-id')
def get_customer_by_id(id:int=8):
    return RequestMethods.get_customer_by_customer_id(id)

@router.get('/get-customer-by-mobile')
def get_customer_by_mobile(mobile:int=9823579775):
    return RequestMethods.get_cutomer_by_mobile(mobile)


@router.get('/get-customer-by-idno')
def get_customer_by_idno(id:int):
    try:
      return RequestMethods.get_customer_by_id_no(id)
    except Exception as e:
        return e


@router.get('/service_charge')
def service_charge(serviceCharge:GetServiceCharge= Depends()):
    return RequestMethods.get_service_charge(serviceCharge)

@router.post('/search-csp')
def searchCSP(cspsearchrequest:SearchCsp):
    return RequestMethods.search_csp(cspsearchrequest)


@router.post('/search-transactions')
def searchCSP(searchTransactions:SearchTransactionRequest):
    return RequestMethods.search_transaction(searchTransactions)
@router.post('/send-transactions')
def sendTransaction(sendTransaction:SendTransasctionRequest):
   return RequestMethods.send_transaction(sendTransaction)

@router.post('/verify-transaction')
def verify_transaction(verifyTransaction:ValidateTransactionRequest):
    return RequestMethods.verifyTransactions( verifyTransaction)

@router.get('/unverified-customer')
def unverified_customers():
    return RequestMethods.unverified_customer()

@router.post('/uploadcspDocument')
def uploadCSPDocument(document):
      return RequestMethods.uploadCSPDocument(document)

# @router.post('/upload-customer-document')
# def upload_customer_document():
#     return RequestMethods.search_transaction(searchTransactions)
