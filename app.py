import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask import Flask, jsonify,request
import time
from handlers import *
from search import search_results

app = Flask(__name__)

#Specifying path of targert folder
UPLOAD_PATH = os.path.join(os.getcwd(), 'upload')
PROCESSED_PATH = os.path.join(os.getcwd(), 'processed')

@app.route("/upload",methods=["GET","POST"])
def upload_file():
    if request.method == 'POST':
        #if image is uploaded as a local file    
        if (request.headers.get('Content-type').split(';')[0] == 'multipart/form-data'):

            # Save the image in uploads folder. Store filepath in a variable and call the pass_file function.
            if 'image' in request.files.keys():
                file = request.files['image']
                if file.filename == '':
                    return jsonify('no image received')
                SAVED_FILE_PATH = os.path.join(UPLOAD_PATH, secure_filename(file.filename))
                print("File save path : {}".format(SAVED_FILE_PATH))
                file.save(SAVED_FILE_PATH)
                objects_detected = object_detection_handler(SAVED_FILE_PATH, None) 
                crop_file(objects_detected, SAVED_FILE_PATH, file.filename, PROCESSED_PATH)
                results=search_results()
                return jsonify(results)
                
            else:
                return jsonify(message_builder("Invalid body", "Please provide an Image as form data with key name 'image'")), 415  

        #if image is uploaded as URL
        if request.headers.get("Content-type")=="application/json":
            body = request.get_json()
            IMAGE_URL = body['url']

            objects_detected = object_detection_handler(None, IMAGE_URL)
            
            image_stream = requests.get(IMAGE_URL, stream=True)
            image = Image.open(BytesIO(image_stream.content)).convert('RGB')
            filename = str(time.time()).split('.')[0]
            SAVED_FILE_PATH = os.path.join(UPLOAD_PATH, secure_filename(filename) + '.jpg')
            image.save(SAVED_FILE_PATH)
            crop_file(objects_detected, SAVED_FILE_PATH, filename + '.jpg', PROCESSED_PATH)
             
            results=search_results()
            return jsonify(results)

    

def message_builder(argument, message):
    res = {
        "error": {
            "code": argument,
            "message": message
        }
    }
    return res

if (__name__)=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
