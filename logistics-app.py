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

def order(curser,user_name): # Order function to get and enter details of customer order
    product=["table","xerox machine","sofa"] # product list contains list of all the products available
    shipment=["flight","ship","truck","train"] # shipment list contains all the possible shipments available
    print("List of products available are: ")
    i=1
    for p in product:
        print(str(i)+" "+p)
        i=i+1
    p= int(input("Enter the product number of the product you want to ship from above: "))# getting product from customer
    print("List of shipment methods available are:\n1.Flight\n2.ship\n3.truck\n4.Train\n")# getting shipment method from the user
    s=int(input("Choose the shipment method from above list:\t"))
    f=input("Enter the country it should be picked up from:\n")
    t=input("Enter the destination country:\n")
    d=int(input(f"Enter how many days from now on the shipment should take place:\nTodays date: {datetime.date.today()}\t"))
    shipdate=datetime.date.today()
    shipdate=shipdate+datetime.timedelta(days=d)
    print(f"Your order will be shipped on : {shipdate}")
    cursor.execute("insert into order_db (User_Name,Product,Shipment,Pick_from,Destination,Ship_date,Created_at) values (?, ?, ?, ?, ?, ?, ?)",
            (user_name, product[p-1],shipment[s-1],f,t,shipdate,datetime.date.today() ))
    conn.commit()
    print("Order entered succesfully!!\n")
#cursor.execute("DROP TABLE User_db;")
cursor.execute('''CREATE TABLE IF NOT EXISTS User_db (User_id integer PRIMARY KEY,User_Name text NOT NULL,Password text NOT NULL,Count integer NOT NULL);''')
cursor.execute('''CREATE TABLE IF NOT EXISTS order_db (order_id integer PRIMARY KEY,User_Name text NOT NULL,Product text NOT NULL,Shipment text NOT NULL,Pick_from text NOT NULL,Destination text NOT NULL,Ship_date date NOT NULL,Created_at date NOT NULL);''')
cursor.execute('''SELECT * from User_db;''')
records = cursor.fetchall()
print(records)
log_del=input("If you are a new user enter 'Y'.If not enter 'N'\n")
if(log_del=='Y'):
   user_name=input("Enter your user name\n")
   message=input("enter your password\n")
   count=0
   encMessage = encrypt_data(message)
   cursor.execute("insert into User_db (User_Name,Password,Count) values (?, ?, ?)",
            (user_name, encMessage,count ))
   conn.commit()
   print("user account created successfully!!")
   head=True
   while(head==True):
       order(cursor,user_name)
       if(int(input("To exit press 0 \t to continue press 1\n"))==0):
           head= False
       print("List of all orders:\n")
       cursor.execute('''SELECT * from order_db WHERE User_Name=?;''',(user_name,))
       records = cursor.fetchall()
       print(records)

else:
   user_name=input("Enter your user name\n")
   message=input("enter your password\n")
   message=encrypt_data(message)
   cursor.execute('''UPDATE User_db SET Count = Count+1 WHERE  User_Name= ? and Password=?;''',(user_name,message))
   conn.commit()
   print("Updated count")
   file = open("Logdata.txt", "a") 
   cursor.execute('''SELECT User_id,Password,Count from User_db WHERE User_Name=?  and Password=?;''',(user_name,message))
   records = cursor.fetchall()
   file.write(f'{user_name},{message},{records[0][2]+1},{datetime.datetime.now()}\n')
   head=True
   while(head==True):
       order(cursor,user_name)
       if(int(input("To exit press 0 \t to continue press 1\n"))==0):
           head= False
       print("List of all orders:\n")
       cursor.execute('''SELECT * from order_db WHERE User_Name=?;''',(user_name,))
       records = cursor.fetchall()
       print(records)



    
    
