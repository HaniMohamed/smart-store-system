import tools.face_recognition
import tools.qr_reader


def read_qr():
    return qr_reader.read_usb(2), True


def register(user_id):
    face_recognition.datasetCreator.register(user_id,"http://192.168.12.244:8080/shot.jpg)
    face_recognition.face_trainer.train()
    return False

def check_face(user_id):
    IDs = face_recognition.detector.get_faceID()
    if user_id in IDs:
        return True
    return False



