import requests
import os
import json
from PIL import Image
from io import BytesIO
from input_url import *
# This is the function
def computer_vision(image_uri):
    url = "https://centralindia.api.cognitive.microsoft.com/vision/v3.0/analyze?visualFeatures=Categories,Color,Objects,Description&language=en"

    payload = json.dumps({
    "url": image_uri
    })
    headers = {
    'Ocp-Apim-Subscription-Key': 'a731048f9a6448a799920bf28d220f2d',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    result = json.loads(response.text)
    return result['objects']


# This is the call
URL = "https://images.unsplash.com/photo-1513694203232-719a280e022f?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1049&q=80"

objects = computer_vision(URL)

image_stream = requests.get(URL, stream=True)
image = Image.open(BytesIO(image_stream.content)).convert('RGB')

cropped_images = list()
object_names = list()
PATH=r"C:\Users\Anshuman\Vision Search Project\uploads"
for items in objects:
    x = items['rectangle']['x']
    y = items['rectangle']['y']
    w = items['rectangle']['w']
    h = items['rectangle']['h']
    print('Bounding Box : {}, {}, {}, {}'.format(x, y, w, h))
    print('Object : {}'.format(items['object']))
    cropped_image = image.crop((x,y,x+w,y+h))
    cropped_images.append(cropped_image)
    object_names.append(format(items['object']))
for i in range(0,len(cropped_images)):
    img=cropped_images[i]
    img_name=object_names[i]
    img.save((os.path.join(PATH, img_name))+".png") 
   
    



