# importing modules
# we need to have an HTML form with the  multipart/form-data encryption. Saved that in templates.
from flask import *  



app = Flask(__name__)
  
@app.route('/') 
def upload():  
        return render_template("upload.html")  
     
@app.route('/recognize', methods = ['POST'])  
def success():  
        if request.method == 'POST':  
# Fetches the file using the request and stores to the server
            f = request.files['file']  
            f.save(f.filename)  
            return jsonify({"message":"Uploaded successfully"}, 200 )  
      
if __name__ == '__main__':  
     app.run(debug = True)  