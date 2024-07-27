import os
from dotenv import load_dotenv
import pymysql

# Setup
def init_sql():
    load_dotenv()

# Connect
def get_db_connection():
    host_name = os.environ.get("mysql_host")
    database_name = os.environ.get("mysql_db")
    user_name = os.environ.get("mysql_user")
    user_password = os.environ.get("mysql_pass")

    if not all([host_name, database_name, user_name, user_password]):
        raise ValueError("Database credentials are not fully set in the environment variables.")

    return pymysql.connect(
        host=host_name,
        user=user_name,
        password=user_password,
        database=database_name
    )

# Concatenate fields together in the right format for an SQL query
def query_field_concatenator(fields, operators=None, join_str=", "):
    # Get the number of fields
    num_fields = len(fields)
    
    # If the user doesn't tell us what operator to use, assume they want equal to
    if operators is None:
        operators = "="
    
    # If the user provides a string, then create a list of operators (lets the user provide a list)
    if type(operators) is str:
        operators = [operators] * num_fields
    
    result = []
    for i in range(num_fields):
        result += [fields[i] + " " + operators[i] + " '%s'"]
    result = join_str.join(result)
    return result

# Order_Specific_Function
def get_order_details_with_products():
    """
    Retrieves order details including customer names, courier names, and associated products with quantities.
    
    :return: List of dictionaries containing order details with customer, courier names, and products.
    """
    # SQL query to retrieve order details with customer and courier names along with products and quantities
    sql_query = """
    SELECT 
        Orders.id AS order_id,
        Orders.order_status,
        Customers.id,
        Customers.customer_name,
        Couriers.id,
        Couriers.courier_name,
        Products.id,
        Products.product_name,
        Order_Products.quantity
    FROM Orders
    INNER JOIN Customers ON Orders.customer_id = Customers.id
    INNER JOIN Couriers ON Orders.courier_id = Couriers.id
    INNER JOIN Order_Products ON Orders.id = Order_Products.order_id
    INNER JOIN Products ON Order_Products.product_id = Products.id;
    """
    
    # Run the SQL query
    try:
        connection = get_db_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                results = cursor.fetchall()
                
                # Process results to aggregate products by order
                orders = {}
                for row in results:
                    order_id = row[0]
                    order_status = row[1]
                    customer_id = row[2]
                    customer_name = row[3]
                    courier_id = row[4]
                    courier_name = row[5]
                    product_id = row[6]
                    product_name = row[7]
                    quantity = row[8]
                    
                    if order_id not in orders:
                        orders[order_id] = {
                            'Order ID': order_id,
                            'Order Status': order_status,
                            'Customer ID': customer_id,
                            'Customer Name': customer_name,
                            'Courier ID': courier_id,
                            'Courier Name': courier_name,
                            'Products List': []
                        }
                    orders[order_id]['Products List'].append({
                        'ID': product_id,
                        'Name': product_name,
                        'Quantity': quantity
                    })
                
                # Convert the orders dictionary to a list of values
                order_list = list(orders.values())
                return order_list
    except pymysql.MySQLError as e:
        print(f"Error executing the join operation: {e}")
        return None

# Insert
def sql_insert(table_name, insert_fields, insert_values):
    # Create the SQL query
    insert_fields = ", ".join(insert_fields)
    insert_values = [str(value) for value in insert_values]
    insert_values = "', '".join(insert_values)
    sql_query = f"INSERT INTO {table_name} ({insert_fields}) VALUES ('{insert_values}');"
        
    # Run the SQL query
    try:
        connection = get_db_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error inserting into the database: {e}")

# Read
def sql_read(table_name, select_fields, where_fields=None, where_values=None, where_operators=None):
    # Create the SQL query
    select_fields = ", ".join(select_fields)  # = "id, customer_name"
    sql_query = f"SELECT {select_fields} FROM {table_name}"
    
    if where_fields and where_values:
        where_constraints = query_field_concatenator(where_fields, where_operators)
        sql_query += f" WHERE {where_constraints}"
        sql_query = sql_query % tuple(where_values)
    sql_query += ";"
    
    # Run the SQL query
    try:
        connection = get_db_connection()
        with connection:
            with connection.cursor() as cursor:
                if where_values:
                    cursor.execute(sql_query)
                else:
                    cursor.execute(sql_query)
                return cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"Error reading from the database: {e}")
        return []

# Update
def sql_update(table_name, set_fields, set_values, where_fields=None, where_values=None, where_operators=None):
    # Create the SQL query
    set_values = query_field_concatenator(set_fields) % tuple(set_values)
    sql_query = f"UPDATE {table_name} SET {set_values}" 
    if where_fields and where_values:
        where_constraints = query_field_concatenator(where_fields, where_operators)
        sql_query += f" WHERE {where_constraints}"
        sql_query = sql_query % tuple(where_values)
    
    # Run the SQL query
    try:
        connection = get_db_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error updating the database: {e}")

# Delete
def sql_delete(table_name, where_fields=None, where_values=None, where_operators=None):
    # Create the SQL query
    sql_query = f"DELETE FROM {table_name}"
    if where_fields and where_values:
        where_constraints = query_field_concatenator(where_fields, where_operators, " AND ")
        sql_query += f" WHERE {where_constraints}"
        sql_query = sql_query % tuple(where_values)
    
    # Run the SQL query
    try:
        connection = get_db_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error deleting from the database: {e}")

# Main function to run when file is run directly
def main():
    init_sql()
    
    # SQL READ
    sql_query = """
            SELECT * FROM Customers
            WHERE customer_name = 'Birbs';
            """
    sql_return = sql_read("Customers", ["*"], where_fields=["customer_name"], where_values=["Birbs"], where_operators="=")
    print("Records before insertion:", sql_return)
    
    # SQL INSERT
    sql_query = """
            INSERT INTO Customers (customer_name, customer_age)
            VALUES ('Birbs', '32')
            """
    sql_insert("Products", ["product_name"], ["Birbs"])

    # Verify insertion
    sql_query = """
            SELECT * FROM Customers
            WHERE customer_name = 'Birbs';
            """
    sql_return = sql_read("Customers", ["*"])  #, where_fields=["customer_name"], where_values=["Birbs"], where_operators="=")
    print("Records after insertion:", sql_return)
    
    # SQL UPDATE
    sql_query = """
            UPDATE Customers
            SET customer_address = Equestria
            WHERE customer_name = Birbs
            """
    sql_update("Customers", ["customer_address"], ["Equestria"], where_fields=["customer_name"], where_values=["Birbs"], where_operators="=")

    # Verify Update
    sql_query = """
            SELECT * FROM Customers
            WHERE customer_name = 'Birbs';
            """
    sql_return = sql_read("Customers", ["*"], where_fields=["customer_name"], where_values=["Birbs"], where_operators="=")
    print("Records after update:", sql_return)

    # SQL DELETE
    sql_query = """
            DELETE FROM Customers
            WHERE customer_name = Birbs
            """
    # sql_delete("Customers", where_fields=["customer_name"], where_values=["Birbs"], where_operators="=")

    # Verify Deletion
    sql_query = """
            SELECT * FROM Customers
            WHERE customer_name = 'Birbs';
            """
    sql_return = sql_read("Customers", ["*"], where_fields=["customer_name"], where_values=["Birbs"], where_operators="=")
    print("Records after deletion:", sql_return)

if __name__ == '__main__':
    main()
