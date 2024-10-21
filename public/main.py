from ultralytics import YOLO
import cv2
from yaml import safe_load
import pyttsx3

class FruitDetector:
    def __init__(self, config_path='dev/config.yaml'): # Change the path according to your project configuration (recommended absolute path)
        with open(config_path, 'r') as file:
            self.config = safe_load(file)
        try:
            self.model = YOLO(self.config['model_path']).to('cuda' if self.config['gpu'] else 'cpu')
        except Exception:
            self.model = YOLO(self.config['model_path']).to('cpu')

        self.camera = cv2.VideoCapture(self.config['camera_index'])
        self.engine = pyttsx3.init()
        try:
            self.engine.setProperty('voice', self.engine.getProperty('voices')[self.config['voice_index']].id)
        except IndexError:
            self.engine.setProperty('voice', self.engine.getProperty('voices')[0].id)

        self.last_detections = set()
        self.colors = {
            'red' : '\033[91m',
            'reset' : '\033[0m',
        }
        self.index = 0

    def check_available_voices(self):
        index = 0
        for voice in self.engine.getProperty('voices'):
            print(f"Voice Index: {index}, Name: {voice.id.split('\\')[-1]}, Language: {voice.name.split('-')[-1]}")
            print(f'{self.colors['red']} = = = = = = = =  = = = = = = {self.colors['reset']}')
            index = index + 1
        
    def talk(self, text):
        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(self._talk_async, text)

    def _talk_async(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def detect(self, frame):
        results = self.model.predict(frame, imgsz=self.config['imgsz'], conf=self.config['confidence_threshold'])
        current_detections = set()
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls)
                if class_id in self.config['class_names']:
                    item_name = self.config['class_names'][class_id]
                    current_detections.add(item_name)

        new_detections = current_detections - self.last_detections
        for item in new_detections:
            self.talk(f"There is {item} in front of you")

        self.last_detections = current_detections
        return results[0].plot()
    
    def get_model_info(self, model):
        info = {
            "Model type": type(model),
            "Task": model.task,
            "Number of parameters": sum(p.numel() for p in model.model.parameters()),
            "Class names": model.names,
            "Input size": model.model.args['imgsz'],
            "YOLO version": model._version,
            "Weights file": model.ckpt_path,
            "Device": model.device,
        }
        return info

    def inference(self, img, model=None, confidence=None, gpu=None, local=True, save_image_debug_path=None):
        model = model if model != None else self.config['model_path']
        confidence = confidence if confidence != None else self.config['confidence_threshold']
        gpu = gpu if gpu != None else self.config['gpu']

        local_model = YOLO(model).to('cuda' if gpu else 'cpu')

        result = local_model.predict(img, conf=confidence)
        if save_image_debug_path != None:
            result[0].save(f"{save_image_debug_path[:-1] if save_image_debug_path.endswith('/') else save_image_debug_path}/debug_image{self.index}.png")

        self.index = self.index +1
        if local:
            result[0].show()
        else:
            return {'image': result[0].plot(), 'json': result[0].tojson()}

    def run(self):
        try:
            while True:
                ret, frame = self.camera.read()

                if not ret:
                    break

                detection = self.detect(frame)
                cv2.imshow("DETECTION | Press ESC to exit", detection)

                if cv2.waitKey(1) == 27:  # ESC key, (if press esc the detection going to end)
                    break

        finally:
            self.camera.release()
            cv2.destroyAllWindows()

    def check_cuda_support(self):
        import torch
        import torchvision

        print(f"{self.colors['red']}CUDA SUPPORT:{self.colors['reset']} {'✅' if torch.cuda.is_available() else '❌, VISIT https://pytorch.org/get-started/locally/'}")
        print(f"{self.colors['red']}Device:{self.colors['reset']} {torch.cuda.get_device_name(0)}")

        print(f"{self.colors['red']}Model are using:{self.colors['reset']} {self.model.device}")
        print(f"{self.colors['red']}PyTorch version:{self.colors['reset']} {torch.__version__}")
        print(f"{self.colors['red']}Torchvision version:{self.colors['reset']} {torchvision.__version__}")
        print(f"{self.colors['red']}CUDA available:{self.colors['reset']} {torch.cuda.is_available()}")
        print(f"{self.colors['red']}CUDA version:{self.colors['reset']} {torch.version.cuda}")

    def train_model(self, model_name:str='yolov9m.pt', data:str='data/dataset.yaml', epochs:int=300, imgsz:int=640, batch:int=4):
        global model, result
        model = YOLO(model_name)
        result = model.train(data=data, epochs=epochs, imgsz=imgsz, batch=batch)

    def get_boxes(self):
        for item in model.names.items():
            print(f'{item[0]} {item[1]}')


if __name__ == "__main__":
    detector = FruitDetector()
    # detector.run()
    # detector.inference('public/images/oranges2.jpg')