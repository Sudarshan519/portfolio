
from zeep import Client
from zeep.transports import Transport
from zeep.plugins import HistoryPlugin
from zeep.helpers import serialize_object
from zeep import Client
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.xsd import Element
from lxml import etree
from zeep.transports import Transport
username="testRps"
password="testRps"
type_data="IncomeSource"
session = Session()
transport = Transport(session=session)
session.headers=HTTPBasicAuth(username,password)
# Replace "your_soap_service_url" with the actual URL of the SOAP service
soap_service_url ="https://rps.digital-remittance.com/api/Send.svc?wsdl"
client=Client(soap_service_url,transport=transport)
 
payload=f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
 
    <Body>
        <GetStaticData xmlns="http://tempuri.org/">
            <!-- Optional -->
            <GetStaticDataRequest>
                <UserName xmlns="http://schemas.datacontract.org/2004/07/Remit.API">{username}</UserName>
                <Password xmlns="http://schemas.datacontract.org/2004/07/Remit.API">{password}</Password>
                <Type xmlns="http://schemas.datacontract.org/2004/07/Remit.API">{type_data}</Type>
            </GetStaticDataRequest>
        </GetStaticData>
    </Body>
</Envelope>"""
# headers
headers = { 
 
"Accept-Encoding": "gzip,deflate",
"Content-Type": "text/xml;charset=UTF-8",
"SOAPAction": "http://tempuri.org/ISend/GetStaticData",
"Connection": "Keep-Alive",
"User-Agent":"Apache-HttpClient/4.5.5 (Java/16.0.1)"


}
response = client.transport.post_xml(
    address=soap_service_url,
    envelope=payload,
    headers=headers
)
 
# Print the XML content
print("SOAP Response:",response.content)