from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel,EmailStr

class UserBaseSchema(BaseModel):
    # name: str
    email: EmailStr
    # photo: str

    class Config:
        orm_mode = True
#properties required during user creation
class UserCreate(UserBaseSchema):
    # username: str
    # email : EmailStr
    password : str
    # is_employer:Optional[bool]
    # class Config():  #tells pydantic to convert even non dict obj to json
    #     orm_mode = True

class ShowUser(BaseModel):   #new
    username : str=None
    email : EmailStr='test@test.com'
    is_active : bool=False

    class Config():  #tells pydantic to convert even non dict obj to json
        orm_mode = True


class UserResponse(UserBaseSchema):
    pass
    id: int
    # created_at: datetime
    # updated_at: datetime


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
    class Config:
                schema_extra = {
            "example": {
            "FirstName": "E",
            "LastName": "string",
            "MiddleName": "string",
            "Nationality": "string",
            "ResidenceStatus": "Japanese",
            "ResidenctType": "Japanese",
            "Profession": "string",
            "Email": "string",
            "Mobile": "9876543211",
            "PostalCode": "string",
            "BuildingName": "string",
            "Dob": "2002-02-22",
            "IDType": "Residence Card",
            "IDNumber": "string1",
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
            "District": "string"
}
        }


class Receiver(BaseModel):
    CustomerId:str
    Name:str
    Gender:str
    Mobile:str
    Relationship:str
    Address:str
    PaymentMode:str
    BankBranchId:str
    AccountNumber:str
    OTPProcessId:str
    OTP:str


class GetServiceChargeByCollection(BaseModel):
    Country:str
    PaymentMode:str
    CollectionAmount:str
    PayoutAmount:str
    BankBranchId:str
    ISNewAccount:str


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
    Mobile:str
    CustomerId:str=None
    ReceiverId:str=None
    PinNo:str=None
    PaymentMode:str=None
    BankBranchId:str=None
    AccountNumber:str=None
    CustomerFullName:str=None
    CustomerDOB:str=None
    CustomerIdNumber:str=None

class SendTransasctionRequest(BaseModel):
    CustomerId:str
    SenderName:str
    SendGender:str
    SenderDoB:str
    SenderAddress:str

    #Optional
    SenderPhone:str=None
    SenderMobile:str 
    SenderCity:str 
    SenderDistrict:str 
    SenderState:str 
    SenderNationality:str 
    Employer:str 
    SenderIDType:str 
    SenderIDNumber:str
    SenderIDExpiryDate:str=None
    SenderIDIssuedPlace:str=None
    ReceiverId:str=None
    RecevierName:str
    ReceviverGender:str
    ReceiverAddress:str
    ReceiverMobile:str
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
    PartnerPinNo:str
    IncomeSource:str
    RemittanceReason:str

    Relationship:str
    CSPCode:str
    OTPProcessId:str
    OTP:str


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