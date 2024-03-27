# GDSC_ControlVariant

A control variant management API created with python, as a task for technical club recruitments.

**Description:**

Users will be able to perform various operations such as CRUD - Create, Read, Update, Delete product and its variant data from the database.

**Requirements:**

1. Users will have to use different API endpoints to perform different operations.
2. There are total of 9 endpoints, consisting of 3-POST, 1-GET, 2-PUT, 3-DELETE requests.
3. Purpose of each request is as follows :-
    -     POST-1 To add product name to the database.
    - POST-2 To add product and its variants to the database.
    - POST-3 To add variants of an existing product to the database.
      
      
    - GET-1 To read data from the database. Enter product name, and all variants of it will be displayed.


    - PUT-1 To update product data in the database. It will update product names in both the schemas - Products and Variants.
    - PUT-2 To update variant data of a product in the database. It will update various attribute of a product in schema - Variants.

  
    - DELETE-1 To delete a single variant of a product from the database. Enter Variant_id to delete it.
    - Delete-2 To delete all the variants of a product from the database. Enter product name to delete all the variants of it.
    - DELETE-3 To delete product from the database. Enter product name for the same. Note: Without deleting variants, product cannot be deleted due to foreign key infringement.

    
5. Error handling has been taken care to handle invalid input entries incase of missing objects.
6. The database consists of 2 schemas - Products and Variants :-
   - Products relation consists of 2 fields - Product_id(Primary Key) and Product_name.
   - Variants relation consists of 6 fields - Variant_id(Primary Key), Size, Color, Material, Product_id(Foreingn Key), Product_name.
