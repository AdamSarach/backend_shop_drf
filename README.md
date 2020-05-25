# Piping Components Online Store REST API

Project cannot be used with commercial purpose without owner permission.

An application uses Django and Django Rest Framework. Created application is a REST API which allows maintain data for running bussiness.

Table of content:
```
1. Download repository
2. Run project
    a) with venv
    b) with Docker
3. Endpoints
```
1. Download repository
    Download GitHub Repository using following command
```
$ git clone https://github.com/adamsarach/restapi.git
```

2a. Run project with venv

 Create Virtual Environment ('venv') inside project directory
 ```
 $ python -m venv <your_env_name>
```
 Install required packages
```
(with_open_virtual_env)
$ pip install -r requirements.txt
```

2b. Run project with Docker
To build containers user command
 ```
 $ docker-compose -f docker-compose.yml build
```
Run services:
```
 $ docker-compose -f docker-compose.yml up -d
```
Get fixtures to check endpoints
```
 $ docker-compose exec -d web bash -c "python manage.py loaddata fixtures.json"
```

3. Endpoints
 Usage:
 The application distinguish 3 groups of users. An user can be assigned to group: 'Customer', 'Employee' or 'Admin'.
 Depending on user's group, one can access different data.
 There are a few endpoints. To handle them, use following commands:
 
    [GET] /api/ - main site with welcoming information
    
    Requirements: Being in Employee Group
    [GET] /api/suppliers - retrieve supplier list
    [POST] /api/suppliers - create a new supplier
    [GET] /api/suppliers/<int:pk> - retrieve a specified supplier
    [PUT] /api/suppliers/<int:pk> - update an existing supplier
    [DELETE] /api/suppliers/<int:pk> - delete a supplier
    
    Requirements: None
    [GET] /api/products - retrieve product list
    [GET] /api/supplier/<int:pk> - retrieve a specified product
    
    Requirements: Being in Employee Group
    [POST] /api/products - create a new product
    [PUT] /api/products/<int:pk> - update an existing product
    [DELETE] /api/products/<int:pk> - delete a product
    
    Requirements: Being in Employee Group (1) or Customer Group (2)
    [GET] /api/orders - retrieve order list (1) retrieve users's orders (2)
    [POST] /api/orders - create a new order for anyone (1) create an own new order (2)
    [GET] /api/orders/<int:pk> - retrieve any order data (1) retrieve only own single order data (2)
    [PUT] /api/orders/<int:pk> - update any order data (1) update only own single order data (2)
    [DELETE] /api/orders/<int:pk> - delete any order (1) delete only own order (2)
    
    Requirements: Being in Employee Group (1) or Customer Group (2)
    [GET] /api/orders/<int:pk>/items - retrieve order items (1) retrieve own order items (2)
    [POST] /api/orders/<int:pk>/items - create a new item for any order (1) create a new item for own order (2)
    [PUT] /api/orders/<int:pk>/items/<int:item> - update any order item data (1) update only own order item data (2)
    [DELETE] /api/orders/<int:pk>/items/<int:item> - delete any order item (1) delete only own order item (2)


