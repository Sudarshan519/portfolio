import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json

import requests
websiteUrl='http://127.0.0.1:8000'
# Load email configuration from JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

# Send a GET request to retrieve the HTML content
response = requests.get(websiteUrl)
html_content = response.text

# Email configuration
sender_email = config['sender_email']
receiver_email = config['receiver_email']
subject = "Email with Attachment"
message = """
<html>
<body>
<h2>Hello!</h2>
<p>This is an email with an attachment.</p>
</body>
</html>
"""+html_content

# Create a multipart message
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

# Attach the HTML message
msg.attach(MIMEText(message, 'html'))

# Attach a file (PDF, image, etc.)
filename = 'uploaded.txt'
attachment = open(filename, 'rb')

# Create the attachment part
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment', filename=filename)

# Attach the attachment to the email
msg.attach(part)

# Convert the multipart message to a string
text = msg.as_string()

# Send the email
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
 
    server.login(config['smtp_username'], config['smtp_password'])
    server.sendmail(sender_email, receiver_email, text)
