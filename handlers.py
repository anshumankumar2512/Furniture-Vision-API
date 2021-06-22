import requests
import os
import json
from PIL import Image
from io import BytesIO

def object_detection_handler(file_path, file_uri):
    url = "https://centralindia.api.cognitive.microsoft.com/vision/v3.0/analyze?visualFeatures=Categories,Color,Objects,Description&language=en"
    payload = dict()
    files = list()
    headers = {
        'Ocp-Apim-Subscription-Key': os.environ.get('Ocp-Apim-Subscription-Key')
    }
    if not (file_uri is None):
        print("Url exists")
        payload = json.dumps({
            "url": file_uri
        })
        print("Payload : ", payload)

    elif not (file_path is None):
        print("Local file")
        files = [('image', ('file', open(file_path, 'rb'), 'application/octet-stream'))]
        
    else:
        print("Exception")

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    result = json.loads(response.text)
    return result['objects']

def crop_file(objects_detected, source, filename, destination):
    image = Image.open(source)
    
    print("No. of objects detected were : {}".format(len(objects_detected)))

    for items in objects_detected:
        
        x = items['rectangle']['x']
        y = items['rectangle']['y']
        w = items['rectangle']['w']
        h = items['rectangle']['h']
        print('Bounding Box : {}, {}, {}, {}'.format(x, y, w, h))
        print('Object : {}'.format(items['object']))

        cropped_image = image.crop((x, y, x+w, y+h))

        extension =  filename.split('.')[len(filename.split('.'))-1]
        cropped_image.save(os.path.join(destination, items['object'] + '.' + extension))

