import base64
import json
def b64EncodeString(msg):
    msg_bytes = msg.encode('ascii')
    base64_bytes = base64.b64encode(msg_bytes)
    return base64_bytes.decode('ascii')

def writefile(data):
    f = open("extracted.txt", "a")
    f.write(str(data))
    f.close()
with open('rasanadmin-72aed785bfb5.json') as jsonfile:
    data=json.load(jsonfile)
    datastr = json.dumps(data)
    encoded=(base64.encodebytes(datastr.encode('utf-8')))
    # encoded=b64EncodeString(data)
    print(encoded)
    writefile(encoded)
    print(base64.decodebytes(encoded))