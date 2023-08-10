
from enum import Enum
from pydantic import BaseModel
from datetime import date

class StaticDataList(str,Enum):
    Gender= 'Gender'
    NATIONALITY= "Nationality"
    IDTYPE="IDType"
    INCOMESOURCE="IncomeSource"
    RELATIONSHIP="Relationship"
    PAYMENTMODE="PaymentMode"
    REMITANCEREASON= "RemittanceReason"
    RESIDENCETYPE="Residence Type"

class CreateCSPRequest(BaseModel):
    csp_code:str
    entityType:str
    name:str
    state:str
    district:str
    city:str
    address:str
    pincode:str
    phone:str
    email:str
    isownbranch:bool

    # optional
    gstin:str=None
    device:str=None
    connectivity:str=None
    start_time:str=None
    end_time:str=None
    offDay:str=None
    accBankName:str=None
    acType:str=None
    acifsCode:str=None
    acNumber:str=None

class CreateCustomer(BaseModel):
    FirstName:str
    LastName:str
    MiddleName:str=None
    Nationality:str
    ResidenceStatus:str
    ResidenctType:str
    Profession:str
    Email:str
    Mobile:str
    PostalCode:str
    BuildingName:str
    Dob:str
    IDType:str
    IDNumber:str
    IDExpiryDate:str=None
    IDIssuedPlace:str
    IntendUseOfAccount:str
    PassportNumber:str=None
    Prefecture:str=None
    Street:str=None
    Phone:str=None
    Country:str
    Gender:str=None
    Address:str=None
    City:str=None
    Employer:str=None
    IncomeSource:str=None
    OTPProcessId:str=None
    OTP:str
    CitizenshipNo:str
    State:str
    District:str
    firebase_token:str
    class Config:
                schema_extra = {
            "example": {
            "FirstName": "E",
            "LastName": "string",
            "MiddleName": "string",
            "Nationality": "Nepal",
            "ResidenceStatus": "Japanese",
            "ResidenctType": "Japanese",
            "Profession": "string",
            "Email": "string",
            "Mobile": "0709876543212",
            "PostalCode": "0000000",
            "BuildingName": "string",
            "Dob": "2002-02-22",
            "IDType": "Residence Card",
            "IDNumber": "string1234",
            "IDExpiryDate": "2022-02-22",
            "IDIssuedPlace": "string",
            "IntendUseOfAccount": "string",
            "PassportNumber": "string",
            "Prefecture": "string",
            "Street": "string",
            "Phone": "010809876543210",
            "Country": "string",
            "Gender": "Female",
            "Address": "string",
            "City": "string",
            "Employer": "string",
            "IncomeSource": "string",
            "OTPProcessId": "string",
            "OTP": "string",
            "CitizenshipNo": "string",
            "State": "string",
            "District": "string",
            "firebase_token":"string"
}
        }


class Receiver(BaseModel):
    CustomerId:int
    Name:str
    Gender:str="Male"
    Mobile:str="9863432121"
    Relationship:str
    Address:str
    PaymentMode:str="Cash Payment"
    BankBranchId:int
    AccountNumber:str
    OTPProcessId:int
    OTP:int


class GetServiceChargeByCollection(BaseModel):
    Country:str
    PaymentMode:str
    CollectionAmount:str
    PayoutAmount:str
    BankBranchId:str
    ISNewAccount:str

class GetServiceCharge(BaseModel):
    Country:str
    CollectionAmount: str=None
    CollectionCurrency : str=None
    ServiceCharge: str=None
    TransferAmount    : str=None
    ExchangeRate  : str=None
    PayoutAmount  : str=None
    PayoutCurrency    : str=None
    PaymentMode:str=None
class SearchCsp(BaseModel):
    CSPCode:str
    CMobile:str
    PanNo:str=None


# numbers = {k:v for k, v in enumerate(range(0, 11))}

class SearchTransactionRequest(BaseModel):
    PinNo:str
    PartnerPinNo:str
    FromDate:date
    ToDate:str

class SendOtpRequest(BaseModel):
    Operation:str
    Mobile:str="9876543212"
    CustomerId:str=None
    ReceiverId:str=None
    PinNo:str=None
    PaymentMode:str=None
    BankBranchId:int
    AccountNumber:str=None
    CustomerFullName:str=None
    CustomerDOB:str=None
    CustomerIdNumber:str=None

class SendTransasctionRequest(BaseModel):
    CustomerId:int
    SenderName:str
    SenderGender:str='Male'
    SenderDoB:date
    SenderAddress:str

    #Optional
    SenderPhone:str=None
    SenderMobile:str="0709876543211" 
    SenderCity:str 
    SenderDistrict:str 
    SenderState:str 
    SenderNationality:str 
    Employer:str 
    SenderIDType:str 
    SenderIDNumber:int
    SenderIDExpiryDate:str=None
    SenderIDIssuedPlace:str=None
    ReceiverId:int
    ReceiverName:str
    ReceiverGender:str="Male"
    ReceiverAddress:str
    ReceiverMobile:int="9823579775"
    ReceiverCity:str
    SendCountry:str
    PayoutCountry:str
    PayoutMode:str
    CollectedAmount:str
    ServiceCharge:str
    SendAmount:str
    SendCurrency:str
    PayAmount:str
    PayCurrency:str
    ExchangeRate:str
    BankBranchId:str=None
    AccountNumber:str=None
    AccountType:str=None
    NewAccountRequest:str=None
    PartnerPinNo:int
    IncomeSource:str
    RemittanceReason:str

    Relationship:str
    CSPCode:int
    OTPProcessId:int
    OTP:int
    # PaymentMode:str="Cash Payment"
    class Config:
        schema_extra={
            "example":{
                    "CustomerId": 0,
                    "SenderName": "string",
                    "SenderGender": "Male",
                    "SenderDoB": "2023-08-08",
                    "SenderAddress": "string",
                    "SenderPhone": "9876543212",
                    "SenderMobile": "0809876543211",
                    "SenderCity": "string",
                    "SenderDistrict": "string",
                    "SenderState": "string",
                    "SenderNationality": "string",
                    "Employer": "string",
                    "SenderIDType": "string",
                    "SenderIDNumber": 0,
                    "SenderIDExpiryDate": "string",
                    "SenderIDIssuedPlace": "string",
                    "ReceiverId": 0,
                    "ReceiverName": "string",
                    "ReceiverGender": "Male",
                    "ReceiverAddress": "string",
                    "ReceiverMobile": "9823579775",
                    "ReceiverCity": "string",
                    "SendCountry": "string",
                    "PayoutCountry": "string",
                    "PayoutMode": "Cash",
                    "CollectedAmount": "string",
                    "ServiceCharge": "string",
                    "SendAmount": "string",
                    "SendCurrency": "string",
                    "PayAmount": "string",
                    "PayCurrency": "string",
                    "ExchangeRate": "string",
                    "BankBranchId": "string",
                    "AccountNumber": "string",
                    "AccountType": "string",
                    "NewAccountRequest": "string",
                    "PartnerPinNo": 0,
                    "IncomeSource": "string",
                    "RemittanceReason": "string",
                    "Relationship": "string",
                    "CSPCode": 0,
                    "OTPProcessId": 0,
                    "OTP": 0,
                   
}
        }


class ValidateBankAccountRequest(BaseModel):
    BankCode:str
    AccountNumber:str

class ValidateTransactionRequest(BaseModel):
    PinNo:str


class AcPayBankListRequest(BaseModel):
    Country:str=None
    State:str=None
    District:str=None
    City:str=None
    BankName:str=None
    BranchName:str=None
 
class CancelTransactionRequest(BaseModel):
    pinNo:str=None
    reason:str=None
    opt_process_id:str=None
    otp:str=None


class CashPayoutLocationRequest(BaseModel):
     Country:str=None
     State:str=None
     District:str=None
     City:str=None