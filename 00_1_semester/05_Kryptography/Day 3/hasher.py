import bcrypt

username = input("Write username: ")
password = input("Write password: ")

pass_bytes = password.encode("utf-8")

salt = bcrypt.gensalt(rounds=15)

hashed_password = bcrypt.hashpw(pass_bytes, salt)

print(hashed_password)

with open("passwords.txt", "a") as file:
    lines = file.readlines()

    for line in lines:
        

