import requests
import json

host = "http://mommmmom.esy.es/ras"


def new_entry(user_id):
    url = host+"/in"
    payload = {'user_id': user_id}
    response = requests.request("POST", url, data=payload)
    resJSON= json.loads(response.text)
    if(resJSON['error']== 0):
        return resJSON['order_id'] , False
    return None , True

def new_exit(orderID):
    url = host+"/out"
    payload = {'order_id': orderID}
    response = requests.request("POST", url, data=payload)
    resJSON= json.loads(response.text)
    if(resJSON['error'] == 0):
        return False
    return True


def new_orderline(orderID, prodID, status):
    url = host+"/item"
    payload = {'order_id': orderID,'product_id': prodID,'status': status}
    response = requests.request("POST", url, data=payload)
    resJSON= json.loads(response.text)
    print(response.text)
    if(resJSON['error'] == 0):
        return False
    return True

def get_perm(user_id):
    print("getPerm")
    url = host+"/user/"+str(user_id)
    response = requests.get( url)
    resJSON= json.loads(response.text)
    if(resJSON['error']== 0):
        return resJSON['pics'], False
    return None , True

def set_perm(user_id):
    url = host+"/user/"+str(user_id)
    payload = {'pics':str(1)}
    response = requests.post( url, data=payload)
    resJSON= json.loads(response.text)
    if(resJSON['error']==0):
        return False
    return True




