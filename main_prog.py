import serial
import sqlite3
from termcolor import colored

import api_handler
import entry_gate
#import shooping
import exit_gate

##conect to the local database
conn = sqlite3.connect('store.db')
c = conn.cursor()

def init_db(): 
    try:
        c.execute("CREATE TABLE IF NOT EXISTS products(ID integer PRIMARY KEY, Name  text, typeID integer)")
        c.execute("CREATE TABLE IF NOT EXISTS orders(orderID integer PRIMARY KEY, userID integer)")
        return True
    except sqlite3.Error as er:
        print (colored("SQLite Error: "+ er, 'red'))
    return False

def init_serialCom():
    port = "/dev/ttyACM0"
    baud = 9600
    try:
        ser = serial.Serial(port, baud, timeout=1)
        return True, ser
    except Exception as e:
        print (colored("Serial Error: opening serial port: " + str(e), 'red'))
    
    return False, None

def execute_tasks(message):
    
    if 'enter' in message :
        ...
        user_id, erorr = entry_gate.read_qr()
        if not erorr:
            perm = api_handler.get_perm(user_id)

            if perm == 1:   #full registered
                entry_done = entry_gate.checkFace(user_id)

            else:  #no pics
                erorr = entry_gate.register()
                if not erorr:
                    api_handler.set_perm(user_id)
                    entry_done = entry_gate.checkFace(user_id)
            
            if entry_done:
                try:
                    order_id = api_handler.new_entry(user_id)
                    c.execute("INSERT INTO orders ('userID', 'orderID') Values( "+user_id+" , "+ order_id+" )")
                    conn.commit()                            
                    
                    send_serialData("approve entry") 
                except sqlite3.Error:
                    print (colored("SQLite Error: Inserting orderID", 'red'))
                    send_serialData("refuse entry") 

            else:
                send_serialData("refuse entry") 
        else:
            send_serialData("refuse entry")

    elif 'shop' in message :
        ...
        #  user_id, error = shooping.getUser()

        # if not error:
        #     try:
        #         c.execute("SELECT orderID FROM orders WHERE userID = "+user_id)
        #         order_id=c.fetchone()[0] 

        #         c.execute("SELECT typeID FROM products WHERE ID = "+prod_id)
        #         type_id = c.fetchone()[0]
        #         #api_handler.new_orderline(order_id, type_id, state)

        #         send_serialData("approve shoping")        
        #     except sqlite3.Error as er :
        #         print (colored("SQLite Error: "+ er, 'red'))
        #         send_serialData("refuse shoping")
    
        # else:
        #     send_serialData("refuse shoping")

    elif 'exit' in message :
        ...
        # user_id, error = exit_gate.read_qr()
        # if not erorr:
        #     api_handler.new_exit(user_id)
        #     send_serialData("approve exit")
        # else:
        #     send_serialData("refuse exit")

    else:
        print (colored("Warning: unknown recieved serial data !", 'yellow'))

def send_serialData(message):
    ser.write(bytes(message,'utf-8'))
            
## main programe:
if init_db():
    while(True):
        initalized,ser = init_serialCom()
        if initalized:
            ser.reset_input_buffer()
            message= str(ser.readline())
            print(message)
            if len(message)>5:
                execute_tasks(message)
        else:
            message = input(colored("insert command manually >> ","green"))
            execute_tasks(message)