shift = 3

def encrypt(text):
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            result += char
    return result

def decrypt(text):
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        else:
            result += char
    return result

message = input("Enter a message: ")

encrypted = encrypt(message)
print(f"Encrypted: {encrypted}")

decrypted = decrypt(encrypted)
print(f"Decrypted: {decrypted}")
