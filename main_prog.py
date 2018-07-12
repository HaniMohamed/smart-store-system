import serial
import sqlite3
from termcolor import colored
from multiprocessing import Process
import time


import constants
import api_handler
import entry_gate
import shooping
import exit_gate

##conect to the local database
conn = sqlite3.connect('store.db')
c = conn.cursor()

def init_db(): 
    try:
        c.execute("CREATE TABLE IF NOT EXISTS products(ID integer PRIMARY KEY, Name  text, typeID integer, color text)")
        c.execute("CREATE TABLE IF NOT EXISTS orders(orderID integer PRIMARY KEY, userID integer, checkedOut integer)")
        return True
    except sqlite3.Error as er:
        print (colored("SQLite Error: "+ er, 'red'))
    return False

def init_serialCom():
    port = constants.arduino_port
    baud = 9600
    try:
        ser = serial.Serial(port, baud, timeout=1)
        return True, ser
    except Exception as e:
        print (colored("Serial Error: opening serial port: " + str(e), 'red'))
    
    return False, None

def send_serialData(message):
    ser.write(bytes(message,'utf-8'))    
   
def gate():
    user_id, erorr = entry_gate.read_qr()
    print(user_id)
    if not erorr:
        try:
            c.execute("SELECT userID FROM orders WHERE checkedOut = 0")    
            row = c.fetchone()            
            if(row is not None and int(user_id) in row):
                try:
                    c.execute("SELECT orderID FROM orders WHERE checkedOut = 0 AND userID = "+ str(user_id)) 
                    order_id=c.fetchone()[0]
                    print(order_id)
                    print (colored("Checking out please wait ...", 'blue'))
                    if(not api_handler.new_exit(order_id)):
                        print(colored("Thank your for visiting us, Have a good day :)", 'green'))
                        c.execute("UPDATE orders SET checkedOut = 1 WHERE orderID = "+str(order_id))
                        conn.commit() 
                    else:
                        print(colored("Error in Checking out, please check your app for more details", 'red'))

                except sqlite3.Error as er :
                    print (colored("SQLite Error: "+ str(er), 'red'))
                    send_serialData("refuse shoping")
            else:
                print(colored("Welcome, "+user_id,"green"))
                print(colored("Getting profile from server ... ","blue"))
                perm, error = api_handler.get_perm(user_id)

                if perm == 1:   #full registered
                    print(colored("Checking face, please keep your face in front of the camera ","green"))
                    entry_done = entry_gate.check_face(user_id)

                elif perm == 0:  #no pics
                    input(colored("This user need to register his pics press ENTER to continue","blue"))
                    erorr = entry_gate.register(user_id)
                    if not erorr:
                        api_handler.set_perm(user_id)
                        entry_done = entry_gate.check_face(user_id)
                else :
                    print (colored("Error happens: This user may not be in database", 'red'))



                if entry_done:
                    try:
                        order_id, error = api_handler.new_entry(user_id)
                        c.execute("INSERT INTO orders ('userID', 'orderID','checkedOut') Values( "+user_id+" , "+ str(order_id)+" , 0 )")
                        conn.commit() 
                        print(colored("Authenticating complete, enjoy shoping :)","green"))
                           
                        
                        send_serialData("approve entry") 
                    except sqlite3.Error:
                        print (colored("SQLite Error: Inserting orderID", 'red'))
                        send_serialData("refuse entry") 

                else:
                    send_serialData("refuse entry") 
           
        except sqlite3.Error as er :
                print (colored("SQLite Error: "+ str(er), 'red'))

    else:
                send_serialData("refuse entry")

def shop():
    msg=[x.strip() for x in message.split(',')]
    prod_id = msg[1]
    state = msg[2]
    user_id, error = shooping.getUser()
    if not error:
        print(user_id)
        try:
            c.execute("SELECT orderID FROM orders WHERE userID = "+str(user_id)+" AND  checkedOut = 0 ")    
            order_id=c.fetchone()[0] 

            c.execute("SELECT typeID FROM products WHERE ID = "+prod_id)
            type_id = c.fetchone()[0]
            print("sending ",order_id,type_id,state)
            api_handler.new_orderline(order_id, type_id, state)

            send_serialData("approve shoping")        
        except sqlite3.Error as er :
            print (colored("SQLite Error: "+ str(er), 'red'))
            send_serialData("refuse shoping")

    else:
        send_serialData("refuse shoping")

def tessst():
    user_id = 24
    c.execute("SELECT userID FROM orders WHERE checkedOut = 0")    
    row = c.fetchone()            
    if(row is not None and user_id in row):
        try:
            c.execute("SELECT orderID FROM orders WHERE checkedOut = 0 AND userID = "+ str(user_id)) 
            order_id=c.fetchone()[0]
            print(order_id)
            print (colored("Checking out please wait ...", 'blue'))
            if(not api_handler.new_exit(order_id)):
                print(colored("Thank your for visiting us, Have a good day :)", 'green'))
            c.execute("UPDATE orders SET checkedOut = 1 WHERE orderID = "+str(order_id))
            conn.commit() 

        except sqlite3.Error as er :
            print (colored("SQLite Error: "+ str(er), 'red'))
            send_serialData("refuse shoping")
    else:
        print(colored("Welcome, "+str(user_id),"green"))


    
## main programe:
if init_db():
    while(True):
        initalized,ser = init_serialCom()
        if initalized:
            ser.reset_input_buffer()
            message= str(ser.readline(), "utf-8")
            if len(message)>5:
                print(message)
                if 'gate' in message :
                    #gate()
                    p1 = Process(target=gate)
                    p1.start()

                elif 'shop' in message :
                    p2 = Process(target=shop)
                    p2.start()
                

                else:
                    print (colored("Warning: unknown recieved serial data !", 'yellow'))

        else:
            message = input(colored("insert command manually >> ","green"))
            if len(message)>2:
                print(message)
                if 'gate' in message :
                    #gate()
                    p1 = Process(target=gate)
                    p1.start()

                elif 'shop' in message :
                    p2 = Process(target=shop)
                    p2.start()
                
                elif 'test' in message:
                    p3 = Process(target=storeProducts)
                    p3.start()

                else:
                    print (colored("Warning: unknown recieved serial data !", 'yellow'))



