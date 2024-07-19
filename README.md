![Python](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffczanetti%2Floan_api%2Fmain%2FPipfile.lock&query=%24._meta.requires.python_version&label=Python&labelColor=%233776ab&color=%233d3d3e)
![Django](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffczanetti%2Floan_api%2Fmain%2FPipfile.lock&query=%24.default.django.version&label=Django&labelColor=%230c3c26&color=%233d3d3e)
![Django REST framework](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffczanetti%2Floan_api%2Fmain%2FPipfile.lock&query=%24.default.djangorestframework.version&label=Django%20REST%20framework&labelColor=%23a30000&color=%233d3d3e)

[![codecov](https://codecov.io/gh/fczanetti/loan_api/graph/badge.svg?token=n28xxXxXOG)](https://codecov.io/gh/fczanetti/loan_api)
![CI](https://github.com/fczanetti/loan_api/actions/workflows/wf.yml/badge.svg)
![Sentry](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffczanetti%2Floan_api%2Fmain%2FPipfile.lock&query=%24.default%5B'sentry-sdk'%5D.version&label=Sentry&labelColor=%23452650&color=%2322272e)


# Loan API

Welcome to Loan API. 

This is an API that can be used to manage loans from banks to clients. The clients, once authenticated, are able to create, read, update and delete their loans. When creating a new Loan, the client/user has to inform the value, interest rate, number of installments to quit the Loan and the bank responsible for loaning the money. Users can also create, read, update and delete payments related to their loans.

When retrieving a Loan, users can also view how much they still own to the bank, and this value is calculated based on the interest rate, value and number of installments informed when creating the loan. Also, if there is any payments related to the Loan retrieved, the owned value (unpaid value) will be discounted.

You can check the project instructions/requirements [on this link](https://github.com/fczanetti/loan_api/blob/main/project_instructions.md). 

Or, if you prefer, you can also check [the original repository](https://github.com/onidata/vagas).

<br></br>
# Content

- [Database models](https://github.com/fczanetti/loan_api?tab=readme-ov-file#database-models)
- [Folder structure](https://github.com/fczanetti/loan_api?tab=readme-ov-file#folder-structure)
- [How to install and test](https://github.com/fczanetti/loan_api?tab=readme-ov-file#how-to-install-and-test)
- [How to install and test with Docker](https://github.com/fczanetti/loan_api?tab=readme-ov-file#how-to-install-and-test-with-docker)
- [NGINX](https://github.com/fczanetti/loan_api?tab=readme-ov-file#nginx)
- [Outstanding balance calculation (unpaid value)](https://github.com/fczanetti/loan_api?tab=readme-ov-file#outstanding-balance-calculation-unpaid-value)
- [API documentation](https://github.com/fczanetti/loan_api?tab=readme-ov-file#api-documentation)
    - [Listing elements](https://github.com/fczanetti/loan_api?tab=readme-ov-file#listing-elements)
    - [Endpoints](https://github.com/fczanetti/loan_api?tab=readme-ov-file#endpoints)
    - [Authentication](https://github.com/fczanetti/loan_api?tab=readme-ov-file#authentication)
    - [Making requests](https://github.com/fczanetti/loan_api?tab=readme-ov-file#making-requests)
        - [Creating a new Loan](https://github.com/fczanetti/loan_api?tab=readme-ov-file#1---creating-a-new-loan)
        - [Retrieving a specific Loan](https://github.com/fczanetti/loan_api?tab=readme-ov-file#2---retrieving-a-specific-loan)
        - [Listing loans](https://github.com/fczanetti/loan_api?tab=readme-ov-file#3---listing-loans)
        - [Updating a Loan](https://github.com/fczanetti/loan_api?tab=readme-ov-file#4---updating-a-loan)
        - [Deleting a Loan](https://github.com/fczanetti/loan_api?tab=readme-ov-file#5---deleting-a-loan)
        - [Creating a Payment](https://github.com/fczanetti/loan_api?tab=readme-ov-file#6---creating-a-payment)
        - [Retrieving a Payment](https://github.com/fczanetti/loan_api?tab=readme-ov-file#7---retrieving-a-payment)
        - [Listing payments](https://github.com/fczanetti/loan_api?tab=readme-ov-file#8---listing-payments)
        - [Updating a Payment](https://github.com/fczanetti/loan_api?tab=readme-ov-file#9---updating-a-payment)
        - [Deleting a Payment](https://github.com/fczanetti/loan_api?tab=readme-ov-file#10---deleting-a-payment)
        - [Filtering payments by loan ID](https://github.com/fczanetti/loan_api?tab=readme-ov-file#11---filtering-payments-by-loan-id)

<br></br>
# Database models

```mermaid
classDiagram

    Loan "*" <--> "1" Bank
    Loan "1" <--> "*" Payment

    class Bank {
        - id: ~int~
        - name: ~string~
    }

    class Loan {
        - id: ~int~
        - value: ~decimal~
        - interest_rate: ~float~
        - ip_address: ~string~
        - request_date: ~date~
        - bank id: ~int~ FK
        - client: ~string~
        - installments: ~int~
    }

    class Payment {
        - id: ~int~
        - loan id: ~int~ FK
        - payment_date: ~date~
        - value: ~decimal~
    }

    class User {
        - id: ~int~
        - email: ~email~ unique
        - first_name: ~string~
        - password: ~string~
    }
```

<br></br>
# Folder structure

Some of the main folders and files.

```
├── 📂 loan_api
|   ├── 📂 contrib
|   |   ├── env-sample
|   ├── manage.py
|   ├── Pipfile
|   ├── Pipfile.lock
|   ├── .flake8
|   ├── pytest.ini
|   ├── README.md
|   ├── 📂 nginx
|   |   ├── nginx.conf
|   ├── 📂 loan_api
|   |   ├── urls.py
|   |   ├── settings.py
|   |   ├── 📂 base
|   |   |   ├── 📂 migrations
|   |   |   ├── 📂 tests
|   |   |   ├── ├── 📂 tests_loans
|   |   |   ├── ├── 📂 tests_payments
|   |   |   ├── 📂 fixtures
|   |   |   ├── ├── initial_data.json
|   |   |   ├── admin.py
|   |   |   ├── loans.py
|   |   |   ├── payments.py
|   |   |   ├── models.py
|   |   |   ├── serializers.py
|   |   |   ├── validators.py
|   |   |   ├── views.py
```

<br></br>
# How to install and test

You can follow the next steps to install and test this API. These steps consider you are using a Linux environment and Pipenv as the virtualenv management tool.

1 - Clone this repository:

```
git clone git@github.com:fczanetti/loan_api.git
```

2 - Install the necessary libraries (default and development libraries):

```
pipenv sync -d
```

3 - Activate the virtual environment:

```
pipenv shell
```

4 - Copy the content from env-sample file inside contrib diretory to a new file called .env. This .env file has to be placed in the root diretory of the application.

```
cp contrib/env-sample .env
```
As we are not using Docker on this tutorial, you have to comment or remove the environment variable DATABASE_URL in your .env file.

5 - Apply Django migrations:

```
python manage.py migrate
```

6 - At this point, if everything worked as expected, you are able to start Django server. The only problem is that you have neither a Bank nor a User created to make requests. You can create both manually using Django ORM or use the following command to populate the database with two Bank instances and a User:

```
python manage.py loaddata initial_data.json
```

User credentials:
- email: admin@admin.com
- password: admin

The Bank instances created have ID's 1 and 2, and that is enough for now.

7 - Start Django server:

```
python manage.py runserver
```

8 - With the credentials above and the server running you can, in another terminal, [create a token](https://github.com/fczanetti/loan_api?tab=readme-ov-file#authentication) and start testing the API by [making requests](https://github.com/fczanetti/loan_api?tab=readme-ov-file#making-requests).

9 - This quick example shows how to make a POST request to create your first Loan. You can use the same terminal you used to create your token, just remember to insert it in the request header:

```
curl -H 'Content-Type: application/json' \
     -H 'Authorization: Token INSERT_THE_TOKEN_CREATED_HERE' \
     -d '{"value": 1000, "interest_rate": 2.5, "installments": 10, "bank": 1}' \
     -X POST http://127.0.0.1:8000/api/loans/
```

10 - Finally, to run the tests, just use this command:

```
pytest
```

<br></br>
# How to install and test with Docker

1 - To install using Docker we can start by following the steps 1 to 4 of [this tutorial](https://github.com/fczanetti/loan_api?tab=readme-ov-file#how-to-install-and-test). But, this time, we are neither removing nor commenting the DATABASE_URL environment variable from our .env file.

2 - Having the .env file created, we can start the containers:

```
docker compose up -d
```

A '.pgdata/' directory will be created in the root of the application, and this is where our database data will be stored.

3 - Now we can load some initial data (one User and two Bank instances) in our database, this time running the command inside the LOAN_API_APP container:

```
docker exec <CONTAINER_ID> python manage.py loaddata initial_data.json
```

You can use the credentials from the User created to [create a token](https://github.com/fczanetti/loan_api?tab=readme-ov-file#authentication) and start testing requests.
- email: admin@admin.com
- password: admin

4 - To run the tests you can use this command:

```
docker exec <CONTAINER_ID> pytest
```

That's it. If everything worked fine the application is already running and you can start making requests.

<br></br>
# NGINX

It's important to mention that, when running the command `docker compose up -d`, you will also be starting an nginx container that works as a simple proxy and is responsible for serving static files. Because of this, the library [django-ipware](https://pypi.org/project/django-ipware/) was installed and used to get the client's ip_address when receiving new requests, and not the proxy's.

```mermaid
flowchart LR

Client(Client)
nginx("`nginx server
(proxy)`")
loan_api(Loan API)
request_1("`request
(originating/client IP)`")
request_2("`request
(client IP, proxy IP)`")

style Client fill:#6f6f73
style nginx fill:#6f6f73
style loan_api fill:#6f6f73

Client --- request_1 --> nginx --- request_2 --> loan_api

```

<br></br>
# Outstanding balance calculation (unpaid value)

When a Loan in created, the value, interest rate and number of monthly installments have to be informed. Based on these information, the installment value and also the total outstanding value are calculated as follows:

- iv = installment value
- ov = original loan value
- n = number of installments
- i = interest_rate / 100
- uv = unpaid value
- pv = paid value

$$
iv = ov * \frac{(1+i)^n * i}{(1 + i)^n - 1}
$$

Having the installment value we can calculate the total outstanding balance from the Loan. This is the value that will appear when retrieving loans for which no payments were created.

$$
uv = iv * n
$$

Finally, if some payments were already made, the value paid is discounted from the total unpaid value.

$$
uv = uv - pv
$$

As a quick example, let's suppose you requested a loan of $10,000.00, interest rate of 1.5% per month and to be paid in 5 installments.

|Month      |Installment value|Unpaid value |
| :---:     | :---:           | :---:       |
| 1         | 2,090.89        | 8,363.56    |
| 2         | 2,090.89        | 6,272.67    |
| 3         | 2,090.89        | 4,181.78    |
| 4         | 2,090.89        | 2,090.89    |
| 5         | 2,090.89        | 0           |
| **Total** | **10,454.45**   | **-**       |

The total value to be paid will be $10,454.45.

<br></br>
# API documentation

&nbsp;
## Listing elements

When listing loans or payments, for example, the number of results that will appear in a page is 10. If necessary you can change this behaviour by going to settings.py module. There will be a setting called REST_FRAMEWORK. It is a dictionary, and one of its keys is called PAGE_SIZE. You can then change the PAGE_SIZE value to something that is more appropriate you.

&nbsp;
## Endpoints

Here is a list of the endpoints. If you need more details you can continue reading the documentation.

| Action | Endpoint | Method | Status Code |
| --- | --- | :---: | :---: |
| Generate token | `/api-auth-token/` | POST | - |
| Create Loan | `/api/loans/` | POST | 201 |
| Retrieve Loan | `/api/loans/{loan_id}` | GET | 200 |
| List loans | `/api/loans/` | GET | 200 |
| Update Loan | `/api/loans/{loan_id}` | PUT | 200 |
| Delete Loan | `/api/loans/{loan_id}` | DELETE | 204 |
| Create payment | `/api/payments/` | POST | 201 |
| Retrieve payment | `/api/payments/{payment_id}` | GET | 200 |
| List payments | `/api/payments/` | GET | 200 |
| Update payment | `/api/payments/{payment_id}` | PUT | 200 |
| Delete payment | `/api/payments/{payment_id}` | DELETE | 204 |
| Filter payments by Loan ID| `/api/payments/?loan={loan_id}` | GET | 200 |

&nbsp;
## Authentication

The authentication system used to build this API is the token authentication. This means that a token has to be created for a user to be able to make requests, and every request must be authenticated.

```
from rest_framework.authtoken.models import Token

token = Token.objects.create(user=...)
```

Another way of creating a token is making a POST request to the `/api-auth-token/` endpoint informing a valid email and password. Here is an example:

```
curl -H 'Content-Type: application/json' \
     -d '{"username": "user@email.com", "password": "pass"}' \
     -X POST http://127.0.0.1:8000/api-auth-token/
```

The token then has to be included in the Authorization HTTP header. 

This is an example of an authenticated request:

```
curl -X GET http://127.0.0.1:8000/api/loans/ \
     -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
```

&nbsp;
## Making requests

&nbsp;
### 1 - Creating a new Loan

To create a new loan, send a POST request to `/api/loans/` informing the value, interest_rate, request_date, number of installments to quit the loan and bank ID. 

The **request_date** field is not required. If not informed, the current day will be filled automatically. But, if informed, the ISO 8601 format has to be used (YYYY-MM-DD). For example:

```
{
    "value": 1000,
    "interest_rate": 2.5,
    "request_date": '2024-07-10',
    "installments": 5,
    "bank": 1
}
```

This request will create a Loan with value = 1.000,00, interest_rate of 2.5% per month, 5 installments and the bank to provide the Loan will be the one with ID = 1. If successfull, the response will have a 201 status code and will look like this:

```
{
    "id": 5,
    "value": 1000.0,
    "interest_rate": 2.5,
    "installments": 5,
    "installment_value": 215.25,
    "ip_address": "127.0.0.1",
    "request_date": "2024-07-10",
    "bank": 1,
    "client": "email@email.com",
    "payment_sum": 0,
    "unpaid_value": 1076,25
}
```

&nbsp;
### 2 - Retrieving a specific Loan

To retrieve a specific loan, we have to inform the it's ID in the url. For example, to retrieve the loan with ID = 1, we have to send a GET request to `/api/loans/1/`. If successfull, the response will return with a 200 status code and in this format:

```
{
    "id": 1,
    "value": 30000.0,
    "interest_rate": 1.5,
    "installments": 12,
    "installment_value": 2750.4,
    "ip_address": "127.0.0.1",
    "request_date": "2024-07-08",
    "bank": 1,
    "client": "email@email.com",
    "payment_sum": 5500.8,
    "unpaid_value": 27504,00
}
```

It's important to note that the unpaid_value is the sum of the value and the interest, which is calculated based on the interest_rate, value and number of installments.

&nbsp;
### 3 - Listing loans

To list all loans, send a GET request to `/api/loans/`. If successfull, the response will have a 200 status code and will look like this:

```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 5,
            "value": 1000.0,
            "interest_rate": 2.5,
            "installments": 5,
            "installment_value": 215.25,
            "ip_address": "127.0.0.1",
            "request_date": "2024-07-10",
            "bank": 1,
            "client": "email@email.com",
            "payment_sum": 0,
            "unpaid_value": 1076,25
        },
        {
            "id": 1,
            "value": 30000.0,
            "interest_rate": 1.5,
            "installments": 12,
            "installment_value": 2750.4,
            "ip_address": "127.0.0.1",
            "request_date": "2024-07-08",
            "bank": 1,
            "client": "email@email.com",
            "payment_sum": 5500.8,
            "unpaid_value": 27504,00
        }
    ]
}
```

&nbsp;
### 4 - Updating a Loan

To update a Loan, we have to send a PUT request to `/api/loans/{loan_id}/` informing the ID of the Loan that we want to update. For example, if we need to update the Loan we created [on this step](https://github.com/fczanetti/loan_api?tab=readme-ov-file#1---creating-a-new-loan) we have to send a request to `/api/loans/5/` as follows:

```
{
    "value": 2500,
    "interest_rate": 2.5,
    "installments": 5,
    "bank": 1
}
```

On this request we updated just the value, from 1.000,00 to 2.500,00. If successfull, the response will have a 200 status code and will return the updated Loan:

```
{
    "id": 5,
    "value": 2500.0,
    "interest_rate": 2.5,
    "installments": 5,
    "installment_value": 538.12,
    "ip_address": "127.0.0.1",
    "request_date": "2024-07-10",
    "bank": 1,
    "client": "email@email.com",
    "payment_sum": 0,
    "unpaid_value": 2690,60
}
```

&nbsp;
### 5 - Deleting a Loan

To delete a Loan, send a DELETE request to `/api/loans/{loan_id}/` informing the ID of the Loan to be deleted. For example, to delete the Loan of ID = 5, this is the address: `/api/loans/5/`. If successfull, a response with a 204 status code will return.

&nbsp;
### 6 - Creating a payment

To create a Payment, send a POST request to `/api/payments/`. You'll need the ID of the Loan you are creating a Payment for. 

The **payment_date** field is not required. If not informed, the current day will be filled automatically. But, if informed, the ISO 8601 format has to be used (YYYY-MM-DD). For example:

```
{
    "loan": 1,
    "payment_date": "2024-07-10",
    "value": 250
}
```

In this case, you are creating a Payment for the Loan of ID = 1. If successfull a response will return with a 201 status code, and the format will be as follows:

```
{
    "id": 5,
    "loan": 1,
    "payment_date": "2024-07-10",
    "value": 250.0
}
```

&nbsp;
### 7 - Retrieving a Payment

To retrieve a Payment you just need to send a GET request informing the Payment ID on the URL `/api/payments/{payment_id}/`. If successfull, a response with a 200 status code will return, and it will be its format:

```
{
    "id": 5,
    "loan": 1,
    "payment_date": "2024-07-10",
    "value": 250.0
}
```

&nbsp;
### 8 - Listing payments

To list all the payments, send a GET request to `/api/payments/`. If successfull, the response will have a 200 status code and will look like this:

```
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 5,
            "loan": 1,
            "payment_date": "2024-07-10",
            "value": 250.0
        },
        {
            "id": 1,
            "loan": 1,
            "payment_date": "2024-07-08",
            "value": 2750.4
        }
    ]
}
```

&nbsp;
### 9 - Updating a Payment

To update a Payment, send a PUT request to `/api/payments/{payment_id}/` informing the ID of the Payment to be updated. You will also have to send the request on this format:

```
{
    "loan": 1,
    "value": 3000
}
```
If successfull, the response will have a 200 status code and look like this:

```
{
    "id": 1,
    "loan": 1,
    "payment_date": "2024-07-08",
    "value": 2780.0
}
```

&nbsp;
### 10 - Deleting a Payment

To delete a Payment just send a DELETE request to `/api/payments/{payment_id}/` informing the ID of the Payment to be deleted. If successfull there will be a response with a 204 status code.

&nbsp;
### 11 - Filtering payments by Loan ID

If you need to list only the payments related to a specific Loan you can send a GET request to `/api/payments/?loan={loan_id}` informing the ID of the Loan from which you wish to see the payments. If successfull a 200 status code response will return, and the format will be the same as in [step number 8](https://github.com/fczanetti/loan_api?tab=readme-ov-file#8---listing-payments).
