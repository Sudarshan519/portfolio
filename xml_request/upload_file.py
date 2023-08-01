# Path to the file you want to upload
import base64
from zeep import Client
from zeep.transports import Transport
from zeep.plugins import HistoryPlugin
 

file_path = 'path/to/your/file.txt'

# Load the file content and encode it in base64
with open(file_path, 'rb') as file:
    file_content = file.read()
    encoded_file_content = base64.b64encode(file_content).decode()

# Create a HistoryPlugin to store the request and response for debugging
history = HistoryPlugin()

# Create the Zeep client
transport = Transport()
client = Client('your_wsdl_url', transport=transport, plugins=[history])

# Initialize the Attachments
attachments = client.create_message(client.service, 'uploadAttachment', _soapheaders={'Attachments': []})

# Add the attachment to the Attachments object
attachment = client.create_message(attachments, 'Attachment')
attachment.Id = 1  # You can set an ID for the attachment if needed
attachment.Name = 'file.txt'  # The name of the attachment
attachment.ContentType = 'text/plain'  # The content type of the attachment
attachment.Content = encoded_file_content  # The base64-encoded content of the attachment

# Add the attachment to the Attachments list
attachments._value_1.append(attachment)

# Make the request with the attachment
response = client.service.uploadAttachment(_soapheaders={'Attachments': attachments})

# Print the response
print(response)