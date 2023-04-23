import os
from dotenv import load_dotenv

load_dotenv()
from pymongo.mongo_client import MongoClient

uri = os.getenv("URI")
client = MongoClient(uri)
db = client.testbase
coll = db.users


def create_user_in_db(user_id, name):
    coll.insert_one({
        "_id": user_id,
        "name": name,
        "prompt": "Mangust",
        "arguments": {
            "steps": 20,
            "cfg_scale": 7,
            "sampler_index": "Euler a"
        }
    })





def add_prompt_to_user(user_id, prompt):
    current_data = {"_id": user_id}
    new_data = {"$set": {"prompt": prompt}}
    coll.update_one(current_data, new_data)


def get_prompt_by_user(user_id):
    for prompt in coll.find({"_id": user_id}, {"_id": 0, "prompt": 1}):
        print(prompt)
        return prompt


def add_argument_to_user(user_id, param, value):
    current_data = {"_id": user_id}
    new_data = {"$set": {"arguments": {
        param: value
    }}}
    coll.update_one(current_data, new_data)
    return new_data


def get_arguments_by_user(user_id):
    for arguments in coll.find({"_id": user_id}, {"_id": 0, "arguments": 1}):
        print(arguments)
        return arguments


def add_style_to_user(user_id, value):
    current_data = {"_id": user_id}
    new_data = {"$set": {"styles": value}}
    coll.update_one(current_data, new_data)
    return new_data


def get_style_by_user(user_id):
    for style in coll.find({"_id": user_id}, {"_id": 0, "styles": 1}):
        print(style)
        return style


def set_model_to_user(user_id, value):
    current_data = {"_id": user_id}
    new_data = {"$set": {"sd_model_checkpoint": value}}
    coll.update_one(current_data, new_data)
    return new_data


def get_model_by_user(user_id):
    for model in coll.find({"_id": user_id}, {"_id": 0, "sd_model_checkpoint": 1}):
        print(model)
        return model


def set_default_params(user_id):
    current_data = {"_id": user_id}
    new_data = {"$set": {
        "styles": [],
        "arguments": {
            "steps": 20,
            "cfg_scale": 7,
            "sampler_index": "Euler a",
            "sd_model_checkpoint": "ANYTHING_MIDJOURNEY_V_4.1.ckpt [041eabfcc6]"
        }
    }}
    coll.update_one(current_data, new_data)
