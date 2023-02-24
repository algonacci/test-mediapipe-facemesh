import os
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import module as md


app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = "static/"
app.config['STATIC_FOLDER'] = "static/"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def root():
    return jsonify({
        "status": {
            "msg": "Hello world!",
            "code": 200
        }
    }), 200

@app.route("/detect", methods=["GET", "POST"])
def detect():
    if request.method == "POST":
        file = request.files['image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        md.detect_landmark(image)        
        return jsonify({
            "status": {
                "msg": "Success detect",
                "code": 200
            },
            "data": "http://127.0.0.1:5000/static/idx.png"
        }), 200
    else:
        return jsonify({
            "status": {
                "msg": "USE POST!",
                "code": "405"
            }
        }), 405

if __name__ == "__main__":
    app.run()