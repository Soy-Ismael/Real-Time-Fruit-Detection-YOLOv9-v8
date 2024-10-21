from flask import request, Flask, jsonify, send_file
from flask_cors import CORS
from PIL import Image
from io import BytesIO
from main import FruitDetector
detector = FruitDetector()
import base64
import cv2
import os
from json import loads as str_to_json

app = Flask(__name__)
CORS(app)
@app.route("/inference", methods=['POST'])
def run_inference():
    if 'image' not in request.files:
        return jsonify({
            'Error': 'Imagen was not received',
            'ok': False,
            'status': 400,
            'Details': 'Please ensure an image file is attached to the request'
        }), 400

    image_file = request.files['image']
    config_model = request.form.get('model')
    config_gpu = bool(request.form.get('gpu'))
    config_confidence = float(request.form.get('confidence', 0))

    parent_path = os.path.dirname(os.path.abspath(__file__))
    config_model = os.path.join(parent_path, 'runs', 'detect', 'train8', 'weights', 'best.pt') if config_model == "custom" else os.path.join(os.path.dirname(parent_path), 'models', f"{config_model}.pt")

    image = Image.open(BytesIO(image_file.read()))
    try:
        data = detector.inference(image, config_model, config_confidence, config_gpu, False) # Don't change the last argument

        _, buffer = cv2.imencode('.webp', data['image'])
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'image': img_base64,
            'data': str_to_json(data['json']),
            'ok': True,
            'status': 200,
            'detail': 'Images was processed sucesfull'
        })
    except Exception as e:
        return jsonify({
            'Error': 'An error occurred during processing',
            'ok': False,
            'status': 500,
            'details': str(e)
        }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)