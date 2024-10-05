def input_password():
    while True:
        password = input("Enter password (exactly 7 characters, including letters and numbers): ")
        if len(password) == 7 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password):
            return password
        print("Invalid password. Please ensure it is exactly 7 characters long, including letters and numbers.")
