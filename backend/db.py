import os
import redis
from dotenv import load_dotenv


def connect_redis():
    load_dotenv()
    
    redis_host = os.getenv('REDIS_HOST_URL')
    redis_port = os.getenv('REDIS_PORT')
    redis_password = os.getenv('REDIS_PASSWORD')
    
    db = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    print(f'Connecting to Redis at {redis_host}:{redis_port} with password {redis_password}')
    
    return db