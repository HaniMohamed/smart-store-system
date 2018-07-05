import serial
import sqlite3
from termcolor import colored

import api_handler
import entry_gate
import shooping
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
        user_id, erorr = entry_gate.read_qr()

        if not erorr:
            perm, error = api_handler.get_perm(user_id)
            print(perm)

            if perm == 1:   #full registered
                entry_done = entry_gate.check_face(user_id)

            elif perm == 0:  #no pics
                input(colored("This user need to register his pics press enter to continue","green"))
                erorr = entry_gate.register(user_id)
                if not erorr:
                    api_handler.set_perm(user_id)
                    entry_done = entry_gate.checkFace(user_id)
            else :
                print (colored("Error happens: This user may not be in database", 'red'))

            print(entry_done)

            if entry_done:
                try:
                    order_id, error = api_handler.new_entry(user_id)
                    c.execute("INSERT INTO orders ('userID', 'orderID') Values( "+user_id+" , "+ str(order_id)+" )")
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
        msg=[x.strip() for x in message.split(',')]
        prod_id = msg[1]
        state = msg[2]
        user_id, error = shooping.getUser()
        if not error:
            print(user_id)
            try:
                c.execute("SELECT orderID FROM orders WHERE userID = "+str(user_id))    
                order_id=c.fetchone()[0] 

                c.execute("SELECT typeID FROM products WHERE ID = "+prod_id)
                type_id = c.fetchone()[0]
                print("sending ",order_id,type_id,state)
                api_handler.new_orderline(order_id, type_id, state)

                send_serialData("approve shoping")        
            except sqlite3.Error as er :
                print (colored("SQLite Error: "+ er, 'red'))
                send_serialData("refuse shoping")
    
        else:
            send_serialData("refuse shoping")

    elif 'exit' in message :
        user_id, error = exit_gate.read_qr()
        if not erorr:
            api_handler.new_exit(user_id)
            send_serialData("approve exit")
        else:
            send_serialData("refuse exit")

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
            message= str(ser.readline(), "utf-8")
            print(message)
            if len(message)>5:
                execute_tasks(message)
        else:
            message = input(colored("insert command manually >> ","green"))
            execute_tasks(message)