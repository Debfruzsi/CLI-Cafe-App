from sql_queries import *

# Order status global
order_statuses = ["Preparing", "Delivery", "Completed"]

#Menu functions
def print_main_menu():
    print("\nMain Menu Options:")
    menu_options = ["Exit", "Products Menu", "Couriers Menu", "Orders Menu", "Customers Menu"]
    print_numbering(menu_options, 0)

def print_numbering(my_list, start_id):
    for idx, item in enumerate(my_list, start=start_id):
        print(f"{idx}. {item}")

def print_product_menu():
    print("\nProduct Menu Options:")
    menu_options = ["Return to Main Menu", "View Products List", "Add New Product", "Update a Product", "Delete a Product"]
    print_numbering(menu_options, 0)

def print_courier_menu():
    print("\nCourier Menu Options:")
    menu_options = ["Return to Main Menu", "View Couriers List", "Add New Courier", "Update a Courier", "Delete a Courier"]
    print_numbering(menu_options, 0)

def print_orders_menu():
    print("\nOrder Menu Options:")
    menu_options = ["Return to Main Menu", "View all orders", "Add New Order", "Update Order Status", "Update Order Details", "Delete an Order"]
    print_numbering(menu_options, 0)

def print_customer_menu():
    print("\nCustomer Menu Options:")
    menu_options = ["Return to Main Menu", "View Customers List", "Add New Customer", "Update a Customer", "Delete a Customer"]
    print_numbering(menu_options, 0)

# Helper functions
def display_order_statuses():
    print_numbering(order_statuses, 1)

def display_order_sort():
    print_numbering(["Status", "Courier"], 1)

def print_from_sql_read(field_names, results):
    field_names = ",\t".join(field_names)
    print(field_names)
    for result in results:
        result_str = [str(x) for x in result]
        print(",\t".join(result_str))

def valid_index_selection(display_function, user_prompt, valid_ids, offset=0, accept_empty=False):
    while True:
        display_function()
        index = input(user_prompt)
        print()
        if accept_empty and not index:
            return index
        
        try:
            index_int = int(index) - offset
            if not index_int in valid_ids:
                print("Invalid index!")
            else:
                break
        except:
            print("Invalid index! Not an integer.")
    return index_int

#Using SQL to fetch all ID from a table
def get_valid_ids(table_name):
    sql_read_results = sql_read(table_name, ["ID"])
    id_list = [x[0] for x in sql_read_results]
    return id_list

def get_input(user_prompt, error_message, type_cast=None):
    while True:
        try:
            response = input(user_prompt)
            if type_cast:
                response = type_cast(response)
            return response
        except:
            print(error_message)

#Product management functions
def display_products():
    print("\nProducts List:")
    # SQL Read
    sql_read_results = sql_read("Products", ["*"])
    print_from_sql_read(["ID", "Name", "Price", "Stock"], sql_read_results)

def add_product():
    product_name = input("Enter the name of the new product: ")
    product_price = get_input("Enter the price of the product: ", "Invalid Price. Try again.", float)
    available_stock = get_input("Enter the amount of available stock of the product: ", "Not an integer, try again.", int)
    new_product = {
        "product_name" : product_name,
        "product_price" : product_price,
        "available_stock" : available_stock
    }
    
    # SQL Insert
    sql_insert("Products", ["product_name", "product_price", "available_stock"], [product_name, product_price, available_stock])
    print(f"Product '{new_product}' added successfully!")

def update_product():
    print("\nUpdate a Product:")
    valid_ids = get_valid_ids("Products")
    update_index = valid_index_selection(display_products, "Enter the index of the product you want to update: ", valid_ids, accept_empty=True)
    if update_index:
        product_name = input("Update the name of the product: ")
        product_price = input("Update the price of the product: ")
        available_stock = input("Update the amount of available stock of the product: ")
        
        # SQL Update
        set_fields = []
        set_fields += ["product_name"] if product_name else []
        set_fields += ["product_price"] if product_price else []
        set_fields += ["available_stock"] if available_stock else []
        
        set_values = []
        set_values += [product_name] if product_name else []
        set_values += [product_price] if product_price else []
        set_values += [available_stock] if available_stock else []
        
        if set_fields:
            sql_update("Products", set_fields, set_values, where_fields=["ID"], where_values=[update_index])
            print("Product has been updated")

def delete_product():
    print("\nDelete Product:")
    valid_ids = get_valid_ids("Products")
    product_index = valid_index_selection(display_products, "Enter the index of the product you want to delete: ", valid_ids, accept_empty=True)
    if product_index:
        # SQL Delete
        sql_delete("Products", where_fields=["ID"], where_values=[product_index])
        print("Product deleted successfully!")

#courier management functions

def display_couriers():
    print("\nCouriers List:")
    # SQL Read
    sql_read_results = sql_read("Couriers", ["*"])
    print_from_sql_read(["ID", "Name", "Phone"], sql_read_results)

def add_courier():
    courier_name = input("Enter the name of the new courier: ")
    courier_phone = input ("Enter the phone number of the new courier: ")
    new_courier = {
        "courier_name" : courier_name,
        "courier_phone" : courier_phone
    }
    
    # SQL Insert
    sql_insert("Couriers", ["courier_name", "courier_phone"], [courier_name, courier_phone])
    print(f"Courier '{new_courier}' added successfully!")

def update_courier():
    print("\nUpdate a Courier:")
    valid_ids = get_valid_ids("Couriers")
    update_index = valid_index_selection(display_couriers, "Enter the index of the courier you want to update: ", valid_ids, accept_empty=True)
    if update_index:
        courier_name = input("Update the name of the courier: ")
        courier_phone = input ("Update the phone number of the courier: ")
        
        # SQL Update
        set_fields = []
        set_fields += ["courier_name"] if courier_name else []
        set_fields += ["courier_phone"] if courier_phone else []
        
        set_values = []
        set_values += [courier_name] if courier_name else []
        set_values += [courier_phone] if courier_phone else []
        
        if set_fields:
            sql_update("Couriers", set_fields, set_values, where_fields=["ID"], where_values=[update_index])
            print("Courier has been updated")

def delete_courier():
    print("\nDelete Courier:")
    valid_ids = get_valid_ids("Couriers")
    courier_index = valid_index_selection(display_couriers, "Enter the index of the courier you want to delete: ", valid_ids, accept_empty=True)
    if courier_index:
        # SQL Delete
        sql_delete("Couriers", where_fields=["ID"], where_values=[courier_index])
        print("Courier deleted successfully!")
        
#order management functions

def display_orders():
    print("\nOrders List:")
    results = get_order_details_with_products()
    order_type = valid_index_selection(display_order_sort, "How would you like to sort the orders?", [0, 1], 1, accept_empty=True)
    if order_type == 0:
        sort = ["Order Status", "Courier Name"]
    elif order_type == 1:
        sort = ["Courier Name", "Order Status"]
    else:
        sort = ["Order ID", "Courier Name"]
    
    results = sorted(results, key=lambda x: (x[sort[0]], x[sort[1]]))
    if results:
        headings = results[0].keys()
        print(", ".join(headings))
        for result in results:
            values = list(result.values())
            row = ",\t".join(map(str, values))
            print(row)
    else:
        print("No orders found.")

def add_order():
    # customer selection
    valid_ids = get_valid_ids("Customers")
    customer_index = valid_index_selection(display_customers, "Enter the index of the customer: ", valid_ids)

    # courier selection
    valid_ids = get_valid_ids("Couriers")
    courier_index = valid_index_selection(display_couriers, "Enter the index of the courier: ", valid_ids)
        
    # product selection 
    items = []
    valid_ids = get_valid_ids("Products") + [0]
    while True:
        product_index = valid_index_selection(display_products, "Enter the index of the product, or 0 to finish: ", valid_ids)
        if product_index == 0:
            break
        else:
            items.append(product_index)
            print(items)
        
    # insert order
    sql_insert("Orders", ["customer_id", "courier_id", "order_status"], [customer_index, courier_index, order_statuses[0]])
    order_id = max(get_valid_ids("Orders"))

    # for each product, count number of instances the user selected it
    item_counts = {}
    for item in items:
        if item in item_counts:
            item_counts[item] += 1
        else:
            item_counts[item] = 1
        
    # for each unique product, insert it into order_products
    for product_id in item_counts.keys():
        sql_insert("Order_Products", ["order_id", "product_id", "quantity"], [order_id, product_id, item_counts[product_id]])
    print("Order added successfully!")

def update_order_status():
    print("\nUpdate an Order Status:")
    valid_ids = get_valid_ids("Orders")
    order_index = valid_index_selection(display_orders, "Enter the index of the order you want to update the status of: ", valid_ids, accept_empty=True)

    if order_index:
        new_status_index = valid_index_selection(display_order_statuses, "Enter the index of the new status: ", list(range(len(order_statuses))), 1)
        sql_update("Orders", ["order_status"], [order_statuses[new_status_index]], where_fields=["ID"], where_values=[order_index])
        print("Order status has been updated")

def update_order_details():
    print("\nUpdate an Order's Details:")
    # customer selection
    valid_ids = get_valid_ids("Orders")
    order_id = valid_index_selection(display_orders, "Enter the index of the order you wish to update: ", valid_ids, accept_empty=True)
    
    if not order_id:
        return
    
    # customer selection
    valid_ids = get_valid_ids("Customers")
    customer_id = valid_index_selection(display_customers, "Enter the index of the customer: ", valid_ids, accept_empty=True)

    # courier selection
    valid_ids = get_valid_ids("Couriers")
    courier_id = valid_index_selection(display_couriers, "Enter the index of the courier: ", valid_ids, accept_empty=True)
        
    # product selection 
    items = []
    valid_ids = get_valid_ids("Products") + [0]
    first_id = True
    while True:
        product_index = valid_index_selection(display_products, "Enter the index of the product, or 0 to finish: ", valid_ids, accept_empty=first_id)
        if product_index == 0 or (first_id and not product_index):
            break
        else:
            first_id = False
            items.append(product_index)
            print(items)
    
    # update orders table
    set_fields = []
    set_fields += ["customer_id"] if customer_id else []
    set_fields += ["courier_id"] if courier_id else []
    
    set_values = []
    set_values += [customer_id] if customer_id else []
    set_values += [courier_id] if courier_id else []
        
    if set_fields:
        sql_update("Orders", set_fields, set_values, where_fields=["ID"], where_values=[order_id])
    
    # If there are any changes to the products list
    if items:
        # for each product, count number of instances the user selected it
        item_counts = {}
        for item in items:
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1
        
        # remove entries from order products table
        bad_product_ids = sql_read("Order_Products", ["product_id"], ["order_id"], [order_id])
        bad_product_ids = [x[0] for x in bad_product_ids]
        for product_id in bad_product_ids:
            sql_delete("Order_Products", ["order_id", "product_id"], [order_id, product_id])

        # add new entries to order products table
        for product_id in item_counts.keys():
            sql_insert("Order_Products", ["order_id", "product_id", "quantity"], [order_id, product_id, item_counts[product_id]])
    print("Order updated successfully!")

def delete_order():
    print("\nDelete Order:")
    valid_ids = get_valid_ids("Orders")
    order_index = valid_index_selection(display_orders, "Enter the index of the order you want to delete: ", valid_ids, accept_empty=True)
    
    if order_index:
        # Find the Product ID's associated with this order
        product_ids = sql_read("Order_Products", ["product_id"], ["order_id"], [order_index])
        product_ids = [x[0] for x in product_ids]
        for product_id in product_ids:
            sql_delete("Order_Products", ["order_id", "product_id"], [order_index, product_id])
        sql_delete("Orders", ["ID"], [order_index])
        print("Order deleted successfully!")

#Customer management functions

def display_customers():
    print("\nCustomers List:")
    sql_read_results = sql_read("Customers", ["*"])
    print_from_sql_read(["ID", "Name", "Age", "Phone", "Address"], sql_read_results)

def add_customer():
    name = input("Enter the new customer's name: ")
    age = get_input("Enter the customer's age: ", "Not an integer, try again.", int)
    phone = input("Enter the customer's phone number: ")
    address = input("Enter the customer's address: ")
    new_customer = {
        "name" : name,
        "age" : age,
        "phone": phone,
        "address": address
    }
    sql_insert("Customers", ["customer_name", "customer_age", "customer_phone", "customer_address"], [name, age, phone, address])
    print(f"Customer '{new_customer}' added successfully!")

def update_customer():
    print("\nUpdate a Customer:")
    valid_ids = get_valid_ids("Customers")
    index = valid_index_selection(display_customers, "Enter the index of the customer you want to update: ", valid_ids, accept_empty=True)
    if index:
        name = input("Update the customer's name: ")
        age = input("Update the customer's age: ")
        phone = input("Update the customer's phone number: ")
        address = input("Update the customer's address: ")
        
        # SQL Update
        set_fields = []
        set_fields += ["customer_name"] if name else []
        set_fields += ["customer_age"] if age else []
        set_fields += ["customer_phone"] if phone else []
        set_fields += ["customer_address"] if address else []
        
        set_values = []
        set_values += [name] if name else []
        set_values += [age] if age else []
        set_values += [phone] if phone else []
        set_values += [address] if address else []
        
        if set_fields:
            sql_update("Customers", set_fields, set_values, where_fields=["ID"], where_values=[index])
            print("Customer has been updated")

def delete_customer():
    print("\nDelete Customer:")
    valid_ids = get_valid_ids("Customers")
    index = valid_index_selection(display_customers, "Enter the index of the product you want to delete: ", valid_ids, accept_empty=True)
    if index:
        sql_delete("Customers", where_fields=["ID"], where_values=index)
        print("Customer deleted successfully!")

#######################################################################################
#Main loop
def main(path=''):
    init_sql()

    while True:
        print_main_menu()
        user_input_main = get_input("Enter your choice: ", "Invalid Selection. Try again.", int)

        if user_input_main == 0:
            print("Exiting the application...")
            break

        elif user_input_main == 1:
            while True:
                print_product_menu()
                user_input_products = get_input("Enter your choice: ", "Invalid Selection. Try again.", int)

                if user_input_products == 0:
                    print("Returning to Main Menu...")
                    break
                task = [display_products, add_product, update_product, delete_product]
                if 1 <= user_input_products <= 4:
                    task[user_input_products - 1]()
                else:
                    print("Invalid input. Please try again.")

        elif user_input_main == 2:
            while True:
                print_courier_menu()
                user_input_couriers = get_input("Enter your choice: ", "Invalid Selection. Try again.", int)

                if user_input_couriers == 0:
                    print("Returning to Main Menu...")
                    break
                task = [display_couriers, add_courier, update_courier, delete_courier]
                if 1 <= user_input_couriers <= 4:
                    task[user_input_couriers - 1]()
                else:
                    print("Invalid input. Please try again.")

        elif user_input_main == 3:
            while True:
                print_orders_menu()
                user_input_orders = get_input("Enter your choice: ", "Invalid Selection. Try again.", int)

                if user_input_orders == 0:
                    print("Returning to Main Menu...")
                    break
                task = [display_orders, add_order, update_order_status, update_order_details, delete_order]
                if 1 <= user_input_orders <= 5:
                    task[user_input_orders - 1]()
                else:
                    print("Invalid input. Please try again.")

        elif user_input_main == 4:
            while True:
                print_customer_menu()
                user_input_customers = get_input("Enter your choice: ", "Invalid Selection. Try again.", int)

                if user_input_customers == 0:
                    print("Returning to Main Menu...")
                    break
                task = [display_customers, add_customer, update_customer, delete_customer]
                if 1 <= user_input_customers <= 4:
                    task[user_input_customers - 1]()
                else:
                    print("Invalid input. Please try again.")


if __name__ == '__main__':
    main('src\\week6\\')
