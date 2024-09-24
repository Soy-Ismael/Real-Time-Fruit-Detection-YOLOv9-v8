from flask import request, Flask, jsonify, send_file
from flask_cors import CORS
from PIL import Image # PIL (Python Imaging Library) es una biblioteca de Python para abrir, manipular y guardar diferentes formatos de archivos de imagen.
import io #En el contexto de procesamiento de imágenes, io se usa a menudo con PIL/Pillow para manejar imágenes en memoria sin necesidad de guardarlas en disco.
from io import BytesIO
from main import FruitDetector
detector = FruitDetector()
import base64 # Este módulo me permite códificar la imagen en base64 para poder enviarla a Js posteriormnete.
import cv2

# Flask va a ser el servidor backend, para ello creamos una instancia de Flask
app = Flask(__name__) #El name es recomendado en la documentación de Flask

CORS(app) #Permite solicitudes de origenes cruzados para todos los origenes o rutas
# CORS(app, resources={r"/inference": {"origins": "http://127.0.0.1:5500"}})
# CORS(app, origins=["https://homis.duckdns.org/fruit-detection"],  methods=["POST"])
# Para crear un endpoint podemos hacerlo de la siguiente manera:
# Método GET
@app.route("/inference", methods=['POST']) #Este endpoint recibe datos enviados a la ruta-#/inference por el méotod POST
# def root():
    # Esto imprimira Home en la página web que abre Flask
    # return "Home"
def run_inference():
    if 'image' not in request.files:
        return jsonify({
            'Error': 'Imagen was not received',
            'ok': False,
            'status': 400,
            'Details': 'Please ensure an image file is attached to the request'
        }), 400

    # Si por el contrario si se recibio una imagen entonces guardala en una variable:
    image_file = request.files['image']
    # Abrir la imagen con PIL
    image = Image.open(io.BytesIO(image_file.read()))
    # Pasandole el archivo de imagen a la función que correra la inferencia
    image_processed = detector.inference(image)
    # Devolviendo el resultado:

    # Convertir la imagen procesada a bytes para enviarla a Js
    # img_byte_arr = BytesIO()
    # image_processed.save(img_byte_arr, format='JPEG')
    # img_byte_arr.seek(0)
    # Convertir el array de NumPy a una imagen PIL
    #todo img_pil = Image.fromarray(np.uint8(img_array))
    
    # Convertir la imagen PIL a bytes
    #todo img_byte_arr = BytesIO()
    #todo img_pil.save(img_byte_arr, format='PNG')
    #todo img_byte_arr = img_byte_arr.getvalue()
    
    # return send_file(img_byte_arr, mimetype='image/jpeg')
    # todo todo abajo
    # return send_file(
    #     BytesIO(img_byte_arr),
    #     mimetype='image/png',
    #     as_attachment=True,
    #     download_name='processed_image.png'
    # )

    # Convertir la imagen procesada a png y luego códificarla a base64
    # _, buffer = cv2.imencode('.png', image_processed)
    # img_base64 = base64.b64encode(buffer).decode('utf-8')

    # # Crear la respuesta JSON
    # response = {
    #     'image': img_base64,
    #     'status': 'sucess',
    #     'ok': True,
    # }
    
    # # Enviar respuesta al cliente
    # return jsonify(response), 200

    # ?
    # img_byte_arr = io.BytesIO()
    # image_processed.save(img_byte_arr, format='PNG')
    # img_byte_arr = img_byte_arr.getvalue()

    # return send_file(
    #     io.BytesIO(img_byte_arr),
    #     mimetype='image/png',
    #     as_attachment=True,
    #     download_name='processed_image.png'
    # )

    # ? 3
    # return jsonify(results.pandas().xyxy[0].to_dict(orient="records"))

    # ?4
    # return jsonify(image_processed)

    # ? 5
     # Convertir la imagen procesada a bytes
    # img_byte_arr = BytesIO()
    # image_processed.save(img_byte_arr, format='PNG')
    # img_byte_arr.seek(0)

    # return send_file(img_byte_arr, mimetype='image/png')

    # ? 6 ✅
    _, buffer = cv2.imencode('.png', image_processed)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    
    # Crear la respuesta JSON
    response = {
        'image': img_base64,
        'ok': True,
        'status': 200,
        'detail': 'Images was processed sucesfull'
    }
    
    return jsonify(response)




# GET -> Para obtener datos
# POST -> Para enviar datos
# PUT -> Para actualizar datos
# DELETE -> Para eliminar datos

# Si necesito implementar todos estos métodos puedo añadir más endpoints
# @app.route("/user/<user_id>") los signos de mayor y menos que indican que en la ruta user quiero pasar un parametro user_id por la URL
# def get_user(user_id):
#     return f'El usuario es el número: {user_id}'

# Si se quiere enviar un query (más argumentos como el ejemplo de esta ruta: #/users/2354?query=query_test)
# request.args.get('query') De este modo se obtiene

# if query:
#     user["query"] = query
#     Esto es solo un ejemplo para comprobar que se envio un query y ejecuta un código

# Para devolver una respuesta:
# def response():
    # Esto no tiene sentido porque no tiene de donde sacar user, pero sirve para ejemplificar que se devuelve el archivo procesado con un código 200 si todo salio bien.
    # return jsonify(user), 200

# Ejemplo de implementación de método POST
# @app.route('/users', methods=['POST'])
# def create_user():
    # De este modo se obtiene el json enviado a la API en python
    # data = request.get_json()
    # data['status'] = "user created" # De este módo añado una propiedad y un valor status a la respuesta
    # return jsonify(data), 201 # El 201 indica que la información se creo



if __name__ == "__main__":
    # Esto crea un servidor web y pone la terminal de python en modo debug
    app.run(host='0.0.0.0', port=5000, debug=True)