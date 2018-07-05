from tools.face_recognition import detector
import constants

def getUser():
    return detector.get_faceID(constants.shop_camera), False