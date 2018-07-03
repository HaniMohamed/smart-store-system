import requests
import json

host = "http://mommmmom.esy.es/ras"


def new_entry(user_id):
    url = host+"/in"
    payload = {'user_id': user_id}
    response = requests.request("POST", url, data=payload)
    print(response.text)

def new_exit(orderID):
    url = host+"/out"
    payload = {'order_id': orderID}
    response = requests.request("POST", url, data=payload)
    print(response.text)


def new_orderline(orderID, prodID, status):
    url = host+"/item"
    payload = {'order_id': orderID,'product_id': prodID,'status': status}
    response = requests.request("POST", url, data=payload)
    print(response.text)

def get_perm(user_id):
    url = host+"/in"
    payload = {'user_id':user_id}
    response = requests.post( url, data=payload)
    print(response.text)
    resJSON= json.loads(response.text)
    if(resJSON['error']=='0'):
        print(resJSON['msg'])


def set_perm(user_id):
    url = host+"/in"
    payload = {'user_id':user_id}
    response = requests.post( url, data=payload)
    print(response.text)
    resJSON= json.loads(response.text)
    if(resJSON['error']=='0'):
        print(resJSON['msg'])



new_entry(24)
