from tools.face_recognition import datasetCreator
from tools.face_recognition import face_trainer
from tools.face_recognition import detector
from tools import qr_reader
import constants


def read_qr():
    print("getEnter QR")
    qr_data , error = qr_reader.read_usb(constants.qr_camera)
    if not error:
        return str(qr_data, "utf-8"), error
    else:
        return None, error
        
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
    if user_id in IDs:
        return True
    return False



