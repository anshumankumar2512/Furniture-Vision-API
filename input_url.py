import cgi, cgitb
from flask import *  



app = Flask(__name__)
  
@app.route('/') 
def upload():  
        return render_template("urlinput.html")  

def store():
# Create instance of FieldStorage
 form = cgi.FieldStorage()
# Get data from fields
 url = form.getvalue('Enter URL:')
 return url



if __name__ == '__main__':  
     app.run(debug = True)  

