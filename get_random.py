import random
from datetime import datetime

def get_random_timestamp(start_timestamp, end_timestamp):
    random_timestamp = random.uniform(start_timestamp, end_timestamp)
    return datetime.fromtimestamp(random_timestamp)

def get_random_array_element(array):
    return random.choice(array)