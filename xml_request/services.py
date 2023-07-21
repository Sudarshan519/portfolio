from zeep import Client
from zeep.transports import Transport
url = "https://rps.digital-remittance.com/api/Send.svc?wsdl"
# Replace "your_soap_service_url" with the actual URL of the SOAP service
soap_service_url =url
wsdl_url = 'http://rps.digital-remittance.com/api/Send.svc?singleWsdl'
# Replace placeholders with actual values for username, password, and type_data
username = "testRps"
password = "testRps"
type_data = "IncomeSource"

# Replace "your_custom_envelope_xml" with the custom SOAP envelope XML you want to send
custom_envelope_xml = f"""\
<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
    <Body>
        <GetStaticData xmlns="http://tempuri.org/">
            <GetStaticDataRequest>
                <UserName xmlns="http://schemas.datacontract.org/2004/07/Remit.API">{username}</UserName>
                <Password xmlns="http://schemas.datacontract.org/2004/07/Remit.API">{password}</Password>
                <Type xmlns="http://schemas.datacontract.org/2004/07/Remit.API">{type_data}</Type>
            </GetStaticDataRequest>
        </GetStaticData>
    </Body>
</Envelope>
"""

# Create a custom transport with Zeep and set the custom XML envelope
 
# transport.load_custom_xml(custom_envelope_xml)

# Create the Zeep client using the custom transport
client = Client(wsdl_url)
input_params = {
    'username': username,
    'password': password,
    'type': type_data,
}
# Call the 'GetStaticData' SOAP operation with the necessary parameters in the request body
response = client.service.GetStaticData (GetStaticDataRequest={
        'UserName': username,
        'Password': password,
        'Type': type_data
    })

# Process the response
print(response)