key = "CODE"

def vigenere(text, encrypt=True):
    result = ""
    key_index = 0
    for char in text.upper():
        if char.isalpha():
            key_shift = ord(key[key_index % len(key)]) - ord('A')
            if not encrypt:
                key_shift = -key_shift
            result += chr((ord(char) - ord('A') + key_shift) % 26 + ord('A'))
            key_index += 1
        else:
            result += char
    return result

message = input("Enter a message: ")

encrypted = vigenere(message, encrypt=False)
print(f"Encrypted: {encrypted}")

##decrypted = vigenere(encrypted, encrypt=False)
#print(f"Decrypted: {decrypted}")
