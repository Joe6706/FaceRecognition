import os
import getpass

password = 198623
mode = int(input("Mode: ")) #1 for face recognition, 2 for new face

if mode == 1:
    os.system("python Face_Detection.py")    #Run Face_Detection.py
elif mode == 2:
    count = 0

    while count < 3:
        try:
            authorize = int(getpass.getpass("Password: "))   # Use getpass to hide password input
        except ValueError:
            print("Invalid input. Please enter numbers only.")
            count += 1
            continue

        if authorize == password:
            os.system("python Video_Encoding.py")    #Run Video_Encoding.py
            break
        else:
            print("Incorrect")
            count += 1
            
    if count == 3:
        print("Authorization Failed")
        exit(1)
else:
    print("Invalid")
    exit(1)
