import tools.qr_reader
import constants


def read_qr():
    return qr_reader.read_usb(constants.qr_camera), True
