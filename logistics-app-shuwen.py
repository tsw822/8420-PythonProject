import sys
import sqlite3
import time
import datetime
import csv
 
conn = sqlite3.connect('mydb.db')
cursor = conn.cursor()
def encrypt_data(password):         # For encryting and decrypting password
    filename = open('chyper-code.csv', 'r') # file contains the crypt values for all uppercase letters and numbers
    file = csv.DictReader(filename)
    User_type = []
    Sys_type=[]
    enc_password=''
    for col in file:
        User_type.append(col['USER TYPE'])
        Sys_type.append(col['SYSTEM CONVERT'])
    for i in password:
        enc_password=enc_password+Sys_type[User_type.index(i)]
    return(enc_password)

def create_order(curser,user_name): # Order function to get and enter details of customer order
    product=["Table","Xerox machine","Sofa"] # product list contains list of all the products available
    shipment=["Flight","Ship","Truck","Train"] # shipment list contains all the possible shipments available
    departure=["Canada","U.S.A","China","India"] # departure list contains list of all the departure countries available
    destination=["Canada","U.S.A","China","India"] # destination list contains all the possible destination countries available
    print("List of products available are: ")
    i=1
    for p in product:
        print(str(i)+" "+p)
        i=i+1
    while True:
        input_int = input("Enter the product number of the product you want to ship from above: \t")
        if input_int not in ['1','2','3','4']:
            print("please input a valid int")
        else:
            p = int(input_int)
            break
    
    print("List of shipment methods available are:\n1.Flight\n2.Ship\n3.Truck\n4.Train\n")# getting shipment method from the user
    while True:
        input_int = input("Choose the shipment method from above list:\t")
        if input_int not in ['1','2','3','4']:
            print("please input a valid int")
        else:
            s = int(input_int)
            break
    print("List of countries available for picking up from:\n1.Canada\n2.U.S.A\n3.China\n4.India\n")# getting pick up country from the user
    while True:
        input_int = input("Choose the departure country from above list:\t")
        if input_int not in ['1','2','3','4']:
            print("please input a valid int")
        else:
            f = int(input_int)
            break
    print("List of available desitination countries:\n1.Canada\n2.U.S.A\n3.China\n4.India\n")# getting destination country from the user
    while True:
        input_int = input("Choose the desitination country from above list:\t")
        if input_int not in ['1','2','3','4']:
            print("please input a valid int")
        else:
            t = int(input_int)
            break
    while True:
        input_int = input(f"Enter how many days from now on the shipment should take place (Max 10 days):\nTodays date: {datetime.date.today()}\t")
        if input_int not in ['0','1','2','3','4','5','6','7','8','9','10']:
            print("please input a int value")
        else:
            d = int(input_int)
            break
    shipdate=datetime.date.today()
    shipdate=shipdate+datetime.timedelta(days=d)
    print(f"Your order will be shipped on : {shipdate}")
    cursor.execute("insert into order_db (User_Name,Product,Shipment,Pick_from,Destination,Ship_date,Created_at) values (?, ?, ?, ?, ?, ?, ?)",
            (user_name, product[p-1],shipment[s-1],departure[f-1],destination[t-1],shipdate,datetime.date.today() ))
    conn.commit()
    print("Order entered succesfully!!\n")
    
def show_order(user_name):
    print("List of all orders:\n")
    cursor.execute('''SELECT * from order_db WHERE User_Name=?;''',(user_name,))
    records = cursor.fetchall()
    print(records)

def check_username(user_name):
    cursor.execute('''SELECT User_Name from User_db Where User_Name= ?;''',(user_name,))
    records = cursor.fetchall()
    if len(records)>0:
        print('the user %s has been in the db, please use a new name'%user_name)
        return main()

def check_exist_username(user_name):
    cursor.execute('''SELECT User_Name from User_db Where User_Name= ?;''',(user_name,))
    records = cursor.fetchall()
    if len(records)==0:
        print('the user %s is not in the db, please enter the correct user name'%user_name)
        return main()
    else:
        return user_name

def check_pw_letter():
    while True:
        message=input("enter your password\n")
        err_no = 0
        for i in message:
            if i not in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"):
                err_no+=1
        if err_no!=0:
            print(err_no)
            print('your must use Captal Letter and Number only')
        else:
            break
    return message
    
def order_or_exit_logic(user_name):
    head=True
    while(head==True):
        create_order(cursor,user_name)
        show_order(user_name)
        while True:
            input_int = input("To exit press 0 \t to continue press 1\n")
            if input_int not in ['0','1']:
                print("please input 0 or 1")
            else:
                input_exit = int(input_int)
                break
        if input_exit == 0:
            head= False
            sys.exit("Exit Successfully!")

def main():
    #cursor.execute("DROP TABLE User_db;")
    cursor.execute('''CREATE TABLE IF NOT EXISTS User_db (User_id integer PRIMARY KEY,User_Name text NOT NULL,Password text NOT NULL,Count integer NOT NULL);''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS order_db (order_id integer PRIMARY KEY,User_Name text NOT NULL,Product text NOT NULL,Shipment text NOT NULL,Pick_from text NOT NULL,Destination text NOT NULL,Ship_date date NOT NULL,Created_at date NOT NULL);''')
    cursor.execute('''SELECT * from User_db;''')
    records = cursor.fetchall()
    print(records)
    while True:
        input_sel = input("If you are a new user enter 'Y'.If not enter 'N'\n")
        if input_sel not in ['Y','N','y','n']:
            print("please input a valid selection Y or N")
        else:
            log_sel = input_sel
            break
    if(log_sel=='Y' or log_sel=='y'):
        user_name=input("Enter your user name\n")
        check_username(user_name)
        message = check_pw_letter()
        count=0
        encMessage = encrypt_data(message)
        cursor.execute("insert into User_db (User_Name,Password,Count) values (?, ?, ?)",
                (user_name, encMessage,count ))
        conn.commit()
        print("user account created successfully!!")

        order_or_exit_logic(user_name)


    else:
        user_name=check_exist_username(input("Enter your user name\n"))
        message=check_pw_letter()
        message=encrypt_data(message)
        cursor.execute('''SELECT Password from User_db WHERE User_Name= ?;''',(user_name,))
        check_message = cursor.fetchone()[0]
        if  message == check_message:
            cursor.execute('''UPDATE User_db SET Count = Count+1 WHERE  User_Name= ? and Password=?;''',(user_name,message))
            conn.commit()
            print("Updated count")
            with open("Logdata.txt", "a") as file:
                cursor.execute('''SELECT User_id,Password,Count from User_db WHERE User_Name=?  and Password=?;''',(user_name,message))
                records = cursor.fetchall()
                for item in records:
                    print(item)
                file.write(f'{user_name},{message},{records[0][2]+1},{datetime.datetime.now()}\n')
                print("user table backup completed")
                
            order_or_exit_logic(user_name)

        else:
            print("Please input the right password")
            main()
        

if __name__ == '__main__':
    main()