from ultralytics import YOLO
import cv2

# * El modelo en carpeta train4 es el mejor que funciona hasta ahora
#* YOLOV9C

# Model	                Filenames   	                 Tasks         	    Inference    Validation      Training    	Export
# YOLOv9	        yolov9c.pt yolov9e.pt	        Object Detection	        ✅      	    ✅      	    ✅	        ✅
# YOLOv9-seg  	yolov9c-seg.pt yolov9e-seg.pt	  Instance Segmentation	        ✅	        ✅	        ✅	        ✅

#* Colors
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# Leer modelo
# Detección personalizada
print(f'{YELLOW} = = PRESS ESC TO EXIT = = {RESET}')
model = YOLO("runs/detect/train4/weights/best.pt")
# model = YOLO("runs/segment/train/weights/best.pt")

# Detecta muy bien, pero detecta todo
# model = YOLO("yolov9c.pt")

# print(model.info()) # Imprimir información del modelo.

#* Ejemplo para predecir si el objeto para el que fue entrenado YOLO esta en una imagen
# Run predictions
# results = model.predict('C:/path/to/img')
# Display results
# results[0].show()

import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# for voice in voices:
#     print(f"ID: {voice.id}, Nombre: {voice.name}")
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

# talk('Hello, this is a test')


def check_cuda_support():
    import torch
    # Comprobar si los nucleos CUDA de la GPU Nvidia estan habilitados para usar con la red neuronal
    print('CUDA SUPPORT: ✅') if torch.cuda.is_available() else print('CUDA SUPPORT: ❌, VISIT https://pytorch.org/get-started/locally/')


def train_model(model_name:str='yolov9m.pt', data:str='data/dataset.yaml', epochs:int=300, batch:int=4):
    global model, result
    model = YOLO(model_name)  # Cargar un modelo preentrenado

    # Entrenar el modelo
    result = model.train(data=data, epochs=epochs, imgsz=640, batch=batch)


def get_boxes():
    # print(model.names)
    index=0
    for item in model.names.items():
        print(f'{item[0]} {item[1]}')


def custom_dataset(boxes):
    for box in boxes:
        match box.cls:
            case 0:
                talk('There is an apple in front of you')
            case 1:
                talk('There is a banana in front of you')
            case 2:
                talk('There is a green apple in front of you')
            case 3:
                talk('There is an orange in front of you')    
            case _:
                pass



def default_dataset(boxes, more_than_fruits=False):
    for box in boxes:
        match box.cls:
            case 47:
                talk('There is an apple in front of you')
            case 46:
                talk('There is a banana in front of you')
            case 51:
                talk('There is a carrot in front of you')
            case 49:
                talk('There is an orange in front of you')
            case 50:
                talk('There is a brocoli in front of you')
            case 40:
                talk('There is a wine glass in front of you')
            case _:
                pass

        if more_than_fruits:
            match box.cls:
                case 67:
                    talk('There is a cell phone in front of you')
                case 64:
                    talk('There is a mouse in front of you')
                case 42:
                    talk('There is a fork in front of you')
                case 0:
                    talk('There is a person in front of you')
                case _:
                    pass



# Realizar video captura
cap = cv2.VideoCapture(0) # Indice de la camara (por si tienes más de una)
def run():
    while True:
        # Leer fotogramas
        ret, frame = cap.read()

        # Leermos resultados
        # Toma el video de la camara, redimencionalo a 640px y muestrame las predicciones que supere el 80% de concidencia
        result = model.predict(frame, imgsz = 640, conf = 0.5)
        # result = model.predict(frame, imgsz = 640)

        #* Ejemplo para analizar inferencia de una imagen
        # Run inference with the YOLOv9c model on the 'bus.jpg' image
        # results = model('path/to/bus.jpg')

        # Mostramos resultados
        detection = result[0].plot()
        cv2.imshow("DETECTION", detection)

        #* My dataset
        # custom_dataset(result[0].boxes)

        # *YOLO COCO DATASET
        # Verificar si se detectó una fruta específica
        # print(f'{RED} Se encontraron ' + str(len(result[0].boxes)) +' cajas' + RESET)
        # default_dataset(result[0].boxes)
        
        # Mostrar fotogramas
        # cv2.imshow("DETECCION Y SEGMENTACION", frame)
        # Ya no mostraremos frame, si no detection (aquí si busca el objeto con el que el modelo se entreno)

        # Cerrar programa
        if cv2.waitKey(1) == 27:
            break

run()
# get_boxes()
cap.release()
cv2.destroyAllWindows()