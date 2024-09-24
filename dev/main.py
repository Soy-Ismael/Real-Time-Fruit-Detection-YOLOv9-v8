from ultralytics import YOLO
import cv2
from yaml import safe_load
import pyttsx3

# Usar esta página si se necesita formatear código python: https://codebeautify.org/python-formatter-beautifier

# * El modelo en carpeta train4 es el mejor que funciona hasta ahora
#* YOLOV9C

# Model	                Filenames   	                 Tasks         	    Inference    Validation      Training    	Export
# YOLOv9	        yolov9c.pt yolov9e.pt	        Object Detection	        ✅      	    ✅      	    ✅	        ✅
# YOLOv9-seg  	yolov9c-seg.pt yolov9e-seg.pt	  Instance Segmentation	        ✅	        ✅	        ✅	        ✅

#* Colors
# colors = {
#     red : '\033[91m',
#     # GREEN : '\033[92m',
#     # BLUE : '\033[94m',
#     # CYAN : '\033[96m',
#     # MAGENTA : '\033[95m',
#     yellow : '\033[93m',
#     reset : '\033[0m',
# }
# print(f'{colors['yellow']} = = PRESS ESC TO EXIT = = {colors['reset']}')

class FruitDetector:
    # Inicializar la clase con el path de configuración del asistente
    def __init__(self, config_path='dev/config.yaml'):
        # Abrir el archivo de configuración proporcionado
        with open(config_path, 'r') as file:
            # Implementarlo en toda la clase
            self.config = safe_load(file)
        # Creando más atributos para la clase
        # Lo ideal seria añadir un bloque try-catch aquí, pero eso creo que no me permitiria utilizar el modelo por fuera
        try:
            if self.config['gpu']:
                self.model = YOLO(self.config['model_path']).to('cuda')
            else:
                self.model = YOLO(self.config['model_path']).to('cpu')
        except:
            self.model = YOLO(self.config['model_path']).to('cpu')

        self.camera = cv2.VideoCapture(self.config['camera_index'])
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', self.engine.getProperty('voices')[self.config['voice_index']].id)
        # Crea un set vacio para evitar duplicados posteriormente
        self.last_detections = set()
        self.colors = {
            'red' : '\033[91m',
            # GREEN : '\033[92m',
            # BLUE : '\033[94m',
            # CYAN : '\033[96m',
            # MAGENTA : '\033[95m',
            'yellow' : '\033[93m',
            'reset' : '\033[0m',
        }
        self.index = 0

    # for voice in voices:
    #     print(f"ID: {voice.id}, Nombre: {voice.name}")
    # engine.setProperty('voice', voices[1].id)
        
    def talk(self, text):
        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(self._talk_async, text)

    def _talk_async(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        # La nomenclatura del guion bajo en python significa varias cosas, pero en este caso indica que es una función privada (es decir, es para ser utilizada dentro de la clase, no fuera)

    def detect(self, frame):
        results = self.model.predict(frame, imgsz=self.config['imgsz'], conf=self.config['confidence_threshold'])

        # Crea un nuevo conjunto vacío para almacenar las detecciones del frame actual.
        current_detections = set()

        # Detecta las frutas del frame
        for result in results:
            for box in result.boxes:
                # Convierte de texto a número para comparar en el archivo  yaml
                class_id = int(box.cls)
                # Añade cada objeto detectado en el frame actual al conjunto current_detections.
                if class_id in self.config['class_names']:
                    item_name = self.config['class_names'][class_id]
                    current_detections.add(item_name)

        # Esta es la operación clave. Realiza una "diferencia de conjuntos".
        # El operador - entre conjuntos crea un nuevo conjunto que contiene elementos que están en current_detections pero no en self.last_detections.
        # En otras palabras, new_detections contendrá solo los objetos que se detectaron en este frame pero que no estaban presentes en el frame anterior.
        new_detections = current_detections - self.last_detections

        # Anuncia solo los objetos nuevos (los que no estaban en el frame anterior).
        for item in new_detections:
            self.talk(f"There is {item} in front of you")

        # Actualiza last_detections para el próximo frame.
        self.last_detections = current_detections

        # Dibuja la silueta de la fruta detectada
        return results[0].plot()
        # La lógica paso a paso:
        # En cada frame, se crea un nuevo conjunto de detecciones actuales.
        # Se compara este conjunto con el conjunto de detecciones del frame anterior.
        # Solo se anuncian los objetos que son "nuevos" (no estaban en el frame anterior).
        # Se actualiza el conjunto de "últimas detecciones" para el próximo frame.
        # Ejemplo práctico:
        # Frame 1: Detecta {manzana, plátano}
        # Anuncia: "manzana", "plátano"
        # last_detections = {manzana, plátano}
        # Frame 2: Detecta {manzana, plátano, naranja}
        # current_detections = {manzana, plátano, naranja}
        # new_detections = {manzana, plátano, naranja} - {manzana, plátano} = {naranja}
        # Anuncia: "naranja"
        # last_detections se actualiza a {manzana, plátano, naranja}
        # Frame 3: Detecta {manzana, naranja}
        # current_detections = {manzana, naranja}
        # new_detections = {manzana, naranja} - {manzana, plátano, naranja} = {}
        # No anuncia nada (no hay nuevas detecciones)
        # last_detections se actualiza a {manzana, naranja}
        # Esta lógica asegura que solo se anuncien objetos nuevos, evitando repeticiones constantes y mejorando la experiencia del usuario.
    
    def get_model_info(self, model):
        # import torch
        info = {
            "Model type": type(model),
            "Task": model.task,
            "Number of parameters": sum(p.numel() for p in model.model.parameters()),
            "Class names": model.names,
            "Input size": model.model.args['imgsz'],
            "YOLO version": model._version,
            "Weights file": model.ckpt_path,
            "Device": model.device,
            # "CUDA available": torch.cuda.is_available()
        }
        
        # if torch.cuda.is_available():
        #     info["CUDA device"] = torch.cuda.get_device_name(0)
        
        # if hasattr(model, 'metrics'):
        #     info["Model metrics"] = model.metrics
        
        return info


    def inference(self, img, save_debug_img=False):
        with open("//10.0.0.68/html/fruit-detection/dev/web/php/new_config.yaml", 'r') as local_file:
            # Implementarlo en toda la clase
            local_config = safe_load(local_file)
        # Creando más atributos para la clase
        if local_config['gpu']:
            local_model = YOLO(local_config['model_path']).to('cuda')
        else:
            local_model = YOLO(local_config['model_path']).to('cpu')

        # print(f'{self.colors['red']}Model are using:{self.colors['reset']} {local_model.device}')
        # model_info = self.get_model_info(local_model)
        # for key, value in model_info.items():
        #     print(f"{self.colors['red']}{key}:{self.colors['reset']} {value}")

        #? Código para obtener la imagen desde Js...
        # result = self.model.predict(img, conf=self.config['confidence_threshold'])

        result = local_model.predict(img, conf=local_config['confidence_threshold'])
        # result[0].show() # Si se quiere mostrar
        # result[0] #Almacena la imagen procesada
        #? Código para enviar la imagen procesada a JavaScript
        # Convertir la imagen a un formato que Flask pueda enviar
        # self.check_cuda_support()
        
        # self.model.save('./inferenced')
        if save_debug_img:
            result[0].save(f'//10.0.0.68/html/fruit-detection/dev/web/inferenced/test{self.index}.png')
        self.index = self.index +1
        return result[0].plot() # Genera una imagen con las detecciones visualizadas


    def run(self):
        try:
            while True:
                # Inicializando la lectura de la camara para deteccion en directo
                ret, frame = self.camera.read()
                # ret algo que devuelve opencv camera para verificar si se obtuvo algo con la camara, es para verificar que si hay un fotograma.
                if not ret:
                    break

                detection = self.detect(frame)
                cv2.imshow("DETECTION | Press ESC to exit", detection)

                if cv2.waitKey(1) == 27:  # ESC key
                    break

        finally:
            self.camera.release()
            cv2.destroyAllWindows()
            # self.executor.shutdown() # Comentado porque utilice un context (with) para el threadexecutor

    def check_cuda_support(self):
        import torch
        import torchvision

        # Comprobar si los nucleos CUDA de la GPU Nvidia estan habilitados para usar con la red neuronal
        #! NOTA DEBERIA CAMBIAR LOS EMOJIS POR ICONOS DE TEXTO PORQUE LINUX NO LOS SOPORTA
        # \u2705" if torch.cuda.is_available() else "
        print(f"{self.colors['red']}CUDA SUPPORT:{self.colors['reset']} {'✅' if torch.cuda.is_available() else '❌, VISIT https://pytorch.org/get-started/locally/'}")
        print(f"{self.colors['red']}Device:{self.colors['reset']} {torch.cuda.get_device_name(0)}")
        # La siguiente linea tiene que ver más con el propio modelo que con el propio cuda, pero no esta de más saber
        print(f"{self.colors['red']}Model are using:{self.colors['reset']} {self.model.device}")

        print(f"{self.colors['red']}PyTorch version:{self.colors['reset']} {torch.__version__}")
        print(f"{self.colors['red']}Torchvision version:{self.colors['reset']} {torchvision.__version__}")
        print(f"{self.colors['red']}CUDA available:{self.colors['reset']} {torch.cuda.is_available()}")
        print(f"{self.colors['red']}CUDA version:{self.colors['reset']} {torch.version.cuda}")

    def train_model(self, model_name:str='yolov9m.pt', data:str='data/dataset.yaml', epochs:int=300, imgsz:int=640, batch:int=4):
        global model, result
        model = YOLO(model_name)  # Cargar un modelo preentrenado

        # Entrenar el modelo
        result = model.train(data=data, epochs=epochs, imgsz=imgsz, batch=batch)


    def get_boxes(self):
        # print(model.names)
        # global model
        for item in model.names.items():
            print(f'{item[0]} {item[1]}')


if __name__ == "__main__":
    detector = FruitDetector()
    # detector.run()
    detector.inference('../public/images/green_apple.jpg')