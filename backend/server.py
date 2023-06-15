import json
from flask import Flask, request
from flask_cors import CORS
from datetime import datetime

from db import connect_redis
import utils

app = Flask(__name__)
CORS(app)

# redis
db = connect_redis()

# init items 
# db.set('items', json.dumps([]))
# db.set('temperature', 5)
# db.set('humidity', 75)

# Internal Service sync
@app.route('/sync/object_detection', methods=['POST'])
def sync_object_detection():
    # update food item list to db
    req_data = request.get_json()
    req_items = [data.split(":")[0] for data in req_data['objects']]
    detected_item_names = utils.filter_none_food_items(req_items)

    db_items = json.loads(db.get("items"))

    # append newly detected items
    for name in detected_item_names:
        exists = any(name in db_item["name"] for db_item in db_items)
        if not exists:
            now = datetime.now().strftime("%Y-%m-%d")
            db_items.append({"name": name, "expiration_date": None, "in_fridge_since": now})
            
    # remove undetected items
    items = utils.remove_undetected_items(detected_item_names, db_items)

    db.set('items', json.dumps(items))

    return ('', 204)

@app.route('/sync/face_detection', methods=['POST'])
def sync_face_detection():
    # update new face detection result to db
    data = request.get_json()
    
    print(data)
    return ('', 200)

@app.route('/sync/temp_humidity', methods=['POST'])
def sync_temp_humidity():
    # update temperature & humidity to db
    data = request.get_json()
    
    print(data)
    temp = 5
    humidity = 75
    
    db.set('temperature', temp)
    db.set('humidity', humidity)
    return ('', 200)

# frontend
@app.route('/fridge', methods=['GET'])
def get_fridge_state():
    temperature, humidity, items = db.mget('temperature', 'humidity', 'items')
    items = json.loads(items)
    
    state = {
        'temperature': temperature,
        'humidity': humidity,
        'status': 'Closed',
        'items': items,
        'notification': utils.generate_notification(items)
    }
    return state

@app.route('/fridge/recipe', methods=['GET'])
def get_recipe():
    items = request.args.get('items')
    print(items)
    try:
        reply = utils.get_reply_from_chatgpt(items)
        return ({"reply": reply}, 200)
    except:
        return ({"reply": "Sorry, ChatGPT service is currently unavailable"}, 400)
    

@app.route('/fridge/item', methods=['PATCH'])
def update_item_expiration_date():
    req_body = request.get_json()
    name = req_body['name']
    expiration_date = req_body['expiration_date']
    print(name, expiration_date)
    
    items = json.loads(db.get('items'))
    item_to_update = next((item for item in items if item['name'] == name), None)
    
    if item_to_update:
        item_to_update['expiration_date'] = expiration_date
        print(item_to_update)
        updated_json_data = json.dumps(items)
        db.set('items', updated_json_data)
        return ({"status": "success"}, 200)
    else:
        print("Object not found in the list.")
        return (f'{name} not found in fridge items', 400)

# iottalk
@app.route('/sync/iottalk', methods=['GET'])
def send_to_iottalk():
    temperature, humidity, items = db.mget('temperature', 'humidity', 'items')
    items = json.loads(items)
    
    state = {
        'temperature': temperature,
        'humidity': humidity,
        'status': 'Normal',
        'items': items,
        'notification': utils.generate_notification(items)
    }
    return state

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
