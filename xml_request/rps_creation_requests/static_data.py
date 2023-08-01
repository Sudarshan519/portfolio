from xml_request.services import client

username = "testRps"
password = "testRps"
type_data = "IncomeSource"

input_params = {
    'username': username,
    'password': password,
    'type': type_data,
}
# Call the 'GetStaticData' SOAP operation with the necessary parameters in the request body
response = client.service.GetStaticData(GetStaticDataRequest={
        'UserName': username,
        'Password': password,
        'Type': type_data
    })

# Process the response
print(response)