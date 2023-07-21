from urllib.request import HTTPBasicAuthHandler
from zeep import Client
from zeep.transports import Transport
url = "https://rps.digital-remittance.com/api/Send.svc"

username="testRps"
password="testRps"
type_data="IncomeSource"
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
 