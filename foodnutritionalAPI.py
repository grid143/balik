from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

#-------------------------------------------------Tig activate sa authorizaton-----------------------------------------#
auth = HTTPBasicAuth()

#---------------------------------------------------------Mongodb Database---------------------------------------------#
client = MongoClient('mongodb+srv://gamutingridjezreeln:foodnutritionalAPI@cluster1.6wm59m1.mongodb.net/')
db = client['food_nutritional_API']

#-----------------------------------------------Food Nutritional database collection-----------------------------------#
food_collection = db['food_data']

#------------------------------------------For User Authentication database collection---------------------------------#
user_collection = db['user_data']



#-----------------------------------------------------For Food Nutritional Data----------------------------------------#
@auth.verify_password
def verify_password(username, password):
    # Find user in the MongoDB collection
    user = user_collection.find_one({'username': username, 'password': password})

    if user:
        return True
    return False



#----------------------------------------------------User data CRUD----------------------------------------------------#


#---------------------------------------------Route for to get the list of Users---------------------------------------#

@app.route('/users', methods=['GET'])
@auth.login_required

def get_users():
    user_data = user_collection.find()

    return jsonify({'user': list(user_data)})




#----------------------------------------Route to get the list by user ID----------------------------------------------#

@app.route('/user/id/<int:userId>', methods=['GET'])
@auth.login_required

def get_user_by_id(userId):
    # Ensure that 'userID' is treated as an integer
    user_data = user_collection.find_one({'_id': userId})
    if user_data is None:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'user': user_data})




#-----------------------------------------------Route for to add another users-----------------------------------------#

@app.route('/users', methods=['POST'])
@auth.login_required

def create_users():
    required_fields = ['username', 'password', '_id', 'email']
    if not request.json or not all(field in request.json for field in required_fields):
        missing_fields = [field for field in required_fields if field not in request.json]
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    new_user = {
                   '_id': request.json['_id'],
                   'name' : request.json['name'],
                   'address' : request.json['address']       ,
                   'username': request.json['username'],
                   'password': request.json['password'],
                   'emailaddress' : request.json['emailaddress']

    }

    result = user_collection.insert_one(new_user)
    success_message = f"New user has been added successfully!"
    return jsonify({f'users': new_user, 'message': success_message}), 201


#-------------------------------------------------------Raw input for POST---------------------------------------------#

#{
  #"name" : "Name Example",
  #"address" : "Address Example",
  #"username": "Username Example",
  #"password": "Password Example",
  #"emailaddress": "Email Example",


#}



#----------------------------------------------Route to update a user information--------------------------------------#

@app.route('/users/id/<int:id>', methods=['PUT'])
@auth.login_required

def update_users(id):
    # Mag check if naa bay data ga exist sa database which is the id
    existing_food = user_collection.find_one({'_id': id})
    if existing_food is None:
        return jsonify({'error': f'User with ID {id} not found'}), 404

    # Mag kuha og udated data for request
    updated_data = request.json

    # Update ang existing food data
    user_collection.update_one({'_id': id}, {'$set': updated_data})

    success_message = f"User with _id {id} has been updated successfully!"
    return jsonify({'message': success_message}), 200


#-------------------------------------------------Request body for PUT method------------------------------------------#
# "name" : "Name Example",
# "address" : "Address Example",
# "username": "Username Example",
# "password": "Password Example",
# "emailaddress": "Email Example",





#---------------------------------------------------Food Nutritional Value CRUD----------------------------------------#




#-----------------------------------------------Food route for listing all the data------------------------------------#

@app.route('/food', methods=['GET'])
@auth.login_required


def get_food():
    food_data = food_collection.find()
    return jsonify({'food': list(food_data)})



#----------------------------------------Food route para mag request of data just by an ID-----------------------------#

@app.route('/food/id/<int:foodId>', methods=['GET'])
@auth.login_required

def get_food_by_id(foodId):
    # Ensure that 'foodId' is treated as an integer
    food_data = food_collection.find_one({'_id': foodId})
    if food_data is None:
        return jsonify({'error': 'Food not found'}), 404

    return jsonify({'food': food_data})


#---------------------------------------------Food route para maka request by foodcategory-----------------------------#

@app.route('/food/category/<string:category>', methods=['GET'])
@auth.login_required

def get_food_by_ctgry(category):
    # Assuming food_collection is your MongoDB collection
    food_data_cursor = food_collection.find({'category': category})

    # Convert the cursor to a list of dictionaries
    food_list = list(food_data_cursor)

    if not food_list:
        return jsonify({'error': 'Food type not found'}), 404

    return jsonify({'food': food_list})


#---------------------------------------Food route para maka request by foodType---------------------------------------#


#--------------------------------------------------Seafood Type--------------------------------------------------------#
@app.route('/food/seafood/type/<string:seaFoodType>', methods=['GET'])
@auth.login_required
def get_food_by_seafood_type(seafoodType):
    # Assuming food_collection is your MongoDB collection
    food_data_cursor = food_collection.find({'seafoodType':seafoodType})

    # Convert the cursor to a list of dictionaries
    food_list = list(food_data_cursor)

    if not food_list:
        return jsonify({'error': 'Food type not found'}), 404

    return jsonify({'food': food_list})



#--------------------------------------------------Fruitfood Type------------------------------------------------------#
@app.route('/food/fruit/type/<string:fruitType>', methods=['GET'])
@auth.login_required
def get_food_by_fruitfood_type(fruitType):
    # Assuming food_collection is your MongoDB collection
    food_data_cursor = food_collection.find({'fruitType': fruitType})

    # Convert the cursor to a list of dictionaries
    food_list = list(food_data_cursor)

    if not food_list:
        return jsonify({'error': 'Food type not found'}), 404

    return jsonify({'food': food_list})



#--------------------------------------------------Meat Type-----------------------------------------------------------#
@app.route('/food/meat/type/<string:foodType>', methods=['GET'])
@auth.login_required
def get_food_by_meatfood_type(meatType):
    # Assuming food_collection is your MongoDB collection
    food_data_cursor = food_collection.find({'meatType': meatType})

    # Convert the cursor to a list of dictionaries
    food_list = list(food_data_cursor)

    if not food_list:
        return jsonify({'error': 'Food type not found'}), 404

    return jsonify({'food': food_list})



#------------------------------------------------Vegetable Type--------------------------------------------------------#
@app.route('/food/vegetable/type/<string:foodType>', methods=['GET'])
@auth.login_required
def get_food_by_vegetable_type(vegetableType):
    # Assuming food_collection is your MongoDB collection
    food_data_cursor = food_collection.find({'vegetableType': vegetableType})

    # Convert the cursor to a list of dictionaries
    food_list = list(food_data_cursor)

    if not food_list:
        return jsonify({'error': 'Food type not found'}), 404

    return jsonify({'food': food_list})




#----------------------------------------Food route para maka post og new set of datas---------------------------------#


@app.route('/food/seafood', methods=['POST'])
@auth.login_required

def create_food_seafood():
    required_fields = ['seafoodType', 'seafoodName','category', 'servingSize', '_id', 'Calories', 'Protein', 'Fat', 'Cholesterol', 'Sodium', 'Carbohydrate', 'DietaryFiber', 'Vitamins' ]
    if not request.json or not all(field in request.json for field in required_fields):
        missing_fields = [field for field in required_fields if field not in request.json]
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    sea_food = {
        '_id': request.json['_id'],
        'seafoodType': request.json['seafoodType'],
        'seafoodName': request.json['seafoodName'],
        'category': request.json['category'],
        'servingSize': request.json['servingSize'],
        'Calories': request.json.get('Calories', ""),
        'Protein': request.json.get('Protein', ""),
        'Fat': request.json.get('Fat', ""),
        'Cholesterol': request.json.get('Cholesterol', ""),
        'Sodium': request.json.get('Sodium', ""),
        'Carbohydrate': request.json.get('Carbohydrate', ""),
        'DietaryFiber': request.json.get('DietaryFiber', ""),
        'Vitamins': request.json.get('Vitamins', [])
    }



    result = food_collection.insert_one(sea_food)
    ##success_message = f"New food has been added successfully!"
    success_message = f"New seafood data information has been added successfully!"
    return jsonify({'food': sea_food, 'message': success_message}), 201


#---------------------------------------------POST for fruit-----------------------------------------------------------#
@app.route('/food/fruit', methods=['POST'])
@auth.login_required

def create_food_fruit():
    required_fields = ['fruitType', 'fruitName','category', 'servingSize', '_id', 'Calories', 'Protein', 'Fat', 'Cholesterol', 'Sodium', 'Carbohydrate', 'DietaryFiber', 'Vitamins' ]
    if not request.json or not all(field in request.json for field in required_fields):
        missing_fields = [field for field in required_fields if field not in request.json]
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    fruit_food = {
        '_id': request.json['_id'],
        'fruitType': request.json['fruitType'],
        'fruitName': request.json['fruitName'],
        'category': request.json['category'],
        'servingSize': request.json['servingSize'],
        'Calories': request.json.get('Calories', ""),
        'Protein': request.json.get('Protein', ""),
        'Fat': request.json.get('Fat', ""),
        'Cholesterol': request.json.get('Cholesterol', ""),
        'Sodium': request.json.get('Sodium', ""),
        'Carbohydrate': request.json.get('Carbohydrate', ""),
        'DietaryFiber': request.json.get('DietaryFiber', ""),
        'Vitamins': request.json.get('Vitamins', [])
    }



    result = food_collection.insert_one(fruit_food)
    ##success_message = f"New food has been added successfully!"
    success_message = f"New fruit data information has been added successfully!"
    return jsonify({'food': fruit_food, 'message': success_message}), 201


#---------------------------------------------POST for meat------------------------------------------------------------#

@app.route('/food/meat', methods=['POST'])
@auth.login_required

def create_food_meat():
    required_fields = ['meatType', 'meatName','category', 'servingSize', '_id', 'Calories', 'Protein', 'Fat', 'Cholesterol', 'Sodium', 'Carbohydrate', 'DietaryFiber', 'Vitamins' ]
    if not request.json or not all(field in request.json for field in required_fields):
        missing_fields = [field for field in required_fields if field not in request.json]
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    meat_food = {
        '_id': request.json['_id'],
        'meatType': request.json['meatType'],
        'meatName': request.json['meatName'],
        'category': request.json['category'],
        'servingSize': request.json['servingSize'],
        'Calories': request.json.get('Calories', ""),
        'Protein': request.json.get('Protein', ""),
        'Fat': request.json.get('Fat', ""),
        'Cholesterol': request.json.get('Cholesterol', ""),
        'Sodium': request.json.get('Sodium', ""),
        'Carbohydrate': request.json.get('Carbohydrate', ""),
        'DietaryFiber': request.json.get('DietaryFiber', ""),
        'Vitamins': request.json.get('Vitamins', [])
    }



    result = food_collection.insert_one(meat_food)
    ##success_message = f"New food has been added successfully!"
    success_message = f"New fruit data information has been added successfully!"
    return jsonify({'food': meat_food, 'message': success_message}), 201


#-----------------------------------------------POST for vegetable-----------------------------------------------------#
@app.route('/food/vegetable', methods=['POST'])
@auth.login_required

def create_food_vegetable():
    required_fields = ['vegetableType', 'vegetableName','category', 'servingSize', '_id', 'Calories', 'Protein', 'Fat', 'Cholesterol', 'Sodium', 'Carbohydrate', 'DietaryFiber', 'Vitamins' ]
    if not request.json or not all(field in request.json for field in required_fields):
        missing_fields = [field for field in required_fields if field not in request.json]
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    vegetable_food = {
        '_id': request.json['_id'],
        'vegetableType': request.json['vegetableType'],
        'vegetableName': request.json['vegetableName'],
        'category': request.json['category'],
        'servingSize': request.json['servingSize'],
        'Calories': request.json.get('Calories', ""),
        'Protein': request.json.get('Protein', ""),
        'Fat': request.json.get('Fat', ""),
        'Cholesterol': request.json.get('Cholesterol', ""),
        'Sodium': request.json.get('Sodium', ""),
        'Carbohydrate': request.json.get('Carbohydrate', ""),
        'DietaryFiber': request.json.get('DietaryFiber', ""),
        'Vitamins': request.json.get('Vitamins', [])
    }



    result = food_collection.insert_one(vegetable_food)
    ##success_message = f"New food has been added successfully!"
    success_message = f"New fruit data information has been added successfully!"
    return jsonify({'food': vegetable_food, 'message': success_message}), 201



#----------------------------------------------Request Body for the POST method----------------------------------------#



#REQUEST BODY NI SYA PARA SA POSTMAN
#MAKE SURE NAKA HEADERS MO AND ANG HEADERS KAY:
#key          value
#Content-Type application/json

#------------------------------------------CHANGE THE NECESSARY DATA PARA SA REQUEST BODY------------------------------#
# {
  #"_id": 1,
  #"meatType": "Example Type",           --Depends sa type sa food, ma meat,fruit,or vegetable
  #"meatName": "Example Name",           --Depends sa type sa food
  #"category": "meat",
  #"Calories": "200",
  #"Protein": "10",
  #"Fat": "5",
  #"Cholesterol": "20",
  #"Sodium": "300",
  #"Carbohydrate": "30",
  #"DietaryFiber": "5",
  #"Vitamins": ["Vitamin A", "Vitamin C"]
# }



#----------------------------------------Food route to upate specific data of the API----------------------------------#


# Example: foodName, foodType, and their nutritional value

@app.route('/food/id/<int:id>', methods=['PUT'])
@auth.login_required

def update_food(id):
    # Mag check if naa bay data ga exist sa database which is the id
    existing_food = food_collection.find_one({'_id': id})
    if existing_food is None:
        return jsonify({'error': f'Food with ID {id} not found'}), 404

    # Mag kuha og udated data for request
    updated_data = request.json

    # Update ang existing food data
    food_collection.update_one({'_id': id}, {'$set': updated_data})

    success_message = f"Food with _id {id} has been updated successfully!"
    return jsonify({'message': success_message}), 200


#--------------------------------------------------Request body for PUT method-----------------------------------------#
#{
 # "foodType": "",  --Depende sa unsa nga foodtype
 # "foodName": "",  --Depende pud sa foodtype
 # "Calories": "",
 # "Protein": "",
 # "Fat": "",
 # "Cholesterol": "",
 # "Sodium": "",
 # "Carbohydrate": "",
 # "DietaryFiber": "",
 # "Vitamins": [""]
#}



#---------------------------------------------------Food route para maka delete og data--------------------------------#
@app.route('/food/id/<int:id>', methods=['DELETE'])
@auth.login_required

def delete_food(id):
    # Mag check if naa bay data ga exist sa database which is the id
    existing_food = food_collection.find_one({'_id': id})
    if existing_food is None:
        return jsonify({'error': f'Food with ID {id} not found'}), 404

    # Mag delete og existing food data
    result = food_collection.delete_one({'_id': id})

    if result.deleted_count == 0:
        return jsonify({'error': f'Error deleting food with ID {id}'}), 500

    success_message = f"Food with id {id} has been deleted to your database successfully!"
    return jsonify({'message': success_message}), 200


if __name__ == '__main__':
    app.run(debug=True)