from flask import Flask, request, Response
import json
import requests
from io import BytesIO
import random
import base64
from PIL import Image, PngImagePlugin
import os
#FastAPI Init
fl = app = Flask(__name__)
#Set Server Address
url = "http://127.0.0.1:7861"

@fl.route('/' , methods = ["POST"])
def main():
    data = request.get_json() #得到json格式的传参
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=data) #直接发送给后端
    r = response.json() #得到后端传回的json参数
    for i in r['images']: #得到base64的png
        image = Image.open(BytesIO(base64.b64decode(i.split(",",1)[0])))
        png_payload = {
        "image": "data:image/png;base64," + i
    }
    response_from_backend = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload) #post后端图片base64
    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response_from_backend.json().get("info"))
    filename = str(random.randint(0,1000000)) + ".png"
    filename = os.path.join("images", filename.strip())
    image.save(filename, pnginfo=pnginfo)
    file_address = "http://261084.proxy.nscc-gz.cn:8888/" + filename
    return Response(file_address, mimetype="text/event-stream") #返回图片url给用户

@fl.route('/img2img' , methods = ["POST"])
def main2():
    data = request.get_json() #得到json格式传参
    #decoded_data = json.load(data) #解析json为dict
    url = data["url"] #获得传入的图片url
    #receive = requests.get(url) #get图片
    #img = Image.open(BytesIO(receive.content)) #图片encode为PIL List
    payload = {
            "init_images": [url],
            "prompt": data["prompt"],
            "seed": int(data["seed"]),
            "batch_size": 1,
            "n_iter": data["n_iter"],
            "steps": 28,
            "cfg_scale": 8,
            "width": int(data["width"]),
            "height": int(data["height"]),
            "negative_prompt": data["negative_prompt"] + "nsfw,{{{ugly}}}, {{{duplicate}}}, {{morbid}}, {{mutilated}}, {{{tranny}}}, mutated hands,{{{poorly drawn hands}}}, blurry, {{bad anatomy}},{{{bad proportions}}}, extra limbs, cloned face,{{{disfigured}}}, {{{more than 2 nipples}}}, {{{{missing arms}}}},{{{extra legs}}},mutated hands,{{{{{fused fingers}}}}}, {{{{{too many fingers}}}}}, {{{unclear eyes}}}, lowers, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality,jpeg artifacts, signature, watermark, username, blurry, bad feet, text font ui,malformed hands, long neck, missing limb,{mutated hand and finger: 1.5},{long body: 1.3},{mutation poorly drawn: 1.2}, disfigured, malformed mutated, multiple breasts, futa, yaoi, {{{{:3}}}}, {{{3d}}},sex,nipple,pussy,naked,nake",
            "sampler_index": data["sampler_index"],
            "include_init_images": False,
            "resize_mode": 1,
            "inpaint_full_res" : True
        }
    response_From_backend = requests.post(url= 'http://127.0.0.1:7861/sdapi/v1/img2img', json=payload) #获得后端回应
    return Response(To_api_result(response_From_backend), mimetype="text/event-stream") #返回图片url给用户

def To_api_result(response):
    receive = response.json()
    for i in receive['images']: #得到base64的png
        image = Image.open(BytesIO(base64.b64decode(i.split(",",1)[0])))
        png_payload = {
            "image": "data:image/png;base64," + i
        }
    response_From_backend = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload) #post后端图片base64
    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response_From_backend.json().get("info"))
    filename = str(random.randint(0,1000000)) + ".png"
    filename = os.path.join("images", filename.strip())
    image.save(filename, pnginfo=pnginfo)
    file_address = "http://261084.proxy.nscc-gz.cn:8888/" + filename
    return file_address
