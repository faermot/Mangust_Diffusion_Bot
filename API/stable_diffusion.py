import requests
from PIL import Image, PngImagePlugin
import io
import base64
import database.functions as df


def render_photo(user_id):
    url = "http://127.0.0.1:7860"
    model = df.get_model_by_user(user_id)
    option_payload = {
        "sd_model_checkpoint": "ANYTHING_MIDJOURNEY_V_4.1.ckpt [041eabfcc6]"
    }
    option_payload.update(model)
    requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)


    prompt = df.get_prompt_by_user(user_id)
    print(prompt)
    arguments = df.get_arguments_by_user(user_id)
    styles = df.get_style_by_user(user_id)

    # revAnimated_v122.safetensors [f8bb2922e1]

    payload = {
        "prompt": "Mangust",
        "steps": 20,
        "cfg_scale": 7,
        "sampler_index": "Euler a",
        "negative_prompt": "(worst quality:1.2), "
                           "(low quality:1.2), "
                           "(lowres:1.1), (monochrome:1.1), "
                           "(greyscale), multiple views, comic, sketch, "
                           "(((bad anatomy))), (((deformed))), "
                           "(((disfigured))), watermark, multiple_views, "
                           "mutation hands, mutation fingers, extra fingers, "
                           "missing fingers, watermark"
    }
    payload.update(prompt)
    payload.update(styles)
    for key, value in arguments.items():
        if isinstance(value, dict):
            for k, v in value.items():
                payload[k] = v

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        photo = io.BytesIO()
        image.save(photo, format='PNG', pnginfo=pnginfo)
        return photo.getvalue()
