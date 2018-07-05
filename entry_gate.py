from tools.face_recognition import datasetCreator
from tools.face_recognition import face_trainer
from tools.face_recognition import detector
from tools import qr_reader
import constants


def read_qr():
    print("getEnter QR")
    return str(qr_reader.read_usb(constants.qr_camera), "utf-8"), False


def register(user_id):
    datasetCreator.register(user_id,constants.entry_camera)
    face_trainer.train()
    return False

def check_face(user_id):
    IDs=[]
    i=0
    while (i<3):
        IDs.append(str(detector.get_faceID(constants.entry_camera)))
        i=i+1
    print(IDs)
    print(user_id)
    if user_id in IDs:
        return True
    return False



