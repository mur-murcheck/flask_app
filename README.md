ORDER SYSTEM API

1. GET /showGoods
show all fruits

Response:
[
    {
        "id": 1,
        "name": "apple",
        "price": 20
    }
]
___________________________________________

2. POST /showGoods
Search fruit by key

Request:
{
    "key": "orange"
}

Response:
[
    {
        "id": 1,
        "name": "apple",
        "price": 20
    }
]
____________________________________________

3. POST /addMember
Add Customer Informatioin

Request:
{
    "name": "Mary",
    "phone": "0912345678",
    "address": "Taichung"
}

Response:
{
    "address": "Taichung",
    "message": "Order information added successfully",
    "name": "Mary",
    "phone": "0912345678",
    "success": true
}
____________________________________________

4. POST /buy
Add product to cart

Request:
{
    "code": 2,
    "quantity": 2
}

Response:
{
    "cart": [
        {
            "code": 2,
            "name": "banana",
            "price": 45,
            "quantity": 2,
            "total": 90
        }
    ],
    "cartTotal": 90,
    "message": "Product added to cart",
    "success": true
}
____________________________________________

5. GET /order
Show order receipt

Response:
{
    "customer": {
        "address": "Taichung",
        "name": "Mary",
        "phone": "0912345678"
    },
    "fruitTypes": 1,
    "item": [
        {
            "code": 2,
            "name": "banana",
            "price": 45,
            "quantity": 2,
            "total": 90
        }
    ],
    "message": "Order created successfully",
    "success": true,
    "total": 90
}