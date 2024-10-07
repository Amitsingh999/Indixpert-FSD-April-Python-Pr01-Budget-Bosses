import json
import os
from SRC.inventory_management import InventoryManagementSystem
from SRC.utils import input_password

user_path = 'data/user.json'

def load_users():
    if os.path.exists(user_path):
        with open(user_path, 'r') as file:
            return json.load(file)
    return []

def save_users(users_data):
    os.makedirs(os.path.dirname(user_path), exist_ok=True)
    with open(user_path, 'w') as file:
        json.dump(users_data, file, indent=2)

def sign_up():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("* [USER_SIGN_UP_NEW_ACCOUNT] *")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    existing_users = load_users()

    admin_exists = any(user.get('is_admin', False) for user in existing_users)

    if len(existing_users) >= 4:
        print("Already four users have access. Cannot sign up more users.\n")
        return

    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    username = input("Enter username: ")
    
    if any(user['username'] == username for user in existing_users):
        print("Username already exists. Please choose a different username.")
        return

    password = input_password()

    is_admin = False
    if not admin_exists:
        is_admin = input("Should this user be an admin? (yes/no): ").strip().lower() == "yes"

    if is_admin and admin_exists:
        print("Only one admin user can be created. This user will be a regular user.")
        is_admin = False

    user_data = {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "password": password,
        "is_admin": is_admin
    }
    
    existing_users.append(user_data)

    save_users(existing_users)
    print("User Signed Up Successfully!")

def login():
    print("[Login Your Account] \n")
    users_data = load_users()
    
    if users_data:
        username = input("Enter username: ")
        password = input("Enter password: ")

        if any(u['username'] == username and u['password'] == password for u in users_data):
            print("User Login Successful!")
            return username
        print("Invalid username or password.")
        print("Account is not available here please sign up first")
    else:
        print("No users available. Please sign up first.")
    return False

def admin_login():
    print(" [Admin Login] \n")
    username = input("Enter Admin Username: ")
    password = input("Enter Admin Password: ")
    

    if any(u['username'] == username and u['password'] == password and u.get('is_admin', False) for u in load_users()):
        print("Admin Login Successful!")
        return True
    else:
        print("Invalid admin username or password.")
    return False

def delete_user_data():
    users_data = load_users()
    if users_data:
        print("Current Users:")
        for idx, user in enumerate(users_data, start=1):
            print(f"{idx}. {user['username']}")

        try:
            user_idx = int(input("Enter the number of the user to delete: ")) - 1
            
            if 0 <= user_idx < len(users_data):
                confirmation = input(f"Are you sure you want to delete user '{users_data[user_idx]['username']}'? (yes/no): ")
                if confirmation.lower() == 'yes':
                    deleted_user = users_data.pop(user_idx)
                    save_users(users_data)
                    print(f"User '{deleted_user['username']}' deleted successfully.")
                else: 
                    print("User deletion canceled.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
    else:
        print("No users available to delete.")

def update_user_data():
    users_data = load_users()
    if users_data:
        print("Current Users:")
        for idx, user in enumerate(users_data, start=1):
            print(f"{idx}. {user['username']}")

        try:
            user_idx = int(input("Enter the number of the user to change: ")) - 1
            
            if 0 <= user_idx < len(users_data):
                user_to_edit = users_data[user_idx]
                print(f"Editing user: {user_to_edit['username']}")

                attribute = input("Which attribute do you want to change? (first_name, last_name, username, password): ")
               
                if attribute in user_to_edit:
                    if attribute == "password":
                        new_value = input_password()  
                    else:
                        new_value = input(f"Enter new value for {attribute}: ")
                    
                    user_to_edit[attribute] = new_value 
                    save_users(users_data)  
                    print(f"User '{user_to_edit['username']}' updated successfully.")
                else:
                    print("Invalid attribute.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
    else:
        print("No users available to change.")



def login_user_data():
    users_data = load_users()
    if not users_data:
        print("No users available.")
        return

    print("Current Users:")
    for idx, user in enumerate(users_data, start=1):
        print(f"{idx}. {user['username']}")

    try:
        user_idx = int(input("Enter the number of the user to view options: ")) - 1

        if 0 <= user_idx < len(users_data):
            selected_user = users_data[user_idx]
            print(f"Selected User: {selected_user['username']}")
            inventory_system = InventoryManagementSystem(selected_user['username'])
            user_menu(inventory_system)
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

def display_user_data():
    users_data = load_users()
    if users_data:
        print("Current Users:")
        for idx, user in enumerate(users_data, start=1):
            admin_status = " (Admin)" if user.get('is_admin', False) else ""
            print(f"{idx}. {user['username']}{admin_status}")
    else:
        print("No users available.")


def check_all_product_with_who_enter():
    users_data = load_users()
    products_summary = {}
    
    for user in users_data:
        username = user['username']
        inventory = InventoryManagementSystem(username)
        for product in inventory.products.values():
            if username not in products_summary:
                products_summary[username] = []
            products_summary[username].append(product)

    if products_summary:
        print("\nSummary of Products Added by Each User:")
        for user, products in products_summary.items():
            total_products = len(products)
            print(f"\n{user} has added {total_products} product(s):")
            for product in products:
                print(f"- {product.name} (ID: {product.product_id}) - Price: {product.price}, Stock: {product.quantity}")
    else:
        print("No products found for any user.")

        
def replace_admin():
    users_data = load_users()
    if not users_data:
        print("No users available to replace admin.")
        return
    
    print("Current Users:")
    for idx, user in enumerate(users_data, start=1):
        print(f"{idx}. {user['username']} (Admin: {user.get('is_admin', False)})")

    try:
        user_idx = int(input("Enter the number of the user to promote to admin: ")) - 1
        
        if 0 <= user_idx < len(users_data):
            new_admin = users_data[user_idx]
            if new_admin.get('is_admin', False):
                print("This user is already an admin.")
                return
            
            current_admin = next((u for u in users_data if u.get('is_admin', False)), None)
            if current_admin:
                current_admin['is_admin'] = False  
            new_admin['is_admin'] = True  
            save_users(users_data)  
            
            print(f"User '{new_admin['username']}' has been promoted to admin.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

def admin_menu():
    while True:
        print("\n~~~~~~~~~~~~~~~~")
        print("* [Admin Menu] *")
        print("~~~~~~~~~~~~~~~~")
        print("1. Delete User Data")
        print("2. Update User Data")
        print("3. Login User Data")
        print("4. Display User Data")
        print("5. Checking All Product")
        print("6. Replace Admin")
        print("7. Exit Admin Menu\n")  
        choice = input("Enter your choice: ")

        if choice == "1":
            delete_user_data()
        elif choice == "2":
            update_user_data()
        elif choice == "3":
            login_user_data()
        elif choice == "4":
            display_user_data()
        elif choice == "5":
           check_all_product_with_who_enter()
        elif choice == "6":
            replace_admin()
        elif choice == "7":  
            print("Exiting Admin Menu.")
            break
        else:
            print("Invalid choice. Please try again.")

def run_inventory_system():
    while True:
        print("~~~~~~~~~~~~~~~~~~~~")
        print("*  [Welcome_User]  *")
        print("~~~~~~~~~~~~~~~~~~~~")
        print("\n1. Sign Up ")
        print("2. Login ")
        print("3. Admin Menu")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            sign_up()
            if (login_status := login()):
                initialize_user_products(login_status)
                inventory_system = InventoryManagementSystem(login_status)
                user_menu(inventory_system)
        elif choice == "2":
            if (login_status := login()):
                initialize_user_products(login_status)
                inventory_system = InventoryManagementSystem(login_status)
                user_menu(inventory_system)
        elif choice == "3":
            if admin_login():  
                admin_menu()  
        elif choice == "4":
            print("Exiting the system. Goodbye!")
            return
        else:
            print("Invalid choice. Please try again.")

def display_menu():
    print("\n*****************************")
    print("* [PROJECT_PRODUCT:SYSTEM] *")
    print("****************************")
    print("\n1. Add Product")
    print("2. Update Stock")
    print("3. Check Stock")
    print("4. Delete Product")
    print("5. Display Inventory")
    print("6. Search Product")  
    print("7. Logout")  
    print("\n*************")
    print("* [Thanks] *")
    print("*************\n")

def initialize_user_products(username):
    user_file = f'data/products/products.{username}.json'
    os.makedirs(os.path.dirname(user_file), exist_ok=True)
    if not os.path.exists(user_file):
        with open(user_file, 'w') as file:
            json.dump([], file)

def user_menu(inventory_system):
    while True:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("* [Do You Want To See The Menu Options?] *")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        confirm_menu = input("(yes/no): ")

        if confirm_menu.lower() == 'yes':
            display_menu()
        elif confirm_menu.lower() == 'no':
            print("Continuing without showing the menu.")
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")
            continue 

        choice = input("Please choose an option (1-7): ")
        if choice == '1':
            inventory_system.add_product(input("Enter product name: "), input("Enter product price: "), input("Enter product quantity: "))
        elif choice == '2':
            inventory_system.update_stock(input("Enter product name to update stock: "))
        elif choice == '3':
            inventory_system.check_stock(input("Enter product name to check stock: "))
        elif choice == '4':
            inventory_system.delete_product(input("Enter product name to delete: "))
        elif choice == '5':
            inventory_system.display_inventory()
        elif choice == '6':
            inventory_system.search_product()    
        elif choice == '7':
            if input("Are you sure you want to log out? (yes/no): ").lower() == 'yes':
                print("Logging out...")
                break

run_inventory_system()