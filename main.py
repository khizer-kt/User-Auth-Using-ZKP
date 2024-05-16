# NONCE VALUE
import random
import hashlib
import mysql.connector
import secrets

db = mysql.connector.connect(
    host="localhost",
    user="<username>",
    password="<password>",
    database="<db>"
)
cursor = db.cursor()

def register_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
    print("User Registered")
    db.commit()

def generate_challenge():
    return random.randint(1, 10)

def calculate_proof(challenge, secret, nonce):
    hashed_secret = hashlib.sha256(secret.encode()).hexdigest()
    return hashlib.sha256(str(challenge).encode() + hashed_secret.encode() + str(nonce).encode()).hexdigest()

def verify_proof(challenge, proof, hashed_secret, nonce):
    expected_proof = hashlib.sha256(str(challenge).encode() + hashed_secret.encode() + str(nonce).encode()).hexdigest()
    return proof == expected_proof

def authenticate_user(username, password):
    cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    # print("SELECT password_hash FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result:
        # print(type(result))
        hashed_secret = result[0]
        nonce = secrets.token_hex(16) 
        challenge = generate_challenge()
        proof = calculate_proof(challenge, password, nonce)
        if verify_proof(challenge, proof, hashed_secret, nonce):
            print("User authenticated successfully!")
        else:
            print("Authentication failed. Incorrect password.")
    else:
        print("User not found.")

register_user("abc3", "password123") # reg
authenticate_user("abc3", "password123") # auth

# Attacks:
def sql_injection():
    print("Carrying out SQL Injection")
    username = "abc3"
    password = "' OR '1'='1"
    authenticate_user(username, password)
sql_injection()

def brute_force():
    print("Carrying out Brute-Force Attack")
    for i in range(1,5):
        authenticate_user("abc3", str(i))
brute_force()

def dictionary_attacks():
    print("Carrying out Dictionary Attacks")
    with open('passwords.txt', 'r') as file:
        lines = file.readlines()
    entries = [line.strip() for line in lines]
    for i in entries:
        authenticate_user("abc3", i)
dictionary_attacks()

def replay_attack():
    print("Simulating Replay Attack")
    username = "abc3"
    password = "password123"
    nonce = secrets.token_hex(16)
    challenge = generate_challenge()
    proof = calculate_proof(challenge, password, nonce)

    cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result:
        hashed_secret = result[0]
        # In order to fail the replay attack uncomment the line below
        # nonce = secrets.token_hex(16)
        if verify_proof(challenge, proof, hashed_secret, nonce):
            print("Replay Attack: User authenticated successfully!")
        else:
            print("Replay Attack: Authentication failed. Incorrect proof.")
    else:
        print("Replay Attack: User not found in database.")
replay_attack()


cursor.close()
db.close()