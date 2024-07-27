import os
from dotenv import load_dotenv
import pymysql

# Setup
def init_sql():
    load_dotenv()

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

def setup_database(db_schema: dict):
    try:
        # Connect to the server (without specifying a database)
        connection = get_db_connection()
        database_name = os.getenv("mysql_db")
        
        with connection:
            with connection.cursor() as cursor:
                # Check if the database exists
                cursor.execute("SHOW DATABASES LIKE %s", (database_name,))
                result = cursor.fetchone()
                
                if result:
                    # Database exists, ask user if they want to delete it
                    response = input(f"The database {database_name} already exists. Do you want to delete it? (yes/no): ").strip().lower()
                    if response != 'yes' and response != 'y':
                        # User does not want to delete everything and create a new database
                        print("User did not want to delete and create a fresh database.")
                        return
                        
                    # Drop the existing database
                    cursor.execute(f"DROP DATABASE {database_name}")
                    print(f"Database {database_name} deleted.")
                
                # Create a new database
                cursor.execute(f"CREATE DATABASE {database_name}")
                print(f"Database {database_name} created.")
                
                # Connect to the new database
                cursor.execute(f"USE {database_name}")
                
                # Create tables based on the provided schema
                for table_name in db_schema.keys():
                    fields = db_schema[table_name]["Fields"]
                    field_definitions = [f"{name} {type}" for name, type in fields]
                    fields_str = ", ".join(field_definitions)
                    
                    constraints = db_schema[table_name]["Constraints"]
                    constraints = constraints if not constraints else [""] + constraints
                    constraints_str = ", ".join(constraints)
                    
                    create_table_query = f"CREATE TABLE {table_name} ({fields_str}{constraints_str})"
                    cursor.execute(create_table_query)
                    print(f"Table {table_name} created with fields and constraints:\n{fields_str}, {constraints_str}\n")

                connection.commit()
                print("Database setup completed.")

    except pymysql.MySQLError as e:
        print(f"Error setting up the database: {e}")

# Example usage / product_name, product_price, available_stock
if __name__ == '__main__':
    init_sql()
    db_schema = {
        "Products": {
            "Fields" : [
                ("id", "INT AUTO_INCREMENT PRIMARY KEY"),
                ("product_name", "VARCHAR(100) NOT NULL"),
                ("product_price", "FLOAT"),
                ("available_stock", "INT"),
            ],
            "Constraints" : []
        },
        "Couriers": {
            "Fields" : [
                ("id", "INT AUTO_INCREMENT PRIMARY KEY"),
                ("courier_name", "VARCHAR(100) NOT NULL"),
                ("courier_phone", "VARCHAR(15)"),
            ],
            "Constraints" : []
        },
        "Customers": {
            "Fields" : [
                ("id", "INT AUTO_INCREMENT PRIMARY KEY"),
                ("customer_name", "VARCHAR(100) NOT NULL"),
                ("customer_age", "INT"),
                ("customer_phone", "VARCHAR(15)"),
                ("customer_address", "VARCHAR(1000)"),
            ],
            "Constraints" : []
        },
        "Orders": {
            "Fields" : [
                ("id", "INT AUTO_INCREMENT PRIMARY KEY"),
                ("customer_id", "INT NOT NULL"),
                ("courier_id", "INT NOT NULL"),
                ("order_status", "VARCHAR(9) NOT NULL"),
            ],
            "Constraints" : [
                "FOREIGN KEY (customer_id) REFERENCES Customers(id)",
                "FOREIGN KEY (courier_id) REFERENCES Couriers(id)"
            ]
        },
        "Order_Products": {
            "Fields" : [        
                ("order_id", "INT NOT NULL"),
                ("product_id", "INT NOT NULL"),
                ("quantity", "INT NOT NULL"),
            ],
            "Constraints" : [
                "PRIMARY KEY (order_id, product_id)",
                "FOREIGN KEY (order_id) REFERENCES Orders(id)",
                "FOREIGN KEY (product_id) REFERENCES Products(id)"
            ]
        },
    }
    setup_database(db_schema)
