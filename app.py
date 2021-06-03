import os
from flask import Flask,render_template,jsonify,request
from functions import *

app=Flask(__name__)

#Specifying path of targert folder
app.config["UPLOAD_PATH"] = r"C:\Users\Anshuman\Vision Search Project\uploads"


@app.route("/upload_file",methods=["GET","POST"])
def upload_file():
    if request.method == 'POST':
        #if image is uploaded as a local file    
        if (request.headers.get('Content-type').split(';')[0] == 'multipart/form-data'):

            # Save the image in uploads folder. Store filepath in a variable and call the pass_file function.
            
            for f in request.files.getlist('file_name'):
                 f.save(os.path.join(app.config['UPLOAD_PATH'],f.filename))
                 print(os.path.join(app.config['UPLOAD_PATH'],f.filename))
                 filepath=os.path.join(app.config['UPLOAD_PATH'],f.filename)
                 result=pass_file(filepath)  
                 crop_file(result,filepath)

        #if image is uploaded as URL
        if request.headers.get("Content-type")=="application/json":
            
            URL=request.args.get('url')
            result=pass_url(URL)
            crop_url(result,URL)         

        return jsonify({"message":"Uploaded successfully"}, 200 )
    #return render_template("upload_file.html", msg="Please select file")

if (__name__)=='__main__':
    app.run(debug=True)
