from flask import Flask, jsonify, request
import uuid
# from src import routes

app = Flask(__name__)


@app.route("/healthCheck", methods=["GET"])
def health_check():
    return "I am healthy!"


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

    for product_id in goods:
        item = goods[product_id]
        goods_list.append({
            "product_id": product_id,
            "name": item["name"],
            "price": item["price"]
        })

    if request.method == "POST":
        inputData = request.json
        name = inputData.get("name")
        product_id = inputData.get("product_id")
        price = inputData.get("price")

        if not inputData:
            return jsonify(goods_list)
        
        if name:
            result = []
            for item in goods_list:
                if name in item["name"]:
                    result.append(item)

            return jsonify(result)

        if product_id:
            result = []
            for item in goods_list:
                if item["product_id"] == product_id:
                    result.append(item)

            return jsonify(result)
        
        if price:
            result = []
            if price.startswith(">="):
                bound = int(price[2:])

                for item in goods_list:
                    if item["price"] >= bound:
                        result.append(item)

                return jsonify(result)

            if price.startswith("<="):
                bound = int(price[2:])

                for item in goods_list:
                    if item["price"] <= bound:
                        result.append(item)

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


@app.route('/showMembers', methods=['GET', 'POST'])
def show_members():

    if request.method == 'POST':
        inputData = request.json
        name = inputData.get('name')
        member_id = inputData.get('member_id')

        if not inputData:
            return jsonify(members)
        
        if name:
            result = {}
            for member_id in members:
                member = members[member_id]

                if name in member["name"]:
                    result[member_id] = member

            return jsonify(result)
        
        if member_id:
            if member_id in members:                    
                return jsonify({
                    member_id: members[member_id]
                })
            return jsonify({})
        
    return jsonify(members)


@app.route('/buy', methods=['POST'])
def buy():
    inputData = request.json
    print('input', inputData)

    product_id = inputData.get('product_id')
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

    if not product_id:
        return jsonify({
            "success": False,
            "message": "Product ID is required"
        })
    
    if not quantity:
        return jsonify({
            "success": False,
            "message": "Quantity is required"
        })

    product_id = int(product_id)
    quantity = int(quantity)

    if product_id not in goods:
        return jsonify({
            "success": False,
            "message": "Product does not exist"
        })
    
    if quantity <= 0:
        return jsonify({
            "success": False,
            "message": "Quantity must be greater than zero"
        })
    
    item = goods[product_id]
    total = item["price"] * quantity

    found = False

    member_cart = carts[member_id]

    for cart_item in member_cart:
        if cart_item["product_id"] == product_id:
            cart_item["quantity"] += quantity
            cart_item["total"] = cart_item["price"] * cart_item["quantity"]
            found = True
            break

    if not found:
        member_cart.append({
            "product_id": product_id,
            "name": item["name"],
            "price": item["price"],
            "quantity": quantity,
            "total": total
    })

    cart_total = 0

    for item in member_cart:
        cart_total += item["total"]

    total_categories = len(member_cart)

    return jsonify({
        "success": True,
        "message": "Product added to cart",
        "cart": member_cart,
        "total_amount": cart_total,
        "total_categories": total_categories
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
    carts[member_id] = []

    return jsonify({
        "success": True,
        "message": "Order created successfully",
        "customer": member,
        "item": member_cart,
        "total_amount": total,
        "total_categories": fruit_types,
        "member_id": member_id
    })