import json
import os

# JSON file paths
PRODUCTS_FILE = "products.json"
DELIVERIES_FILE = "deliveries.json"

def initialize_files():
    """Create JSON files if they don't exist"""
    if not os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'w') as f:
            json.dump([], f)
    if not os.path.exists(DELIVERIES_FILE):
        with open(DELIVERIES_FILE, 'w') as f:
            json.dump([], f)

def load_data(filename):
    """Load data from JSON file"""
    with open(filename, 'r') as f:
        return json.load(f)

def save_data(filename, data):
    """Save data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def display_menu(menu, min_choice, max_choice):
    """Display menu and validate input"""
    print(menu)
    while True:
        choice = input(f"Enter your choice ({min_choice}-{max_choice}): ")
        if choice.isdigit() and min_choice <= int(choice) <= max_choice:
            return choice
        print(f"Invalid choice! Please enter {min_choice}-{max_choice}.")

def exit_program():
    """Exit the program gracefully"""
    print("\nExiting program. Goodbye!")
    exit()

# ===== PRODUCT MANAGEMENT FUNCTIONS =====
def product_stocks_menu():
    while True:
        choice = display_menu(product_stocks, 1, 4)
        if choice == "1":
            display_all_products()
        elif choice == "2":
            products_by_menu()
        elif choice == "3":
            break  # Go back
        elif choice == "4":
            exit_program()

def products_by_menu():
    while True:
        choice = display_menu(products_by, 1, 5)
        if choice == "1":
            search_products("name")
        elif choice == "2":
            search_products("category")
        elif choice == "3":
            search_products("code")
        elif choice == "4":
            break  # Go back
        elif choice == "5":
            exit_program()

def display_all_products():
    products = load_data(PRODUCTS_FILE)
    if not products:
        print("\nNo products found!\n")
        return
    
    print("\n=== ALL PRODUCTS ===")
    for idx, product in enumerate(products, 1):
        print(f"{idx}. {product['name']} (Code: {product['code']})")
        print(f"   Category: {product['category']}")
        print(f"   Stock: {product['stock']}")
        print(f"   Price: ${product['price']:.2f}\n")

def search_products(search_by):
    products = load_data(PRODUCTS_FILE)
    if not products:
        print("\nNo products found!\n")
        return
    
    search_term = input(f"Enter {search_by} to search: ").lower()
    found = [p for p in products if search_term in str(p[search_by]).lower()]
    
    if not found:
        print("\nNo matching products found!\n")
        return
    
    print(f"\n=== PRODUCTS MATCHING '{search_term}' ===")
    for product in found:
        print(f"Name: {product['name']}")
        print(f"Code: {product['code']}")
        print(f"Category: {product['category']}")
        print(f"Stock: {product['stock']}")
        print(f"Price: ${product['price']:.2f}\n")

# ===== DELIVERY MANAGEMENT FUNCTIONS =====
def delivery_edits_menu():
    while True:
        choice = display_menu(delivery_edits, 1, 4)
        if choice == "1":
            edit_delivery()
        elif choice == "2":
            erase_delivery()
        elif choice == "3":
            break  # Go back
        elif choice == "4":
            exit_program()

def create_delivery():
    deliveries = load_data(DELIVERIES_FILE)
    products = load_data(PRODUCTS_FILE)
    
    if not products:
        print("\nNo products available to deliver!\n")
        return
    
    display_all_products()
    try:
        product_code = input("Enter product code to deliver: ")
        quantity = int(input("Enter quantity: "))
        
        product = next((p for p in products if p['code'] == product_code), None)
        if not product:
            print("\nProduct not found!\n")
            return
            
        if product['stock'] < quantity:
            print("\nNot enough stock available!\n")
            return
            
        # Update product stock
        product['stock'] -= quantity
        save_data(PRODUCTS_FILE, products)
        
        # Create delivery
        new_delivery = {
            "id": len(deliveries) + 1,
            "product_code": product_code,
            "product_name": product['name'],
            "quantity": quantity,
            "status": "Pending"
        }
        deliveries.append(new_delivery)
        save_data(DELIVERIES_FILE, deliveries)
        
        print("\nDelivery created successfully!\n")
    except ValueError:
        print("\nInvalid input! Please enter valid data.\n")

def edit_delivery():
    deliveries = load_data(DELIVERIES_FILE)
    if not deliveries:
        print("\nNo deliveries found!\n")
        return
    
    display_deliveries()
    try:
        delivery_id = int(input("Enter delivery ID to edit: "))
        delivery = next((d for d in deliveries if d['id'] == delivery_id), None)
        if not delivery:
            print("\nDelivery not found!\n")
            return
            
        new_status = input("Enter new status (Pending/Shipped/Delivered): ").capitalize()
        if new_status not in ["Pending", "Shipped", "Delivered"]:
            print("\nInvalid status!\n")
            return
            
        delivery['status'] = new_status
        save_data(DELIVERIES_FILE, deliveries)
        print("\nDelivery updated successfully!\n")
    except ValueError:
        print("\nInvalid input! Please enter a number.\n")

def erase_delivery():
    deliveries = load_data(DELIVERIES_FILE)
    if not deliveries:
        print("\nNo deliveries found!\n")
        return
    
    display_deliveries()
    try:
        delivery_id = int(input("Enter delivery ID to delete: "))
        delivery = next((d for d in deliveries if d['id'] == delivery_id), None)
        if not delivery:
            print("\nDelivery not found!\n")
            return
            
        # Restore product stock if delivery is deleted
        if delivery['status'] == "Pending":
            products = load_data(PRODUCTS_FILE)
            product = next((p for p in products if p['code'] == delivery['product_code']), None)
            if product:
                product['stock'] += delivery['quantity']
                save_data(PRODUCTS_FILE, products)
        
        deliveries.remove(delivery)
        save_data(DELIVERIES_FILE, deliveries)
        print("\nDelivery deleted successfully!\n")
    except ValueError:
        print("\nInvalid input! Please enter a number.\n")

def display_deliveries():
    deliveries = load_data(DELIVERIES_FILE)
    if not deliveries:
        print("\nNo deliveries found!\n")
        return
    
    print("\n=== CURRENT DELIVERIES ===")
    for delivery in deliveries:
        print(f"ID: {delivery['id']}")
        print(f"Product: {delivery['product_name']} (Code: {delivery['product_code']})")
        print(f"Quantity: {delivery['quantity']}")
        print(f"Status: {delivery['status']}\n")

# ===== MAIN MENU FUNCTIONS =====
def product_management_menu():
    while True:
        choice = display_menu(product_management, 1, 4)
        if choice == "1":
            product_stocks_menu()
        elif choice == "2":
            search_term = input("Enter product name to search: ")
            search_products("name")
        elif choice == "3":
            break  # Go back
        elif choice == "4":
            exit_program()

def delivery_management_menu():
    while True:
        choice = display_menu(delivery_management, 1, 5)
        if choice == "1":
            create_delivery()
        elif choice == "2":
            delivery_edits_menu()
        elif choice == "3":
            display_deliveries()
        elif choice == "4":
            break  # Go back
        elif choice == "5":
            exit_program()

# ===== MENU DEFINITIONS =====
main_menu = """******************************
Enter the desired option:
1. Product Management
2. Delivery Management
3. Quit
******************************"""

product_management = """******************************
Enter the desired option:
1. Products Stock
2. Search Product
3. Go Back
4. Quit
******************************"""

delivery_management = """******************************
Enter the desired option:
1. Create Delivery
2. Edit or Erase Delivery
3. See Current Deliveries
4. Go Back
5. Quit
******************************"""

product_stocks = """******************************
Enter desired option:
1. See Products
2. Search Products by Name, Category or Code
3. Go Back
4. Quit
******************************"""

products_by = """******************************
Enter desired option:
1. Name
2. Category
3. Code
4. Go Back
5. Quit
******************************"""

delivery_edits = """******************************
Enter desired option:
1. Edit Delivery
2. Erase Delivery
3. Go Back
4. Quit
******************************"""

# ===== INITIALIZATION =====
def initialize_sample_data():
    """Create sample data if files are empty"""
    products = load_data(PRODUCTS_FILE)
    if not products:
        sample_products = [
            {"name": "Laptop", "code": "LP100", "category": "Electronics", "stock": 50, "price": 999.99},
            {"name": "Smartphone", "code": "SP200", "category": "Electronics", "stock": 100, "price": 699.99},
            {"name": "Desk Chair", "code": "DC300", "category": "Furniture", "stock": 30, "price": 149.99}
        ]
        save_data(PRODUCTS_FILE, sample_products)

    deliveries = load_data(DELIVERIES_FILE)
    if not deliveries:
        sample_deliveries = [
            {"id": 1, "product_code": "LP100", "product_name": "Laptop", "quantity": 5, "status": "Pending"},
            {"id": 2, "product_code": "SP200", "product_name": "Smartphone", "quantity": 10, "status": "Shipped"}
        ]
        save_data(DELIVERIES_FILE, sample_deliveries)

# ===== MAIN PROGRAM =====
if __name__ == "__main__":
    initialize_files()
    initialize_sample_data()
    
    print("\nWelcome to the Management System!\n")
    while True:
        choice = display_menu(main_menu, 1, 3)
        if choice == "1":
            product_management_menu()
        elif choice == "2":
            delivery_management_menu()
        elif choice == "3":
            exit_program()