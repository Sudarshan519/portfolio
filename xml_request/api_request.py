import requests
import xmltodict
# SOAP request URL
url = "https://rps.digital-remittance.com/api/Send.svc"
  
# structured XML
# payload = """
# <?xml version=\"1.0\" encoding=\"utf-8\"?>
# <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/" xmlns:rem="http://schemas.datacontract.org/2004/07/Remit.API">
#   http://schemas.xmlsoap.org/soap/envelope/
#     <soapenv:Header/>
#    <soapenv:Body>
#       <tem:GetStaticData>
#          <!--Optional:-->
#          <tem:GetStaticDataRequest>
#             <rem:UserName>testRps</rem:UserName>
#             <rem:Password>testRps</rem:Password>
#             <rem:Type>Gender</rem:Type>
#          </tem:GetStaticDataRequest>
#       </tem:GetStaticData>
#    </soapenv:Body>
# </soapenv:Envelope>
# """
username="testRps"
password="testRps"
type_data="ReasonOfTransfer"
payload=f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
 
    <Body>
        <GetStaticData xmlns="http://tempuri.org/">
           
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

def postprocess_dict(path, key, value):
    # Filter out any unnecessary elements or attributes based on your requirements
    if key.startswith("http://tempuri.org/:"):
        key.replace("http://tempuri.org/:","")
    elif key.startswith("http://schemas.xmlsoap.org/soap/envelope/:"):
        key=key.replace("http://schemas.xmlsoap.org/soap/envelope/:","")
    elif key.startswith("http://schemas.datacontract.org/2004/07/Remit.API:"):

        key = key.replace("http://schemas.datacontract.org/2004/07/Remit.API:", "")  # Remove the "xmlns" attribute if present
    return key, value
import json
# POST request
response = requests.request("POST", url, headers=headers, data=payload,)
# print(response.text)


my_dict = xmltodict.parse(response.text, process_namespaces=True, postprocessor=postprocess_dict) 
print(json.dumps(my_dict,indent=2),)
# for k,v in my_dict.items():
#     print(k.split(":")[-1],v)
# prints the response
# print(response.body)