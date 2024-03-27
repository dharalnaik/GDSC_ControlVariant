# GDSC_ControlVariant

A control variant management API created with python, as a task for technical club recruitments.

**Description:**

Users will be able to perform various operations such as CRUD - Create, Read, Update, Delete product and its variant data from the database.

**Requirements:**

1. Users will have to use different API endpoints to perform different operations.
2. There are total of 9 endpoints, consisting of 3-POST, 1-GET, 2-PUT, 3-DELETE requests.
3. Purpose of each request is as follows:
    - POST-1 To add product name to the database.
    - POST-2 To add product and its variants to the database.
    - POST-3 To add variants of an existing product to the database.
      
    - GET-1 To read data from the database, enter product name, and all variants of it will be displayed.
  
    - PUT-1 To update product data in the database. It will update product names in both the schemas - Products and Variants.
    - PUT-2 To update variant data of a product in the database. It will update various attribute of a product in schema - Variants.
  
    - DELETE-1 To 
    - Load tasks from a file.
    - Quit the program.
    - (The menu is in the same order in the program.)
5. Error handling has been taken care to handle invalid input and missing tasks gracefully.
6. The data structures for task storage is lists.
