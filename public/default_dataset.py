from ultralytics import YOLO
import cv2

YELLOW = '\033[93m'
RESET = '\033[0m'

# Leer modelo
print(f'{YELLOW} = = PRESS ESC TO EXIT = = {RESET}')
model = YOLO("yolov9c.pt")
# model = YOLO("runs/detect/train4/weights/best.pt")

import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()


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


# Video recording
cap = cv2.VideoCapture(0)

def run(img_path:str=''):
    if img_path != '':
        # Example of inference in an image
        results = model.predict(img_path)
        results[0].show()
    else:
        while True:
            # Read frame
            ret, frame = cap.read()

            # take the framse, resize to 640px and show me the predictioins with more than 50% of confidence
            result = model.predict(frame, imgsz = 640, conf = 0.5)

            # Mostramos resultados
            detection = result[0].plot() # Create image
            cv2.imshow("DETECTION", detection) # Show image

            #* My dataset
            default_dataset(result[0].boxes)

            # Close the program
            if cv2.waitKey(1) == 27:
                break


run()
# run('images/fruits_in_supermarket.jpg')
cap.release()
cv2.destroyAllWindows()