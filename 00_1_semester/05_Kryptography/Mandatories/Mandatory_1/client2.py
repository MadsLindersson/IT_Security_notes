import bcrypt

password = b"client1password"

salt = bcrypt.gensalt(rounds=16)

hashed_password = bcrypt.hashpw(password, salt)

print (hashed_password)
