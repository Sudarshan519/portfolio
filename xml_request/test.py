# from zeep import Client

# # Replace 'https://rps.digital-remittance.com/api/Send.svc?wsdl' with the WSDL URL you want to check
# wsdl_url = 'https://rps.digital-remittance.com/api/Send.svc?wsdl'

# try:
#     client = Client(wsdl_url)
#     print("WSDL is valid and accessible.")
# except Exception as e:
#     print("Error: ", e)



data=(
               { 
                'UserName': "username",
                'Password': "password",
                **{k:v for k,v in enumerate(range(0, 11))}

                }
             )
print(data)




