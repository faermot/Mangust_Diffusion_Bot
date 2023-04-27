import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
load_dotenv()


uri = os.getenv("URI")
client = MongoClient(uri)
db = client.testbase
coll = db.users


def check_key(user_id):
    filter_dict = {"_id": str(user_id), "key": True}
    if coll.count_documents(filter_dict):
        answer = True
        return answer
    else:
        answer = False
        return answer


def create_user_in_db(user_id, name):
    coll.insert_one({
        "_id": user_id,
        "name": name,
        "key": True,
        "prompt": "Mangust",
        "negative_prompt": "(worst quality:1.2), "
                           "(low quality:1.2), "
                           "(lowres:1.1), (monochrome:1.1), "
                           "(greyscale), multiple views, comic, sketch, "
                           "(((bad anatomy))), (((deformed))), "
                           "(((disfigured))), watermark, multiple_views, "
                           "mutation hands, mutation fingers, extra fingers, "
                           "missing fingers, watermark",
        "styles": [],
        "sd_model_checkpoint": "ANYTHING_MIDJOURNEY_V_4.1.ckpt [041eabfcc6]",
        "arguments": {
            "steps": 20,
            "cfg_scale": 7,
            "sampler_index": "Euler a",
            "width": 512
        }
    })


def add_prompt_to_user(user_id, prompt):
    current_data = {"_id": user_id}
    new_data = {"$set": {"prompt": prompt}}
    coll.update_one(current_data, new_data)


def get_prompt_by_user(user_id):
    for prompt in coll.find({"_id": user_id}, {"_id": 0, "prompt": 1}):
        return prompt


def add_negative_prompt_to_user(user_id, negative_prompt):
    current_data = {"_id": user_id}
    new_data = {"$set": {"negative_prompt": negative_prompt}}
    coll.update_one(current_data, new_data)


def get_negative_prompt_by_user(user_id):
    for negative_prompt in coll.find({"_id": user_id}, {"_id": 0, "negative_prompt": 1}):
        return negative_prompt


def add_argument_to_user(user_id, param, value):
    current_data = {"_id": user_id}
    new_data = {"$set": {f"arguments.{param}": value}}
    coll.update_one(current_data, new_data)
    return new_data


def get_arguments_by_user(user_id):
    for arguments in coll.find({"_id": user_id}, {"_id": 0, "arguments": 1}):
        return arguments


def add_style_to_user(user_id, value):
    current_data = {"_id": user_id}
    new_data = {"$set": {"styles": value}}
    coll.update_one(current_data, new_data)
    return new_data


def get_style_by_user(user_id):
    for style in coll.find({"_id": user_id}, {"_id": 0, "styles": 1}):
        return style


def set_model_to_user(user_id, value):
    current_data = {"_id": user_id}
    new_data = {"$set": {"sd_model_checkpoint": value}}
    coll.update_one(current_data, new_data)
    return new_data


def get_model_by_user(user_id):
    for model in coll.find({"_id": user_id}, {"_id": 0, "sd_model_checkpoint": 1}):
        return model


def get_name_model(name_model):
    if name_model == "ANYTHING_MIDJOURNEY_V_4.1.ckpt [041eabfcc6]":
        model = "🏞 ANYTHING MIDJ v1.0"
        return model

    elif name_model == "revAnimated_v122.safetensors [f8bb2922e1]":
        model = "🌄 RevAnimated v1.22"
        return model

    elif name_model == "v1-5-pruned.ckpt [e1441589a6]":
        model = "🌁 Pruned v1.5"
        return model

    elif name_model == "deliberate_v2.safetensors [9aba26abdf]":
        model = "🌇 Deliberate v2.0"
        return model

    else:
        return "Error"


def convert_format(no_convert_format):
    if no_convert_format == 512:
        format = "1:1"
        return format
    elif no_convert_format == 683:
        format = "4:3"
        return format
    elif no_convert_format == 910:
        format = "16:9"
        return format


def get_info_for_render(user_id):
    prompt = get_prompt_by_user(user_id).get("prompt")
    negative_prompt = get_negative_prompt_by_user(user_id).get("negative_prompt")
    arguments = get_arguments_by_user(user_id)
    cfg = arguments.get("arguments").get("cfg_scale")
    steps = arguments.get("arguments").get("steps")
    sampler = arguments.get("arguments").get("sampler_index")
    name_model = get_model_by_user(user_id).get("sd_model_checkpoint")
    no_convert_format = arguments.get("arguments").get("width")
    format = convert_format(no_convert_format)
    model = get_name_model(name_model)
    style = get_style_by_user(user_id).get("styles")
    info = f"*📋 Предпросмотр:*\n" \
           f"\n" \
           f"_{prompt}_\n" \
           f"\n" \
           f"_{negative_prompt}_\n" \
           f"\n" \
           f"*📊 Значение CFG*: {cfg}\n\n" \
           f"*🌌 Метод отбора*: {sampler}\n\n" \
           f"*🥇 Шаг выборки*: {steps}\n\n" \
           f"*⭐ Стиль*: {style}\n\n" \
           f"*↔️ Формат*: {format}\n\n" \
           f"*🤖 Модель*: {model}\n"
    return info



def set_default_params(user_id):
    current_data = {"_id": user_id}
    new_data = {"$set": {
        "negative_prompt": " ",
        "styles": [],
        "sd_model_checkpoint": "ANYTHING_MIDJOURNEY_V_4.1.ckpt [041eabfcc6]",
        "arguments": {
            "steps": 20,
            "cfg_scale": 7,
            "sampler_index": "Euler a",
            "width": 512
        }
    }}
    coll.update_one(current_data, new_data)
