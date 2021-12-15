import csv
def encrypt_data(password):
    filename = open('chyper-code.csv', 'r')
    file = csv.DictReader(filename)
    User_type = []
    Sys_type=[]
    enc_password=''
    for col in file:
        User_type.append(col['USER TYPE'])
        Sys_type.append(col['SYSTEM CONVERT'])
    for i in password:
        enc_password=enc_password+Sys_type[User_type.index(i)]
    print(enc_password)
def decrypt_data(password):
    filename = open('chyper-code.csv', 'r')
    file = csv.DictReader(filename)
    User_type = []
    Sys_type=[]
    enc_password=''
    for col in file:
        User_type.append(col['USER TYPE'])
        Sys_type.append(col['SYSTEM CONVERT'])
    for i in password:
        enc_password=enc_password+User_type[Sys_type.index(i)]
    print(enc_password)

decrypt_data("DA32")