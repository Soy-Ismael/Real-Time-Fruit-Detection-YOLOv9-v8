from ultralytics import YOLO
import cv2

YELLOW = '\033[93m'
RESET = '\033[0m'

# Leer modelo
print(f'{YELLOW} = = PRESS ESC TO EXIT = = {RESET}')
model = YOLO("dev/runs/detect/train4/weights/best.pt")

import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()


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


# Video recording
cap = cv2.VideoCapture(0) # -> Change this number if you have more than 1 camera

def run(img_path:str=''):
    if img_path != '':
        # Example of inference in an image
        results = model.predict(img_path)
        results[0].show()
    else:
        while True:
            # Read frame
            ret, frame = cap.read()

            # take the frames, resize to 640px and show me the predictioins with more than 50% of confidence
            result = model.predict(frame, imgsz = 640, conf = 0.5)

            # Mostramos resultados
            detection = result[0].plot() # Create image
            cv2.imshow("DETECTION", detection) # Show image

            #* My dataset
            # custom_dataset(result[0].boxes)

            # Close the program
            if cv2.waitKey(1) == 27:
                break


run()
# run('path/to/image')
cap.release()
cv2.destroyAllWindows()