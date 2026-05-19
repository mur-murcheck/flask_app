from flask import Flask, jsonify, request
import uuid
# from src import routes

app = Flask(__name__)


goods = {
    1: {"name": "apple", "price": 20},
    2: {"name": "banana", "price": 45},
    3: {"name": "guava", "price": 50},
    4: {"name": "dragon fruit", "price": 75},
    5: {"name": "orange", "price": 30},
    6: {"name": "grape", "price": 350},
    7: {"name": "bala", "price": 40},
    8: {"name": "kiwi", "price": 75}
}

members = {}
carts = {}

# @app.route('/')
@app.route("/showGoods", methods=["GET", "POST"])
def show_goods():
    
    goods_list = []

    for code in goods:
        item = goods[code]
        goods_list.append({
            "id": code,
            "name": item["name"],
            "price": item["price"]
        })

    if request.method == "POST":
        inputData = request.json
        key = inputData.get("key")

        if not key:
            return jsonify({
                "success": False,
                "message": "Keyword is required"
            })
        
        result = []
        
        for item in goods_list:
            if item["name"] == key:
                result.append(item)

        if not result:
            return jsonify({
                "success": False,
                "message": "Product not found"
            })

        return jsonify(result)

    return jsonify(goods_list)


@app.route('/addMember', methods=['POST'])
def add_member():
    inputData = request.json
    print("input: ", inputData)

    name = inputData.get("name")
    phone = inputData.get("phone")
    address = inputData.get("address")

    if not name:
        return jsonify({
            "success": False, 
            "message": "Name is required"
        })
    
    if not phone:
        return jsonify({
            "success": False, 
            "message": "Phone is required"
        })
    
    if not phone.isdigit() or len(phone) != 10:
        return jsonify({
            "success": False, 
            "message": "Phone must contain 10 digits"
        })
    
    if not address:
        return jsonify({
            "success": False, 
            "message": "Address is required"
        })

    member_id = str(uuid.uuid4())

    members[member_id] = {
        "name": name,
        "phone": phone,
        "address": address
    }

    carts[member_id] = []

    return jsonify({
        "success": True,
        "message": "Order information added successfully",
        "member_id": member_id
    })


@app.route('/members', methods=['GET'])
def show_members():
    return jsonify(members)


@app.route('/buy', methods=['POST'])
def buy():
    inputData = request.json
    print('input', inputData)

    code = inputData.get('code')
    quantity = inputData.get('quantity')
    member_id = inputData.get("member_id")

    if not member_id:
        return jsonify({
            "success": False,
            "message": "Member ID is required"
        })
    
    if member_id not in members:
        return jsonify({
            "success": False,
            "message": "Member does not exist"
        })

    if not code:
        return jsonify({
            "success": False,
            "message": "Product code is required"
        })
    
    if not quantity:
        return jsonify({
            "success": False,
            "message": "Quantity is required"
        })

    code = int(code)
    quantity = int(quantity)

    if code not in goods:
        return jsonify({
            "success": False,
            "message": "Product does not exist"
        })
    
    if quantity <= 0:
        return jsonify({
            "success": False,
            "message": "Quantity must be greater than zero"
        })
    
    item = goods[code]
    total = item["price"] * quantity

    found = False

    member_cart = carts[member_id]

    for cart_item in member_cart:
        if cart_item["code"] == code:
            cart_item["quantity"] += quantity
            cart_item["total"] = cart_item["price"] * cart_item["quantity"]
            found = True
            break

    if not found:
        member_cart.append({
            "code": code,
            "name": item["name"],
            "price": item["price"],
            "quantity": quantity,
            "total": total
    })

    cart_total = 0

    for item in member_cart:
        cart_total += item["total"]

    return jsonify({
        "success": True,
        "message": "Product added to cart",
        "cart": member_cart,
        "cartTotal": cart_total
    })


@app.route('/order', methods=['GET'])
def order():
    member_id = request.args.get("member_id")

    if not member_id:
        return jsonify({
            "success": False,
            "message": "Customer ID is required"
        })
    
    if member_id not in members:
        return jsonify({
            "success": False,
            "message": "Member does not exist"
        })

    member = members[member_id]
    member_cart = carts[member_id]

    if not member_cart:
        return jsonify({
            "success": False,
            "message": "Cart is empty"
        })
    
    total = 0

    for item in member_cart:
        total += item['total']

    fruit_types = len(member_cart)

    return jsonify({
        "success": True,
        "message": "Order created successfully",
        "customer": member,
        "item": member_cart,
        "total": total,
        "fruitTypes": fruit_types,
        "member_id": member_id
    })