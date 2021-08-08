# catalogAPI

This app is a catalog to manage products, developed using Django 3.2 and Django REST framework 3.12.

The app can be found [here](https://product-catalog-sandravera.herokuapp.com/).

It has the following features:

* Users module, only accessible by admin users. This module provides CRUD operations on user instances. It also allows the user logged in to change their password.
* Brands module, only accessible by admin users. This module provides CRUD operations on brand instances. It also allows the listing of all brand's products.
* Products module, accessible by admin and anonymous users. This module provides CRUD operations on product instances for admin users. Anonymous users are only allowed to list and retrieve product information.

## Local build

### Installation

Before running this app, install the following packages:

* Python (3.8)
* Virtualenv (20.6.0)
* pip (21.2.3)

### Environment variables

Create a script with the following environment variables:

| Variable        | Description           |
| ------------- |-------------|
| SECRET_KEY | A secret key for the Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value. |
| EMAIL_HOST | The host to use for sending email. |
| EMAIL_HOST_USER | Username to use for the SMTP server defined in EMAIL_HOST. |
| EMAIL_HOST_PASSWORD | Password to use for the SMTP server defined in EMAIL_HOST. |
| DEBUG | An integer that turns on/off debug mode. For debug mode use value 1, otherwise 0. |

Run the script in the terminal where the project will be run, so all variables can be accessed by it.

### Virtual environment configuration

Create a new virtual environment inside the project folder by running:

```
virtualenv env --python=$(which python3.8)
```

To activate the virtual environment run:
```
source env/bin/activate
```

To deactivate the virtual environment run:
```
deactivate
```

For the following steps, the virtual environment should be activated.

### Dependencies

To install dependencies, run the following command inside the project folder:
```
pip install -r requirements.txt
```

### Database configuration

By default, an SQLite database file is created.

To run migrations, run the following command inside the project folder:
```
python manage.py migrate
```

### Create a superuser

To create a superuser for the project, run the following command inside de project folder:
```
python manage.py createsuperuser
```

### Run the app

To run the app, run the following command inside the project folder:
```
python manage.py runserver
```

Your application will be running at ```http://localhost:8000```.

## Endpoints

### Authentication

Authentication endpoints, such as ```login``` and ```logout``` are provided, respectively in:

```
/api/auth/login/
```

```
/api/auth/logout/
```

### Users

For list and create operations:

```
/api/users/
```

For retrieve, update and delete operations:

```
/api/users/USER_ID
```

Where ```USER_ID``` is the ID of the user instance in the database.

To change password:

```
/api/users/change_password/
```


### Brands

For list and create operations:

```
/api/brands/
```

For retrieve, update and delete operations:

```
/api/brands/BRAND_ID
```

Where ```BRAND_ID``` is the ID of the brand instance in the database.

To list all products of a brand:

```
/api/brands/BRAND_ID/products/
```

Where ```BRAND_ID``` is the ID of the brand instance in the database.

### Products

For list and create operations:

```
/api/products/
```

For retrieve, update and delete operations:

```
/api/products/PRODUCT_ID
```

Where ```PRODUCT_ID``` is the ID of the product instance in the database.

## User Interface

The interface used is the one provided by the browsable API of Django REST framework. It provides actions not defined in CRUD operations as an "Extra Actions" button.
