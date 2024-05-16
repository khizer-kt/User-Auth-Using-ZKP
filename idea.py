import random
import hashlib

secret = "1234"
hashed_secret = hashlib.sha256(secret.encode()).hexdigest()

challenge = random.randint(1, 10)
print("Challenge:", challenge)

expected_response = hashlib.sha256(str(challenge).encode() + hashed_secret.encode()).hexdigest()

def verify(expected_response, response):
    return response == expected_response

def calculate_response(challenge, secret):
    hashed_secret = hashlib.sha256(secret.encode()).hexdigest()
    return hashlib.sha256(str(challenge).encode() + hashed_secret.encode()).hexdigest()

ask_key = input("Enter Key: ")

response = calculate_response(challenge, ask_key)

if verify(expected_response, response):
    print("Key was known")
else:
    print("Key was not known")
