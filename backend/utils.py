import os
import openai
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

food_items = [
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "hot dog",
    "pizza",
    "cake"
]

def filter_none_food_items(raw_items): 
    filtered_items = []
    for item in raw_items:
        if item in food_items:
            filtered_items.append(item)
    return filtered_items



undetected_times_before_deleted = 3
items_not_detected_count = dict()

def remove_undetected_items(detected_item_names, db_items):
    print(items_not_detected_count)
    
    # pop any detected items
    for name in detected_item_names:
        if name in items_not_detected_count.keys():
            items_not_detected_count.pop(name, None)
            
    # append currently undetected items
    for db_item in db_items:
        if not db_item["name"] in detected_item_names:
            if not db_item["name"] in items_not_detected_count.keys():
                items_not_detected_count[db_item["name"]] = 0

    # update count of undetected items
    for undetected_name in list(items_not_detected_count.keys()):
        if not undetected_name in detected_item_names:
            items_not_detected_count[undetected_name] += 1
            
        # remove undetected items from db
        if items_not_detected_count[undetected_name] > undetected_times_before_deleted:
            removed_name = undetected_name
            db_items = [db_item for db_item in db_items if db_item["name"] != removed_name]
            items_not_detected_count.pop(removed_name, None)

    return db_items


def get_reply_from_chatgpt(ingredients):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    messages = [ {"role": "system", "content": "You are a brilliant cook."} ]
    ing_str = ','.join(ingredients)
    
    message = "provide some recipe ideas using" + ing_str
    
    messages.append(
        {"role": "user", "content": message},
    )
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )
        
    reply = chat.choices[0].message.content
    print('reply', reply)
    
    return reply

def generate_notification(items):
    notification = []
    
    current_time = datetime.now().date()
    for item in items:
        if item['expiration_date']:
            time_object = datetime.strptime(item['expiration_date'], "%Y-%m-%d").date()
            difference = time_object - current_time

            # Compare if the difference is less than 3 days
            if difference < timedelta(days=3):
                notification.append(f"Your {item['name']} is going to expire soon!")
                
    return notification