import requests

# send detection result to smart-fridge server
def send_detection_result(names):
    url = 'https://1ccb-180-177-2-79.jp.ngrok.io/sync/object_detection'
    headers={
        'Content-type':'application/json',
        'Accept':'application/json'
    }
    r = requests.post(url, json={'objects': names}, headers=headers)
    
    return r.status_code