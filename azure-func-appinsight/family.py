import uuid
import json as jsonparser





       

def generateid(req_body):
    req_body['id'] = str(uuid.uuid4())
    return req_body 
