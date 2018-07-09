from tools.face_recognition import detector
import constants
import sqlite3
from termcolor import colored
from tools import color_objects_detect

##conect to the local database
conn = sqlite3.connect('store.db')
c = conn.cursor()


def getUser():
    return detector.get_faceID(constants.shop_camera), False

def storeProducts():
    red_objetcs=0
    green_objetcs=0
    yellow_objetcs=0
    try:
            c.execute("SELECT COUNT(Name),color FROM products GROUP BY color")    
            rows = c.fetchall()
            print(rows)
            for row in rows:
                if 'red' in row[1]:
                    red_objetcs = row[0]
                elif 'green' in row[1]:
                    green_objetcs = row[0]
                elif 'yellow' in row[1]:
                    yellow_objetcs = row[0]
    
    except sqlite3.Error as er :
            print (colored("SQLite Error: "+ str(er), 'red'))
            
    print("red:",red_objetcs)
    print("green:",green_objetcs)
    print("yellow:",yellow_objetcs)

    return red_objetcs, green_objetcs, yellow_objetcs


def getItem():
    red, green, yellow = color_objects_detect.detect_objects(constants.produtcs_camera)
    red_objetcs, green_objetcs, yellow_objetcs = storeProducts()
    diffRed = red-red_objetcs
    diffGreen = green-green_objetcs
    diffYellow = yellow-yellow_objetcs

    if (diffRed>0 or diffRed <0):
        return 1, diffRed
    elif(diffGreen>0 or diffGreen <0):
        return 2, diffGreen
    elif(diffYellow>0 or diffYellow <0):
        return 3, diffYellow

    return None, True
    