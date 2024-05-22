import random
import string
import banking_app

def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(12))
    return password

def main():
    password = generate_password()
    print("Generated Password:", password)

if __name__ == "__main__":
    main()
