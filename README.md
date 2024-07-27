# fruzsi.deb.mini.project
A data organiser app for a coffee shop.

### Project Background

The client has a pop-up cafe, offering a range of hot beverages and needed an organiser app to keep track of the orders. The app helps manage the data related to orders, inventory, and customer preferences, making it easier for the coffee shop to operate efficiently. 
This is a study project for Generation's Data Engineering course. 

### Client requirements

- Maintain a collection of products and couriers
- Create new orders
- Update the status of an order i.e: preparing, out-for-delivery, delivered
- Data presisted upon exiting the app
- Data loaded when starting the app
- Reliable and tested app
- Regular software updates

### How to run the app

To run the app, you first need to set up the docker image for the SQL database.

1) Build docker container:
    - Run the docker application
    - Navigate to `"Directory to your project folder"/src/final_week6`.
    - Run `docker-compose build` to build the docker image container.

2) Run the docker container:
    - Run the docker application
    - Run `docker-compose up` to run the docker image container.

3) Install python dependencies.
    - Run `pip install -r requirements.txt`

4) Once the docker container is running, you then need to set up the SQL database.
    - Run `python sql_creator.py`. If you already have a database of the same name, then you will be asked whether you wish to delete it or not. This cannot be undone.

5) Run the application.
    - Run `python mini_project_week6.py`.

For previous versions run `mini_project_weekX.py`, where X is the week number. 
- Week 5 contains CSV and JSON integration and data persistence
- Week 6 contains SQL integration and data persistence

Known bug in week 6: Customer can add an order without any products, and this will be invisible when viewing orders via the menu, but will be present within the SQL database.
Known bug in week 5: The interface is not robust to various user inputs that are outside of the intended responses.

### Unit tests

The unit test is related to the project version week5, it will NOT run in final version. The unit test is created for a function to save CSV files. Further unit testing is needed. 

### Project Reflections


I attempted a modular design approach, using the Model-View-Controller (MVC) pattern. This allowed me to mostly separate the data (model), user interface (view), and control logic (controller). This separation made it easier to manage and extend the application. 
To meet the requirement of persisting data, I implemented a MySQL database in `final_week6` and CSV & JSON solution in `week5`. The app was designed to save and retrieve data from the database, ensuring that all information is preserved across sessions.
The user interface was designed with simplicity in mind, using clear navigation and intuitive forms. I developed two functions to handle type sensitive user input, `valid_index_selection` and `get_input`, including error messages in case of invalid user input. 
The order management using SQL was significantly more involved than I initially anticipated, as data normalisition and joining tables in order to read the data for the UI required additional efforts compared to CSV and JSON implementations. 
I guaranteed the project's requirements by taking a functional programming approach and creating small functions that do simple tasks rather than large function covering multiple tasks. This made it easier to verify each function manually, and it will make it easier to implement unit tests in the future.
I most enjoyed implementing modular functions and creating a robust UI.


# Future improvements:
- Robust unit testing
- Import / Export to and from the SQL database to CSV and JSON files
- split `get_order_details_with_products` into SQL and model components for better modularity